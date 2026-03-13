# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    """销售订单行 — 继承扩展标准 sale.order.line"""
    _inherit = 'sale.order.line'

    # === SQL 约束 ===
    _sql_constraints = [
        (
            'qty_positive',
            'CHECK(product_uom_qty > 0)',
            '销售数量必须大于零',
        ),
    ]

    # === Python 约束 ===
    @api.constrains('product_uom_qty')
    def _check_product_uom_qty(self):
        """验证订单行数量大于零（US-032 AC: 数量 ≤ 0 → 阻止保存）"""
        for line in self:
            if line.product_uom_qty <= 0:
                raise ValidationError('数量必须大于 0')
