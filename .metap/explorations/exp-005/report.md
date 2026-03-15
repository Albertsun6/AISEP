# Deep Dive 报告：S0 项目初始化内容合理性验证

**exp-005 | deepdive | 2026-03-15**

---

## Phase 1: 探索发现（3 Scout · 12+ 来源）

### AISEP S0 vs 行业标准对标矩阵

| 维度 | Agile Charter (PMI) | Spec-Driven Dev (AI) | Lean Startup | **AISEP S0** | 评价 |
|------|---|---|---|---|---|
| 项目名称+描述 | ✅ | ✅ | — | ✅ Step 1 | **够用** |
| 目标模块/范围 | ✅ scope | ✅ specs | — | ✅ Step 2 | **够用** |
| **问题定义/Why** | ✅ vision | ✅ purpose | ✅ Problem | ❌ 缺失 | **需改进** |
| **成功指标/KPI** | ✅ KPIs | ✅ metrics | ✅ Key Metrics | ❌ 缺失 | **需改进** |
| 技术栈 | ⚠️ 可选 | ✅ | — | ✅ Step 5 | **够用** |
| 约束条件 | ✅ | — | — | ✅ Step 3 | **够用** |
| 现有系统 | ✅ AS-IS | — | — | ✅ Step 4 | **够用** |
| **利益相关者** | ✅ 必选 | ✅ users | ✅ Customer | ❌ 缺失 | **可选改进** |
| **风险预扫** | ✅ 必选 | ⚠️ | — | ❌ 缺失 | **需改进** |
| 术语统一 | ⚠️ glossary | ✅ context | — | ✅ glossary | **领先** |
| 结构化输出 | ❌ 自由文本 | ✅ yaml | — | ✅ yaml | **领先** |
| Gate 清单 | ⚠️ | ✅ validation | ✅ MVP 验证 | ✅ | **领先** |

**得分：8/12 维度覆盖，4 个 gap（Problem · KPI · Stakeholder · Risk）**

---

## Phase 2: 自动判断 → 触发辩论

```yaml
trigger_hit:
  - "proposals > 3 且优先级无明显差异"  # 5 个 gap 需要排序
  - "改动影响后续所有项目（risk > medium）" # S0 是 pipeline 入口
```

---

## Phase 3: 辩论（4 角色 × 3 轮）

**议题**：S0 的 4 个 gap（Problem · KPI · Stakeholder · Risk），哪些值得改、哪些过度设计？

### Round 1: 探索

**🏗️ 架构师**：
> S0 是 pipeline 的入口。如果在 S0 就收集了 Problem 和 Risk，后续阶段的决策质量会显著提升。特别是 S3 架构设计需要 Risk 信息来做技术选型。**但 Stakeholder 分析对 AI 辅助开发意义不大**——没有 Scrum Master、没有 BA 团队，Stakeholder 就是用户本人。

**🎯 产品经理**：
> Problem 定义和 KPI 是最关键的两个 gap。没有 Problem 定义，S1 领域分析就像没有指南针的航海——你知道船在哪，但不知道要去哪。没有 KPI，S8 复盘时无法量化成功。**建议把 Problem + KPI 合并为一个步骤「问题与成功定义」**。

**⚖️ 批判者**：
> 等一下。AISEP 的核心用户场景是**一个人用 AI 做小项目**。问 "你的利益相关者是谁" 和 "你的成功指标是什么" 可能让用户感觉在填表——**过度流程化反而降低体验**。S0 应该尽量轻，快速进入 S1 才是关键。风险预扫？对于 AI 辅助的小项目，大部分风险在 S3 架构设计时才有意义。

**🔬 研究员**：
> 数据支撑：Lean Inception workshop 实践中，Problem Statement 和 MVP 定义的投入产出比最高。PMI 的统计显示，"unclear objectives" 是项目失败第一大原因（31%），但 "missing stakeholder analysis" 是第四（12%）。这支持了**优先加 Problem，Stakeholder 可选**的策略。

### Round 2: 深入

**🏗️ 架构师**：
> 批判者说得有道理。我修正观点：Risk 不应该在 S0 做全面评估，但可以做**轻量标记**。只加一个字段 `known_risks: []`，用户可填可不填。这不增加流程负担，但给 S3 提供了提前信号。

**🎯 产品经理**：
> 同意批判者的"填表感"担忧。建议 Problem + KPI 不要作为**强制步骤**，而是作为**询问引导**：AI 在 Step 1 提取描述后，**主动补问一句**"这个系统主要解决什么痛点？"。不需要新增步骤号，也不需要新的 YAML 字段。自然地融入现有对话。

**⚖️ 批判者**：
> 这个方向对了。区分**结构改进**和**行为改进**：
> - 结构改进 = 加新字段、新步骤（高成本，增加填表感）
> - 行为改进 = 在现有步骤中优化 AI 引导方式（低成本，不增加摩擦）
>
> Problem 和 KPI 应该用**行为改进**，而不是结构改进。

**🔬 研究员**：
> Spec-Driven Development 的最佳实践佐证了这一点：GitHub Blog 的 Spec Kit 用"high-level description"启动，然后 AI 自动追问细节。不是让用户填完整表格，而是 AI 引导式提取。

### Round 3: 收敛

**共识点（4/4 角色同意）：**

1. **Problem 定义必须加**，但方式是 AI 在 Step 1 中**主动追问**"解决什么痛点"，不加新步骤
2. **KPI 应该加**，但仅作为**可选字段**，可以只写一句话，不需要结构化指标
3. **Stakeholder 分析跳过** — 对 AI 辅助个人开发场景过度了
4. **Risk 用轻量字段** `known_risks: []` — 可填可不填，不增加流程负担

**分歧点：**

5. **constitution.md 初始化**：架构师认为应在 S0 填充，批判者认为等 S3 再填更合适（需要技术栈信息后才有意义）
   → **决议**：保持模板，S0 不强制填充，S3 Gate 检查清单增加 constitution 一项

---

## 综合行动建议（经辩论验证后修正）

| ID | 建议 | 类型 | 工作量 | 优先级 |
|----|------|------|--------|--------|
| **prop-010** | S0 Step 1 增加 AI 引导：追问痛点 + 可选 KPI | 行为改进 | ~10m · 1 file | **P1** |
| **prop-011** | project.yaml 增加 `problem` + `known_risks` 可选字段 | 结构改进 | ~10m · 2 files | **P1** |
| **prop-012** | S3 Gate 清单增加 constitution 检查项 | 结构改进 | ~5m · 1 file | **P2** |
| ~~prop-013~~ | ~~Stakeholder 分析步骤~~ | ~~结构改进~~ | — | **跳过** |

### 辩论元分析

```yaml
辩论触发原因: "5 个 gap 需优先级排序 + 影响后续所有项目"
实际价值: 高 — 从 5 个 gap 收敛到 3 个行动 + 1 个跳过，且发现了"行为改进 vs 结构改进"的关键区分
未触及盲区: 无
```
