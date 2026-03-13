# -*- coding: utf-8 -*-
from odoo import models


class MrpBomLine(models.Model):
    """BOM 行（子件） — 继承扩展标准 mrp.bom.line"""
    _inherit = 'mrp.bom.line'
    _description = 'BOM 明细行'

    # === SQL 约束 ===
    _sql_constraints = [
        ('qty_positive',
         'CHECK(product_qty > 0)',
         '子件用量必须大于零'),
    ]
