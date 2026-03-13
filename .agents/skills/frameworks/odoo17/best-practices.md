# Odoo 17 最佳实践

## Model 设计

### 基本规范

1. **一个文件一个 Model** — 避免在同一文件中定义多个主 Model
2. **`_description` 必须有** — 每个 Model 必须有可读的描述 string
3. **`_order` 字段** — 明确定义默认排序，避免依赖隐式 ID 排序
4. **`_rec_name`** — 如果没有 `name` 字段，必须设置 `_rec_name` 指向显示字段

### 字段定义

```python
class MrpBom(models.Model):
    _name = 'mrp.bom'
    _description = '物料清单'
    _order = 'sequence, id'
    _rec_name = 'product_id'

    # 关系字段放最前
    product_id = fields.Many2one(
        'product.product',
        string='产品',
        required=True,
        index=True,              # Many2one 建议加索引
        ondelete='cascade',      # 明确删除策略
    )

    # 普通字段
    quantity = fields.Float(
        string='数量',
        required=True,
        default=1.0,
    )

    # 计算字段放最后
    total_cost = fields.Float(
        string='总成本',
        compute='_compute_total_cost',
        store=True,              # 频繁读取 → 存储
    )

    # 约束
    _sql_constraints = [
        ('quantity_positive', 'CHECK(quantity > 0)', '数量必须大于零'),
    ]
```

### 字段顺序约定

```
1. 关系字段 (Many2one, One2many, Many2many)
2. Selection 字段 (state 等)
3. 普通数据字段 (Char, Integer, Float, Date, Boolean)
4. 计算字段 (compute)
5. 约束 (_sql_constraints)
```

### 计算字段

```python
@api.depends('bom_line_ids.cost', 'bom_line_ids.quantity')
def _compute_total_cost(self):
    for record in self:                    # ← 始终用 for 循环（Recordset）
        record.total_cost = sum(
            line.cost * line.quantity
            for line in record.bom_line_ids
        )
```

**规则**：
- `compute` + `store=True` → 频繁读取的计算字段（报表用）
- `compute` + `store=False` → 实时变化的字段（如"距今天数"）
- `depends` **必须完整** — 遗漏依赖 = 不触发重算 = 数据不一致
- 计算方法内 **必须有 `for record in self`** — 因为 self 是 Recordset

## 继承策略

| 场景 | 继承类型 | 语法 |
|------|---------|------|
| 给 `sale.order` 加字段 | 类继承 | `_inherit = 'sale.order'` |
| 创建类似订单的新对象 | 原型继承 | `_inherit = 'sale.order'` + `_name = 'custom.order'` |
| 自定义对象"天然拥有"联系人 | 委托继承 | `_inherits = {'res.partner': 'partner_id'}` |

```python
# 类继承示例 — 给已有 Model 添加字段
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'        # 无 _name → 修改原 Model

    custom_field = fields.Char(string='自定义字段')

    def action_confirm(self):
        result = super().action_confirm()   # ← 必须调用 super()
        # 自定义逻辑
        return result
```

## View 设计

### Form 视图结构

```xml
<record id="view_mrp_bom_form" model="ir.ui.view">
    <field name="name">mrp.bom.form</field>
    <field name="model">mrp.bom</field>
    <field name="arch" type="xml">
        <form string="物料清单">
            <!-- 1. Header: 状态栏和按钮 -->
            <header>
                <button name="action_confirm" type="object"
                        string="确认" class="btn-primary"
                        states="draft"/>
                <field name="state" widget="statusbar"
                       statusbar_visible="draft,confirmed,done"/>
            </header>

            <!-- 2. Sheet: 主数据区 -->
            <sheet>
                <group>
                    <group>  <!-- 左列 -->
                        <field name="product_id"/>
                        <field name="quantity"/>
                    </group>
                    <group>  <!-- 右列 -->
                        <field name="company_id"/>
                        <field name="create_date"/>
                    </group>
                </group>

                <!-- 3. Notebook: 分页区 -->
                <notebook>
                    <page string="BOM 明细">
                        <field name="bom_line_ids">
                            <tree editable="bottom">
                                <field name="product_id"/>
                                <field name="quantity"/>
                            </tree>
                        </field>
                    </page>
                </notebook>
            </sheet>

            <!-- 4. Chatter: 消息和跟踪 -->
            <div class="oe_chatter">
                <field name="message_ids"/>
                <field name="activity_ids"/>
            </div>
        </form>
    </field>
</record>
```

### View 继承

```xml
<!-- xpath 精确定位 — 推荐 -->
<field name="arch" type="xml">
    <xpath expr="//field[@name='partner_id']" position="after">
        <field name="custom_field"/>
    </xpath>
</field>
```

**规则**：
- 继承 View 的 `priority` 设为 **20-40**（避免与核心 View 冲突）
- xpath 使用 `//field[@name='x']` 精确定位，不用 position 偏移
- `groups="模块.组名"` 控制字段/按钮可见性

## 安全

1. **ACL 格式** — `ir.model.access.csv`：

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_mrp_bom_manager,mrp.bom.manager,model_mrp_bom,mrp_custom.group_mrp_manager,1,1,1,1
access_mrp_bom_user,mrp.bom.user,model_mrp_bom,mrp_custom.group_mrp_user,1,1,1,0
access_mrp_bom_viewer,mrp.bom.viewer,model_mrp_bom,base.group_user,1,0,0,0
```

2. **Record Rule 示例**：

```xml
<record id="rule_bom_company" model="ir.rule">
    <field name="name">BOM: Current Company</field>
    <field name="model_id" ref="model_mrp_bom"/>
    <field name="domain_force">[('company_id', 'in', company_ids)]</field>
    <field name="perm_read" eval="True"/>
</record>
```

3. **API 方法权限** — 对外暴露的方法加 `check_access_rights`

## 性能

### 避免 N+1 查询

```python
# ❌ N+1 — 循环内 search/write
for order in orders:
    partner = self.env['res.partner'].search([('id', '=', order.partner_id.id)])

# ✅ 批量 — 一次查询
partner_ids = orders.mapped('partner_id.id')
partners = self.env['res.partner'].browse(partner_ids)
```

### 聚合查询

```python
# ❌ Python 层聚合 — 慢
total = sum(order.amount for order in orders)

# ✅ 数据库层聚合 — 快
result = self.env['sale.order'].read_group(
    [('state', '=', 'done')],
    ['amount_total:sum'],
    ['partner_id']
)
```

### 大数据报表

```python
# SQL View — 大数据量报表
class ReportBomAnalysis(models.Model):
    _name = 'report.bom.analysis'
    _auto = False                   # ← 不创建表
    _description = 'BOM 分析报表'

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE VIEW %s AS (
                SELECT ...
            )
        """ % self._table)
```

## 测试

### 测试基类选择

| 基类 | 用途 | 事务 |
|------|------|------|
| `TransactionCase` | 单元测试（最常用） | 每个 test 自动回滚 |
| `SavepointCase` | 共享 setUp 数据 | setUpClass 不回滚，每个 test 用 savepoint |
| `HttpCase` | 前端/API 测试 | 不回滚，需手动清理 |

### 测试模板

```python
from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestMrpBom(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Test Product',
        })

    def test_create_bom_success(self):
        """创建 BOM 基本流程"""
        bom = self.env['mrp.bom'].create({
            'product_id': self.product.id,
            'quantity': 1.0,
        })
        self.assertTrue(bom.id)

    def test_bom_qty_negative_raises(self):
        """数量为负时应抛出 ValidationError"""
        with self.assertRaises(ValidationError):
            self.env['mrp.bom'].create({
                'product_id': self.product.id,
                'quantity': -1.0,
            })
```
