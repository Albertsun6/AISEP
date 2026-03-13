# -*- coding: utf-8 -*-
{
    'name': '制造管理扩展',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': '扩展 Odoo MRP 模块，实现 BOM 管理、生产执行和 MRP 建议',
    'description': """
制造业ERP — 制造管理扩展模块
==============================
* BOM 生命周期管理（草稿 → 生效 → 归档）
* BOM 子件校验（子件不可与父件相同）
* 生产工单确认前置检查（BOM 有效性校验）
* 生产执行：一键领料 + 报工完工
* 数量差异计算字段（计划 vs 实际）
* 基于销售需求的 MRP 生产建议向导
    """,
    'author': 'AISEP',
    'license': 'LGPL-3',
    'depends': [
        'mrp',
        'stock',
        'product',
        'sale',  # Slice 6: MRP 建议需查询销售订单
    ],
    'data': [
        # P1-01: 安全文件必须在最前面
        'security/mrp_mfg_security.xml',
        'security/ir.model.access.csv',
        'views/mrp_bom_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_production_suggestion_views.xml',
        'views/mrp_mfg_menus.xml',
    ],
    'demo': [
        'demo/mrp_mfg_demo.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
