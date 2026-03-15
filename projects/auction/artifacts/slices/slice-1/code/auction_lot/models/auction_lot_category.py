from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AuctionLotCategory(models.Model):
    _name = 'auction.lot.category'
    _description = '拍品分类'
    _order = 'name'
    _parent_name = 'parent_id'
    _parent_store = True

    # --- 关系字段 ---
    parent_id = fields.Many2one(
        'auction.lot.category',
        string='父分类',
        ondelete='cascade',
        index=True,
    )
    child_ids = fields.One2many(
        'auction.lot.category',
        'parent_id',
        string='子分类',
    )

    # --- 普通字段 ---
    name = fields.Char(
        string='分类名称',
        size=64,
        required=True,
    )
    parent_path = fields.Char(
        index=True,
        unaccent=False,
    )

    # --- 约束 ---
    _sql_constraints = [
        ('name_parent_uniq', 'UNIQUE(name, parent_id)',
         '同级分类名称不可重复'),
    ]

    @api.constrains('parent_id')
    def _check_category_recursion(self):
        if not self._check_recursion():
            raise ValidationError('不允许创建循环分类')
