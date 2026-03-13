---
name: odoo17
description: "Odoo 17 Community Edition 框架知识库"
applicable_stages: [s3, s4, s5, s6, s7]

requires:
  stage: [s3, s4, s5, s6, s7]
  tech_stack: "odoo17"
  bins: ["python3"]

always: false
---

# Odoo 17 框架知识库

> Odoo 17 Community Edition 的核心知识。S3 确认技术栈后由 Gating 自动加载。

## 适用阶段

| 阶段 | 用途 |
|------|------|
| **S3** 架构设计 | 模块结构规划、数据模型设计、标准模块映射 |
| **S4** Slice 设计 | Model 字段详设、View 布局、继承策略选择 |
| **S5** 代码实现 | 代码生成模板、命名规范、API 使用 |
| **S6** 测试验证 | 测试框架（`TransactionCase` / `HttpCase`）、安装验证 |
| **S7** 部署配置 | Docker 配置、`odoo.conf` 参数、模块安装命令 |

## 核心约定（必须遵守）

1. **继承优先于修改** — 使用 `_inherit` 扩展，**禁止**直接修改核心模块代码
2. **ORM 操作数据库** — 不写裸 SQL（除非性能需要且经人确认）
3. **业务逻辑在 models/** — UI 定义在 views/，严格分离
4. **每个 Model 必须有 ACL** — `ir.model.access.csv` 至少定义 base user 权限
5. **XML ID 唯一** — 所有 XML ID 必须以模块名为前缀

## MVC-A 架构

Odoo 使用 **Model-View-Action** 架构变体：
- **Model**：Python 类 → `models.Model` / `models.TransientModel`
- **View**：XML 声明 → form / tree / kanban / search / graph / pivot
- **Action**：`ir.actions.act_window` → 连接 Model 和 View
- **Menu**：`ir.ui.menu` → 用户导航入口

## 模块结构速查

```
{module_name}/
├── __init__.py              ← 包初始化
├── __manifest__.py          ← 模块声明（必须）
├── models/                  ← 数据模型（必须有 __init__.py）
├── views/                   ← XML 视图定义
├── security/                ← ACL + Record Rules
├── data/                    ← 初始数据 XML
├── demo/                    ← 演示数据
├── wizards/                 ← TransientModel 弹窗向导
├── reports/                 ← QWeb 报表模板
├── controllers/             ← HTTP 路由控制器
├── static/description/      ← 模块图标和描述
├── tests/                   ← 单元测试
└── i18n/                    ← 翻译文件
```

## 命名规范

| 对象 | 规则 | 示例 |
|------|------|------|
| 模块名 | `snake_case`，前缀标识领域 | `hr_attendance_tracking` |
| Model 类名 | `PascalCase` | `AttendanceRecord` |
| `_name` | `模块.实体`，点号分隔 | `hr.attendance.record` |
| 字段名 | `snake_case` | `check_in_time` |
| XML ID (View) | `view_{model}_{type}` | `view_attendance_record_form` |
| XML ID (Action) | `action_{model}` | `action_attendance_record` |
| XML ID (Menu) | `menu_{model}` | `menu_attendance_record` |
| XML ID (Group) | `group_{role}` | `group_hr_manager` |
| 测试类 | `Test{Feature}` | `TestAttendance` |
| 测试方法 | `test_{what}_{scenario}` | `test_create_record_success` |

## 标准模块映射（ERP 领域 → Odoo 模块）

| 领域 | Odoo 模块 | 描述 |
|------|-----------|------|
| 人力资源 | `hr` | 员工、部门、岗位 |
| 薪资 | `hr_payroll` | 薪资计算和发放 |
| 考勤 | `hr_attendance` | 打卡和出勤 |
| 会计 | `account` | 总账、应收、应付 |
| 库存 | `stock` | 仓库管理、调拨 |
| 销售 | `sale` | 报价单、销售订单 |
| 采购 | `purchase` | 采购订单、供应商 |
| CRM | `crm` | 线索、商机管理 |
| 项目 | `project` | 项目和任务管理 |
| 制造 | `mrp` | BOM、生产工单 |
| 维护 | `maintenance` | 设备维护管理 |
| 质量 | `quality_control` | 质量检查 |

## 知识库文件索引

| 文件 | 内容 | 何时参考 |
|------|------|---------|
| `philosophy.md` | 设计哲学和核心概念 | S3 架构设计时 |
| `structure.md` | 模块结构规范和 `__manifest__` 字段 | S4/S5 时 |
| `best-practices.md` | ORM / View / 安全 / 性能最佳实践 | S5 代码生成时（**必读**） |
| `pitfalls.md` | 已知陷阱和规避方法 | S5 代码生成时（**必读，逐条检查**） |
| `manifest.yaml` | 框架版本约束和依赖 | S3/S7 时 |
| `templates/` | 代码生成模板（Jinja2 格式） | S5 时 |
