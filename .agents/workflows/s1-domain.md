---
description: "S1 业务领域分析 — 构建领域模型和能力图谱"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
    - "glossary.yaml"
  load:
    - "artifacts/global/project.yaml"
    - "artifacts/global/research.yaml"
    - ".aisep/templates/artifacts/s1-domain-model.tmpl.yaml"
  exclude:
    - "history/**"
    - "artifacts/slices/**"
    - "artifacts/changes/**"
---

# S1: 业务领域分析

## 前置条件

- `project.yaml` 存在且 S0 Gate 已通过（`pipeline_state.stages.s0.gate_passed == true`）
- 如有 `research.yaml`，一并加载（含技术选型结论、竞品调研）

## 输入

- `project.yaml`（S0 输出）— 项目范围、目标模块、约束条件
- `research.yaml`（可选）— S0 阶段的调研结论

## 加载方法论

- **必须**：DDD（`.agents/skills/methodologies/domain/ddd/SKILL.md`）
- **必须**：Business Blueprint（`.agents/skills/methodologies/domain/business-blueprint/SKILL.md`）
- **可选**：Event Storming（`.agents/skills/methodologies/domain/event-storming/SKILL.md`）

---

## 活动

### 步骤 1: 建立统一语言（Ubiquitous Language）

**AI 执行指引**：
1. 从 `project.yaml` 的 `target_modules` 和 `description` 提取初始业务术语
2. 逐个术语与用户确认：中文名、英文名、缩写、技术名、定义、别名
3. 写入 `glossary.yaml`，后续所有制品必须使用统一语言

**交互节点**：
- 🗣️ 每 5-8 个术语为一批，展示给用户确认（避免一次性倾倒）
- 用户可能提供 AI 不知道的行业专属术语，主动追问

**异常处理**：
- 用户对术语定义有分歧 → 记录分歧，标注 `status: disputed`，S2 前必须解决

### 步骤 2: 业务蓝图 — 端到端流程梳理

**AI 执行指引**：
1. 按 Business Blueprint Skill 的 8 维度，动态生成该行业的业务蓝图
2. 以"动词-名词"格式命名每个流程（如"创建-物料清单"、"审批-采购订单"）
3. **流程链**：标注流程间的触发关系（A 完成后触发 B）和数据流
4. 识别主数据实体、组织架构、报表需求、外部集成、合规要求

**交互节点**：
- 🗣️ 先展示发现的端到端流程列表 → 用户确认完整性 → 再展开细节
- 对于 AI 不确定的业务规则，**必须问用户**，不可假设

### 步骤 3: 识别限界上下文（Bounded Context）

**AI 执行指引**：
1. 根据业务流程划分，识别核心域、支撑域、通用域
2. 每个上下文有明确边界：哪些实体属于此上下文，哪些不属于
3. 命名上下文时使用业务语言（如"生产管理"而非"Production Module"）

**交互节点**：
- 🗣️ 展示上下文划分方案 + 理由 → 用户可调整边界

### 步骤 4: 构建聚合与实体（Aggregate & Entity Design）

**AI 执行指引**：
1. 在每个 Bounded Context 内识别 Aggregate Root
2. 每个 Aggregate 的不变量（Invariant）必须定义，如"BOM 的子件数量必须 > 0"
3. 区分 Entity（有 ID）和 Value Object（无 ID，值相等即相等）
4. 识别 Domain Event（如"生产工单-已完工"）和 Command（如"创建-物料清单"）

**交互节点**：
- 🗣️ 逐上下文展示聚合设计 → 用户确认业务规则是否准确

### 步骤 5: 绘制 Context Map

**AI 执行指引**：
1. 定义各 Context 间的关系模式：
   - ACL（防腐层）— 上下游解耦
   - Open Host Service — 提供公共 API
   - Shared Kernel — 共享核心（慎用）
   - Conformist — 下游适配上游
2. 输出为 `context_map` 结构，包含关系说明

### 步骤 6: 构建能力图谱（Capability Map）

**AI 执行指引**：
1. 按 TOGAF BA 方法，以"能力"而非"功能"组织
2. 能力树形式：L1（战略能力）→ L2（业务能力）→ L3（操作能力）
3. 每个能力节点标注：成熟度、优先级、对应的业务流程

### 步骤 6b: Gap 分析（条件性）

**触发条件**：`project.yaml` 中 `existing_system` 字段非空

**AI 执行指引**：
1. Baseline：列出现有系统覆盖的能力（如"Excel 管理库存"、"用友管理财务"）
2. Target：目标系统的能力覆盖
3. Gap：需要新建的能力（= 开发范围）
4. Overlap：现有系统已满足的能力（可对接或迁移）

**交互节点**：
- 🗣️ Gap 分析结果直接影响 S2 的开发范围，**必须用户确认**

---

## 输出

- `artifacts/global/domain-model.yaml`（必须）— 按 `s1-domain-model.tmpl.yaml` 格式
- `artifacts/global/capability-map.yaml`（必须）
- `artifacts/global/gap-analysis.yaml`（条件性：`existing_system` 非空时）
- 更新 `glossary.yaml` — 添加本阶段发现的所有术语

## Gate 检查清单

### 方法论质量（DDD）
- [ ] Ubiquitous Language 是否覆盖所有核心业务术语？
- [ ] Bounded Context 边界是否清晰且有理由？
- [ ] Context Map 关系模式是否定义？
- [ ] 每个 Aggregate Root 的不变量是否明确？
- [ ] 模块边界是否与 Context 边界对齐？

### 方法论质量（Business Blueprint）
- [ ] 是否覆盖了 ≥ 3 个端到端业务流程？
- [ ] 每个流程是否有明确的起点和终点？
- [ ] 流程链是否连续，没有断裂？
- [ ] 是否识别了所有主数据实体？
- [ ] 能力图谱是否生成？

### 完整性
- [ ] `glossary.yaml` 是否与 `domain-model.yaml` 的术语一致？
- [ ] （如有 Gap 分析）差距是否全部标注处理策略？

## Gate 通过后

1. **Compaction**：自动生成 `domain-model.summary.yaml`（保留 Context 数量、Aggregate 列表、关键决策）
2. **状态更新**：`pipeline_state.stages.s1.status = "completed"`, `gate_passed = true`
3. **推进**：`current_stage` → `s2-requirements`
4. **Gate 日志**：追加记录到 `history/gate-log.yaml`
