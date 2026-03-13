---
description: "想法管理 — add/list/refine/promote/archive"
context:
  always:
    - "AISEP.md"
  load:
    - ".aisep/ideas.yaml"
    - ".aisep/registry.yaml"
  exclude:
    - "projects/**"
    - ".agents/skills/**"
    - "history/**"
---

# 想法管理 Workflow

## 命令总览

| 命令 | 行为 |
|------|------|
| `/idea add <描述>` | 创建 idea，自动分配 ID，写入 `ideas.yaml` |
| `/idea list` | 列出所有非 archived 的 idea |
| `/idea refine <id>` | AI 辅助分析：可行性、范围评估、建议技术栈 |
| `/idea promote <id>` | 用 project-scaffold 模板创建项目 → 进入 S0 |
| `/idea archive <id>` | 标记为 archived，不删除 |

---

## `/idea add <描述>`

**AI 执行指引**：

1. **生成 ID**：
   - 格式：`idea-NNN`（三位数字，零填充）
   - 规则：扫描 `ideas.yaml` 中已有 ID，取最大序号 +1
   - 首个 ID：`idea-001`

2. **创建 idea entry**：
```yaml
- id: "idea-NNN"
  description: "<用户描述>"
  status: "draft"
  created_at: "<ISO8601 时间戳>"
  tags: []                    # 可选，AI 自动推断 1-3 个标签
  refined: null               # refine 后填入
  promoted_to: null           # promote 后填入项目 ID
```

3. **追加到 `ideas.yaml` 的 `ideas` 列表**
4. **确认输出**：「✅ 已记录想法 idea-NNN：<描述前 30 字>...」

**异常处理**：
- 描述为空 → 提示：「请提供想法描述，至少一句话」
- 描述与已有 idea 高度相似 → 提示：「与 idea-XXX 类似：<已有描述>，是否仍要添加？」

---

## `/idea list`

**AI 执行指引**：

1. 读取 `ideas.yaml`
2. 过滤 `status != "archived"` 的 idea
3. 按格式展示：

```
📋 想法池 (N 个活跃)

| ID | 状态 | 描述 | 创建时间 |
|----|------|------|----------|
| idea-001 | draft | 制造业 ERP 系统 | 2026-03-12 |
| idea-002 | refined | 餐饮配送 SaaS | 2026-03-10 |
```

4. 如列表为空 → 提示：「想法池为空。用 `/idea add <描述>` 开始记录」

---

## `/idea refine <id>`

**AI 执行指引**：

1. 查找 `ideas.yaml` 中对应 ID 的 idea
2. 按以下 **5 维度分析框架** 执行分析：

### 分析维度

| 维度 | 关注点 | 输出 |
|------|--------|------|
| **可行性** | 技术可行？资源匹配？时间合理？ | high / medium / low |
| **价值评估** | 解决什么痛点？谁受益？ROI 如何？ | 1-2 句定性描述 |
| **范围评估** | 初步模块拆解 + 预估工作量级 | S/M/L/XL |
| **技术栈建议** | 推荐适合的技术栈 + 理由 | 1-2 个建议 |
| **风险点** | 潜在阻碍因素 | 0-3 个风险项 |

3. 将分析结果写入 idea 的 `refined` 字段：
```yaml
refined:
  feasibility: "high"
  value: "解决制造业小企业缺乏一体化 ERP 的痛点"
  scope: "L"
  suggested_tech_stack: "odoo17"
  risks:
    - "客户行业定制化需求多，标准化程度低"
  analyzed_at: "<timestamp>"
```

4. 更新 `status: "refined"`

**交互节点**：
- 🗣️ 展示分析结论 → 用户确认或补充信息 → AI 迭代分析

**异常处理**：
- ID 不存在 → 提示：「未找到 {id}，请用 `/idea list` 查看现有想法」
- idea 已是 refined 状态 → 提示：「该想法已分析过，是否重新分析？」

---

## `/idea promote <id>`

**AI 执行指引**：

### 步骤 1: 前置检查
- 查找 idea → 如不存在，报错
- 检查 `status` → 如已是 `promoted`，提示：「该想法已提升为项目 {promoted_to}」
- 建议但不强制：如 `status == "draft"`，建议先 refine

### 步骤 2: 生成项目 ID
- 格式：`proj-NNN`（三位数字，零填充）
- 规则：扫描 `registry.yaml` 中已有项目 ID，取最大序号 +1
- 首个 ID：`proj-001`

### 步骤 3: 复制脚手架
1. 将 `.aisep/templates/project-scaffold/` 整体复制到 `projects/{proj-id}/`
2. 复制后的目录结构：
```
projects/{proj-id}/
├── manifest.yaml
├── project.yaml           ← 从 project.yaml.tmpl 展开
├── constitution.md         ← 从 constitution.md.tmpl 展开
├── glossary.yaml           ← 从 glossary.yaml.tmpl 展开
├── adr/
│   └── 000-template.md
├── artifacts/
│   ├── global/            ← S0-S3 全局制品
│   ├── slices/            ← S4-S6 按 Slice 组织
│   └── changes/           ← Brownfield 增量变更
└── history/               ← Gate 日志等
```

### 步骤 4: 占位符替换
在 `project.yaml`、`constitution.md`、`glossary.yaml` 中替换：

| 占位符 | 替换值 |
|--------|--------|
| `{{project_id}}` | `proj-NNN` |
| `{{project_name}}` | idea 的 description（截取前 20 字作为名称） |
| `{{tech_stack}}` | idea.refined.suggested_tech_stack（如有）或空 |
| `{{timestamp}}` | 当前 ISO8601 时间戳 |

### 步骤 5: 注册项目
```yaml
# 更新 registry.yaml
aisep_registry:
  active_project: "proj-NNN"
  projects:
    - id: "proj-NNN"
      name: "<project_name>"
      status: "active"
      current_stage: "s0-init"
      created_at: "<timestamp>"
      source_idea: "<idea_id>"
```

### 步骤 6: 更新导航
更新 `AISEP.md` 中的 `active_project` 字段：
```yaml
active_project: "proj-NNN"
```

### 步骤 7: 更新 idea 状态
```yaml
# ideas.yaml 中对应 idea
status: "promoted"
promoted_to: "proj-NNN"
```

### 步骤 8: 自动进入 S0
- 输出：「✅ 项目 {proj-id} 已创建，自动进入 S0 项目初始化」
- 加载 `s0-init.md` Workflow，传入 idea 的 description 作为初始输入

---

## `/idea archive <id>`

**AI 执行指引**：
1. 查找 idea → 如不存在，报错
2. 如 `status == "promoted"` → 提示：「该想法已提升为项目，请用 `/project archive` 管理项目」
3. 更新 `status: "archived"`, 添加 `archived_at: "<timestamp>"`
4. 确认：「📦 idea-NNN 已归档」

---

## 异常处理汇总

| 场景 | 处理 |
|------|------|
| ideas.yaml 格式损坏 | 尝试解析 → 失败则告知用户手动修复 |
| ID 格式不合法 | 提示正确格式 `idea-NNN` |
| promote 时 projects/ 目录不存在 | 自动创建 `projects/` 目录 |
| promote 时 scaffold 模板缺失 | 报错并指引检查 `.aisep/templates/project-scaffold/` |
