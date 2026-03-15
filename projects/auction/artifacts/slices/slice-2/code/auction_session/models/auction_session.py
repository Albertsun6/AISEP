from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AuctionSession(models.Model):
    """拍卖会"""

    _name = 'auction.session'
    _description = '拍卖会'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_time desc'

    # ── 基本字段 ──────────────────────────────

    name = fields.Char(
        string='场次名称',
        required=True,
        size=128,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', '草稿'),
            ('published', '已发布'),
            ('ongoing', '进行中'),
            ('closed', '已结束'),
            ('cancelled', '已取消'),
        ],
        string='状态',
        required=True,
        default='draft',
        tracking=True,
        copy=False,
    )
    start_time = fields.Datetime(
        string='开始时间',
        required=True,
        tracking=True,
    )
    end_time = fields.Datetime(
        string='结束时间',
        required=True,
        tracking=True,
    )
    description = fields.Html(
        string='描述',
        sanitize_style=True,
    )

    # ── 拍卖规则 ──────────────────────────────

    default_increment = fields.Monetary(
        string='默认加价幅度',
        required=True,
        tracking=True,
        currency_field='currency_id',
    )
    countdown_seconds = fields.Integer(
        string='倒计时秒数',
        required=True,
        default=30,
    )
    extension_seconds = fields.Integer(
        string='延时秒数',
        required=True,
        default=10,
    )
    conditional_sale_pct = fields.Float(
        string='有条件成交阈值(%)',
        required=True,
        default=80.0,
        help='最高价在底价的此百分比以上时，标记为有条件成交',
    )

    # ── 关系字段 ──────────────────────────────

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='币种',
        required=True,
        index=True,
        default=lambda self: self.env.company.currency_id,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='公司',
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    session_lot_ids = fields.One2many(
        comodel_name='auction.session.lot',
        inverse_name='session_id',
        string='编排拍品',
    )

    # ── 计算字段 ──────────────────────────────

    lot_count = fields.Integer(
        string='拍品数量',
        compute='_compute_lot_count',
        store=True,
    )

    # ── SQL 约束 ──────────────────────────────

    _sql_constraints = [
        (
            'check_time',
            'CHECK(start_time < end_time)',
            '开始时间必须早于结束时间',
        ),
        (
            'check_threshold',
            'CHECK(conditional_sale_pct > 0 AND conditional_sale_pct <= 100)',
            '阈值必须在 0-100 之间',
        ),
    ]

    # ── 计算方法 ──────────────────────────────

    @api.depends('session_lot_ids')
    def _compute_lot_count(self):
        for record in self:
            record.lot_count = len(record.session_lot_ids)

    # ── 业务动作 ──────────────────────────────

    def action_publish(self):
        """草稿 → 已发布（需至少 1 件拍品）"""
        for session in self:
            if session.state != 'draft':
                raise UserError(_('只有草稿状态才能发布'))
            if not session.session_lot_ids:
                raise UserError(_('请至少编入一件拍品后再发布'))
            session.state = 'published'
            # 同步更新编入拍品的 lot.state → assigned
            session.session_lot_ids.mapped('lot_id').filtered(
                lambda l: l.state == 'approved'
            ).write({'state': 'assigned'})

    def action_start(self):
        """已发布 → 进行中"""
        for session in self:
            if session.state != 'published':
                raise UserError(_('只有已发布状态才能开始拍卖'))
            session.state = 'ongoing'

    def action_close(self):
        """进行中 → 已结束"""
        for session in self:
            if session.state != 'ongoing':
                raise UserError(_('只有进行中状态才能结束'))
            session.state = 'closed'

    def action_cancel(self):
        """草稿/已发布 → 已取消"""
        for session in self:
            if session.state not in ('draft', 'published'):
                raise UserError(_('只有草稿或已发布状态才能取消'))
            session.state = 'cancelled'
            # 解除已编入拍品的绑定状态
            session.session_lot_ids.mapped('lot_id').filtered(
                lambda l: l.state == 'assigned'
            ).write({'state': 'approved'})
