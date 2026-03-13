# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    """采购订单 — 继承扩展标准 purchase.order"""
    _inherit = 'purchase.order'

    # === 自定义字段 ===
    receipt_status = fields.Selection(
        selection=[
            ('pending', '待收货'),
            ('partial', '部分收货'),
            ('full', '已全部收货'),
        ],
        string='收货状态',
        compute='_compute_receipt_status',
        store=True,
        help='根据关联收货单的状态自动计算',
    )

    # === 计算方法 ===
    # P1-02: depends 完整 — picking_ids.state 是唯一依赖
    @api.depends('picking_ids.state')
    def _compute_receipt_status(self):
        """根据关联收货单状态计算收货进度"""
        for order in self:  # P1-02: 始终用 for 循环（Recordset 思维）
            pickings = order.picking_ids
            if not pickings:
                order.receipt_status = 'pending'
            elif all(p.state == 'done' for p in pickings):
                order.receipt_status = 'full'
            elif any(p.state == 'done' for p in pickings):
                order.receipt_status = 'partial'
            else:
                order.receipt_status = 'pending'
