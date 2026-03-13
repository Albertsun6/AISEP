# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    """销售订单 — 继承扩展标准 sale.order"""
    _inherit = 'sale.order'

    # === 自定义字段 ===
    delivery_status = fields.Selection(
        selection=[
            ('pending', '待发货'),
            ('partial', '部分发货'),
            ('full', '已全部发货'),
        ],
        string='发货状态',
        compute='_compute_delivery_status',
        store=True,
        help='根据关联发货单的状态自动计算',
    )

    # === 计算方法 ===
    # P1-02: depends 完整 — picking_ids.state 是唯一依赖
    @api.depends('picking_ids.state')
    def _compute_delivery_status(self):
        """根据关联发货单状态计算发货进度"""
        for order in self:  # P1-02: 始终用 for 循环（Recordset 思维）
            pickings = order.picking_ids
            if not pickings:
                order.delivery_status = 'pending'
            elif all(p.state == 'done' for p in pickings):
                order.delivery_status = 'full'
            elif any(p.state == 'done' for p in pickings):
                order.delivery_status = 'partial'
            else:
                order.delivery_status = 'pending'
