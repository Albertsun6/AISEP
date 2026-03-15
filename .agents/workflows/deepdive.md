---
description: 深度探索 — explore + deliberate 组合原子操作，一步完成发散→收敛循环
---

# /deepdive — 深度探索

> 触发方式：`/deepdive <方向描述>`
> 本质：`/explore` + `/deliberate` 的自动编排，对应认知科学 Double Diamond 模型的一个完整菱形（发散→收敛）
> 来源：exp-004（explore × deliberate 组合模式研究）

## 工作流步骤

### Phase 1: 探索（Divergent — 发散）

执行 `/explore` 完整流程（Step 1-7），但**不等待用户审批 proposals**，直接进入 Phase 2。

- Director 分解子问题
- Scout ×N 并行搜索
- Synthesizer 综合分析
- 产出：探索报告 + 初步 proposals

### Phase 2: 自动判断——是否需要辩论？

基于 Phase 1 结果，评估以下条件：

```yaml
auto_deliberate_triggers:
  # 任一条件满足 → 进入 Phase 3 辩论
  - condition: "核心发现的 confidence < 0.7"
    reason: "信息可信度不足，需要多角色交叉验证"
  - condition: "Scout 之间存在显著矛盾"
    reason: "不同来源冲突，需要辩论厘清"
  - condition: "行动建议涉及高风险（risk > medium）"
    reason: "高风险决策需要充分质疑"
  - condition: "proposals 数量 > 3 且优先级无明显差异"
    reason: "选项过多，需要辩论收敛"

skip_deliberate_triggers:
  # 全部满足 → 跳过 Phase 3，直接呈现
  - "所有核心发现 confidence > 0.8"
  - "无 Scout 矛盾"
  - "proposals 数量 ≤ 2 且优先级明确"
```

**如果跳过辩论** → 直接进入 Phase 4（呈现报告）
**如果触发辩论** → 进入 Phase 3

### Phase 3: 辩论（Convergent — 收敛）

执行 `/deliberate` 流程，但**议题自动从 Phase 1 探索发现中提取**：

- 议题 = Phase 1 中的最高风险 proposal 或最大矛盾点
- 4 角色 × 3 轮辩论
- 产出：共识点 + 分歧点 + 修正建议

**辩论后自动评估**：

```yaml
post_deliberate_check:
  - condition: "辩论发现信息盲区（所有角色都缺少数据支撑）"
    action: "Mini-explore: 针对盲区定向搜索 1-2 个来源"
  - condition: "分歧无法收敛（3 轮后仍有 > 2 个分歧点）"
    action: "标注为 open_question，呈现给用户决策"
```

### Phase 4: 综合呈现 — ⚠️ 人类检查点

合并 Phase 1 探索报告 + Phase 3 辩论结论，输出：

```
📊 Deep Dive 报告：{方向}

## 探索发现（N 个 Scout，M 个来源）
[探索核心发现]

## 辩论结论（如触发）
[共识 / 分歧 / 修正]

## 行动建议（经辩论验证后修正）
[proposals 列表]
```

**等待用户审批**（自治级别 L1）

## 文件产出

```
.metap/explorations/exp-{NNN}/
├── meta.yaml              # 含 type: deepdive
├── report.md              # 含探索 + 辩论两部分
├── sources.yaml
├── deliberation.md        # 辩论记录（如触发）
└── scout_logs/
```

## 命名规范

> **evo-007**: AISEP 命令命名优先考虑输入便捷性——单词无连字符、无下划线，全小写。
> 例：`/deepdive` 而非 `/deep-dive`，`/tidy` 而非 `/clean-up`
