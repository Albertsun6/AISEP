---
description: "项目管理 — list/switch/status/archive"
context:
  always:
    - "AISEP.md"
  load:
    - ".aisep/registry.yaml"
  exclude:
    - ".agents/skills/**"
    - ".aisep/templates/**"
    - ".aisep/docs/**"
---

# 项目管理 Workflow

## 命令总览

| 命令 | 行为 |
|------|------|
| `/project list` | 列出 `registry.yaml` 中所有项目 |
| `/project switch <id>` | 设置 active_project，更新导航 |
| `/project status` | 简要进度：当前阶段 + 最近 Gate |
| `/project status --full` | 聚合视图：从所有制品合成完整概览 |
| `/project archive <id>` | 标记项目为 archived |

---

## `/project list`

**AI 执行指引**：

1. 读取 `registry.yaml` → 获取 `projects` 列表
2. 按格式展示：

```
📁 项目列表 (N 个)

| ID | 名称 | 状态 | 当前阶段 | 创建时间 |
|----|------|------|----------|----------|
| ★ proj-001 | 制造业 ERP | active | S2 需求规格 | 2026-03-12 |
| proj-002 | 餐饮 SaaS | active | S0 初始化 | 2026-03-11 |
| proj-003 | 库存系统 | archived | S3 架构 | 2026-03-08 |

★ = 当前活跃项目
```

3. 如列表为空 → 提示：「无项目。用 `/idea promote <id>` 从想法创建项目」
4. 如存在 `.aisep/archive/registry-archive.yaml`，在列表末尾追加显示：`📦 归档项目: N 个（详见 .aisep/archive/registry-archive.yaml）`

---

## `/project switch <id>`

**AI 执行指引**：

### 步骤 1: 验证项目
- 查找 `registry.yaml` 中对应 ID → 如不存在，报错并列出可用项目
- 如项目 status = `"archived"` → 提示：「该项目已归档。需要重新激活吗？」

### 步骤 2: 联动更新（3 个文件）

**文件 1 — `registry.yaml`**：
```yaml
aisep_registry:
  active_project: "<new_id>"    # 更新
```

**文件 2 — `AISEP.md`**：
```yaml
active_project: "<new_id>"     # 更新
```

**文件 3 — `AISEP.md` context_fence**：
- 更新 `context_fence.active` 为 `<new_id>`
- 将旧项目加入 `excluded_dirs`：`"projects/{old_id}/**"    # 暂停中"`
- 将新项目从 `excluded_dirs` 中移除（如存在）

### 步骤 3: 确认
```
🔄 活跃项目已切换
   从: {old_id} ({old_name})
   到: {new_id} ({new_name})
📍 当前阶段: {current_stage} — {stage_name}
   上下文围栏已更新
```

**异常处理**：
- 切换到已经是活跃的项目 → 提示：「{id} 已是当前活跃项目」
- 无活跃项目时切换 → 正常处理（old = "无"）

---

## `/project status`

**AI 执行指引**：

1. 获取活跃项目（无活跃项目则报错）
2. 读取 `project.yaml` → `pipeline_state`
3. 读取 `history/gate-log.yaml` → 最近 3 条 gate 记录
4. 按格式展示：

```
📊 项目状态: {project.name} ({project.id})

Pipeline 进度:
  S0 ✅  S1 ✅  S2 ⏳  S3 ⏹️  S4-S6 ⏹️  S7 ⏹️
                 ↑ 当前

最近 Gate:
  • S0 ✅ 通过 (2026-03-12 10:00)
  • S1 ✅ 通过 (2026-03-12 14:30)

下一步: 执行 S2 需求规格。使用 /pipeline 推进。
```

**符号含义**：
| 符号 | 状态 |
|------|------|
| ✅ | completed + gate_passed |
| ⏳ | in_progress |
| 🔄 | revision（Gate 修正中） |
| ❌ | rejected |
| ⏹️ | pending |

---

## `/project status --full`

**AI 执行指引**：

生成项目完整聚合视图。**此视图不持久化**，仅在对话中展示。

### 聚合数据源

| 数据源 | 提取内容 |
|--------|----------|
| `project.yaml` | 项目名称、ID、技术栈、pipeline 状态 |
| `glossary.yaml` | 术语总数 |
| `artifacts/global/*.yaml` | 每阶段制品摘要（优先读 `.summary.yaml`） |
| `artifacts/slices/*/` | Slice 完成度（已完成 / 总数） |
| `artifacts/changes/*/` | 待处理变更请求数 |
| `history/gate-log.yaml` | Gate 通过/修正/拒绝统计 |

### 输出格式

```
📊 项目全景: {project.name} ({project.id})
═══════════════════════════════════════════

🔧 技术栈: Odoo 17
📝 术语表: 42 个术语
📅 创建时间: 2026-03-12

Pipeline 进度:
  ┌─────────────────────────────────────────┐
  │ S0 ✅ │ S1 ✅ │ S2 ✅ │ S3 ✅ │ S7 ⏹️ │
  └─────────────────────────────────────────┘

Slice 进度 (3/5):
  ✅ slice-01: 用户管理        S4✓ S5✓ S6✓
  ✅ slice-02: 物料管理        S4✓ S5✓ S6✓
  ✅ slice-03: 采购订单        S4✓ S5✓ S6✓
  ⏳ slice-04: 生产工单        S4⏳ S5⏹️ S6⏹️
  ⏹️ slice-05: 库存管理

变更请求: 2 个待处理

Gate 统计: 8 通过 / 1 修正 / 0 拒绝

各阶段制品摘要:
  S0: 项目定义 — 5 个目标模块，Odoo17 技术栈
  S1: 领域模型 — 3 个限界上下文，12 个聚合
  S2: 需求规格 — 28 个 Story，5 个 Slice
  S3: 架构设计 — MVC + 3 层分离，PostgreSQL
```

### 数据缺失处理
- 某阶段制品不存在 → 该阶段显示 `(未开始)`
- gate-log.yaml 不存在 → Gate 统计显示 `(无记录)`
- slices/ 目录为空 → Slice 进度显示 `(未规划)`

---

## `/project archive <id>`

**AI 执行指引**：

### 步骤 1: 验证
1. 查找 `registry.yaml` 中对应 ID → 如不存在，报错
2. 如是当前活跃项目 →「该项目是当前活跃项目。归档后将清除活跃状态，确认？」

### 步骤 2: 冷热迁移（3 个文件联动）

**文件 1 — `registry.yaml`**：
- 从 `projects` 列表中**移除**该项目

**文件 2 — `.aisep/archive/registry-archive.yaml`**：
- 在 `archived_projects` 中**追加**：
  ```yaml
  - id: "{id}"
    name: "{name}"
    stage: "{current_stage}"
    archived_at: "{timestamp}"
    summary: "{自动生成的一行摘要: 模块数/代码行数/Gate统计}"
    project_dir: "projects/{id}/"
  ```

**文件 3 — `AISEP.md`**：
- 在 `context_fence.excluded_dirs` 中追加：`"projects/{id}/**"    # 已归档`
- 如是活跃项目：`active_project: null`，`context_fence.active: null`

### 步骤 3: 确认输出
```
📦 项目 {id} ({name}) 已归档
   → 迁移到 registry-archive.yaml
   → 上下文围栏已排除 projects/{id}/**
   → 项目文件保留在 projects/{id}/（不删除）
```

> [!NOTE]
> 归档不删除项目文件。`projects/{id}/` 目录保留，但被 context_fence 排除，AI 不会意外加载。
> 
> 如需恢复归档项目，手动从 `registry-archive.yaml` 移回 `registry.yaml`，并从 `AISEP.md` 的 `context_fence.excluded_dirs` 中移除对应行。

---

## 异常处理汇总

| 场景 | 处理 |
|------|------|
| registry.yaml 不存在 | 自动创建空注册表 |
| 项目 ID 不存在 | 报错 + 列出可用项目 |
| 无活跃项目时调用 status | 提示「无活跃项目，请先 `/project switch <id>`」 |
| project.yaml 缺失 | 提示「项目可能未正确初始化，请检查 `projects/{id}/`」 |
| gate-log.yaml 缺失 | 状态中 Gate 部分显示「无记录」 |
