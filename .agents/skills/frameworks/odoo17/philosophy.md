# Odoo 17 设计哲学

## 核心设计原则

### 1. 模块化（Modularity）

Odoo 的每个功能是一个**独立可安装的模块**。模块间通过 `depends` 声明依赖。

**关键理解：模块 ≠ 应用**
- **应用（Application）**：在 `__manifest__` 中 `application: True`，出现在 Apps 菜单
- **模块（Module）**：任何可安装的包，不一定是应用
- 建议：自定义业务模块通常**不设为 Application**，除非它是一个全新的顶级功能区

### 2. 继承体系（Inheritance System）

Odoo 的灵魂是**通过继承扩展而非修改**。理解三种继承至关重要：

| 类型 | 用途 | 关键语法 | 结果 |
|------|------|---------|------|
| **类继承** | 给已有 Model 添加字段/方法 | `_inherit = 'sale.order'`（无 `_name`） | 修改原 Model，不创建新表 |
| **原型继承** | 以已有 Model 为模板创建新 Model | `_inherit = 'sale.order'` + `_name = 'custom.order'` | 创建新表，复制所有字段 |
| **委托继承** | 嵌入式组合（composition） | `_inherits = {'res.partner': 'partner_id'}` | 透明访问父 Model 字段 |

**决策指南**：
- 需要给 `sale.order` 加字段？→ **类继承**
- 需要一个类似订单但独立的业务对象？→ **原型继承**
- 需要让自定义实体"天然拥有"联系人信息？→ **委托继承**

### 3. 数据驱动 UI（Data-Driven UI）

Odoo 的 UI 完全用 **XML 声明**，不需要写 JavaScript/HTML：
- 表单布局 → `<form>` + `<group>` + `<field>`
- 列表 → `<tree>` + `<field>`
- 看板 → `<kanban>` + QWeb 模板
- 搜索 → `<search>` + `<filter>` + `<group>`

**哲学含义**：前端完全由后端数据驱动。改变 View XML 就改变 UI，零前端代码。

### 4. Convention over Configuration

Odoo 依赖大量**命名约定**来减少配置：
- `_name = 'module.model'` → 自动创建表 `module_model`
- `name` 字段 → 自动成为 `_rec_name`（默认显示名）
- `company_id` 字段 → 自动启用多公司支持
- `sequence` 字段 → 自动支持拖拽排序
- `active` 字段 → 自动支持"归档"功能（`active = False` 的记录默认隐藏）

### 5. 安全模型（Security by Default）

安全不是可选项，而是**默认行为**：
- 没有 ACL 的 Model → 所有用户**完全无法访问**（deny by default）
- Record Rules → 行级过滤（如"只看自己部门的数据"）
- Groups 继承 → `implied_ids` 链式继承（Manager 自动拥有 User 的权限）

## ORM 核心概念

### Recordset 思维

Odoo ORM 的核心是 **Recordset**（记录集）——所有操作都是面向"一组记录"的：

```python
# ✅ Recordset 思维 — 批量操作
orders = self.env['sale.order'].search([('state', '=', 'draft')])
orders.write({'state': 'sent'})  # 一次 SQL 更新所有

# ❌ 逐条思维 — N+1 问题
for order in orders:
    order.write({'state': 'sent'})  # N 次 SQL
```

### 环境（Environment）

`self.env` 是 Odoo 的"上下文对象"，携带：
- `self.env.user` — 当前用户
- `self.env.company` — 当前公司
- `self.env.cr` — 数据库游标（谨慎使用）
- `self.env.context` — 传递上下文参数

### 计算字段（Computed Fields）

计算字段是 Odoo 的强大特性，但也是**主要陷阱来源**：
- `store=True` → 存储到数据库，可搜索、可分组
- `store=False`（默认）→ 实时计算，不可搜索
- `depends` → 声明依赖，**必须完整**，否则不会触发重计算

## AISEP 使用指引

在 AISEP 的 Pipeline 中，理解这些哲学有助于：

| 阶段 | 指导作用 |
|------|---------|
| **S3** | 利用继承体系决定模块关系（inherit/new/depend） |
| **S4** | 理解 Convention 简化设计（不需要设计的部分由约定承担） |
| **S5** | 生成符合 ORM 思维的代码（Recordset 批量操作，非逐条） |
| **S6** | 用 `TransactionCase` 测试 Model 逻辑，每个 test 自动回滚 |
