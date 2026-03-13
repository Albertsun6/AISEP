# AISEP 逆向 Onboard 设计（V1 草案）

> [!NOTE]
> 这是初步框架，标记了大量待深化的点。正向 pipeline 完成后再展开细化。

## 定位

独立的 Onboard 流程，将现有 Odoo 模块逆向为 AISEP 标准制品，纳入项目管理。

```
/onboard --source ./path/to/modules
  → R1 扫描 → R2 领域还原 → R3 制品对齐 → Gate
  → 项目出现在 registry.yaml，可用 /pipeline 继续正向演进
```

## 逆向准确度（Odoo 特化）

| 层级 | 准确度 | 来源 |
|------|--------|------|
| 模块元数据 | 100% | `__manifest__.py` |
| 数据模型 + 字段 | 100% | `models/*.py` 声明式 |
| 视图结构 | 100% | `views/*.xml` 声明式 |
| 安全规则 | 100% | `ir.model.access.csv` |
| 计算逻辑 / 业务规则 | ~85-90% | Python 代码需 AI 理解意图 |
| 业务需求（WHY） | ~60% | 代码只有 WHAT，需人补充 |

低置信度项标注 `confidence` 字段，交用户在 Gate 补充。

## 已知待解决问题

### 🔴 模块依赖与处理顺序

```
custom_hr
├── depends: [hr, hr_contract]        ← 标准模块（不需逆向）
└── depends: [custom_base_utils]      ← 自定义模块（需要先逆向）

处理顺序应为：
1. 扫描所有模块的 __manifest__.py
2. 构建依赖图
3. 区分标准模块 vs 自定义模块
4. 按拓扑序逆向自定义模块（被依赖的先处理）
```

- TODO: 标准模块如何识别？通过 `skills/frameworks/odoo17/` 的 standard_modules 列表
- TODO: 循环依赖如何处理？

### 🔴 跨模块引用

- `_inherit` 扩展另一个模块的 model
- `_inherits` 委托继承
- 跨模块的 `Many2one` / `Many2many` 关系
- TODO: 逆向时如何保持跨模块引用的完整性？

### 🟡 未覆盖的 Odoo 制品类型

| 制品 | 文件 | 优先级 |
|------|------|--------|
| Wizard（向导） | `wizards/*.py` | 高 — 包含业务流程 |
| Report（报表） | `reports/*.xml` (QWeb) | 中 |
| Controller（路由） | `controllers/*.py` | 中 — HTTP API |
| Scheduled Action | `data/ir_cron.xml` | 中 |
| Email Template | `data/mail_template.xml` | 低 |
| Demo Data | `demo/*.xml` | 低 |
| i18n 翻译 | `i18n/*.po` | 低 — 但对 glossary 有价值 |
| 静态资源 | `static/` | 低 |

### 🟡 逆向后的 Slice 划分

- 现有模块的功能如何自动划分为 Slice？
- 依据：model 间的聚合关系 + view 的菜单结构
- TODO: 需要定义自动 Slice 推断规则

### 🟢 数据迁移

- 逆向管理的是**代码结构**，不涉及数据迁移
- 如果用户要从旧系统迁移数据，是另一个话题

---

## 人工补齐机制（Completion Template）

逆向完成后，系统对低置信度字段生成**结构化补齐清单**，用精准问题引导用户：

```yaml
# projects/{id}/artifacts/onboard/completion-checklist.yaml
completion:
  - artifact: glossary.yaml
    items:
      - field: "terms[0].definition"
        current: "生产任务记录"          # AI 推断
        confidence: 0.7
        question: "production_order 的业务定义是什么？AI 推断为'生产任务记录'，准确吗？"
        status: pending                  # pending → confirmed → revised

  - artifact: domain-model.yaml
    items:
      - field: "business_rules[2].rationale"
        current: null
        confidence: 0
        question: "约束 _check_qty_positive 要求数量为正，业务原因是什么？"
        status: pending
```

### 三类需补齐内容

| 类型 | 内容 | AI 能做的 | 人要补的 |
|------|------|----------|---------|
| **确认类** | 术语定义、模型描述 | AI 给出推断 | 确认或修正 |
| **意图类** | 业务目标、用户故事 | 无法推断 | 从零填写（AI 提供引导问题） |
| **演进类** | 改进方向、已知问题 | 无法推断 | 填写期望 Target 状态 |

---

## 🆕 增量演进机制（借鉴 OpenSpec `changes/` 变更隔离）

Onboard 完成后，项目进入**增量演进**模式。每次变更作为一个独立的"变更单元"隔离管理：

### Greenfield vs Brownfield 路径

```
Greenfield（新项目）                 Brownfield（Onboard 后）
  artifacts/slices/                   artifacts/changes/
    slice-1-bom/                        change-001-add-qc/
      design.yaml (S4)                   proposal.yaml    ← 🆕
      code/       (S5)                   design.yaml      (对齐 S4)
      tests/      (S6)                   implementation/  (对齐 S5-S6)

  共享：S4-S6 的执行逻辑和 Gate 检查完全一致
```

### 变更提案 `proposal.yaml`

Brownfield 项目的每次变更需要先进行**影响分析**（这是 Greenfield Slice 不需要的额外步骤）：

```yaml
# projects/{id}/artifacts/changes/change-001-add-qc/proposal.yaml
change:
  id: "change-001"
  title: "增加质量检验模块"
  type: "feature"                # feature | bugfix | refactor | migration
  priority: high

  # 影响分析（Onboard 后有 baseline，可以做差异分析）
  impact:
    affected_models:
      - model: "production.order"
        change: "extend"         # 新增 qc_status 字段
      - model: "quality.check"
        change: "create"         # 全新 model
    affected_views:
      - "view_production_order_form"  # 需要追加质检按钮
    dependencies:
      - "slice-2-production-order"    # 依赖的已有 Slice
    risk: medium
    estimated_lines: 400

  # Gate：用户确认影响范围后进入 S4 设计
  status: proposed               # proposed → approved → in_progress → completed
```

### 生命周期

```
用户提出变更需求
  ↓
生成 proposal.yaml（影响分析）
  ↓ Gate: 用户确认影响范围
进入 S4-S6 正向流程（复用 Slice 的执行逻辑）
  ↓
完成后状态标记 completed
```

> [!TIP]
> `changes/` 和 `slices/` 不互斥。一个 Onboard 后的项目可以同时有：
> - `slices/`：Onboard 时逆向还原的原有功能切片
> - `changes/`：后续新增的功能变更

---

## 后续行动

- [ ] 正向 pipeline 完成后展开 Onboard 的详细设计
- [ ] 设计依赖图构建和拓扑排序算法
- [ ] 设计跨模块引用的处理策略
- [ ] 补充 Wizard / Report / Controller 的逆向规则
- [ ] 设计自动 Slice 推断机制
- [ ] 细化 completion-checklist 的交互流程
- [ ] 🆕 设计 `proposal.yaml` 的 schema 验证规则
- [ ] 🆕 设计 `changes/` 与 `slices/` 混合模式下的依赖管理
