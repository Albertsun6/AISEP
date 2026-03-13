---
name: adr
description: "Architecture Decision Record — 架构决策记录"
category: architecture
applicable_stages: [s3]

requires:
  stage: [s3]

always: false
---

# ADR（Architecture Decision Record）

## 核心指令

每个重要架构决策产出一个 ADR 文件（`adr/NNN-标题.md`），记录：

1. **上下文**：为什么需要做这个决策？约束是什么？
2. **决策**：我们选择了什么？
3. **理由**：考虑了哪些替代方案？为什么选这个？
4. **影响**：这个决策带来什么正面/负面后果？

## 触发条件

以下情况必须产出 ADR：
- 技术栈选择（如 Odoo 17 vs 18）
- 数据库设计的不可逆决策
- 安全模型选择
- 第三方集成方案选择

## Gate 检查清单

- [ ] 重要决策是否都有对应 ADR？
- [ ] ADR 是否记录了替代方案？
- [ ] ADR 是否标注了影响和风险？
