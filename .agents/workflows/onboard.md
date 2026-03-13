---
description: "逆向 Onboard — 接管现有系统模块"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
  load:
    - ".aisep/registry.yaml"
    - ".aisep/docs/onboard-reverse-engineering.md"
    - ".aisep/templates/project-scaffold/project.yaml.tmpl"
  skills:
    required: []
    conditional:
      - skill: "frameworks/odoo17"
        condition: "源码包含 __manifest__.py"
  exclude:
    - ".aisep/templates/artifacts/**"
    - "history/**"
---

# 逆向 Onboard Workflow

## 触发

`/onboard --source <path>`

## 前置条件

- `<path>` 指向一个包含可分析源码的目录
- 如目标是 Odoo 模块：目录下存在 `__manifest__.py`

---

## 活动

### 阶段 R1: 扫描与发现

**AI 执行指引**：

#### 步骤 1: 目录探测
1. 扫描 `<path>` 下的文件结构
2. **框架识别**（按优先级匹配）：

| 标志文件 | 识别为 | 加载 Skill |
|----------|--------|------------|
| `__manifest__.py` | Odoo 模块 | `frameworks/odoo17/SKILL.md` |
| `package.json` + `next.config.*` | Next.js 项目 | `frameworks/nextjs/` (如有) |
| `requirements.txt` + `manage.py` | Django 项目 | `frameworks/django/` (如有) |
| 无法识别 | 通用 Python/JS | 不加载框架 Skill |

3. 如框架 Skill 不存在 → 告知用户：「当前知识库不覆盖此框架，逆向质量可能较低」

#### 步骤 2: 依赖图构建（Odoo 特化）
1. 扫描所有模块的 `__manifest__.py` → 提取 `depends` 列表
2. 构建依赖图（DAG）
3. **区分模块类型**：
   - **标准模块**：在 Odoo 官方 addons 列表中（如 `base`, `sale`, `stock`）→ 不逆向，仅记录依赖
   - **自定义模块**：不在标准列表中 → 需要逆向
4. **拓扑排序**：按依赖关系确定处理顺序（被依赖的先处理）

**异常处理**：
- 循环依赖 → 标注警告，将循环中的模块作为一组同时处理
- 依赖的自定义模块不在 `<path>` 中 → 标注缺失，降低相关制品置信度

**交互节点**：
- 🗣️ 展示发现的模块列表 + 依赖关系图 → 用户确认范围（排除不需要逆向的模块）

---

### 阶段 R2: 领域还原

**AI 执行指引**：

按拓扑顺序逐模块执行以下提取。

#### 逆向规则矩阵（代码 → 制品映射）

| 代码来源 | 提取方法 | → 制品字段 | 置信度 |
|----------|----------|------------|--------|
| `__manifest__.py` → `name` | 直接提取 | `project.target_modules[]` | 1.0 |
| `__manifest__.py` → `description` | 直接提取 | `glossary.terms[].definition` | 0.9 |
| `__manifest__.py` → `depends` | 直接提取 | 依赖图 | 1.0 |
| `models/*.py` → `class X(models.Model)` | AST 解析 | `domain-model.entities[]` | 1.0 |
| `models/*.py` → `_name = 'x.y'` | 直接提取 | `entity.technical_name` | 1.0 |
| `models/*.py` → `_description` | 直接提取 | `entity.description` | 0.9 |
| `models/*.py` → `fields.Char/Integer/...` | 类型映射 | `entity.attributes[]` | 1.0 |
| `models/*.py` → `fields.Many2one(...)` | 关系提取 | `entity.relationships[]` | 1.0 |
| `models/*.py` → `fields.computed` + `@api.depends` | 逻辑分析 | `entity.computed_fields[]` | 0.85 |
| `models/*.py` → `@api.constrains` | 约束提取 | `aggregate.invariants[]` | 0.9 |
| `models/*.py` → 方法（非 CRUD） | AI 意图推断 | `business_rules[]` | 0.6-0.8 |
| `views/*.xml` → `<record model="ir.ui.view">` | XML 解析 | `architecture.views[]` | 1.0 |
| `views/*.xml` → `<menuitem>` | XML 解析 | 菜单结构 → Slice 线索 | 1.0 |
| `security/ir.model.access.csv` | CSV 解析 | `architecture.security.access_rules[]` | 1.0 |
| `security/*.xml` → `<record model="ir.rule">` | XML 解析 | `architecture.security.record_rules[]` | 1.0 |
| `data/*.xml` → `<record model="ir.cron">` | XML 解析 | `architecture.scheduled_actions[]` | 0.9 |
| `wizards/*.py` | AI 流程推断 | `business_rules[]` + 流程线索 | 0.7 |
| `reports/*.xml` | QWeb 解析 | `architecture.reports[]` | 0.8 |
| `controllers/*.py` | 路由提取 | `architecture.api_endpoints[]` | 0.9 |
| `i18n/*.po` | PO 解析 | `glossary.terms[]` 补充 | 0.8 |

#### 置信度评估标准

| 级别 | 分数范围 | 含义 | 需要人补全？ |
|------|----------|------|-------------|
| **高** | ≥ 0.9 | 从声明式代码直接提取，几乎无误 | 否（但可选确认） |
| **中** | 0.7-0.89 | AI 推断逻辑大致准确，细节可能有偏差 | 建议确认 |
| **低** | < 0.7 | AI 猜测业务意图，可能不准 | **必须确认** |

#### Bounded Context 推断

1. 按 Odoo 模块边界作为初始 Bounded Context
2. 一对一映射：1 个 Odoo 模块 → 1 个 Bounded Context
3. 如多个模块紧密耦合（大量 `_inherit` 和跨模块引用）→ 合并为同一 Context

**交互节点**：
- 🗣️ 逐模块展示提取结果 + 置信度标注 → 用户确认或修正

---

### 阶段 R3: 制品对齐

**AI 执行指引**：

将 R2 提取的原始数据对齐到 AISEP 标准制品格式。

#### 生成制品清单

| 目标制品 | 来源 | 输出路径 |
|----------|------|----------|
| `project.yaml` | R1 模块列表 + R2 描述 | `artifacts/global/project.yaml` |
| `glossary.yaml` | R2 模型名/字段名/描述 | `glossary.yaml` |
| `domain-model.yaml` | R2 Entity/Aggregate/Context | `artifacts/global/domain-model.yaml` |
| `capability-map.yaml` | R2 领域推断（置信度较低） | `artifacts/global/capability-map.yaml` |
| `architecture.yaml` | R2 Views/Security/Reports | `artifacts/global/architecture.yaml` |

#### pipeline_state 设定

逆向项目的 pipeline 状态特殊处理：
```yaml
pipeline_state:
  current_stage: "s4-design"     # 逆向项目从 S4 开始正向推进
  stages:
    s0: { status: "completed", gate_passed: true, source: "onboard" }
    s1: { status: "completed", gate_passed: true, source: "onboard" }
    s2: { status: "completed", gate_passed: true, source: "onboard" }
    s3: { status: "completed", gate_passed: true, source: "onboard" }
    s4: { status: "pending", gate_passed: false }
    ...
```

> [!IMPORTANT]
> 逆向产出的制品标注 `source: "onboard"`，与正向产出区分。逆向制品的 Gate 通过是"逆向 Gate"（验证提取准确性），不同于正向 Gate（验证设计质量）。

---

### 阶段 R4: 生成补全清单

**AI 执行指引**：

1. 扫描所有生成制品中 `confidence < 0.7` 的字段
2. 按 **三类** 生成补全问题：

| 类型 | 内容 | AI 做的 | 人补的 |
|------|------|---------|--------|
| **确认类** | 术语定义、模型描述 | 给出推断值 | 确认或修正 |
| **意图类** | 业务目标、用户故事、为什么有此约束 | 无法推断 | 从零填写 |
| **演进类** | 改进方向、已知问题 | 无法推断 | 填写期望 |

3. 生成 `completion-checklist.yaml`：
```yaml
completion:
  total_items: 15
  confirmed: 0
  pending: 15
  items:
    - artifact: "glossary.yaml"
      field: "terms[0].definition"
      current: "生产任务记录"       # AI 推断
      confidence: 0.7
      type: "confirm"              # confirm | intent | evolve
      question: "production_order 的业务定义是'生产任务记录'，准确吗？"
      status: "pending"            # pending → confirmed → revised
```

**交互节点**：
- 🗣️ 按优先级（意图类 > 确认类 > 演进类）逐批展示补全问题
- 每批 5-8 个问题，避免一次性倾倒
- 用户回答后立即更新对应制品和 checklist

---

### 阶段 R5: Slice 推断

**AI 执行指引**：

1. **推断依据**（按优先级）：
   - 菜单结构（`<menuitem>` 的层级关系）→ 顶层菜单 ≈ Slice 候选
   - 模型聚合关系（Aggregate Root + 其依附 Entity/VO）→ 1 个聚合 ≈ 1 个 Slice
   - 业务流程（wizard 驱动的多步操作）→ 1 个流程 ≈ 1 个 Slice

2. 为每个推断的 Slice 创建目录：
```
artifacts/slices/
├── slice-01-{name}/
│   └── .onboard-meta.yaml    # 逆向来源标记
├── slice-02-{name}/
│ ...
```

3. 生成 `slice-plan.yaml`（复用 S2 的 Schema 格式）

**交互节点**：
- 🗣️ 展示 Slice 划分方案 → 用户确认或调整边界

---

### 阶段 R6: 项目注册 + 进入增量模式

**AI 执行指引**：

1. 在 `registry.yaml` 注册项目（同 idea promote 流程）
2. 设为活跃项目
3. 更新 `AISEP.md`
4. 输出完成信息：

```
✅ Onboard 完成

📦 项目: {project.name} ({project.id})
📊 逆向结果:
   模块数: N
   实体数: M
   置信度分布: 高 X% | 中 Y% | 低 Z%
   待补全项: K 个

📋 补全清单: projects/{id}/artifacts/onboard/completion-checklist.yaml
🔀 后续路径:
   • 先完成补全清单 → 提升制品准确性
   • 然后用 /pipeline 从 S4 开始正向推进
   • 新增需求走 changes/ 流程
```

---

## Gate 检查清单

### 逆向质量
- [ ] 所有模块是否已扫描？
- [ ] 依赖图是否完整（无悬挂引用）？
- [ ] 每个逆向制品是否标注了 `confidence`？
- [ ] `confidence < 0.7` 的条目是否全部出现在补全清单中？

### 制品对齐
- [ ] `project.yaml` 是否符合 Schema？
- [ ] `domain-model.yaml` 是否覆盖所有逆向模型？
- [ ] `glossary.yaml` 是否包含所有模型和关键字段的术语？
- [ ] `architecture.yaml` 是否包含视图和安全规则？

### 用户确认
- [ ] 用户已确认模块范围（R1）
- [ ] 用户已确认领域还原结果（R2）
- [ ] 用户已确认 Slice 划分（R5）
- [ ] 用户已完成优先级为"必须确认"的补全项

## Gate 通过后

1. **状态更新**：S0-S3 全部标记为 completed（`source: "onboard"`）
2. **推进**：`current_stage` → `s4-design`
3. **Gate 日志**：记录逆向 Gate 通过 + 置信度统计
4. **模式切换**：后续变更走 `changes/` 流程（`proposal.yaml` → S4-S6）

---

## 已知限制与缓解

| 限制 | 当前缓解 | 未来方向 |
|------|----------|----------|
| Wizard 逆向不完整 | 标注低置信度，入补全清单 | 补充 wizard 结构化解析规则 |
| Report QWeb 复杂模板 | 提取名称和数据源，跳过渲染逻辑 | 补充 QWeb 模板解析 |
| 跨模块 `_inherit` | 记录继承关系，不合并模型 | 设计继承链追踪算法 |
| 循环依赖 | 同组处理，警告用户 | 依赖图算法优化 |
| 业务意图（WHY） | 全部入补全清单 | 结合用户文档的 NLP 提取 |
