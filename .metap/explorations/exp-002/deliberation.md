# 辩论记录：AISEP 知识体系收敛策略

**探索 ID**: exp-002 | **日期**: 2026-03-15 | **角色**: 🟢🔴🟡🔵

**议题**：exp-002 发现三大问题（知识双轨重叠 / 本体论分裂 / evolution 分散），当前的"桥接而非合并"策略是否最优？

---

## Round 1: 陈述与质疑

### 🟢 倡导者：桥接策略是当前最优解

**核心价值主张**：exp-002 提出的"桥接而非合并"（prop-003/prop-005）是正确的渐进式收敛策略。理由如下：

1. **演进安全性**：MetaP 的 schema 仍在 v0.2.0，连续两次探索（exp-001, exp-002）都触发了 schema 变更（增加了 concepts、修改了倒排索引）。过早合并会固化不成熟的设计。来源：exp-002 洞见 3 "分离仍然优于统一（当前阶段）"。

2. **已验证的双向引用**：`metap_concept_ref` 和 `aisep_note_ref` 字段已落地，`/tidy` 一致性检查已注册。这意味着信息可以跨系统流通而不需要物理合并。来源：ontology-conventions.yaml § metap_convergence。

3. **有明确退出标准**：收敛路线图定义了 `bridge → migrate → unify` 三阶段，且每个阶段有具体的迁移标准（"MetaP schema 在 3 次 explore 中不改 → 进入 migrate"）。这不是无限拖延，而是有数据驱动的转换点。

4. **成本可控**：当前维护两套系统的增量成本仅是 `/tidy` 时的双向一致性检查（~30 秒自动化），而强合并的一次性成本极高（需要重写所有 workflow 引用）。

---

### 🔴 质疑者：桥接策略的三个隐患

**质疑 1 ⚠️ 可管理的风险：桥接不等于收敛**

桥接只建立了"引用"，但没有解决根本问题——两套独立的成熟度模型仍在并行运行。`note → decision → skill_draft → skill` 和 `seed → growing → validated → established` 追踪的是同一件事（知识成长），但用了不同的刻度。

**具体场景**：一个在 `.aisep/knowledge` 中达到 `skill` 级别（如 learn-006 TransientModel 向导模式）的条目，在 `.metap/ontology/concepts` 中没有对应实体。这意味着 MetaP 的语义记忆对 AISEP 最有价值的知识完全不感知。

---

**质疑 2 ⚠️ 可管理的风险：退出标准过于乐观**

"MetaP schema 在 3 次 explore 中不改"——但每次 explore *都在发现新概念*（exp-001 注册了 5 个 concepts）。schema 不改 ≠ schema 成熟。可能只是没有触及 schema 的 corner case。

---

**质疑 3 ❌ 致命缺陷风险：evolution 分散没有收敛路径**

`ontology-conventions.yaml` 的收敛路线图只涵盖了知识体系（cognitive_note ↔ Concept），但完全没有提到 evolution 的收敛。`.aisep/evolution/interaction-rules.yaml` 和 `.metap/evolution/observations.yaml` 至今没有任何桥接机制。

---

> **📋 质量守护 #1**: ✅ 双方坚守立场约束。倡导者引用了具体来源（exp-002 洞见 3、ontology-conventions.yaml）。质疑者区分了"可管理的风险"和"致命缺陷"。质疑 3 提出了计划中未覆盖的盲区。

---

## Round 2: 回应、约束与视野

### 🟢 倡导者回应

**回应质疑 1**：成熟度模型的差异是有意设计——AISEP 的 4 级追踪的是*工程复用价值*（note→skill），MetaP 的 4 级追踪的是*认知确定性*（seed→established）。两者不是同一维度。但承认可以通过 `maturity_mapping` 做自动对齐（已在 ontology-conventions.yaml 中定义但未激活）。

**让步**：应尽快激活 `maturity_mapping` 的自动同步——当 AISEP 条目升到 `skill` 时，自动创建/提升对应的 MetaP Concept 到 `established`。

**回应质疑 2**：接受批评。将退出标准从"schema 不改"修改为"schema 的 Object Type 定义不改 + 所有新 concepts 可被现有 schema 描述"。

**回应质疑 3**：这是一个真正的盲区。当前确实没有 evolution 的收敛路径。建议把 evolution 收敛作为 Phase 4 的工作项。

---

### 🟡 务实者评估

**资源分析**：
- AISEP 当前 ~150 文件，知识条目 11（AISEP）+ 5（MetaP）= 16 条
- 即使完全不做任何收敛，在 16 条的规模下双轨管理的成本极低
- 按当前积累速度（~5 条 / 项目），要到 100+ 条时双轨才会成为真正的负担

**ROI 分析**：

| 选项 | 成本 | 收益 | ROI |
|------|------|------|-----|
| A: 维持桥接 + 激活 maturity_mapping | ~15m · 2 files · low | 双轨痛点降低 80% | ⭐⭐⭐ |
| B: 立即全量合并 | ~4h · 20+ files · high | 消除双轨 100% | ⭐ |
| C: 只合并 evolution | ~30m · 5 files · mid | 解决质疑 3 | ⭐⭐ |

**MVP 建议**：选项 A（桥接+激活 mapping）为 MVP，选项 C（evolution 合并）可作为 Phase 4 首个任务。选项 B 在现阶段 ROI 最差——投入大但条目太少看不出效果。

**具体工作量估算**：
- 选项 A：修改 `/tidy` 增加 maturity 同步检查 ~10m + ontology-conventions 激活 mapping ~5m = **15 分钟**
- 选项 C：迁移 interaction-rules.yaml ~10m + 更新 5 个 workflow 引用 ~15m + 验证 ~5m = **30 分钟**

---

### 🔵 远见者补充

**长期影响——认知统一性定律**

*为什么在这里引入*：双轨问题本质上是一个*认知架构*问题，软件工程和认知科学在这里有深刻的同构性。

在认知科学中，大脑的知识不是存成两套独立的数据库，而是通过**多重编码**（Multiple Encoding）实现——同一个记忆在海马体（事件记忆）和新皮层（语义记忆）中各有一份表征，但通过*巩固过程*（consolidation）自动同步。这恰好对应了 MetaP 的三级记忆架构（工作记忆 → 事件记忆 → 语义记忆）。

**二阶效应**：如果 AISEP 成功实现认知统一性，它可能成为 AI 辅助知识管理的一个*参考实现*——证明 AI Agent 可以维护一个自洽的、跨项目的概念体系。这比任何具体的 workflow 都更有长期价值。

**跨领域启示**：Palantir 的 Ontology 之所以成功，不是因为它一开始就统一了所有数据源，而是因为它提供了一个**渐进式吸收**机制（先 bridge → 再 model → 再 unify）。AISEP 的路径 A 与此高度同构。

---

> **📋 质量守护 #2**: ✅ 务实者给出了具体工作量估算（15m/30m/4h）和 ROI 矩阵。远见者锚定在认知统一性议题上，通过认知科学类比增强了论点，没有脱离议题。

---

## Round 3: 立场修正与共识

### 🟢 倡导者最终立场：**修正坚持**

坚持桥接策略作为基础框架，但接受两项修正：
1. 激活 `maturity_mapping` 自动同步（解决质疑 1）
2. 将退出标准从 "schema 不改" 修正为 "Object Types 不增 + 新概念可被现有 schema 完整描述"（解决质疑 2）

### 🔴 质疑者最终评估

- ✅ 已解决：质疑 1（成熟度对齐）——通过激活 maturity_mapping
- ✅ 已解决：质疑 2（退出标准）——通过明确化标准
- ⚠️ 仍存在：质疑 3（evolution 分散）——倡导者承认盲区，但推迟到 Phase 4
- 无致命风险：在当前 16 条知识的规模下，双轨系统不会造成实际问题

### 🟡 务实者推荐路径

**推荐 MVP（选项 A）**：~15m · 2 files · low
- 激活 maturity_mapping
- `/tidy` 增加 "成熟度同步检查" 步骤

**Phase 4 规划（选项 C）**：~30m · 5 files · mid
- evolution 目录统一迁移到 `.metap/evolution/`

### 🔵 远见者长期判断

当前的桥接策略是**正确的渐进式架构决策**。二阶效应预测：当 AISEP 积累到第 3 个项目时（每个项目贡献 ~5 条 cognitive_note），将自然触发 `migrate` 阶段。这是系统自组织的体现，不需要人为强推。

---

## 共识结论

> **共识（4/4 同意）**：当前的"桥接而非合并"策略方向正确，但需要两项增强。

| # | 共识结论 | Confidence | 支撑 |
|---|---------|-----------|------|
| 1 | 桥接策略是当前最优解——规模太小，强合并 ROI 极低 | 0.90 | 🟢🔴🟡🔵 一致 |
| 2 | 必须激活 `maturity_mapping` 自动同步 | 0.85 | 🟢让步 + 🔴验证 + 🟡 ROI 分析 |
| 3 | 退出标准需要明确化（Object Types 不增 + 新概念可被现有 schema 描述） | 0.80 | 🟢让步 + 🔴建议 |

> **📋 质量守护 #3: 虚假共识检测** — 结论 1 为全票一致，🔴 强制 devil's advocate：

🔴 **Devil's Advocate**：如果 AISEP 突然需要 onboard 一个大型遗留系统（如 1000+ 文件的 monolith），双轨的知识管理可能在短时间内产生大量 cognitive_notes，而 MetaP 的 Concept 来不及同步。这个场景下桥接策略会快速恶化为"两个不同步的知识孤岛"。

**应对**：将"单次 onboard 产生的 cognitive_note > 20 条"作为提前触发 `migrate` 阶段的紧急条件。

---

## 分歧点

| # | 分歧 | 🟢 | 🔴 | 🟡 | 🔵 |
|---|------|---|---|---|---|
| 1 | evolution 何时合并 | Phase 4 | 尽快（Phase 3.5） | Phase 4 首个任务 | 自然演进，不强推 |

---

## 行动建议（辩论后修正版）

### 修正建议 1：激活 maturity_mapping（含在本轮 Phase 3 中）

**来源**：质疑 1 解决方案 + 务实者 MVP 推荐
**工作量**：~15m · 2 files · low
**优先级**：P1
**具体执行**：
1. 在 `/tidy` workflow 增加 "成熟度同步检查" 步骤
2. 当 AISEP cognitive_note 升级为 skill 时，自动检查对应的 MetaP Concept 是否存在

### 修正建议 2：明确化收敛退出标准

**来源**：质疑 2 解决方案
**工作量**：~5m · 1 file · low
**优先级**：P1
**具体执行**：更新 `ontology-conventions.yaml` 中 `convergence_roadmap.phases.bridge.criterion`

### 修正建议 3：evolution 合并列为 Phase 4 首个任务

**来源**：质疑 3 + 务实者选项 C
**工作量**：~30m · 5 files · mid（Phase 4 执行）
**优先级**：P2（Phase 4）

### 修正建议 4：增加"紧急迁移"触发条件

**来源**：质量守护 #3 devil's advocate
**工作量**：~5m · 1 file · low
**优先级**：P1
**具体执行**：在收敛路线图的 bridge 阶段增加 "单次 onboard 产生 cognitive_note > 20 条 → 紧急触发 migrate" 条件

---

## 元认知洞察

1. **多重编码同构性**：AISEP 的双轨知识系统与大脑的多重编码机制高度同构（事件记忆 / 语义记忆 各有表征，通过巩固过程同步）。这不是 bug，而是认知架构的自然延伸。→ 可注册为新 Concept。

2. **渐进式架构决策模式**：本次辩论验证了"bridge → migrate → unify"是一种可复用的架构收敛模式——适用于任何两个功能重叠但成熟度不同的子系统。→ 可提升 concept-002（三层 Ontology 架构）的 maturity。
