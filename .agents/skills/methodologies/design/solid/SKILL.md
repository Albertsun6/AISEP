---
name: solid
description: "SOLID 原则 — 面向对象设计五原则"
category: design
applicable_stages: [s4, s5]

requires:
  stage: [s4, s5]

always: false
---

# SOLID 原则

## 核心指令

设计每个 Model/类时逐项检查：

| 原则 | 要求 | Odoo 场景示例 |
|------|------|-------------|
| **S** 单一职责 | 一个类只做一件事 | BOM Model 不应包含生产订单逻辑 |
| **O** 开放封闭 | 对扩展开放，对修改封闭 | 用 `_inherit` 扩展而非改源码 |
| **L** 里氏替换 | 子类可替换父类 | 继承的 Model 不破坏父类行为 |
| **I** 接口隔离 | 不强迫依赖不需要的方法 | Mixin 拆细（mail.thread vs mail.activity） |
| **D** 依赖反转 | 依赖抽象而非具体 | 使用 `comodel_name` 字符串引用 |

## Gate 检查清单

- [ ] 每个 Model 是否职责单一？
- [ ] 是否通过继承扩展而非直接修改？
- [ ] Mixin 使用是否合理？
