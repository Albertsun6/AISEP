from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AuctionSessionLot(models.Model):
    """场次拍品编排"""

    _name = 'auction.session.lot'
    _description = '场次拍品编排'
    _rec_name = 'lot_id'
    _order = 'sequence, id'

    # ── 关系字段 ──────────────────────────────

    session_id = fields.Many2one(
        comodel_name='auction.session',
        string='所属场次',
        required=True,
        index=True,
        ondelete='cascade',
    )
    lot_id = fields.Many2one(
        comodel_name='auction.lot',
        string='拍品',
        required=True,
        index=True,
        ondelete='restrict',
    )

    # ── 普通字段 ──────────────────────────────

    sequence = fields.Integer(
        string='上拍顺序',
        required=True,
        default=10,
    )
    lot_state = fields.Selection(
        selection=[
            ('pending', '等待'),
            ('active', '竞价中'),
            ('sold', '成交'),
            ('unsold', '流拍'),
            ('conditional', '有条件成交'),
        ],
        string='竞价状态',
        default='pending',
    )

    # ── Python 约束 ──────────────────────────

    @api.constrains('lot_id', 'session_id')
    def _check_lot_unique_active_session(self):
        """同一拍品不可同时在多场活跃拍卖会中"""
        for record in self:
            active_states = ('draft', 'published', 'ongoing')
            domain = [
                ('lot_id', '=', record.lot_id.id),
                ('session_id.state', 'in', active_states),
                ('id', '!=', record.id),
            ]
            if self.search_count(domain) > 0:
                raise ValidationError(
                    f'拍品 "{record.lot_id.name}" 已在其他活跃拍卖会中'
                )
