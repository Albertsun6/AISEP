# AISEP 模板与规范层设计

## 概述

模板层和规范层是方法论的**落地工具**——方法论说"怎么思考"，模板和规范说"怎么写"。

```
方法论（HOW to think）
    ↓ 指导
模板（HOW to write）+ 规范（WHAT rules to follow）
    ↓ 产出
制品（Artifacts）+ 代码（Code）
```

---

## 1. 模板层（Templates）

### 目录结构

```
制品模板（框架无关）：
.aisep/templates/artifacts/          ← 阶段制品模板
├── domain-model.tmpl.yaml
├── functional-req.tmpl.yaml
├── architecture.tmpl.yaml
├── module-design.tmpl.yaml
└── test-report.tmpl.yaml

代码模板（跟框架绑定，就近原则）：
.agents/skills/frameworks/odoo17/templates/
├── manifest.tmpl.py
├── model.tmpl.py
├── view.tmpl.xml
├── security.tmpl.csv
├── test.tmpl.py
└── docker-compose.tmpl.yml
```

### 制品模板示例

```yaml
# .aisep/templates/artifacts/domain-model.tmpl.yaml
# 用户S1阶段输出的领域模型必须符合此结构
domain_model:
  project_id: "{{project_id}}"
  bounded_contexts:
    - name: "{{context_name}}"
      description: ""
      aggregates:
        - name: "{{aggregate_name}}"
          root_entity: "{{entity_name}}"
          entities:
            - name: ""
              attributes: []
              business_rules: []
          value_objects: []
      domain_events: []
      commands: []
  
  context_map:
    relationships:
      - upstream: "{{context_a}}"
        downstream: "{{context_b}}"
        pattern: "ACL | Open Host | Shared Kernel | Conformist"
  
  ubiquitous_language:
    - term: ""
      definition: ""
      context: "{{which bounded context}}"
```

### 代码模板示例（Odoo）

```python
# .agents/skills/frameworks/odoo17/templates/model.tmpl.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class {{ModelClassName}}(models.Model):
    _name = '{{model.technical_name}}'
    _description = '{{model.description}}'
    _inherit = [{{model.inherit}}]
    _order = '{{model.order}}'

    # === Fields ===
    {% for field in model.fields %}
    {{field.name}} = fields.{{field.type}}(
        string='{{field.label}}',
        {% if field.required %}required=True,{% endif %}
        {% if field.help %}help='{{field.help}}',{% endif %}
    )
    {% endfor %}

    # === Constraints ===
    {% for constraint in model.constraints %}
    @api.constrains('{{constraint.fields|join("', '")}}')
    def _check_{{constraint.name}}(self):
        {{constraint.logic}}
    {% endfor %}

    # === Computed Fields ===
    {% for computed in model.computed_fields %}
    @api.depends('{{computed.depends|join("', '")}}')
    def _compute_{{computed.name}}(self):
        {{computed.logic}}
    {% endfor %}
```

---

## 2. 规范层（Conventions）

### 目录结构

```
.aisep/conventions/
├── _index.yaml                 ← 规范注册表
├── naming.yaml                 ← 命名规范
├── coding-standards.yaml       ← 编码标准
├── commit-convention.yaml      ← 提交规范
├── documentation.yaml          ← 文档规范
└── security.yaml               ← 安全规范
```

### 规范文件格式

```yaml
# .aisep/conventions/naming.yaml
convention:
  id: naming
  name: "命名规范"
  applicable_stages: [s3, s4, s5]

  rules:
    # Odoo 模块命名
    - scope: "module_name"
      pattern: "^[a-z][a-z0-9_]*$"
      example: "hr_attendance_tracking"
      rule: "全小写，下划线分隔，前缀标识领域"

    # Python 模型命名
    - scope: "model_class"
      pattern: "^[A-Z][a-zA-Z]*$"
      example: "AttendanceRecord"
      rule: "PascalCase，与业务实体对应"

    # 技术名称（Odoo _name）
    - scope: "model_technical_name"
      pattern: "^[a-z]+\\.[a-z_]+$"
      example: "hr.attendance.record"
      rule: "模块名.实体名，点号分隔"

    # XML ID
    - scope: "xml_id"
      pattern: "^(view|action|menu|group|rule)_[a-z_]+$"
      example: "view_attendance_record_form"
      rule: "类型前缀_实体名_视图类型"

    # 字段命名
    - scope: "field_name"
      pattern: "^[a-z][a-z0-9_]*$"
      example: "check_in_time"
      rule: "snake_case，业务语义清晰"
```

---

## 与阶段的关系

```yaml
# config.yaml 阶段完整定义
stages:
  - id: s5
    name: "代码实现"
    workflow: ".agents/workflows/s5-implementation.md"
    gate: manual
    methodologies:
      required: [clean-code]
      optional: [tdd]
    conventions: [naming, coding-standards, security]  # ← 新增
    templates:
      artifacts: []
      code: ["odoo17/*"]                                # ← 新增
```

---

## 完整四层模型

```
┌─────────────────────────────────────────────┐
│ Layer 1: 方法论（Methodology）               │
│ "怎么思考" — DDD, C4, SOLID...              │
├─────────────────────────────────────────────┤
│ Layer 2: 规范（Convention）                  │
│ "什么规则" — 命名、编码标准、安全...           │
├─────────────────────────────────────────────┤
│ Layer 3: 模板（Template）                    │
│ "什么格式" — 制品模板、代码模板...            │
├─────────────────────────────────────────────┤
│ Layer 4: Schema（Validation）               │
│ "什么结构" — YAML schema 验证...             │
└─────────────────────────────────────────────┘

每层作用：
  方法论 → 指导思考方向
  规范   → 约束行为边界  
  模板   → 提供格式骨架
  Schema → 验证输出正确性
```

这四层从上到下，抽象度递减，约束力递增。方法论最灵活（可替换），Schema 最严格（必须通过）。
