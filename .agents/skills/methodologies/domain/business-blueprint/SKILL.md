---
name: business-blueprint
description: "业务蓝图方法论 — 基于 SAP ASAP 方法论改良"
category: domain
applicable_stages: [s1]

requires:
  stage: [s1]

always: false
---

# 业务蓝图方法论

## 核心指令

1. 识别 **业务场景（Scenario）** — "从收到客户订单到发货的完整流程"
2. 每个场景分解为 **业务流程（Process）** — "订单创建 → 库存检查 → 生产计划 → ..."
3. 每个流程拆解为 **业务步骤（Step）** — "创建 BOM → 生成工单 → 领料 → 报工"
4. 识别每步骤的 **角色、系统、输入/输出**
5. 标注步骤中的 **决策节点** 和 **异常路径**
6. 汇总生成 **能力图谱（Capability Map）**

## Gate 审查检查清单

- [ ] 是否覆盖了所有核心业务场景？
- [ ] 流程是否有明确的起止点？
- [ ] 是否标注了涉及的角色和系统？
- [ ] 异常路径是否识别？
- [ ] 能力图谱是否与 DDD Context Map 对齐？

## 产出增强

| 阶段 | 字段 | 类型 | 说明 |
|------|------|------|------|
| S1 | `capability_map` | tree | 能力图谱 |
| S1 | `process_flows` | list | 业务流程列表 |
