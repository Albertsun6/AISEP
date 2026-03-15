from odoo import models, fields, api
from odoo.exceptions import UserError


class AuctionBid(models.Model):
    """出价记录 — 不可修改/不可删除"""

    _name = 'auction.bid'
    _description = '出价记录'
    _order = 'bid_time desc, amount desc'

    # ── 关系字段 ──────────────────────────────

    round_id = fields.Many2one(
        comodel_name='auction.bidding.round',
        string='竞价轮次',
        required=True,
        index=True,
        ondelete='cascade',
    )
    bidder_id = fields.Many2one(
        comodel_name='res.partner',
        string='竞拍者',
        required=True,
        index=True,
        ondelete='restrict',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='币种',
        required=True,
        index=True,
        default=lambda self: self.env.company.currency_id,
    )

    # ── 普通字段 ──────────────────────────────

    amount = fields.Monetary(
        string='出价金额',
        required=True,
        currency_field='currency_id',
    )
    bid_time = fields.Datetime(
        string='出价时间',
        required=True,
        default=fields.Datetime.now,
    )

    # ── 计算字段 ──────────────────────────────

    is_winning = fields.Boolean(
        string='当前最高',
        compute='_compute_is_winning',
        store=True,
    )

    # ── SQL 约束 ──────────────────────────────

    _sql_constraints = [
        (
            'amount_positive',
            'CHECK(amount > 0)',
            '出价金额必须大于零',
        ),
    ]

    # ── 计算方法 ──────────────────────────────

    @api.depends('round_id.current_price', 'amount')
    def _compute_is_winning(self):
        for bid in self:
            bid.is_winning = (
                bid.amount == bid.round_id.current_price
            )

    # ── 不可修改/不可删除 ─────────────────────

    def write(self, vals):
        """业务铁律: 出价记录不可修改（is_winning 计算字段除外）"""
        # 允许 ORM 内部更新计算字段
        allowed_fields = {'is_winning'}
        if set(vals.keys()) - allowed_fields:
            raise UserError('出价记录不可修改')
        return super().write(vals)

    def unlink(self):
        """业务铁律: 出价记录不可删除"""
        raise UserError('出价记录不可删除')
