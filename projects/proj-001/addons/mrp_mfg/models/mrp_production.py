# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class MrpProduction(models.Model):
    """生产工单 — 继承扩展标准 mrp.production"""
    _inherit = 'mrp.production'
    _description = '生产工单'

    # === 自定义字段（Slice 4） ===
    qty_variance = fields.Float(
        string='数量差异',
        compute='_compute_qty_variance',
        store=True,
        help='计划数量 − 完成数量（正值=未达产，负值=超产）',
    )

    # === 自定义字段（Slice 5 — 生产执行） ===
    is_material_consumed = fields.Boolean(
        string='已领料',
        compute='_compute_is_material_consumed',
        store=True,
        help='当所有原料的实际领用量 > 0 时为 True',
    )

    consumption_note = fields.Text(
        string='领料备注',
        help='记录领料时的特殊情况（如部分领料原因等）',
    )

    # === 计算方法 ===
    # P1-02: depends 完整 — product_qty 和 qty_producing 是唯一依赖
    @api.depends('product_qty', 'qty_producing')
    def _compute_qty_variance(self):
        """计算计划与完成数量的差异"""
        for production in self:  # P1-02: 始终用 for 循环（Recordset 思维）
            production.qty_variance = production.product_qty - production.qty_producing

    # P1-02: depends 完整 — move_raw_ids.quantity 是唯一依赖
    # 注意：Odoo 17 将 quantity_done 合并为 quantity
    @api.depends('move_raw_ids.quantity')
    def _compute_is_material_consumed(self):
        """计算是否已完成领料（US-009）"""
        for production in self:
            if production.move_raw_ids:
                production.is_material_consumed = all(
                    m.quantity > 0 for m in production.move_raw_ids
                )
            else:
                production.is_material_consumed = False

    # === SQL 约束 ===
    _sql_constraints = [
        ('qty_positive',
         'CHECK(product_qty > 0)',
         '生产数量必须大于零'),
    ]

    # === 按钮方法（Slice 4 — 确认） ===
    def action_confirm(self):
        """确认生产工单（US-008）— 加 BOM 有效性前置检查"""
        for production in self:
            # 前置检查：BOM 必须存在且非归档
            if not production.bom_id:
                raise ValidationError("请关联物料清单（BOM）后再确认工单")
            if hasattr(production.bom_id, 'state') and production.bom_id.state == 'archived':
                raise ValidationError(
                    "BOM '%s' 已归档，请关联有效的 BOM"
                    % production.bom_id.display_name
                )
        # P2-02: 必须调用 super()
        return super().action_confirm()

    # === 按钮方法（Slice 5 — 领料） ===
    def action_consume_materials(self):
        """一键领料：批量设置原料的实际领用量（US-009）"""
        for production in self:
            if production.state != 'confirmed':
                raise UserError("仅已确认的工单可以执行领料操作")
            if not production.move_raw_ids:
                raise UserError("工单没有原料需求，请检查关联的 BOM")
            # 批量设置 quantity = product_uom_qty（全量领料）
            # 注意：Odoo 17 将 quantity_done 合并为 quantity
            for move in production.move_raw_ids:
                move.quantity = move.product_uom_qty
            # 推进工单状态到"进行中"
            production.write({'state': 'progress'})
        return True

    # === 按钮方法（Slice 5 — 报工） ===
    def action_produce(self):
        """报工完成：记录完成数量并完工（US-010）"""
        for production in self:
            if production.state != 'progress':
                raise UserError("仅进行中的工单可以执行报工操作")
            # 如果用户未手动设置 qty_producing，默认全量完成
            if not production.qty_producing:
                production.qty_producing = production.product_qty
        # 调用标准完工方法 — 自动处理成品入库等逻辑
        # P2-02: 利用标准 button_mark_done() 保留核心逻辑
        return self.button_mark_done()

    # === API 约束 ===
    @api.constrains('bom_id')
    def _check_bom_active(self):
        """关联的 BOM 不可处于归档状态（US-008 AC）"""
        for production in self:
            if production.bom_id and hasattr(production.bom_id, 'state'):
                if production.bom_id.state == 'archived':
                    raise ValidationError(
                        "不可关联已归档的 BOM '%s'"
                        % production.bom_id.display_name
                    )
