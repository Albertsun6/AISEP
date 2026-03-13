# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    """物料清单 — 继承扩展标准 mrp.bom"""
    _inherit = 'mrp.bom'
    _description = '物料清单'

    # === 自定义字段 ===
    state = fields.Selection(
        selection=[
            ('draft', '草稿'),
            ('active', '生效'),
            ('archived', '已归档'),
        ],
        string='状态',
        default='draft',
        required=True,
        tracking=True,
        help='BOM 生命周期：草稿 → 生效 → 已归档',
    )

    # === 按钮方法 ===
    def action_activate(self):
        """激活 BOM：草稿 → 生效（US-001）"""
        for bom in self:
            if not bom.bom_line_ids:
                raise ValidationError("BOM 必须至少有 1 个子件才能激活")
            bom.state = 'active'

    def action_archive_bom(self):
        """归档 BOM：生效 → 已归档（预埋 US-004）"""
        for bom in self:
            bom.write({
                'state': 'archived',
                'active': False,
            })

    # === 约束 ===
    # P1-02: depends 完整 — bom_line_ids 触发子件校验
    @api.constrains('bom_line_ids')
    def _check_bom_line_self_reference(self):
        """校验子件不可与父件相同（US-001 AC）"""
        for bom in self:
            parent_product = bom.product_tmpl_id.product_variant_id
            for line in bom.bom_line_ids:
                if line.product_id == parent_product:
                    raise ValidationError(
                        "子件 '%s' 不可与父件产品相同" % line.product_id.display_name
                    )
