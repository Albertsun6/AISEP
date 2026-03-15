import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AuctionBiddingRound(models.Model):
    """竞价轮次"""

    _name = 'auction.bidding.round'
    _description = '竞价轮次'
    _order = 'id desc'

    # ── 关系字段 ──────────────────────────────

    session_lot_id = fields.Many2one(
        comodel_name='auction.session.lot',
        string='场次拍品',
        required=True,
        index=True,
        ondelete='cascade',
    )
    lot_id = fields.Many2one(
        comodel_name='auction.lot',
        string='拍品',
        related='session_lot_id.lot_id',
        store=True,
    )
    session_id = fields.Many2one(
        comodel_name='auction.session',
        string='场次',
        related='session_lot_id.session_id',
        store=True,
    )
    bid_ids = fields.One2many(
        comodel_name='auction.bid',
        inverse_name='round_id',
        string='出价记录',
    )
    winner_id = fields.Many2one(
        comodel_name='res.partner',
        string='买受人',
        index=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='币种',
        required=True,
        index=True,
        default=lambda self: self.env.company.currency_id,
    )

    # ── Selection ─────────────────────────────

    state = fields.Selection(
        selection=[
            ('open', '竞价中'),
            ('hammer', '已落槌'),
            ('unsold', '流拍'),
            ('conditional_pending', '有条件成交-待确认'),
            ('conditional_accepted', '有条件成交-已接受'),
            ('conditional_rejected', '有条件成交-已拒绝'),
        ],
        string='状态',
        required=True,
        default='open',
        copy=False,
    )

    # ── Monetary ──────────────────────────────

    current_price = fields.Monetary(
        string='当前最高价',
        currency_field='currency_id',
    )
    starting_price = fields.Monetary(
        string='本轮起拍价',
        required=True,
        currency_field='currency_id',
    )
    bid_increment = fields.Monetary(
        string='本轮加价幅度',
        required=True,
        currency_field='currency_id',
    )
    hammer_price = fields.Monetary(
        string='成交价',
        currency_field='currency_id',
    )

    # ── 计算字段 ──────────────────────────────

    bid_count = fields.Integer(
        string='出价次数',
        compute='_compute_bid_count',
        store=True,
    )

    # ── 计算方法 ──────────────────────────────

    @api.depends('bid_ids')
    def _compute_bid_count(self):
        for record in self:
            record.bid_count = len(record.bid_ids)

    # ── 核心业务方法 ─────────────────────────

    def place_bid(self, bidder_id, amount):
        """出价核心方法 — ADR-002: FOR UPDATE 行级锁

        1. SELECT FOR UPDATE 锁定竞价轮次行
        2. 验证 state == 'open'
        3. 验证 amount >= min_bid
        4. 创建 bid 记录
        5. 更新 current_price
        6. Bus 推送
        """
        self.ensure_one()

        # ADR-002: 行级锁防止并发超卖
        self.env.cr.execute(
            'SELECT id FROM auction_bidding_round WHERE id = %s FOR UPDATE',
            [self.id],
        )
        # 刷新缓存以获取锁后的最新值
        self.invalidate_recordset()

        if self.state != 'open':
            raise UserError(_('竞价已结束，无法出价'))

        # 计算最低出价
        if self.current_price:
            min_bid = self.current_price + self.bid_increment
        else:
            min_bid = self.starting_price

        if amount < min_bid:
            raise UserError(
                _('出价金额 %(amount)s 低于最低要求 %(min)s',
                  amount=amount, min=min_bid)
            )

        # 创建出价记录
        bid = self.env['auction.bid'].create({
            'round_id': self.id,
            'bidder_id': bidder_id,
            'amount': amount,
            'currency_id': self.currency_id.id,
        })

        # 更新最高价
        self.current_price = amount

        # ADR-001: Bus 实时推送
        channel = f'{self.env.cr.dbname}/auction.bidding.round/{self.id}'
        self.env['bus.bus']._sendone(channel, 'new_bid', {
            'round_id': self.id,
            'bidder_id': bidder_id,
            'amount': amount,
            'bid_count': self.bid_count,
        })

        _logger.info(
            'Bid placed: round=%s bidder=%s amount=%s',
            self.id, bidder_id, amount,
        )
        return bid

    def action_check_hammer(self):
        """落槌判定 — 三路判定逻辑

        1. current_price >= reserve_price → hammer (成交)
        2. current_price >= reserve_price * pct/100 → conditional_pending
        3. else → unsold (流拍)
        """
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('只有竞价中状态才能落槌'))

        lot = self.lot_id
        reserve = lot.reserve_price
        is_no_reserve = lot.is_no_reserve
        pct = self.session_id.conditional_sale_pct

        # 无出价 → 流拍
        if not self.current_price:
            self._set_unsold()
            return

        # 无底价拍品 → 直接成交
        if is_no_reserve:
            self._set_hammer()
            return

        # 三路判定
        threshold = reserve * pct / 100.0

        if self.current_price >= reserve:
            self._set_hammer()
        elif self.current_price >= threshold:
            self.state = 'conditional_pending'
            self.session_lot_id.lot_state = 'conditional'
        else:
            self._set_unsold()

    def _set_hammer(self):
        """设置落槌成交"""
        # 最高出价者为买受人
        top_bid = self.bid_ids.sorted('amount', reverse=True)[:1]
        self.write({
            'state': 'hammer',
            'winner_id': top_bid.bidder_id.id if top_bid else False,
            'hammer_price': self.current_price,
        })
        self.session_lot_id.lot_state = 'sold'
        # 同步拍品主状态
        self.lot_id.state = 'sold'

    def _set_unsold(self):
        """设置流拍"""
        self.state = 'unsold'
        self.session_lot_id.lot_state = 'unsold'
        self.lot_id.state = 'unsold'

    def action_accept_conditional(self):
        """委托方确认有条件成交"""
        self.ensure_one()
        if self.state != 'conditional_pending':
            raise UserError(_('只能对待确认的有条件成交进行确认'))

        top_bid = self.bid_ids.sorted('amount', reverse=True)[:1]
        self.write({
            'state': 'conditional_accepted',
            'winner_id': top_bid.bidder_id.id if top_bid else False,
            'hammer_price': self.current_price,
        })
        self.session_lot_id.lot_state = 'sold'
        self.lot_id.state = 'sold'

    def action_reject_conditional(self):
        """委托方拒绝有条件成交"""
        self.ensure_one()
        if self.state != 'conditional_pending':
            raise UserError(_('只能对待确认的有条件成交进行拒绝'))

        self.state = 'conditional_rejected'
        self.session_lot_id.lot_state = 'unsold'
        self.lot_id.state = 'unsold'
