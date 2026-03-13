---
name: user-story-mapping
description: "用户故事映射 — Jeff Patton 的需求组织方法"
category: requirements
applicable_stages: [s2]

requires:
  stage: [s2]

always: false
---

# 用户故事映射

## 核心指令

1. 识别 **用户活动（Activity）** — 高层级的用户目标（如"管理生产"）
2. 将活动分解为 **用户任务（Task）** — 按时间顺序排列（如"创建工单 → 领料 → 报工 → 入库"）
3. 在每个任务下挂载 **User Story** — 按优先级纵向排列
4. 水平线划分 **Release/Slice 边界** — 水平线以上 = MVP，以下 = 后续迭代
5. 输出 `slice-plan.yaml` — 每个 Slice 包含哪些 Story

## 与 Slice 规划的关系

Story Map 的水平切分**直接**映射为 AISEP 的 Slice：
- 第一行 = Slice 1（Walking Skeleton / MVP）
- 第二行 = Slice 2（核心增强）
- 第三行 = Slice 3（高级功能）

## Gate 审查检查清单

- [ ] Story Map 是否覆盖了所有 Bounded Context？
- [ ] Slice 划分是否合理？（每个 Slice 是否可独立部署/验证）
- [ ] Slice 1 是否足以构成最小可行产品？
- [ ] Slice 间的依赖关系是否清晰？
