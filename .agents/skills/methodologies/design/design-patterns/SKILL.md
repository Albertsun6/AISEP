---
name: design-patterns
description: "设计模式 — 常用 OOP 设计模式与 Odoo 映射"
category: design
applicable_stages: [s4]

requires:
  stage: [s4]

always: false
---

# 设计模式

## 核心指令

在 S4 详细设计阶段，识别适用的设计模式并映射到目标框架的实现方式。

### 高频模式与 Odoo 映射

| 模式 | 意图 | Odoo 实现方式 | 适用场景 |
|------|------|--------------|----------|
| **Strategy** | 算法族可互换 | 工厂方法 + `selection` 字段 | 多种计算规则（税率、折扣） |
| **Observer** | 状态变化通知 | `mail.thread` + `tracking=True` | 关键字段变化通知 |
| **Template Method** | 算法骨架，子类填充步骤 | 基类方法 + `_inherit` 覆写 | 审批流程、状态流转 |
| **Decorator** | 动态添加职责 | `_inherit` + Mixin | 给 Model 增加 mail/activity 能力 |
| **Facade** | 统一简化接口 | Service 层方法 / Wizard | 封装复杂多步操作 |
| **State** | 状态驱动行为 | `selection` 字段 + 各状态的 action 方法 | 订单状态机（draft→confirmed→done） |
| **Repository** | 数据访问抽象 | ORM `env['model'].search/create` | 所有数据操作 |
| **Factory** | 对象创建抽象 | `default_get` + `create` 覆写 | 复杂对象的初始化 |

### 反模式警示

| 反模式 | 表现 | 修复方向 |
|--------|------|----------|
| **God Object** | 一个 Model 超过 500 行 | 拆分为多个 Model + Mixin |
| **Spaghetti Inheritance** | 继承链超过 3 层 | 评估是否可用组合（Mixin）替代 |
| **Feature Envy** | Model A 大量操作 Model B 的数据 | 把逻辑移到 Model B |
| **Shotgun Surgery** | 一个业务变更影响 > 5 个文件 | 缺少封装，需引入 Facade |

## AI 执行指引

1. 在 S4 设计每个 Slice 时，审视**是否有适用的设计模式**
2. 不强求使用模式——**只在确实简化设计时才引入**
3. 对于 Odoo 项目，优先使用 Odoo 惯用法（`_inherit`、Mixin）而非强套经典 GoF 模式
4. 如发现反模式 → 在设计中标注并提出重构建议

## Gate 检查清单

- [ ] 是否存在 God Object（单文件 > 500 行）？
- [ ] 状态流转是否有明确的状态机设计？
- [ ] 继承层级是否 ≤ 3 层？
- [ ] 跨 Model 的复杂操作是否有适当封装？
