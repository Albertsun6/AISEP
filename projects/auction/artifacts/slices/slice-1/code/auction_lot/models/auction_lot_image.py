from odoo import fields, models


class AuctionLotImage(models.Model):
    _name = 'auction.lot.image'
    _description = '拍品图片'
    _rec_name = 'lot_id'
    _order = 'sequence, id'

    # --- 关系字段 ---
    lot_id = fields.Many2one(
        'auction.lot',
        string='所属拍品',
        required=True,
        index=True,
        ondelete='cascade',
    )

    # --- 普通字段 ---
    image = fields.Binary(
        string='图片',
        required=True,
        attachment=True,
    )
    sequence = fields.Integer(
        string='排序',
        default=10,
    )
    description = fields.Char(
        string='图片说明',
    )
