# exp-002: AISEP 目录结构合理性探索报告

> 方向：现在目录结构的合理性
> 置信度：0.85 | 日期：2026-03-15

---

## 一、现状全景

当前目录结构为**四层分离**架构：

```
AISEP250311/
├── .agents/         # 🤖 Agent 能力层（17 Skills + 16 Workflows）
├── .aisep/          # ⚙️ 工程过程层（config, schemas, templates, knowledge, evolution, docs）
├── .metap/          # 🧠 元认知层（ontology, engines, memory, explorations, evolution/state）
├── projects/        # 📦 项目产出层（proj-001 归档, proj-002 活跃）
├── AISEP.md         # AI 入口
├── MetaP.md         # MetaP 入口
├── constitution.md  # 共享铁律
├── note.md          # 临时想法
└── README.md        # 外部说明
```

**数据统计**：

| 层 | 文件数 | 体积 | 首次创建 |
|----|--------|------|----------|
| `.agents/` | ~35 | ~60KB | Day 1 |
| `.aisep/` | ~50 | ~100KB | Day 1 |
| `.metap/` | ~20 | ~30KB | 后期新增 |
| `projects/` | ~40 | ~80KB | Day 1 |
| 根目录文件 | 5 | ~15KB | Day 1 |

---

## 二、Scout 发现

### Scout-A: 内部重叠性分析

**🔴 问题 1：知识体系双轨重叠**

| 分类 | `.aisep/knowledge/` | `.metap/ontology/concepts/` |
|------|---------------------|---------------------------|
| 实体名 | `cognitive_note` (learn-001~011) | `Concept` (concept-001~005) |
| 成熟度模型 | note → decision → skill_draft → skill | seed → growing → validated → established |
| 索引方式 | `index.yaml` + 4维倒排索引 | `index.yaml` + relates_to/derived_from |
| 触发点 | `/tidy` Step 10 | `/explore` Step 5 Registrar |

**本质**：两套系统都在管理「学到的知识」，但用了不同的 schema、不同的 ID 体系、不同的成熟度模型。

```
.aisep/knowledge/entries/learn-007.yaml  ←  "Odoo 版本间 API 破坏性变更"
                  ≈ 等价于 ≈
.metap/ontology/concepts/concept-???     ←  如果用 /explore 发现同一知识
```

**风险**：同一知识可能存在两份、用不同格式、不同成熟度追踪。维护成本随时间倍增。

---

**🟡 问题 2：进化机制分散**

| 位置 | 内容 |
|------|------|
| `.aisep/evolution/interaction-rules.yaml` | 交互进化规则（evo-001~006） |
| `.metap/evolution/observations.yaml` | 进化观察 |
| `.metap/evolution/history.yaml` | 进化历史（不可变审计） |
| `.metap/engines/evolution.yaml` | 进化引擎配置 |

进化相关文件分布在两个顶层目录中。`.aisep/evolution/` 管规则，`.metap/evolution/` 管观察和历史。逻辑上是同一个关注点，但物理上被拆到了两处。

---

**🟢 亮点：Agent 层清晰隔离**

`.agents/` 的职责边界非常清晰：只存 Skills（知道什么）和 Workflows（怎么做）。没有和 `.aisep/` 或 `.metap/` 交叉。这符合行业最佳实践中的**关注点分离**。

---

### Scout-B: 层次感和职责清晰度评估

**当前四层的逻辑定位**：

```
.agents   = HOW（方法论 + 流程定义）    ← 能力
.aisep    = WHAT（工程制品 + 过程管理）  ← 执行
.metap    = WHY（知识 + 探索 + 自治）   ← 思考
projects  = OUTPUT（项目具体产出）      ← 产出
```

**评估**：

| 维度 | 评分 | 说明 |
|------|------|------|
| 职责清晰度 | 7/10 | `.agents` 和 `projects` 很清晰；`.aisep` 和 `.metap` 的边界在知识管理和进化方面模糊 |
| 可发现性 | 6/10 | 新入门者需要理解三个入口文件（AISEP.md / MetaP.md / constitution.md）的关系 |
| 上下文效率 | 8/10 | L0/L1/L2 分层加载协议设计良好；context_fence 有效 |
| 演进友好度 | 9/10 | 新增 Object Type / Workflow / Skill 不需要改结构 |

**🔴 问题 3：本体论分裂**

系统中现在有**两套本体论**在并行运行：

| | `.aisep/conventions/ontology-conventions.yaml` | `.metap/ontology/schema.yaml` |
|-|-----------------------------------------------|-------------------------------|
| 设计时间 | 研究报告 Phase 0 落地 | MetaP Phase 2 设计 |
| 灵感 | Palantir 三要素 | Palantir + ODIS |
| Object Types | 18 种（7层） | 5 种（Concept/Source/Exploration/ActionProposal/Project） |
| Link Types | 12 种 | 5 种（relates_to/derived_from/contradicts/supersedes/applied_in） |
| 标注方式 | `_type` + `_links` 字段 | 独立 yaml 文件 |
| 范围 | 全系统（项目+知识+过程+进化+Agent） | 仅 MetaP 知识层 |

关键矛盾：`.aisep/` 的本体论是**全系统级**的（18 种 Object Types 覆盖所有层），`.metap/` 的本体论是**MetaP 专用**的（5 种，只管探索和概念）。两者定义冲突——如 `Concept` vs `cognitive_note` 管的是同一类东西。

---

### Scout-C: 行业最佳实践对比

| 行业实践 | AISEP 当前 | 评估 |
|----------|-----------|------|
| **AGENTS.md 模式**（专用 AI 指令文件） | ✅ `AISEP.md` + `MetaP.md` | 超越行业——有两个分层入口 |
| **可预测常规化结构** | ✅ `.agents/skills/`、`.aisep/schemas/` 命名清晰 | 良好 |
| **按业务特性组织**（vs 按技术分层） | ⚠️ 混合——顶层按技术分层，projects 内按业务 | 合理折中 |
| **共享组件集中化** | ✅ `.agents/skills/` 和 `.aisep/knowledge/` | 良好 |
| **关注点分离** | ⚠️ 知识层和进化层有重叠 | 需要统一 |
| **AI 友好文档结构** | ✅ 分层加载协议 + context_fence | 超越行业 |

---

## 三、核心洞见

### 洞见 1：「知识」是唯一需要统一的关注点

`.agents`（能力）、`projects`（产出）的边界完美。问题只集中在**知识管理**这一个关注点上——它同时出现在 `.aisep/knowledge/` 和 `.metap/ontology/concepts/` 中。

### 洞见 2：两套本体论是历史演进的副产品，不是设计意图

`.aisep/conventions/ontology-conventions.yaml` 是从 Palantir 研究「自上而下」设计的全系统本体论。`.metap/ontology/schema.yaml` 是 MetaP 迭代中「自下而上」生长出来的。两者从不同方向走到了相同的领域。

### 洞见 3：分离仍然优于统一（当前阶段）

尽管有重叠，现在**强行合并**风险太高——`.metap/` 是新系统，schema 还在演进。过早统一可能固化不成熟的设计。更好的策略是**桥接**而非**合并**。

---

## 四、行动建议

### prop-003: 知识桥接层（Bridge, Don't Merge）

**建议**：在两套知识体系之间建立**双向映射协议**，而非合并。

- 在 `.aisep/knowledge/index.yaml` 中增加 `metap_concept_ref` 字段
- 在 `.metap/ontology/concepts/*.yaml` 中增加 `aisep_note_ref` 字段
- `/tidy` 时检查双向一致性

**工作量**：~20m · 3 files · low
**优先级**：P1
**风险**：低——只加字段，不改结构

---

### prop-004: 统一进化目录

**建议**：将 `.aisep/evolution/` 的内容迁移到 `.metap/evolution/` 下，`.aisep/evolution/` 改为软链接或重定向。

```
.metap/evolution/
├── interaction-rules.yaml   # 从 .aisep/evolution/ 迁移
├── observations.yaml        # 已有
├── history.yaml             # 已有
```

**工作量**：~15m · 5 files · mid
**优先级**：P2
**风险**：中——需要更新所有引用 `.aisep/evolution/` 的 workflow

---

### prop-005: 本体论收敛路线图

**建议**：不立即合并两套本体论，而是设定收敛路线：

1. **短期**：`.metap/ontology/schema.yaml` 作为 MetaP 内部 schema（不变）
2. **短期**：`.aisep/conventions/ontology-conventions.yaml` 增加 MetaP 映射表（哪些 AISEP Object Type ↔ MetaP Object Type）
3. **中期**：当 MetaP schema 稳定后（v1.0），合并为单一本体论
4. **合并标准**：MetaP 连续 3 个 exploration 不需要改 schema → 视为稳定

**工作量**：短期 ~15m · 1 file · low | 中期 TBD
**优先级**：P1（短期映射表）/ P3（最终合并）
**风险**：低——渐进式

---

### prop-006: 根目录精简

**建议**：根目录有 5 个 markdown 文件，可以考虑：

- `note.md` → `.aisep/note.md`（个人想法不属于系统入口）
- `README.md` 保留（GitHub 约定）
- `AISEP.md` / `MetaP.md` / `constitution.md` 保留（系统入口）

**工作量**：~5m · 2 files · low
**优先级**：P3
**风险**：极低

---

## 五、结论

> **当前目录结构在 80% 的维度上是合理的**。四层分离（能力/过程/思考/产出）的逻辑清晰，上下文控制机制领先行业。
>
> 唯一需要关注的是**知识管理的双轨问题**——不是因为设计错误，而是因为系统在演进中自然长出了两套方案。推荐的策略是**桥接而非合并**，等 MetaP 稳定后再考虑统一。
