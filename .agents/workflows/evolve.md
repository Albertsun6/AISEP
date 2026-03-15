---
description: 触发系统自进化分析——从观察中提炼规则优化和能力生成建议
---

# /evolve — 自进化工作流

> 触发方式：`/evolve` 或信任积分达到阈值时自动建议
> 引擎配置：`.metap/engines/evolution.yaml`
> 自治级别：观察 L3 / 提炼 L1 / 规则变更 L0

## 前置条件

- MetaP.md 已加载
- `.metap/engines/evolution.yaml` 已加载
- `.metap/evolution/observations.yaml` 中有积累的观察

## 工作流步骤

### Step 1: 收集进化信号

// turbo
扫描以下来源收集进化信号：

| 来源 | 信号类型 | 数据来源 |
|------|---------|---------|
| `observations.yaml` | 已记录的 Auto-Observation（**主要数据源**） | 每次 Gate 自动生成（pipeline 5f） |
| `gate-log.yaml` | 修正/回退模式 | Gate 审查过程 |
| `trust.yaml` | 信任积分变化趋势 | 自治决策反馈 |
| `concepts/index.yaml` | 概念成熟度分布变化 | 探索/知识管理 |
| `memory/index.yaml` | 重复出现的 episode 类型 | 记忆引擎 |
| 最近 3 次探索报告 | 探索效率指标（有效来源比等） | 探索引擎 |

> **关键变更**（prop-013）：`observations.yaml` 中的数据由 AI 在每次 Gate 通过后**自动生成**（Auto-Observation），不再依赖用户手动提供。`/evolve` 的角色从"从空白开始分析"变为"从已积累的观察中提炼模式"。

### Step 2: 模式识别

**Step 2a: 观察合并（prop-014）**

Auto-Observation 可能跨多个 Gate 产生同主题的重复观察。在模式识别前先做合并预处理：

1. 按 `dimension` 和 `summary` 关键词聚合相似观察
2. 同主题 2+ 条 → 合并为一个**模式候选**，confidence 取最高值，evidence 合并
3. 孤立观察（仅出现 1 次）保留但标注 `singleton: true`
4. 输出合并后的观察列表（预期比原始列表缩减 30-50%）

**Step 2b: 模式匹配**

分析合并后的信号，识别可提炼的模式：

**识别维度**：
1. **行为模式**：用户/AI 在不同场景下的重复行为
2. **效率模式**：哪些流程步骤经常耗时最长或产出最少
3. **质量模式**：哪些类型的概念置信度最高/最低
4. **交互模式**：用户偏好哪种呈现方式

### Step 3: 生成进化提案

按 evolution.yaml 的 4 级进化层次生成提案：

**L2 知识提炼**（autonomy: L1，需人确认）：
- "观察到 X 模式出现 3+ 次 → 建议提炼为 Concept: {name}"
- 输出：Concept 草案（maturity: seed）

**L3 规则优化**（autonomy: L0，仅建议）：
- "Workflow 步骤 X 可优化为 Y → 建议修改 {file}"
- 输出：diff 格式的修改建议

**L4 能力生成**（autonomy: L0，仅建议）：
- "缺少 X 能力 → 建议新增 Skill/Workflow"
- 输出：新文件草案

### Step 4: 呈现进化报告 — ⚠️ 人类检查点

```markdown
## 进化报告

**日期**: {date} | **观察数**: {N} | **提案数**: {M}

### 进化提案

| # | 级别 | 提案 | 影响范围 | 风险 |
|---|------|------|---------|------|
| evo-XXX | L2 | 提炼概念: "..." | ontology | 低 |
| evo-XXX | L3 | 优化探索分解步骤 | explore.md | 中 |

### 系统度量变化
- 概念总数: {N} (+{delta})
- 平均探索效率: {X}%
- 信任积分: {score} ({trend})
- 行动建议采纳率: {X}%

> 📋 回复 `/approve evo-XXX` 逐条审批
```

### Step 5: 应用已批准的进化

1. L2 → 写入新 Concept 到 Ontology
2. L3 → 修改 Workflow/Config 文件（生成 diff → 用户确认 → 应用）
3. L4 → 创建新 Skill/Workflow 文件
4. 记录到 `evolution/history.yaml`（不可变审计日志）
5. **全局规则同步**：如进化规则属于交互偏好类（响应结构、命令行为、发散策略等），提示用户：
   ```
   此规则适用于所有对话，是否同步更新 ~/.gemini/GEMINI.md？(y/n)
   ```
   用户确认后修改 GEMINI.md 对应区块。

## 进化日志格式

```yaml
# .metap/evolution/history.yaml (追加)
- id: evo-{NNN}
  date: <today>
  trigger: user_command | pattern_detected | trust_milestone
  level: L2 | L3 | L4
  observation: "触发进化的观察"
  proposal: "进化提案内容"
  status: proposed | approved | rejected | applied
  applied_to: "受影响的文件路径"
```
