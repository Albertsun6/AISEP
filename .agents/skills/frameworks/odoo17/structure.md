# Odoo 17 模块结构规范

## 目录结构（完整版）

```
{module_name}/
├── __init__.py                  # 包入口，导入子包
├── __manifest__.py              # 模块声明（唯一必须文件）
│
├── models/                      # 数据模型（核心）
│   ├── __init__.py              # 导入所有 model 文件
│   ├── {model_a}.py             # 一个文件一个 Model
│   └── {model_b}.py
│
├── views/                       # XML 视图定义
│   ├── {model_a}_views.xml      # model 的 form/tree/kanban/search
│   ├── {model_b}_views.xml
│   └── {module}_menus.xml       # 菜单和 action 定义（可分离出来）
│
├── security/                    # 安全配置
│   ├── ir.model.access.csv      # ACL（必须）
│   └── {module}_security.xml    # Groups + Record Rules
│
├── data/                        # 初始数据
│   └── {module}_data.xml        # noupdate="1" 的初始化数据
│
├── demo/                        # 演示数据
│   └── {module}_demo.xml        # 仅开发/演示环境加载
│
├── wizards/                     # TransientModel（向导弹窗）
│   ├── __init__.py
│   ├── {wizard_name}.py
│   └── {wizard_name}_views.xml
│
├── reports/                     # QWeb 报表
│   ├── {report_name}.xml        # 报表模板
│   └── {report_name}_action.xml # 报表 Action
│
├── controllers/                 # HTTP 控制器
│   ├── __init__.py
│   └── {controller_name}.py
│
├── tests/                       # 单元测试
│   ├── __init__.py
│   ├── test_{feature_a}.py
│   └── test_{feature_b}.py
│
├── static/                      # 静态资源
│   ├── description/
│   │   ├── icon.png             # 模块图标（128x128）
│   │   └── index.html           # 模块描述页
│   └── src/
│       ├── js/                  # 自定义 JS（OWL 组件）
│       ├── css/                 # 自定义 CSS
│       └── xml/                 # QWeb 前端模板
│
└── i18n/                        # 国际化
    ├── {module_name}.pot        # 翻译模板
    └── zh_CN.po                 # 中文翻译
```

## `__manifest__.py` 字段详解

```python
{
    'name': '模块显示名称',           # 必须
    'version': '17.0.1.0.0',        # 必须，格式：odoo版本.主.次.补丁.构建
    'category': 'Manufacturing',     # 模块分类
    'summary': '一行简述',            # Apps 列表中显示
    'description': '详细描述',        # 可用 RST 格式
    'author': '作者名',
    'website': 'https://...',
    'license': 'LGPL-3',            # 必须，Community 用 LGPL-3

    'depends': [                     # 依赖模块列表
        'base',                      # 几乎所有模块都依赖 base
        'mail',                      # 如需 chatter/消息
        'stock',                     # 如需库存功能
    ],

    'data': [                        # 按顺序加载的数据文件
        'security/ir.model.access.csv',     # ⚠️ 安全文件必须在最前面
        'security/custom_security.xml',
        'views/model_a_views.xml',
        'views/model_b_views.xml',
        'views/menus.xml',                  # 菜单放最后
        'data/initial_data.xml',
    ],

    'demo': [                        # 仅演示模式加载
        'demo/demo_data.xml',
    ],

    'installable': True,             # 可安装
    'application': False,            # 是否为独立应用
    'auto_install': False,           # 依赖全满足时是否自动安装
}
```

> [!WARNING]
> `data` 列表的**顺序很重要**：安全文件必须在 views 之前加载，否则视图引用的 groups 会找不到。

## 版本号约定

```
17.0.1.0.0
 │   │ │ │
 │   │ │ └── 构建号（通常为 0）
 │   │ └──── 补丁版（Bug fix）
 │   └────── 次版本（小功能增加）
 └────────── 主版本 = Odoo 大版本
```

## `__init__.py` 模式

### 根目录

```python
from . import models
from . import wizards      # 如有向导
from . import controllers  # 如有控制器
from . import reports      # 如有报表
```

### models/ 目录

```python
from . import model_a
from . import model_b
# 每新增一个 Model 文件就追加一行
```

## 文件命名约定

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| Model 文件 | `{model_name}.py`（小写下划线） | `bom_line.py` |
| View 文件 | `{model_name}_views.xml` | `bom_line_views.xml` |
| 安全 CSV | `ir.model.access.csv`（固定名） | — |
| 安全 XML | `{module}_security.xml` | `mrp_custom_security.xml` |
| 数据文件 | `{module}_data.xml` | `mrp_custom_data.xml` |
| 演示数据 | `{module}_demo.xml` | `mrp_custom_demo.xml` |
| Wizard 文件 | `{wizard_name}.py` + `_views.xml` | `create_order_wizard.py` |
| 测试文件 | `test_{feature}.py` | `test_bom_creation.py` |
| 翻译模板 | `{module_name}.pot` | `mrp_custom.pot` |

## AISEP 使用指引

在 S5 代码生成阶段：

### Slice 1（创建模块骨架）

必须生成的最小文件集：
1. `__init__.py`（根）
2. `__manifest__.py`
3. `models/__init__.py`
4. `models/{model}.py`（至少一个）
5. `views/{model}_views.xml`（至少一个）
6. `security/ir.model.access.csv`

### Slice N（追加到已有模块）

更新的文件：
1. `models/__init__.py` — 追加 import
2. `__manifest__.py` — 追加 data 列表
3. `security/ir.model.access.csv` — 追加行

新增的文件：
1. `models/{new_model}.py`
2. `views/{new_model}_views.xml`
