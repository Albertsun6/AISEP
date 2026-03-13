---
name: tdd
description: "测试驱动开发 — Red-Green-Refactor 循环"
category: implementation
applicable_stages: [s5]

requires:
  stage: [s5]

always: false
---

# 测试驱动开发 (TDD)

## 核心指令

每个功能单元按 **Red → Green → Refactor** 三步循环实现：

```
Red:      写一个会失败的测试（定义期望行为）
Green:    写最小实现让测试通过（不多写一行）
Refactor: 清理代码结构，保持测试通过
```

### 何时使用 TDD

| 场景 | 推荐度 | 理由 |
|------|--------|------|
| 业务规则 / 约束 / 计算逻辑 | ⭐⭐⭐ 强烈推荐 | 业务规则最易错，测试先行能捕获歧义 |
| 状态机 / 状态流转 | ⭐⭐⭐ 强烈推荐 | 状态组合多，测试先行确保覆盖 |
| CRUD 基础操作 | ⭐ 可选 | 框架已保证，TDD 收益低 |
| UI / 视图 | ✗ 不推荐 | 前端变化快，测试维护成本高 |

### Odoo 场景示例

```python
# Red: 先写测试
class TestBomValidation(TransactionCase):
    def test_bom_requires_positive_quantity(self):
        """BOM 子件数量必须 > 0"""
        with self.assertRaises(ValidationError):
            self.env['mrp.bom.line'].create({
                'product_id': self.product.id,
                'product_qty': 0,  # 应该失败
            })

# Green: 写最小实现
class BomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.constrains('product_qty')
    def _check_positive_qty(self):
        for line in self:
            if line.product_qty <= 0:
                raise ValidationError("子件数量必须 > 0")

# Refactor: 无需重构（实现已足够简单）
```

## AI 执行指引

1. S5 实现时，对每个**业务规则和约束**优先使用 TDD
2. 节奏控制：每个 Red-Green-Refactor 循环应 ≤ 15 分钟
3. 如果发现测试难以编写 → 可能是设计问题，回到 S4 审视
4. 测试命名：`test_{功能}_{场景}_{期望结果}`

## 与 S6 测试阶段的关系

> [!NOTE]
> TDD 产出的测试是 S5 的副产品，自动纳入 S6 的测试集。S6 的增量工作是补充**集成测试和 E2E 测试**（参见 test-pyramid Skill）。TDD 不替代 S6，而是减轻 S6 的单元测试负担。

## Gate 检查清单

- [ ] 业务规则是否通过 TDD 方式实现（测试先于实现）？
- [ ] 每个 constraint 是否有对应的测试用例？
- [ ] 测试是否命名清晰、意图明确？
- [ ] Refactor 步骤是否执行（代码整洁度检查）？
