---
name: ddd
description: "Domain-Driven Design — 领域驱动设计"
category: domain
applicable_stages: [s1, s3, s4]

requires:
  stage: [s1, s3, s4]

always: false
---

# DDD 方法论

## 核心指令（AI 执行时的思考协议）

1. 与用户共同建立 **Ubiquitous Language**（统一语言），所有术语同步到 `glossary.yaml`
2. 识别 **核心域、支撑域、通用域**——核心域投入最多设计精力
3. 划分 **Bounded Context**（限界上下文）——每个 Context 内部术语一致、对外接口清晰
4. 在每个 Context 内识别 **Aggregate Root, Entity, Value Object**
5. 定义 **Context Map** — 各 Context 间的关系（ACL, Open Host, Shared Kernel, Conformist）
6. 将 Bounded Context 映射到模块边界 — 一个 Context 对应一个或多个模块

## 关键原则

- **Aggregate Root 是事务边界** — 一次操作只修改一个 Aggregate
- **Value Object 是不可变的** — 比较靠值而非引用
- **Entity 有生命周期** — 用 ID 标识，状态可变
- **领域事件描述已发生的事** — 可用于跨 Context 通信

## Gate 审查检查清单

- [ ] 是否识别并文档化了 Ubiquitous Language？（同步到 glossary.yaml）
- [ ] 是否划分了 Bounded Context，边界是否清晰？
- [ ] 是否有 Context Map？关系模式是否定义？
- [ ] 每个 Aggregate Root 的不变量是否定义？
- [ ] 模块边界是否与 Context 边界对齐？
- [ ] 核心域是否获得了最充分的设计投入？

## 产出增强

| 阶段 | 字段 | 类型 | 说明 |
|------|------|------|------|
| S1 | `ubiquitous_language` | glossary | 统一语言词汇表 |
| S1 | `context_map` | diagram_spec | 限界上下文映射 |
| S3 | `module_boundary` | architecture | Context → Module 映射 |

## 参考文献

- Eric Evans — *Domain-Driven Design* (2003)
- Vaughn Vernon — *Implementing Domain-Driven Design* (2013)
- Alberto Brandolini — *Event Storming* (2013)
