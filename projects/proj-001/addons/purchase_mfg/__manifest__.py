# -*- coding: utf-8 -*-
{
    'name': '采购管理扩展',
    'version': '17.0.1.0.0',
    'category': 'Purchases',
    'summary': '扩展 Odoo 采购模块，适配制造业采购收货流程',
    'description': """
制造业ERP — 采购管理扩展模块
==============================
* 供应商管理（supplier_rank 过滤）
* 询价单 → 采购订单确认流程
* 收货状态跟踪（receipt_status 计算字段）
* 订单行数量/单价校验（qty > 0, price >= 0 约束）
    """,
    'author': 'AISEP',
    'license': 'LGPL-3',
    'depends': [
        'purchase',
        'stock',
        'product',
    ],
    'data': [
        # P1-01: 安全文件必须在最前面
        'security/purchase_mfg_security.xml',
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/purchase_mfg_menus.xml',
    ],
    'demo': [
        'demo/purchase_mfg_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
