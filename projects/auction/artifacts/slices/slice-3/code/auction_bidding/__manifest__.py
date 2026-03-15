{
    'name': 'Auction - Bidding Engine',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': '竞价引擎：出价、成交判定、有条件成交、竞价记录',
    'author': 'Auction Team',
    'license': 'LGPL-3',
    'depends': ['base', 'bus', 'auction_lot', 'auction_session'],
    'application': False,
    'installable': True,
    'data': [
        # P1-01: Security 优先加载
        'security/ir.model.access.csv',
        # Views
        'views/auction_bidding_views.xml',
        'views/auction_bidding_menus.xml',
    ],
}
