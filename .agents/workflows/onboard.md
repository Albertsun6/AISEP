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

# 逆向 Onboard Workflow (V2)

> 基于 2026-03-15 行业调研重新设计。
> 参考：`.aisep/docs/research/2026-03-15-ai-reverse-engineering/report.md`

## 设计原则

1. **确定性先行**：先用 AST/静态分析提取确定性信息，再用 LLM 推断语义
2. **渐进式揭示（Progressive Disclosure）**：L0 鸟瞰 → L1 模块 → L2 细节，每层独立可交互
3. **论述+选择**：AI 不说「不知道」，而是给出多种假设让人选择
4. **框架无关+插件特化**：通用流程 + 框架适配器
5. **知识图谱中间层**：逆向数据先构建为结构化 KG，再生成 AISEP 制品

## 触发

`/onboard --source <path>`

## 前置条件

- `<path>` 指向一个包含可分析源码的目录
- 目录下文件数 > 0

---

## 活动

### 阶段 R0: 架构鸟瞰（Architecture Scan）

> **目标**：快速获得全局理解，确定逆向范围。几分钟内完成。

**AI 执行指引**：

#### 步骤 1: 目录探测 + 框架识别

1. 扫描 `<path>` 下的文件树（深度 3 层）
2. 统计文件类型分布（按语言/扩展名）
3. **框架识别**（通过适配器检测，按优先级匹配）：

| 标志文件 | 识别为 | 加载 Skill |
|----------|--------|------------|
| `__manifest__.py` | Odoo 模块 | `frameworks/odoo17/SKILL.md` |
| `package.json` + `next.config.*` | Next.js 项目 | `frameworks/nextjs/` (如有) |
| `requirements.txt` + `manage.py` | Django 项目 | `frameworks/django/` (如有) |
| `Cargo.toml` | Rust 项目 | `frameworks/rust/` (如有) |
| `go.mod` | Go 项目 | `frameworks/go/` (如有) |
| 无法识别 | 通用项目 | 不加载框架 Skill |

4. 如框架 Skill 不存在 → 告知用户：「当前知识库不覆盖此框架，逆向将使用通用模式，质量可能较低」

#### 步骤 2: 架构概览生成

1. 生成**项目架构鸟瞰图**：
   - 目录结构概要
   - 主要模块/包 列表
   - 入口文件识别
   - 技术栈检测（语言版本、主要依赖库）
2. 产出 `architecture-overview.md`

#### 步骤 3: 规模评估

```yaml
scale_assessment:
  total_files: N
  total_lines: ~M
  modules_detected: K
  estimated_effort: "small | medium | large"
  recommended_passes: 1-3    # 根据规模推荐分几轮处理
```

**交互节点**：
- 🗣️ 展示架构鸟瞰图 + 规模评估 → 用户确认分析范围（排除不需要逆向的目录/模块）

---

### 阶段 R1: 扫描与发现（Dependency Discovery）

> **目标**：构建模块间依赖关系，确定处理顺序。

**AI 执行指引**：

#### 步骤 1: 知识图谱构建

> [!IMPORTANT]
> 这一步**不用 LLM 推断**，只做确定性提取。思路来自 ThoughtWorks GraphRAG：先构建结构化中间表示，后续再用 LLM 增强理解。

根据框架类型，使用对应适配器进行确定性提取：

**Odoo 适配器**（已实现）：
1. 扫描所有模块的 `__manifest__.py` → 提取 `depends` 列表
2. 扫描 `models/*.py` → 提取 class 定义、`_name`、`_inherit`、字段声明
3. 扫描 `views/*.xml` → 提取视图注册和菜单结构
4. 扫描 `security/ir.model.access.csv` → 提取权限规则

**通用适配器**（fallback）：
1. 扫描 import/require 语句 → 构建模块依赖
2. 扫描 class/function 定义 → 构建符号表
3. 扫描配置文件 → 提取项目元数据

产出：`knowledge-graph.yaml`

```yaml
# 知识图谱结构（借鉴 Palantir Ontology 模式）
knowledge_graph:
  object_types:         # 对应 Palantir 的 Object Types
    - type: "model"
      instances:
        - id: "production.order"
          properties:
            technical_name: "production.order"
            description: "生产订单"    # 从 _description 提取
            source_file: "models/production_order.py"
          confidence: 1.0               # 声明式提取 = 确定性
          
  link_types:           # 对应 Palantir 的 Relationships
    - type: "depends_on"
      source: "production.order"
      target: "product.product"
      cardinality: "many_to_one"
      evidence: "fields.Many2one('product.product')"
      confidence: 1.0
      
    - type: "inherits"
      source: "custom.sale.order"
      target: "sale.order"
      evidence: "_inherit = 'sale.order'"
      confidence: 1.0
```

#### 步骤 2: 依赖图构建

1. 从知识图谱提取模块间依赖
2. 构建 DAG（有向无环图）
3. **区分模块类型**：
   - **标准模块**：在官方 addons 列表中 → 不逆向，仅记录依赖
   - **自定义模块**：不在标准列表中 → 需要逆向
4. **拓扑排序**：按依赖关系确定处理顺序

**异常处理**：
- 循环依赖 → 标注警告，将循环中的模块作为一组同时处理
- 依赖的自定义模块不在 `<path>` 中 → 标注缺失，降低相关制品置信度

**交互节点**：
- 🗣️ 展示发现的模块列表 + 依赖关系图 → 用户确认范围

---

### 阶段 R2: 领域还原（Domain Reconstruction）

> **目标**：深度提取业务逻辑和领域知识。这是**唯一大量使用 LLM 推理的阶段**。

**AI 执行指引**：

按拓扑顺序逐模块执行。每个模块分**两轮**处理：

#### 第一轮：确定性提取（confidence ≥ 0.9）

使用 R1 构建的知识图谱，直接映射到制品字段。不需要 LLM 推断。

| 代码来源 | 提取方法 | → 制品字段 | 置信度 |
|----------|----------|------------|--------|
| `__manifest__.py` → `name` | 直接提取 | `project.target_modules[]` | 1.0 |
| `__manifest__.py` → `description` | 直接提取 | `glossary.terms[].definition` | 0.9 |
| `__manifest__.py` → `depends` | 直接提取 | 依赖图 | 1.0 |
| `models/*.py` → class 声明 | 知识图谱查询 | `domain-model.entities[]` | 1.0 |
| `models/*.py` → `_name` | 知识图谱查询 | `entity.technical_name` | 1.0 |
| `models/*.py` → 字段声明 | 知识图谱查询 | `entity.attributes[]` | 1.0 |
| `models/*.py` → 关系字段 | 知识图谱查询 | `entity.relationships[]` | 1.0 |
| `views/*.xml` → 视图定义 | XML 解析 | `architecture.views[]` | 1.0 |
| `views/*.xml` → 菜单项 | XML 解析 | 菜单结构 → Slice 线索 | 1.0 |
| `security/ir.model.access.csv` | CSV 解析 | `architecture.security[]` | 1.0 |
| `security/*.xml` → record rules | XML 解析 | `architecture.record_rules[]` | 1.0 |
| `data/*.xml` → cron jobs | XML 解析 | `architecture.scheduled_actions[]` | 0.9 |
| `controllers/*.py` → 路由 | 路由提取 | `architecture.api_endpoints[]` | 0.9 |
| `i18n/*.po` → 翻译 | PO 解析 | `glossary.terms[]` 补充 | 0.8 |

#### 第二轮：LLM 推断增强（confidence 0.5-0.89）

> [!NOTE]
> 这一轮使用 LLM 理解意图，但基于第一轮的知识图谱上下文（GraphRAG 模式），而非直接读全部代码。

| 代码来源 | 提取方法 | → 制品字段 | 置信度 |
|----------|----------|------------|--------|
| computed fields + `@api.depends` | LLM 逻辑分析 | `entity.computed_fields[]` | 0.85 |
| `@api.constrains` 方法 | LLM 约束分析 | `aggregate.invariants[]` | 0.9 |
| 非 CRUD 方法 | **AI 论述+假设** | `business_rules[]` | 0.6-0.8 |
| `wizards/*.py` | AI 流程推断 | `business_rules[]` + 流程线索 | 0.7 |
| `reports/*.xml` (QWeb) | QWeb 解析 | `architecture.reports[]` | 0.8 |

#### 论述+选择模式（用于 confidence < 0.8 的推断）

当 AI 对业务意图的推断不确定时，**不标注「未知」**，而是输出**多假设论述**：

```yaml
inference:
  target: "business_rules[2].rationale"
  code_context: "@api.constrains('qty') def _check_qty_positive..."
  
  hypotheses:
    - id: "H1"
      rationale: "防止负数库存，源于仓库管理的实物约束"
      confidence: 0.7
      evidence: "同模块存在 stock.move 关联"
    - id: "H2"
      rationale: "业务规则：不允许退货冲减，需走独立退货流程"
      confidence: 0.5
      evidence: "存在 return.order 模型"
    - id: "H3"
      rationale: "数据质量防护，防止操作员误输入"
      confidence: 0.4
      evidence: "无直接证据，通用推断"
  
  user_action: null    # 待用户选择: select_H1 | revise | write_new
```

#### Bounded Context 推断

1. 按模块边界作为初始 Bounded Context
2. 一对一映射：1 个模块 → 1 个 Bounded Context
3. 如多个模块紧密耦合（大量 `_inherit` 和跨模块引用）→ 合并为同一 Context

**交互节点**：
- 🗣️ 逐模块展示提取结果 + 置信度标注 + 论述假设 → 用户确认、选择或修正

---

### 阶段 R3: 制品对齐（Artifact Alignment）

> **目标**：将 R2 提取的数据对齐到 AISEP 标准制品格式。

**AI 执行指引**：

#### 生成制品清单

| 目标制品 | 来源 | 输出路径 |
|----------|------|----------|
| `project.yaml` | R0 架构概览 + R1 模块列表 | `artifacts/global/project.yaml` |
| `glossary.yaml` | R2 模型名/字段名/描述/翻译 | `glossary.yaml` |
| `domain-model.yaml` | R2 Entity/Aggregate/Context | `artifacts/global/domain-model.yaml` |
| `capability-map.yaml` | R2 领域推断 | `artifacts/global/capability-map.yaml` |
| `architecture.yaml` | R2 Views/Security/Reports/API | `artifacts/global/architecture.yaml` |
| `knowledge-graph.yaml` | R1 结构化知识图谱 | `artifacts/onboard/knowledge-graph.yaml` |

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
```

> [!IMPORTANT]
> 逆向产出的制品标注 `source: "onboard"`，与正向产出区分。逆向制品的 Gate 通过是"逆向 Gate"（验证提取准确性），不同于正向 Gate（验证设计质量）。

---

### 阶段 R4: 生成补全清单（Completion Checklist）

> **目标**：将所有不确定项系统化为可操作的问题清单。

**AI 执行指引**：

1. 扫描所有生成制品中 `confidence < 0.7` 的字段
2. 收集 R2 中所有未被用户确认的「论述+选择」项
3. 按 **三类** 生成补全问题：

| 类型 | 内容 | AI 做的 | 人补的 |
|------|------|---------|--------|
| **确认类** | 术语定义、模型描述 | 给出推断值 + 置信度 | 确认或修正 |
| **意图类** | 业务目标、用户故事、约束原因 | 给出假设（论述+选择） | 选择、修正或从零填写 |
| **演进类** | 改进方向、已知问题 | 无法推断 | 填写期望 |

4. 生成 `completion-checklist.yaml`：

```yaml
completion:
  total_items: 15
  confirmed: 0
  pending: 15
  items:
    - artifact: "glossary.yaml"
      field: "terms[0].definition"
      current: "生产任务记录"
      confidence: 0.7
      type: "confirm"
      question: "production_order 的业务定义是'生产任务记录'，准确吗？"
      status: "pending"
      
    - artifact: "domain-model.yaml"
      field: "business_rules[2].rationale"
      current: null
      confidence: 0
      type: "intent"
      hypotheses:     # 论述+选择模式
        - "H1: 防止负数库存（0.7）"
        - "H2: 独立退货流程（0.5）"
        - "H3: 数据质量防护（0.4）"
      question: "约束 _check_qty_positive 的业务原因是什么？AI 给出了 3 种假设，请选择或补充。"
      status: "pending"
```

**交互节点**：
- 🗣️ 按优先级（意图类 > 确认类 > 演进类）逐批展示补全问题
- 每批 5-8 个问题，避免一次性倾倒
- 用户回答后立即更新对应制品和 checklist

---

### 阶段 R5: Slice 推断（Slice Inference）

> **目标**：将逆向的功能划分为可管理的 Slice。

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
4. **沉淀逆向过程记录**：
   - 推理链记录 → `artifacts/onboard/reasoning-trace.yaml`
   - 决策日志 → `artifacts/onboard/decision-log.yaml`
   - 交互记录摘要 → `artifacts/onboard/qa-summary.md`
5. 输出完成信息：

```
✅ Onboard 完成

📦 项目: {project.name} ({project.id})
📊 逆向结果:
   模块数: N
   实体数: M
   知识图谱节点: P 个 Object Types, Q 个 Link Types
   置信度分布: 高 X% | 中 Y% | 低 Z%
   待补全项: K 个

📋 补全清单: projects/{id}/artifacts/onboard/completion-checklist.yaml
🔀 后续路径:
   • 先完成补全清单 → 提升制品准确性
   • 然后用 /pipeline 从 S4 开始正向推进
   • 新增需求走 changes/ 流程
```

---

## 框架适配器接口

> 通用流程 + 框架特化插件的设计，使 onboard 不锁定于 Odoo。

```yaml
framework_adapter:
  interface:
    detect: "判断源码是否属于该框架 → bool"
    extract_metadata: "提取项目元数据 → metadata{}"
    extract_models: "提取数据模型 → model[]"
    extract_views: "提取视图/UI层 → view[]"
    extract_security: "提取安全规则 → rule[]"
    extract_routes: "提取路由/API → endpoint[]"
    extract_business_logic: "提取业务逻辑 → logic[]（需 LLM）"

  adapters:
    odoo17:
      detect: "__manifest__.py 存在"
      skill: "frameworks/odoo17/SKILL.md"
      status: "implemented"
    django:
      detect: "manage.py + settings.py"
      skill: "frameworks/django/ (待建)"
      status: "planned"
    nextjs:
      detect: "next.config.* + pages/ or app/"
      skill: "frameworks/nextjs/ (待建)"
      status: "planned"
    generic:
      detect: "fallback — 其他所有情况"
      skill: null
      status: "implemented"
```

---

## 知识图谱中间层

> 借鉴 ThoughtWorks GraphRAG + Palantir Foundry Ontology 的设计。

### 为什么需要知识图谱

| 对比 | 直接 LLM 读代码 | 先 KG 再 LLM |
|------|-----------------|--------------|
| **精度** | LLM 可能遗漏或曲解 | KG 确定性提取不出错 |
| **可追溯** | 黑盒推断 | 每条数据有 source_file + line |
| **上下文管理** | 需要一次加载大量代码 | KG 按需查询，节省 context |
| **跨模块理解** | 受限于 context window | KG 天然支持全局关系查询 |

### 本体论模型（Ontology Schema）

参考 Palantir Foundry 的 Object Types + Properties + Link Types 范式：

```yaml
ontology_schema:
  object_types:
    - type: "module"
      properties: [name, technical_name, version, description, source_path]
    - type: "model"
      properties: [name, technical_name, description, source_file, is_abstract]
    - type: "field"
      properties: [name, field_type, required, computed, help_text]
    - type: "view"
      properties: [name, view_type, model, arch_file]
    - type: "menu_item"
      properties: [name, parent, action, sequence]
    - type: "security_rule"
      properties: [model, group, perm_read, perm_write, perm_create, perm_unlink]
    - type: "method"
      properties: [name, decorators, docstring, complexity, source_file, line_range]

  link_types:
    - type: "depends_on"        # module → module
    - type: "defines"           # module → model
    - type: "has_field"         # model → field
    - type: "inherits_from"     # model → model (_inherit)
    - type: "references"        # field → model (Many2one/Many2many target)
    - type: "has_view"          # model → view
    - type: "triggers"          # method → method (调用关系)
    - type: "constrains"        # method → field (@api.constrains)
    - type: "computes"          # method → field (@api.depends)
```

---

## 置信度评估标准

| 级别 | 分数范围 | 含义 | 来源 | 需要人补全？ |
|------|----------|------|------|-------------|
| **高** | ≥ 0.9 | 声明式代码直接提取 | 知识图谱 R1 轮 | 否 |
| **中** | 0.7-0.89 | AI 推断大致准确 | LLM R2 轮 | 建议确认 |
| **低** | 0.5-0.69 | AI 有假设但不确定 | 论述+选择 | **必须确认** |
| **未知** | < 0.5 | 代码无线索 | — | 需人从零提供 |

---

## Gate 检查清单

### 逆向质量
- [ ] 所有模块是否已扫描？
- [ ] 知识图谱是否完整（无悬挂引用）？
- [ ] 依赖图是否无环或环已处理？
- [ ] 每个逆向制品是否标注了 `confidence`？
- [ ] `confidence < 0.7` 的条目是否全部出现在补全清单中？

### 制品对齐
- [ ] `project.yaml` 是否符合 Schema？
- [ ] `domain-model.yaml` 是否覆盖所有逆向模型？
- [ ] `glossary.yaml` 是否包含所有模型和关键字段的术语？
- [ ] `architecture.yaml` 是否包含视图和安全规则？
- [ ] `knowledge-graph.yaml` 是否已生成并结构完整？

### 用户确认
- [ ] 用户已确认分析范围（R0）
- [ ] 用户已确认模块范围（R1）
- [ ] 用户已确认领域还原结果（R2）
- [ ] 用户已确认 Slice 划分（R5）
- [ ] 用户已完成优先级为"必须确认"的补全项

## Gate 通过后

1. **状态更新**：S0-S3 全部标记为 completed（`source: "onboard"`）
2. **推进**：`current_stage` → `s4-design`
3. **Gate 日志**：记录逆向 Gate 通过 + 置信度统计
4. **过程沉淀**：reasoning-trace + decision-log + qa-summary
5. **模式切换**：后续变更走 `changes/` 流程（`proposal.yaml` → S4-S6）

---

## 运行时辅助分析（可选扩展）

> 当有运行环境可用时，可选启用以下增强能力：

| 能力 | 实现方式 | 价值 |
|------|----------|------|
| **截图分析** | 浏览器截图 + 视觉 LLM | 验证 view 逆向的准确性 |
| **API 追踪** | HTTP 请求/响应记录 | 补充 controller 层理解 |
| **数据采样** | 查询 demo 数据库 | 理解数据结构和实际使用 |

启用方式：`/onboard --source <path> --runtime <url>`

> [!NOTE]
> 这是可选增强，不是必须步骤。核心逆向流程以静态分析为主。

---

## 已知限制与缓解

| 限制 | 当前缓解 | 未来方向 |
|------|----------|----------|
| Wizard 逆向不完整 | 标注低置信度 + 论述假设 | 补充 wizard 结构化解析规则 |
| Report QWeb 复杂模板 | 提取名称和数据源 | 补充 QWeb 模板解析 |
| 跨模块 `_inherit` | 知识图谱记录继承链 | 继承链追踪算法 |
| 循环依赖 | 同组处理，警告用户 | 依赖图算法优化 |
| 业务意图（WHY） | 论述+选择模式 | 结合用户文档的 NLP 提取 |
| 非 Odoo 框架 | 通用适配器（精度较低） | 逐步添加框架适配器 |

---

## V1 → V2 变更摘要

| 维度 | V1 | V2 | 变更原因 |
|------|----|----|----------|
| 阶段数 | R1-R6 | R0-R6 | 新增 R0 架构鸟瞰 |
| 分析模式 | 一次性全量 | Multi-Pass 渐进 | 管理 context 预算 |
| LLM 使用 | 全流程 | 仅 R2 第二轮 | 确定性先行原则 |
| 业务意图 | 标「未知」等人填 | 论述+选择 | AI+人共建 |
| 知识表示 | 无中间层 | 知识图谱(Ontology) | GraphRAG 最佳实践 |
| 框架支持 | Odoo 硬编码 | 框架适配器接口 | 可扩展性 |
| 过程记录 | 无 | reasoning-trace + decision-log | runtime 沉淀 |
