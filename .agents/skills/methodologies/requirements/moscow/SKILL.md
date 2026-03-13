---
name: moscow
description: "MoSCoW 优先级排序 — 需求优先级分类"
category: requirements
applicable_stages: [s2]

requires:
  stage: [s2]

always: false
---

# MoSCoW 优先级排序

## 核心指令

对每个 User Story / 功能需求进行四级优先级分类：

| 级别 | 含义 | 判断标准 | 占比建议 |
|------|------|----------|----------|
| **M**ust have | 必须有 | 缺少则系统不可用，合同/法规要求 | ~60% |
| **S**hould have | 应该有 | 重要但有替代方案，延迟不致命 | ~20% |
| **C**ould have | 可以有 | 锦上添花，时间充裕时实现 | ~20% |
| **W**on't have (this time) | 本期不做 | 有价值但明确排出本次范围 | 不计入 |

## AI 执行指引

1. 获取完整 Story 列表后，逐个标注优先级
2. **先让用户定义 Must 的判断标准**（合同承诺？核心业务流程？法规要求？）
3. 按以下顺序分类：先标 Must → 再标 Won't → 剩余的分配 Should / Could
4. 如 Must 占比 > 70% → 发出警告：「Must 占比过高（{n}%），建议重新审视是否有可降级的需求」
5. 如 Won't 为空 → 提醒：「没有明确排除的需求可能导致范围蔓延」

## 与 Slice 划分的关系

- Must have 的 Story → 分配到前置 Slice（优先实现）
- Should have → 中间 Slice
- Could have → 后置 Slice 或标记为「未来迭代」
- Won't have → 不分配 Slice，但保留在 functional.yaml 中做记录

## Gate 检查清单

- [ ] 所有 Story 是否已标注 MoSCoW 级别？
- [ ] Must have 占比是否 ≤ 70%？
- [ ] 是否存在已提升为 Must 但缺乏业务理由的 Story？
- [ ] Won't have 列表是否已与用户确认？
- [ ] 优先级是否与 Slice 执行顺序对齐？
