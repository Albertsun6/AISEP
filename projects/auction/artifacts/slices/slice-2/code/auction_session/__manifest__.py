{
    'name': 'Auction - Session Management',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': '拍卖会管理：场次创建、拍品编排、规则配置',
    'author': 'Auction Team',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'auction_lot'],
    'application': False,
    'installable': True,
    'data': [
        # P1-01: Security 优先加载
        'security/auction_session_security.xml',
        'security/ir.model.access.csv',
        # Views — 被引用的先加载
        'views/auction_session_views.xml',
        'views/auction_session_menus.xml',
    ],
}
