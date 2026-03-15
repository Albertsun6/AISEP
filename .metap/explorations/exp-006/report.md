# Deep Dive 报告：项目执行中的进化植入点

**exp-006 | deepdive | 2026-03-15**

---

## Phase 1: 探索发现 — AISEP 当前进化覆盖 vs 行业最佳实践

### 当前 AISEP 进化触发点（现状）

```
S0  S1  S2  S3  S4  S5  S6  S7  S8  /tidy
 ·   ·   ·   ·   ·   ·   ·   ·   ★   ★
                                  │   │
                         S8 复盘──┘   │
                         /tidy 收尾───┘
```

**问题**：进化触发几乎全部集中在**项目结尾**（S8 复盘 + /tidy）。项目执行中段（S1-S7）没有任何进化植入。

### 行业最佳实践的反射点密度

| 方法论 | 反射点数量 | 反射时机 |
|--------|-----------|---------|
| Agile/Scrum | **每个 Sprint** | Sprint Retro + Sprint Review |
| Kaizen | **持续** | 日常站会 + 改善提案 |
| DevOps | **每次部署** | CI/CD feedback + monitoring |
| Design Thinking | **每个菱形** | 发散后收敛前（Double Diamond） |
| Lean Startup | **每个假设** | Build-Measure-Learn 循环 |

**对比结论**：AISEP 的进化密度远低于行业标准。一个项目跑完 S0-S7 可能需要数天，期间没有任何系统反思机会。

---

## Phase 2: 自动触发辩论

```yaml
trigger_hit:
  - "涉及修改 S0-S8 全部 workflow（risk > medium）"
  - "proposals 可能从 6+ 个方案中选择（需优先级排序）"
```

---

## Phase 3: 辩论 — 该在哪里植入、如何植入？

### Round 1: 各角色提案

**🏗️ 架构师**：
> 按照 AISEP 的 L1-L4 分层，进化植入点应该对应不同层级：
> - **L1（全自动记录）**：每个 Gate 通过时已有 → ✅ 足够
> - **L2（半自动沉淀）**：缺！应在 Gate 修正（revised/rejected）时自动触发
> - **L3（规则优化）**：缺！应在项目中期（S5 后第一个 Slice 完成时）触发 mini-review
> - **L4（能力生成）**：缺！遇到未知框架时在 S3 自动触发

**🎯 产品经理**：
> 关键是**不增加用户负担**。用户做拍卖项目不是为了进化 AISEP——进化应该是**透明无感**的。分三级：
> 1. **无感植入**（Auto）：AI 自动做，用户看不到
> 2. **轻感植入**（Nudge）：AI 在 Gate 时追加一句"顺便问一下…"
> 3. **显性植入**（Prompt）：AI 主动建议 `/deepdive` 或 `/explore`

**⚖️ 批判者**：
> 等等，如果每个阶段都加反射点，项目会被大量"元操作"拖慢。AISEP 已经有 8 个阶段 + Gate——在 S4/S5/S6 的 Slice 循环中再加反射，会让 3 个模块 × 复盘 = 至少 3 次额外中断。**只在高价值时刻植入，不要撒胡椒面。**

**🔬 研究员**：
> Kaizen 的核心原则是"就地改善"（Gemba Kaizen）——问题在哪里发生就在哪里解决，不要等到最后。但 Scrum 也证明了"Sprint Retro 足以覆盖大部分改善需求"——不需要每步都停下来反思。**最佳频率：每个"有意义的交付物"后做一次轻量反思。**

### Round 2: 收敛

基于"有意义的交付物"定义 AISEP 的进化植入点：

```
S0  S1  S2  S3  S4  S5  S6  S7  S8  /tidy
 ·   ·   ·   🔸  ·   ·   🔸  ·   ★   ★
                │           │       │   │
    Gate 修正──┼───────────┤   S8──┘   │
    自动 L1    │           │       /tidy──┘
               │           │
 S3 架构决策后  │  S6 首个 Slice 测试后
 mini-review ──┘  回顾 AI 质量 ──┘
```

### Round 3: 共识 — 6 个植入点

**全员共识（4/4）**：

| # | 植入点 | 级别 | 触发时机 | 做什么 |
|---|--------|------|---------|--------|
| **1** | Gate 修正记录 | Auto | 每次 Gate revised/rejected | L1: 自动写入 correction 到 gate-log（**已有**） |
| **2** | Gate 修正模式检测 | Auto | Gate revised 累计 ≥ 2 次同类 | L2: 自动提示"发现重复修正模式，建议沉淀为 Skill" |
| **3** | S3 后 mini-review | Nudge | S3 Gate 通过时 | "架构决策中有无值得沉淀的 pattern？" 一句话追问 |
| **4** | Slice 循环中期 | Nudge | 第一个 Slice S6 通过时 | "首个 Slice 质量如何？AI 生成的代码修改率？" |
| **5** | S8 复盘 | Prompt | S8 阶段 | **已有**，完整的 6 步复盘流程 |
| **6** | /tidy 进化同步 | Prompt | 对话结束前 | **已有**，interaction-rules 更新 |

**分歧点**：

| 分歧 | 架构师 | 批判者 | 决议 |
|------|--------|--------|------|
| 是否在 S1/S2 也加植入点 | 赞成 | 反对（太频繁） | **跳过**——S1/S2 主要是知识收集，不产生可评估的"修正" |
| Slice 循环每个还是首个 | 每个 | 首个 | **首个 Slice 后**做一次，后续 Slice 只做 Auto 层 |

---

## 行动建议

| ID | 内容 | 类型 | 工作量 |
|----|------|------|--------|
| **prop-014** | Gate workflow 增加**修正模式检测**（同类 correction ≥ 2 时自动提醒） | Auto | ~15m · pipeline.md + gate 逻辑 |
| **prop-015** | S3 Gate 通过时追加**一句话架构经验追问** | Nudge | ~5m · s3-architecture.md |
| **prop-016** | S6 首个 Slice Gate 通过时追加**质量回顾追问** | Nudge | ~5m · s6-testing.md |
| **prop-017** | 更新 self-evolution.md 文档，增加**进化植入点图** | 文档 | ~10m · self-evolution.md |

**总计 ~35m · 4 files · mid**

### 辩论元分析

```yaml
辩论触发: "修改核心 pipeline + 多方案选择"
核心洞察: "有意义的交付物后反思" 比 "每步都反思" 更高效
未触及盲区: 跨项目进化（多个项目间的模式传播），但这已在 L2 触发条件中部分覆盖
```
