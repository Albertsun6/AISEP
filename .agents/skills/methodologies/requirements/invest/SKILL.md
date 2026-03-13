---
name: invest
description: "INVEST 原则 — User Story 质量检查"
category: requirements
applicable_stages: [s2]

requires:
  stage: [s2]

always: false
---

# INVEST 原则

## 核心指令

对每个 User Story 逐条检查 INVEST 六要素：

| 维度 | 要求 | 不通过的典型信号 |
|------|------|-----------------|
| **I**ndependent | Story 之间无强依赖 | "必须先做 X 才能做 Y" |
| **N**egotiable | 实现方式可协商 | "必须用弹窗实现" |
| **V**aluable | 为用户/业务提供价值 | "拆分 model 表" |
| **E**stimable | 可估算工作量 | "集成第三方系统"（范围不清） |
| **S**mall | 1-3 天可完成 | 功能描述超过 3 句话 |
| **T**estable | 有明确的验收标准 | 没有 Given-When-Then |

## Gate 审查检查清单

- [ ] 所有 Story 的 INVEST 六项是否全部通过？
- [ ] 不通过的 Story 是否已标注原因和改进建议？
- [ ] 是否存在 Story 间的环形依赖？
