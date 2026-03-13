# AISEP Pipeline 阶段详细设计

## 流程总览

```
S0 → S1 → S2（+ Slice Planning）→ Gate
  ↓
  框架选择（如 S0 未指定，AI 根据需求推荐）
  ↓
  S3: 整体架构（一次性）→ Gate
  ↓
  ┌─ For each Slice（按依赖拓扑序）:
  │    S4: Slice 详细设计 → Gate
  │    S5: Slice 代码生成（追加到模块）→ Gate
  │    S6: Slice 测试 + 安装验证 → Gate（可演示！）
  └─ Loop
  ↓
  S7: 最终部署配置 → Gate
```

**核心变化**：S0-S2 框架无关（纯业务），框架选择在 S3 前确定，S4-S6 按 Slice 循环迭代。

---

## S0: 项目初始化

| 维度 | 内容 |
|------|------|
| **输入** | 用户一句话描述 / 从 ideas.yaml promote |
| **输出** | `artifacts/global/project.yaml` + **（可选）`research.yaml`** |
| **Gate** | 用户确认项目范围 |

输出 schema 核心字段：
- `project_name`, `description`
- `tech_stack`: **可选**，已知则填，不确定则留空（S3 前由 AI 推荐）
- `target_modules`: 初步模块列表
- `constraints`: 预算、时间、团队等约束
- `existing_system`: **可选**，现有系统描述（如"Excel 管理库存 + 用友财务"），有则触发 S1 的 Gap 分析

### 🆕 可选输出：`research.yaml`（借鉴 SpecKit）

当项目涉及技术选型、竞品调研或可行性验证时，S0 可产出研究制品：

```yaml
# artifacts/global/research.yaml
research:
  entries:
    - topic: "Odoo 17 vs 18：BOM 模块 API 变化"
      context: "项目需要稳定的 BOM/MRP 模块"
      conclusion: "17 的 mrp.bom 结构更稳定，18 引入 ECO 流变更较大"
      decision: "选用 Odoo 17"
      confidence: 0.85
      sources:
        - "Odoo 17 Release Notes"
        - "Odoo 18 EcoUpgrade Guide"

    - topic: "是否需要独立前端"
      context: "用户习惯 Web 操作，无移动端需求"
      conclusion: "Odoo 内置 Webclient 可满足 MVP"
      decision: "S3 不引入独立前端框架"
      confidence: 0.9
```

> [!TIP]
> `research.yaml` 的每条 entry 都有 `confidence` 字段。低置信度的决策应在 S1/S3 Gate 时重新审视。

---

## S1: 业务领域分析

| 维度 | 内容 |
|------|------|
| **输入** | `global/project.yaml` |
| **输出** | `global/domain-model.yaml` + `module-map.yaml` + `capability-map.yaml` + （如有）`gap-analysis.yaml` |
| **Gate** | 领域模型 + 能力映射审查；如有现有系统则审查 Gap 分析 |

核心活动：
- 识别核心业务实体（Employee, Department, Leave, Payroll...）
- 定义实体间关系和业务规则
- 映射到 ERP 模块边界（每个模块的职责划分）
- 识别与现有 Odoo 标准模块的重叠/扩展关系
- **业务能力映射**（能力树，源自 TOGAF BA）
- **Baseline/Target/Gap 分析**（仅当存在现有系统时，源自 TOGAF ADM）

> [!NOTE]
> S1 必须产出**完整**领域模型（即使只实现 MVP）。切的是实现范围，不是认知范围。

---

## S2: 需求规格 + Slice 规划

| 维度 | 内容 |
|------|------|
| **输入** | `global/domain-model.yaml` + `capability-map.yaml` |
| **输出** | `global/functional.yaml` + `non-functional.yaml` + **`slice-plan.yaml`** |
| **Gate** | 需求审查 + Slice 规划审查 — 用户确认切片划分和优先级 |

核心活动：
- 每个模块的用户故事（User Stories）
- 每个故事的验收标准（Acceptance Criteria）
- 非功能需求：性能、安全、可用性、国际化
- 优先级排序（MoSCoW: Must/Should/Could/Won't）
- **垂直切片规划**（Slice Planning）

Slice 规划输出：

```yaml
# artifacts/global/slice-plan.yaml
slice_plan:
  strategy: vertical
  granularity: feature        # L2 功能级
  slices:
    - id: slice-1
      name: "BOM 管理"
      scope: "创建、编辑、查看多级物料清单"
      models: [bom, bom_line]
      stories: [US-001, US-002, US-003]
      estimated_lines: 400
      depends_on: []
      acceptance: "用户能创建 BOM，添加子件，查看物料清单列表"
    - id: slice-2
      name: "生产工单"
      scope: "基于 BOM 创建工单，跟踪状态"
      models: [production_order, order_line]
      stories: [US-004, US-005]
      estimated_lines: 500
      depends_on: [slice-1]
      acceptance: "用户能从 BOM 创建工单，看板跟踪状态"
```

**Slice 粒度标准**：每个 Slice = 1-3 models + 完整 views + security + tests = 300-800 行代码 = 一个可独立演示的业务场景

---

## S3: 架构设计（一次性，看全貌）

| 维度 | 内容 |
|------|------|
| **输入** | `global/functional.yaml` + `slice-plan.yaml` + 框架知识库 |
| **输出** | `global/architecture.yaml` + `data-model.yaml` |
| **Gate** | 架构审查 — 用户确认**完整**数据模型和模块依赖 |
| **执行** | **一次性**，覆盖所有 Slice 的全局视野 |

核心活动：
- 基于框架知识库的技术栈特性进行架构设计
- **完整**数据模型设计（所有 Slice 的 model 都在此定义关系）
- 模块依赖图（`depends` 声明）
- 与标准 Odoo 模块的继承/扩展策略
- 安全模型（groups, access rules, record rules）

> [!IMPORTANT]
> S3 必须一次到位，不能按 Slice 分批做。数据模型需要全局一致性，否则后续 Slice 会出现结构冲突。

---

## S4-S6: 按 Slice 循环迭代

以下三个阶段对**每个 Slice** 依序执行，每完成一个 Slice 即可安装验证。

### S4: Slice 详细设计

| 维度 | 内容 |
|------|------|
| **输入** | `global/architecture.yaml` + 当前 Slice 定义 |
| **输出** | `slices/{slice-name}/design.yaml` |
| **Gate** | 设计审查 — 用户确认该 Slice 的 model/view/security 设计 |

核心活动：
- 该 Slice 包含的 Model 详细定义（字段、约束、compute 方法）
- View 设计（form/tree/kanban/search）
- Action & Menu 结构
- Security 定义（`ir.model.access.csv` 追加行）

### S5: Slice 代码生成

| 维度 | 内容 |
|------|------|
| **输入** | `slices/{slice-name}/design.yaml` |
| **输出** | 追加到 `slices/{slice-name}/code/` |
| **Gate** | 代码审查 — 用户确认生成的代码 |

核心活动（由框架知识库驱动）：
- Slice 1：生成模块骨架（`__manifest__.py`, `__init__.py`）+ 该 Slice 的 model/view/security
- Slice 2+：**追加**新文件到已有模块，更新 `__init__.py` 和 `__manifest__.py`

> [!IMPORTANT]
> 每个 Slice 完成后模块必须处于**可安装状态**（Walking Skeleton 模式）。

### S6: Slice 测试 + 验证

| 维度 | 内容 |
|------|------|
| **输入** | 当前 Slice 的代码 + 对应的 Stories |
| **输出** | `slices/{slice-name}/tests/` + 测试报告 |
| **Gate** | **可演示** — 用户安装模块后能操作该 Slice 的功能 |

核心活动：
- 生成该 Slice 的单元测试（`tests/test_{slice}.py`）
- 验证模块可安装（`odoo-bin -u module_name`）
- 需求↔代码追溯（哪些 Story 被本 Slice 覆盖）
- **用户实际操作验证**

---

## S7: 部署配置（所有 Slice 完成后）

| 维度 | 内容 |
|------|------|
| **输入** | `slices/*/code/` + 框架知识库配置 |
| **输出** | `global/deployment.yaml` + 部署脚本 |
| **Gate** | 部署审查 — 用户确认部署策略 |

核心活动：
- `docker-compose.yml`（Odoo + PostgreSQL）
- `Dockerfile` 定制
- `odoo.conf` 配置
- 模块安装脚本
- 环境变量安全管理
