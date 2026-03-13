# -*- coding: utf-8 -*-
{
    'name': '库存管理扩展',
    'version': '17.0.1.0.0',
    'category': 'Inventory',
    'summary': '扩展 Odoo 库存模块，适配制造业出入库、仓库和库位管理',
    'description': """
制造业ERP — 库存管理扩展模块
==============================
* 仓库和库位配置
* 出入库操作和记录查看
* 实时库存量查看
* 出入库记录历史追溯菜单
    """,
    'author': 'AISEP',
    'license': 'LGPL-3',
    'depends': [
        'stock',
        'product',
        'sale_mfg',      # 依赖 Slice 1（销售确认生成发货单）
    ],
    'data': [
        # P1-01: 安全文件在最前面
        'security/stock_mfg_security.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'views/stock_transfer_views.xml',
        'views/stock_mfg_menus.xml',
    ],
    'demo': [
        'demo/stock_mfg_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
