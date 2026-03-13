---
description: "S0 项目初始化 — 从想法到结构化项目定义"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
  load:
    - ".aisep/templates/artifacts/s0-project.tmpl.yaml"
    - ".aisep/templates/artifacts/s0-research.tmpl.yaml"
    - ".aisep/schemas/s0-project.schema.yaml"
  exclude:
    - "history/**"
    - ".agents/skills/**"
    - "artifacts/**"
---

# S0: 项目初始化

## 前置条件

- 来源之一：
  - `/idea promote <id>` — 从 ideas.yaml 提升，idea 内容自动传入
  - `/s0-init` — 手动启动，需要用户提供描述
  - `/pipeline` — 编排器自动路由到 S0（新项目首阶段）
- 项目脚手架已通过 `promote` 复制到 `projects/{id}/`（如从 idea 进入）

## 输入

- 用户的项目描述（一句话到一段话）
- `project.yaml.tmpl` — 项目结构模板
- `s0-project.tmpl.yaml` + `s0-research.tmpl.yaml` — 制品格式模板

---

## 活动

### 步骤 1: 提取项目名称与描述

**AI 执行指引**：
1. 从用户描述中提取简洁项目名称（2-6 个字），以「行业+系统类型」命名（如「制造业ERP」「餐饮SaaS」）
2. 生成一句话描述（30-80 字），涵盖：做什么 + 给谁用 + 核心价值
3. 展示给用户确认，允许调整

**交互节点**：
- 🗣️ 展示提取的名称和描述 → 用户确认或修改

**异常处理**：
- 用户描述过于模糊（<10 字）→ 引导性提问：「这个系统主要服务哪类用户？核心要解决什么问题？」
- 用户描述过于宽泛 → 提示聚焦：「范围偏大，建议缩窄到一个核心场景先推进，后续迭代扩展」

### 步骤 2: 识别目标模块

**AI 执行指引**：
1. 从描述中尽可能推断初步模块列表
2. 按「核心域 / 支撑域 / 通用域」分类排列
3. 每个模块用「名词短语」命名，保持颗粒度一致

**交互节点**：
- 🗣️ 展示推断的模块列表并分类 → 用户确认、增删、调整
- 追问用户是否有遗漏：「还有其他需要覆盖的业务领域吗？」

**异常处理**：
- 模块数 > 15 → 警告：「模块过多，建议分期。建议第一期聚焦核心域的 N 个模块」
- 模块数 = 0 → 不可通过 Gate，引导用户至少列出 1 个

### 步骤 3: 了解约束条件

**AI 执行指引**：
1. 逐项了解约束（不要一次性全问）：
   - **预算**：有无预算限制？
   - **时间线**：期望的上线时间？
   - **团队规模**：参与开发的人数？是否有 AI 辅助开发的比例预期？
2. 用户可以跳过某些约束（标记为空）

**交互节点**：
- 🗣️ 逐项询问约束条件。用户说「不确定」或「随意」则该字段留空

### 步骤 4: 识别现有系统

**AI 执行指引**：
1. 主动询问：「目前是否使用现有系统（Excel、用友、SAP 等）？」
2. 如有现有系统：
   - 记录系统名称和覆盖范围
   - 标记 `existing_system` 字段 → S1 将自动触发 Gap 分析
3. 如无现有系统：`existing_system` 留空

**交互节点**：
- 🗣️ 现有系统的存在直接影响 S1 范围，**必须确认**

### 步骤 5: 技术栈预判（可选）

**AI 执行指引**：
1. 如用户已明确技术栈 → 填入 `tech_stack` 字段
2. 如用户未确定 → 留空，标注「S3 前确定」
3. 如用户有倾向但未确定 → 可建议触发 research.yaml 做调研

**异常处理**：
- 用户指定了不存在于 `.agents/skills/frameworks/` 的技术栈 → 告知：「当前框架知识库暂不覆盖此技术栈。S3 阶段可以扩展知识库，但请注意 AI 辅助质量可能较低」

### 步骤 6: 技术调研（条件性）

**触发条件**：用户明确需要技术调研，或 AI 判断存在需要验证的技术假设

**AI 执行指引**：
1. 按 `s0-research.tmpl.yaml` 格式，为每个调研课题生成 entry
2. 每个 entry 必须包含：topic、context（为什么调研）、conclusion、decision、confidence、sources
3. `confidence` 按以下标准评估：
   - `≥ 0.8`：来自官方文档或亲身验证
   - `0.5-0.8`：来自社区最佳实践或可靠二手资料
   - `< 0.5`：AI 推断，需后续验证
4. 对 `confidence < 0.5` 的条目，**必须标注需要后续验证**

**交互节点**：
- 🗣️ 展示调研结论和置信度 → 用户确认或要求进一步调研

### 步骤 7: 组装 project.yaml

**AI 执行指引**：
1. 按 `s0-project.tmpl.yaml` 组装最终 `project.yaml`
2. 填入所有已确认字段：name, description, tech_stack, target_modules, constraints, existing_system
3. 添加 `_meta` 节（template_version、created_at）
4. 添加 `pipeline_state` 节（从 `project.yaml.tmpl` 复制）
5. 写入 `projects/{id}/artifacts/global/project.yaml`

**字段映射**：
| 步骤来源 | → project.yaml 字段 |
|----------|---------------------|
| 步骤 1 | `name`, `description` |
| 步骤 2 | `target_modules` |
| 步骤 3 | `constraints.budget`, `constraints.timeline`, `constraints.team_size` |
| 步骤 4 | `existing_system` |
| 步骤 5 | `tech_stack` |

**交互节点**：
- 🗣️ 展示完整 project.yaml 预览 → 用户最终确认

---

## 输出

- `artifacts/global/project.yaml`（必须）— 项目定义制品
- `artifacts/global/research.yaml`（条件性）— 技术调研制品
- 更新 `glossary.yaml` — 用步骤 1/2 中出现的业务术语初始化

## Gate 检查清单

### 完整性
- [ ] `name` 非空（2-100 字符）
- [ ] `description` 非空
- [ ] `target_modules` ≥ 1 项
- [ ] `constraints` 至少有 1 个非空字段

### 合理性
- [ ] 项目范围是否可控（模块数 ≤ 15）？
- [ ] 约束条件是否合理（如有 timeline，是否与模块数匹配）？
- [ ] 技术栈如非空，是否匹配 `skills/frameworks/` 下的目录？

### 可追溯性
- [ ] `existing_system` 是否已确认（即使留空也需明确确认）？
- [ ] 如有 research.yaml，所有 `confidence < 0.5` 的条目是否已标注后续验证计划？

### 用户确认
- [ ] 用户已看过并确认完整的 project.yaml

## Gate 通过后

1. **Compaction**：自动生成 `project.summary.yaml`（保留 name、modules 列表、关键约束）
2. **状态更新**：`pipeline_state.stages.s0.status = "completed"`, `gate_passed = true`
3. **推进**：`current_stage` → `s1-domain`
4. **Gate 日志**：追加记录到 `history/gate-log.yaml`（含通过时间、确认方式）
5. **术语初始化**：将步骤中出现的业务术语写入 `glossary.yaml`（如尚未存在）
