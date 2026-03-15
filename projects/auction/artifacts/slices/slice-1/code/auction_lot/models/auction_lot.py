from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class AuctionLot(models.Model):
    _name = 'auction.lot'
    _description = '拍品'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    # ── 关系字段 ──
    category_id = fields.Many2one(
        'auction.lot.category',
        string='分类',
        required=True,
        index=True,
        ondelete='restrict',
        tracking=True,
    )
    consignor_id = fields.Many2one(
        'res.partner',
        string='委托方',
        index=True,
        ondelete='set null',
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='币种',
        required=True,
        index=True,
        default=lambda self: self.env.company.currency_id,
    )
    company_id = fields.Many2one(
        'res.company',
        string='公司',
        required=True,
        index=True,
        default=lambda self: self.env.company,
    )
    image_ids = fields.One2many(
        'auction.lot.image',
        'lot_id',
        string='拍品图片',
    )

    # ── Selection 字段 ──
    state = fields.Selection(
        [
            ('draft', '草稿'),
            ('approved', '已审核'),
            ('assigned', '已编排'),
            ('sold', '已成交'),
            ('unsold', '流拍'),
            ('withdrawn', '已撤回'),
        ],
        string='状态',
        required=True,
        default='draft',
        tracking=True,
        copy=False,
    )

    # ── 普通数据字段 ──
    name = fields.Char(
        string='拍品名称',
        size=128,
        required=True,
        tracking=True,
    )
    description = fields.Html(
        string='拍品描述',
        sanitize_style=True,
    )
    reserve_price = fields.Monetary(
        string='底价',
        required=True,
        default=0,
        groups='auction_lot.group_auction_manager',
        tracking=True,
        help='仅拍卖经理可见。无底价拍卖时置 0',
    )
    starting_price = fields.Monetary(
        string='起拍价',
        required=True,
        tracking=True,
    )
    is_no_reserve = fields.Boolean(
        string='无底价拍卖',
        default=False,
        tracking=True,
        help='勾选后底价字段自动置 0',
    )
    low_estimate = fields.Monetary(
        string='低估价',
    )
    high_estimate = fields.Monetary(
        string='高估价',
    )
    active = fields.Boolean(
        string='启用',
        default=True,
    )

    # ── 计算字段 ──
    image_count = fields.Integer(
        string='图片数量',
        compute='_compute_image_count',
        store=True,
    )

    # ── SQL 约束 ──
    _sql_constraints = [
        ('check_reserve_starting',
         'CHECK(is_no_reserve = true OR starting_price <= reserve_price)',
         '起拍价不得超过底价'),
        ('check_estimate',
         'CHECK(low_estimate IS NULL OR high_estimate IS NULL OR low_estimate <= high_estimate)',
         '低估价不得超过高估价'),
    ]

    # ── 计算方法 ──
    @api.depends('image_ids')
    def _compute_image_count(self):
        for record in self:
            record.image_count = len(record.image_ids)

    # ── 约束方法 ──
    @api.constrains('reserve_price', 'starting_price', 'is_no_reserve')
    def _check_reserve_starting_price(self):
        for record in self:
            if not record.is_no_reserve and record.starting_price > record.reserve_price:
                raise ValidationError('起拍价不得超过底价')

    @api.constrains('low_estimate', 'high_estimate')
    def _check_estimate_range(self):
        for record in self:
            if record.low_estimate and record.high_estimate:
                if record.low_estimate > record.high_estimate:
                    raise ValidationError('低估价不得超过高估价')

    @api.constrains('state', 'image_ids')
    def _check_images_before_approve(self):
        for record in self:
            if record.state != 'draft' and not record.image_ids:
                raise ValidationError('至少上传 1 张图片后才能审核')

    # ── onchange（仅 UI 提示，遵循 P2-01）──
    @api.onchange('is_no_reserve')
    def _onchange_is_no_reserve(self):
        if self.is_no_reserve:
            self.reserve_price = 0

    # ── 业务动作 ──
    def action_approve(self):
        """审核通过（draft → approved）"""
        self.ensure_one()
        if not self.image_ids:
            raise UserError('至少上传 1 张图片后才能审核')
        self.write({'state': 'approved'})

    def action_withdraw(self):
        """撤回拍品（approved → withdrawn）"""
        self.ensure_one()
        if self.state == 'assigned':
            raise UserError('已编排入拍卖会的拍品请先移出场次')
        self.write({'state': 'withdrawn'})

    def action_reset_draft(self):
        """重置为草稿（withdrawn → draft）"""
        self.ensure_one()
        self.write({'state': 'draft'})
