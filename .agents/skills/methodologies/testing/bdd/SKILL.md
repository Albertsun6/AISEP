---
name: bdd
description: "行为驱动开发 — 以业务行为为中心的验证"
category: testing
applicable_stages: [s6]

requires:
  stage: [s6]

always: false
---

# 行为驱动开发 (BDD)

## 核心指令

以**业务行为**（而非代码实现）为中心编写验证场景。BDD 将 S2 的 GWT 验收标准转化为可执行的集成/E2E 测试。

```
Feature:  [业务功能名称]
Scenario: [具体场景描述]
  Given [业务前置条件]
  When  [用户行为]
  Then  [业务结果]
```

### TDD vs BDD 的分工

| 维度 | TDD（S5 阶段） | BDD（S6 阶段） |
|------|----------------|----------------|
| 驱动者 | 开发者 | 业务 + 开发者 |
| 粒度 | 单一方法/规则 | 端到端业务场景 |
| 语言 | 代码 | 自然语言 → 代码 |
| 覆盖范围 | 单元测试层 | 集成/E2E 层 |
| 来源 | S4 设计细节 | S2 的 GWT 验收标准 |

> [!IMPORTANT]
> BDD 不是 TDD 的替代品。两者互补——TDD 验证实现正确性，BDD 验证业务行为正确性。重叠区域在**集成测试层**，通过 BDD 场景覆盖后可减少 TDD 的集成测试数量。

### Odoo 场景示例

```python
class TestPurchaseOrderWorkflow(TransactionCase):
    """Feature: 采购订单审批流程"""

    def test_manager_approves_large_order(self):
        """
        Scenario: 经理审批大额采购订单
          Given 采购订单金额 > 10000 元
          And   当前用户为采购经理
          When  用户点击「确认」按钮
          Then  订单状态变为 'purchase'
          And   自动生成入库单
        """
        order = self.env['purchase.order'].create({...})
        order.with_user(self.manager).button_confirm()
        self.assertEqual(order.state, 'purchase')
        self.assertTrue(order.picking_ids)

    def test_regular_user_cannot_approve(self):
        """
        Scenario: 普通用户无法审批
          Given 采购订单金额 > 10000 元
          And   当前用户为普通采购员
          When  用户点击「确认」按钮
          Then  系统拒绝操作并提示权限不足
        """
        order = self.env['purchase.order'].create({...})
        with self.assertRaises(AccessError):
            order.with_user(self.regular_user).button_confirm()
```

## AI 执行指引

1. S6 测试阶段，从 S2 的 GWT 验收标准中提取 BDD 场景
2. 每个 Feature 对应一个 Story 或一组相关 Stories
3. **优先编写 Happy Path 场景** → 再覆盖异常路径
4. BDD 场景的测试代码应**可读性优先**（docstring 即 GWT 规格）
5. 对于 Odoo 项目：BDD 场景用 `TransactionCase` or `HttpCase`，**不需要引入额外 BDD 框架**（如 behave）——直接在 test docstring 中写 GWT 即可

### 场景覆盖优先级

| 优先级 | 场景来源 | 覆盖方式 |
|--------|----------|----------|
| 1 | S2 中 Must have Story 的 GWT | 必须有 BDD 测试 |
| 2 | S2 中 Should have Story 的 Happy Path | 建议有 BDD 测试 |
| 3 | S2 中权限相关的 GWT | 必须有 BDD 测试 |
| 4 | Could have Story | 可选 |

## Gate 检查清单

- [ ] 每个 Must have Story 是否至少有 1 个 BDD 场景？
- [ ] 权限相关场景是否覆盖（正向 + 反向）？
- [ ] BDD 场景是否可直接映射到 S2 的 GWT？
- [ ] 测试 docstring 是否清晰描述了业务行为（而非技术实现）？
- [ ] BDD 与 TDD 的覆盖范围是否有意识地分层（避免冗余）？
