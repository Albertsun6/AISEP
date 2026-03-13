---
description: "S5 代码实现"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
    - "glossary.yaml"
  load:
    - "slices/{current-slice}/design.yaml"
    - ".aisep/conventions/naming.yaml"
    - ".aisep/conventions/coding-standards.yaml"
  load_summary:
    - "artifacts/global/architecture.yaml"
  exclude:
    - "history/**"
    - "slices/{other-slices}/**"
    - "changes/**"
---

# S5: 代码实现

> [!IMPORTANT]
> 每个 Slice 完成后模块必须处于**可安装状态**（Walking Skeleton 模式）。

## 前置条件

- 当前 Slice 的 S4 Gate 已通过
- `design.yaml` 存在且 Model/View/Security 设计完整
- Framework Skill 已加载（S3 Gating 触发）

## 输入

- `slices/{current-slice}/design.yaml`（当前 Slice 的详细设计）
- Framework Skill（Odoo17 的 `best-practices.md` + `pitfalls.md` + `templates/`）
- `naming.yaml` + `coding-standards.yaml`

---

## Walking Skeleton 协议

### Slice 1（首个）— 创建模块骨架

```
生成：
  {module}/
  ├── __init__.py           ← 包初始化（自动导入 models/）
  ├── __manifest__.py       ← 模块声明（name, depends, data 列表）
  ├── models/
  │   ├── __init__.py       ← 自动导入所有 Model 文件
  │   └── {model_name}.py   ← 当前 Slice 的 Model
  ├── views/
  │   └── {model_name}_views.xml
  ├── security/
  │   ├── ir.model.access.csv
  │   └── {module}_security.xml   ← Record Rules（如有）
  └── data/                  ← 初始数据（如有）
```

### Slice N（N ≥ 2）— 追加到已有模块

```
更新：
  __manifest__.py     ← 追加新的 data/views 文件到列表
  models/__init__.py  ← 追加新 Model 的 import
  
新增：
  models/{new_model}.py
  views/{new_model}_views.xml
  security/ir.model.access.csv  ← 追加新 Model 的 ACL 行
```

---

## 活动

### 步骤 1: 准备代码生成上下文

**AI 执行指引**：
1. 读取 `design.yaml` 的完整结构
2. 确认当前是 Slice 1（创建新模块）还是 Slice N（追加到已有模块）
3. 加载 Framework Skill 的代码模板（`templates/*.tmpl.*`）

### 步骤 2: 生成 Model 代码

**AI 执行指引**：
1. 按 `design.yaml` 的 Model 定义逐个生成 Python 文件
2. 生成顺序：被依赖的 Model 先生成
3. 每个 Model 包含：
   - 字段定义（含 string, help, required, index 等属性）
   - `_sql_constraints`
   - `@api.constrains` 验证方法
   - `@api.depends` 计算方法
   - `write` / `create` override（如有业务逻辑）
4. **Pitfall 主动检查**：
   - ❌ 不在 onchange 中放业务逻辑（P2）
   - ❌ 不在循环内调 search/write（N+1）
   - ❌ 计算字段依赖链无环（P1）

### 步骤 3: 生成 View XML

**AI 执行指引**：
1. 按 `design.yaml` 的 View 设计生成 XML
2. XML ID 命名规范：`view_{model}_{type}`（符合 `naming.yaml`）
3. Form 视图：header 状态栏 → sheet 字段分组 → chatter（如需）
4. Tree 视图：关键列 + 默认排序
5. Kanban 视图：卡片模板（如有状态流转）
6. Search 视图：过滤器 + 分组

### 步骤 4: 生成 Security 文件

**AI 执行指引**：
1. 生成 `ir.model.access.csv`：
   - 格式：`id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`
   - Slice N 时**追加行**，不覆盖已有行
2. 生成 Record Rules XML（如有行级权限需求）

### 步骤 5: 生成 Manifest 和 Init

**AI 执行指引**：
1. `__manifest__.py`：
   - `name`、`version`、`depends`、`data` 列表
   - Slice N 时更新 `data` 列表，追加新文件
   - `depends` 包含标准模块 + 当前模块依赖的自定义模块
2. `__init__.py`：
   - 根目录：`from . import models`（+ wizards, controllers 如有）
   - models 目录：逐个 import 新 Model 文件

### 步骤 6: 生成初始数据（如有）

**AI 执行指引**：
1. 必要的初始化数据（如 Sequence、默认配置）
2. 注意 `noupdate="1"`（防止更新时覆盖用户数据 — P3）
3. 如有 Demo 数据 → 放在 `demo/` 目录，`__manifest__` 的 `demo` 列表中

### 步骤 7: 可安装性自检

**AI 执行指引**：
1. 检查所有 Python 文件的 import 链是否完整
2. 检查 `__manifest__.py` 的 `data` 列表是否包含所有 XML/CSV 文件
3. 检查 XML 中引用的 `model` 名称是否与 Python 中的 `_name` 一致
4. 检查 CSV 的列数是否匹配

**自检清单**：
```
[ ] models/__init__.py 导入了所有 Model 文件？
[ ] __manifest__.py data 列表包含所有 views + security + data 文件？
[ ] 所有 XML ID 命名规范且无重复？
[ ] 所有 Many2one 的 comodel_name 拼写正确？
[ ] depends 列表包含所有引用的外部模块？
```

---

## 输出

- `artifacts/slices/{slice-name}/code/`（完整或追加的模块代码）

## Gate 检查清单

### 代码规范
- [ ] 代码是否符合 `naming.yaml`？
- [ ] 代码是否符合 `coding-standards.yaml`？
- [ ] Python 代码是否通过 linting？

### Framework 合规
- [ ] 是否规避了 `pitfalls.md` 中的所有已知陷阱？
- [ ] 是否遵循了 `best-practices.md` 的推荐做法？

### 结构完整
- [ ] 每个 Model 是否有 ACL？
- [ ] `__manifest__.py` 的 `depends` 是否正确？
- [ ] `__manifest__.py` 的 `data` 列表是否完整？
- [ ] 模块是否可安装？（结构自检通过）

### 设计一致
- [ ] 代码是否忠实于 `design.yaml` 的设计？
- [ ] 字段定义是否与 `architecture.yaml` 一致？

## Gate 通过后

1. **状态更新**：记录当前 Slice 的 S5 已完成
2. **推进**：进入当前 Slice 的 S6（测试验证）
3. **Gate 日志**：追加记录（含 slice_id + 生成的文件列表）
