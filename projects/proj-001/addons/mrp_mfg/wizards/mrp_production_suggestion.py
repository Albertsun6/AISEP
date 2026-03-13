# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class MrpProductionSuggestion(models.TransientModel):
    """生产建议向导 — 基于销售需求建议生产计划（US-007）"""
    _name = 'mrp.production.suggestion'
    _description = '生产建议向导'

    suggestion_line_ids = fields.One2many(
        'mrp.production.suggestion.line',
        'wizard_id',
        string='建议明细',
    )

    def action_compute_suggestions(self):
        """计算生产建议：扫描已确认销售订单 vs 库存"""
        self.ensure_one()
        self.suggestion_line_ids.unlink()

        # 1. 查询已确认销售订单中的产品需求
        SaleOrderLine = self.env['sale.order.line']
        sale_lines = SaleOrderLine.search([
            ('order_id.state', '=', 'sale'),
            ('product_id.type', '=', 'product'),  # 仅库存型产品
        ])

        if not sale_lines:
            raise UserError("当前无已确认的销售订单，无需生产")

        # 2. 按产品聚合需求量
        demand_map = {}  # product_id -> total_qty
        for line in sale_lines:
            pid = line.product_id.id
            demand_map[pid] = demand_map.get(pid, 0) + line.product_uom_qty

        # 3. 对比库存，计算缺口
        lines_vals = []
        for product_id, demand_qty in demand_map.items():
            product = self.env['product.product'].browse(product_id)
            available = product.qty_available
            shortage = demand_qty - available
            if shortage <= 0:
                continue  # 库存充足，跳过

            # 查找关联的 BOM
            bom = self.env['mrp.bom'].search([
                ('product_tmpl_id', '=', product.product_tmpl_id.id),
                ('active', '=', True),
            ], limit=1)

            lines_vals.append({
                'wizard_id': self.id,
                'product_id': product_id,
                'demand_qty': demand_qty,
                'available_qty': available,
                'shortage_qty': shortage,
                'bom_id': bom.id if bom else False,
                'selected': True,
            })

        if not lines_vals:
            raise UserError("库存充足，当前无需生产")

        self.env['mrp.production.suggestion.line'].create(lines_vals)

        # 重新打开向导
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_create_productions(self):
        """一键创建生产工单"""
        self.ensure_one()
        selected_lines = self.suggestion_line_ids.filtered('selected')
        if not selected_lines:
            raise UserError("请至少选择一项建议")

        productions = self.env['mrp.production']
        for line in selected_lines:
            if not line.bom_id:
                raise UserError(
                    "产品 '%s' 没有关联的 BOM，无法创建工单"
                    % line.product_id.display_name
                )
            productions += self.env['mrp.production'].create({
                'product_id': line.product_id.id,
                'bom_id': line.bom_id.id,
                'product_qty': line.shortage_qty,
                'product_uom_id': line.product_id.uom_id.id,
            })

        # 返回创建的工单列表
        return {
            'type': 'ir.actions.act_window',
            'name': '已创建的生产工单',
            'res_model': 'mrp.production',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', productions.ids)],
            'target': 'current',
        }


class MrpProductionSuggestionLine(models.TransientModel):
    """生产建议行"""
    _name = 'mrp.production.suggestion.line'
    _description = '生产建议明细行'

    wizard_id = fields.Many2one(
        'mrp.production.suggestion',
        string='向导',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string='产品',
        readonly=True,
    )
    demand_qty = fields.Float(
        string='需求量',
        readonly=True,
    )
    available_qty = fields.Float(
        string='可用库存',
        readonly=True,
    )
    shortage_qty = fields.Float(
        string='缺口量',
        readonly=True,
    )
    bom_id = fields.Many2one(
        'mrp.bom',
        string='物料清单',
        readonly=True,
    )
    selected = fields.Boolean(
        string='选择',
        default=True,
    )
