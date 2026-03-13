---
name: test-pyramid
description: "测试金字塔 — 分层测试策略"
category: testing
applicable_stages: [s6]

requires:
  stage: [s6]

always: false
---

# 测试金字塔

## 核心指令

按金字塔比例编写测试：

```
        /  E2E  \          ← 少量（关键业务路径）
       / 集成测试 \         ← 适量（模块间交互）
      /  单元测试  \        ← 大量（每个方法/规则）
```

### 各层职责

| 层级 | 测什么 | Odoo 对应 | 数量占比 |
|------|--------|----------|---------|
| **单元** | 单个方法的逻辑正确性 | `TransactionCase` | ~70% |
| **集成** | 模块间的数据流和权限 | `TransactionCase` + 多 Model | ~20% |
| **E2E** | 完整业务流程 | `HttpCase` / 手动验证 | ~10% |

### 必须测试的场景

- 每个 Model 的 CRUD
- 每个 compute 字段的计算逻辑
- 每个 constraint 的正向和反向
- 每个 action 按钮的状态流转
- 权限隔离（不同 group 的访问）

## Gate 检查清单

- [ ] 单元测试是否覆盖所有业务规则？
- [ ] 是否有正向 + 反向测试？
- [ ] 权限隔离是否有测试？
- [ ] 覆盖率是否 > 80%？
