# -*- coding: utf-8 -*-
{
    'name': '销售管理扩展',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': '扩展 Odoo 销售模块，适配制造业报价-订单-发货流程',
    'description': """
制造业ERP — 销售管理扩展模块
==============================
* 客户管理（customer_rank 过滤）
* 报价单 → 销售订单确认流程
* 发货状态跟踪（delivery_status 计算字段）
* 订单行数量校验（qty > 0 约束）
    """,
    'author': 'AISEP',
    'license': 'LGPL-3',
    'depends': [
        'sale_management',
        'stock',
        'product',
    ],
    'data': [
        # P1-01: 安全文件必须在最前面
        'security/sale_mfg_security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/sale_pricelist_views.xml',
        'views/sale_mfg_menus.xml',
    ],
    'demo': [
        'demo/sale_mfg_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
