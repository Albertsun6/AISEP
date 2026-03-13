# AISEP 框架知识库设计（Framework Knowledge Base）

## 问题

原始设计中 `adapters/odoo17.yaml` 只是一个薄配置层，存在以下不足：

| 问题 | 影响 |
|------|------|
| 没有框架设计哲学说明 | AI 生成的代码不符合框架惯例 |
| 没有版本约束 | 可能生成过时或不兼容的 API 调用 |
| 没有编码规范 | 每次生成的代码风格不一致 |
| 没有最佳实践 | 犯框架新手才会犯的错 |
| 没有已知陷阱 | 踩已知的坑 |

## 设计：Adapter → Framework Knowledge Base（Skill）

把 `adapters/` 升级为 `skills/frameworks/`，对齐 Antigravity Skills 机制，每个框架是一个 skill 目录：

```
.agents/skills/frameworks/
├── _registry.yaml              ← 框架注册表（所有可用框架索引）
├── odoo17/                     ← Odoo 17 框架知识库
│   ├── manifest.yaml           ← 框架元数据 + 版本约束
│   ├── philosophy.md           ← 设计哲学和核心概念
│   ├── structure.md            ← 项目/模块结构规范
│   ├── conventions.md          ← 框架特定编码规范
│   ├── best-practices.md       ← 最佳实践（沉淀研究成果）
│   ├── pitfalls.md             ← 已知陷阱和规避方法
│   ├── api-reference.md        ← 关键 API 速查（ORM, Fields, Views）
│   └── templates/              ← 代码生成模板
│       ├── manifest.tmpl.py
│       ├── model.tmpl.py
│       ├── view.tmpl.xml
│       └── ...
├── react18/                    ← React 18（未来）
│   ├── manifest.yaml
│   ├── philosophy.md
│   └── ...
└── fastapi/                    ← FastAPI（未来）
    ├── manifest.yaml
    ├── philosophy.md
    └── ...
```

---

## 框架元数据 `manifest.yaml`

```yaml
# .agents/skills/frameworks/odoo17/manifest.yaml
framework:
  id: odoo17
  name: "Odoo"
  version: "17.0"
  edition: "Community"          # Community | Enterprise
  language: python
  language_version: ">=3.10"
  
  # 适用的 pipeline 阶段（哪些阶段需要参考此框架知识）
  applicable_stages:
    - s3   # 架构设计 — 需要知道 Odoo 的模块结构
    - s4   # 详细设计 — 需要知道 ORM API
    - s5   # 代码生成 — 需要模板和规范
    - s6   # 测试     — 需要知道 Odoo 测试框架
    - s7   # 部署     — 需要知道运行环境

  # 依赖的外部工具和版本
  dependencies:
    runtime:
      python: ">=3.10"
      postgresql: ">=14"
      wkhtmltopdf: "0.12.6"     # 报表用
    dev:
      docker: ">=24.0"
      docker-compose: ">=2.20"

  # ERP 领域 → 框架标准模块映射
  standard_modules:
    hr: { module: "hr", description: "人力资源基础" }
    payroll: { module: "hr_payroll", description: "薪资管理" }
    accounting: { module: "account", description: "会计核算" }
    inventory: { module: "stock", description: "库存管理" }
    sales: { module: "sale", description: "销售管理" }
    purchase: { module: "purchase", description: "采购管理" }
    crm: { module: "crm", description: "客户关系管理" }
    project: { module: "project", description: "项目管理" }
    manufacturing: { module: "mrp", description: "生产制造" }

  # 部署配置默认值
  deployment:
    runtime: docker
    database: postgresql
    default_port: 8069
    admin_port: 8072
```

---

## 框架知识文件说明

### `philosophy.md` — 设计哲学

```markdown
# Odoo 17 设计哲学

## 核心原则
1. **模块化**：每个功能是独立可安装的模块
2. **继承优先**：通过 _inherit 扩展，不修改核心
3. **Convention over Configuration**：遵循命名约定减少配置
4. **数据驱动 UI**：Views 由 XML 声明，不写前端代码

## AI 生成代码时必须遵守
- 永远不修改核心模块，只创建自定义模块
- 使用 ORM 操作数据库，不写裸 SQL（除非性能需要）
- 业务逻辑放 models/，UI 定义放 views/，严格分离
```

### `structure.md` — 模块结构规范

```markdown
# 模块目录结构

必须的文件：
├── __init__.py          # 包初始化
├── __manifest__.py      # 模块声明

推荐的目录：
├── models/              # 数据模型（必须有 __init__.py）
├── views/               # XML 视图定义
├── security/            # ir.model.access.csv + record rules
├── data/                # 初始数据 XML
├── static/              # 前端静态资源
├── controllers/         # HTTP 路由控制器
├── wizards/             # 弹窗向导
├── reports/             # QWeb 报表模板
├── tests/               # 单元测试
└── i18n/                # 翻译文件
```

### `best-practices.md` — 最佳实践（沉淀研究成果）

这里就是沉淀之前搜索到的 Odoo 最佳实践：

```markdown
# Odoo 17 最佳实践

## ORM 用法
- ✅ 用 `search_read()` 代替 `search()` + `read()` 组合
- ✅ 用 `read_group()` 做聚合，不要 Python 循环计算
- ✅ 批量操作 recordset：`records.write({...})`
- ❌ 不要在循环内调 `search()` 或 `write()`（N+1 问题）
- ❌ 不要在 compute 方法中访问 self.env.cr 执行 SQL

## 字段设计
- `Many2one` 字段加 `index=True`
- `computed` 字段如果频繁搜索/分组，加 `store=True`
- 用 `_sql_constraints` 定义数据库级约束

## View 设计
- 修改已有 view 用 `xpath` + `position="attributes"`，不用 `replace`
- 用 XML ID 引用，不用硬编码数据库 ID

## 安全
- 每个模型必须有 `ir.model.access.csv` 定义
- 敏感字段用 record rules 控制行级权限
```

### `pitfalls.md` — 已知陷阱

```markdown
# Odoo 17 已知陷阱

## P1: compute 字段死循环
- 原因：A compute 依赖 B，B compute 依赖 A
- 规避：画依赖图，确保无环

## P2: onchange 不触发
- 原因：`onchange` 只在 UI 触发，代码 `write()` 不触发
- 规避：业务逻辑放 `write()` override 而非 `onchange`

## P3: 模块更新丢数据
- 原因：`data/` 目录的 XML 带 `noupdate="0"` 时每次更新会覆盖
- 规避：初始数据设 `noupdate="1"`

## P4: Many2many 的 CSV 导入问题
- 原因：CSV 格式不支持 Many2many 的批量写入语法
- 规避：用 XML 而非 CSV 导入 Many2many 数据
```

---

## 版本管理策略

```
.agents/skills/frameworks/
├── odoo17/         ← Odoo 17 知识库
├── odoo18/         ← Odoo 18 知识库（未来）
├── react18/        ← React 18
├── react19/        ← React 19（未来）
└── fastapi/        ← FastAPI（版本变化小，不细分版本）
```

**版本策略**：
- 大版本变化大的框架（Odoo, React）→ **每大版本一个目录**
- 变化小或语义化良好的（FastAPI, Tailwind）→ **一个目录 + manifest 里标版本范围**

---

## 框架组合（Multi-Framework 项目）

未来一个项目可能用多个框架：

```yaml
# projects/{id}/project.yaml
tech_stack:
  backend: odoo17             # Odoo 做 ERP 后端
  frontend: react18           # React 做自定义前端（可选）
  api: fastapi                # FastAPI 做中间层 API（可选）
```

此时 S3 架构设计需要考虑**框架间集成方式**，S5 生成代码时按框架分别调用对应的知识库和模板。

---

## 与现有分层的关系

```
控制面：
  .agents/workflows/                    不变
  .aisep/schemas/                        不变

知识面（对齐 Antigravity Skills）：
  .agents/skills/methodologies/         方法论 = skill
  .agents/skills/frameworks/            框架知识 = skill（含代码模板）
  .aisep/conventions/                    全局通用规范保留

关键变化：
  ❌ .aisep/adapters/          删除
  ❌ .aisep/frameworks/        → 迁移到 .agents/skills/frameworks/
  ❌ .aisep/methodologies/     → 迁移到 .agents/skills/methodologies/
  ❌ .aisep/templates/code/    → 迁移到各 skill/frameworks/{name}/templates/
  ✅ .aisep/templates/artifacts/  保留（制品模板与框架无关）
```
