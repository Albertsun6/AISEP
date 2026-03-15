{
    'name': 'Auction - Lot Management',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': '拍品档案管理：录入、图片、定价、分类',
    'author': 'Auction Team',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'application': True,
    'installable': True,
    'data': [
        # P1-01: Security 优先加载
        'security/auction_lot_security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/auction_lot_category_data.xml',
        # Views — 被引用的先加载
        'views/auction_lot_category_views.xml',
        'views/auction_lot_views.xml',
        'views/auction_lot_menus.xml',
    ],
}
