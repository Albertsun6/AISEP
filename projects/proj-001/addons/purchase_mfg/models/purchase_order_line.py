# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrderLine(models.Model):
    """采购订单行 — 继承扩展标准 purchase.order.line"""
    _inherit = 'purchase.order.line'

    # === SQL 约束 ===
    _sql_constraints = [
        ('qty_positive',
         'CHECK(product_qty > 0)',
         '采购数量必须大于零'),
        ('price_non_negative',
         'CHECK(price_unit >= 0)',
         '单价不可为负'),
    ]

    # === Python 约束 ===
    @api.constrains('product_qty')
    def _check_product_qty(self):
        """数量 ≤ 0 时阻止保存"""
        for line in self:
            if line.product_qty <= 0:
                raise ValidationError('采购数量必须大于零')
