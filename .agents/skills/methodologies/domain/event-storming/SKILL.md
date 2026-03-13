---
name: event-storming
description: "Event Storming — 事件风暴（领域发现工作坊）"
category: domain
applicable_stages: [s1]

requires:
  stage: [s1]

always: false
---

# Event Storming

## 核心指令

按时间线从左到右排列领域事件：

1. **识别领域事件**（橙色便签）— "订单已创建""库存已扣减""质检已通过"
2. **识别触发命令**（蓝色）— "创建订单""扣减库存"
3. **识别触发角色**（黄色）— "销售人员""仓库管理员"
4. **识别聚合**（黄色大便签）— 哪个 Aggregate 处理这个命令
5. **识别外部系统**（粉色）— "支付网关""物流 API"
6. **识别策略/规则**（紫色）— "库存不足时自动生成采购建议"
7. **划分 Bounded Context** — 将相关事件分组

## 与 DDD 的关系

Event Storming 是 DDD 的**发现工具**：
- Event Storming 产出 → 事件流 + 聚合 + Context 边界
- DDD 产出 → 结构化的 domain-model.yaml

两者互补，Event Storming 先做（发散），DDD 后做（收敛）。

## Gate 检查清单

- [ ] 核心业务流程是否都有事件覆盖？
- [ ] 每个事件是否都有明确的触发命令和角色？
- [ ] Context 边界是否从事件分组中自然涌现？
