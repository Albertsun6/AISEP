---
description: "收尾整理 — 对话窗口结束前同步所有变更"
---

# /tidy 收尾整理

## 触发时机

对话窗口即将关闭时执行（用户说 `/tidy` 或 "开新对话"）。

## 整理清单

### 1. 更新 `system-guide.md`（人的入口）

- [ ] 目录速览中的文件数和描述
- [ ] 方法论表与实际 SKILL.md 文件对齐
- [ ] 命令列表与实际 workflows 对齐
- [ ] 追加 changelog 条目

### 2. 更新 `AISEP.md`（AI 的入口）

- [ ] 命令速查与 system-guide 命令列表对齐
- [ ] 系统文件索引（如有新的 L0/L1 文件）

### 3. 更新 `architecture.md`（结构真相源）

- [ ] 目录结构树与实际文件对齐
- [ ] 命令接口段与实际 workflows 对齐
- [ ] 五面体分层图（如有新模块加入）

### 4. 更新 `config.yaml`

- [ ] 新增方法论是否注册到对应阶段的 methodologies 列表
- [ ] 新增 workflow 是否注册到 stages 列表

### 5. 更新 `methodology-layer.md`

- [ ] 目录结构树与实际 SKILL.md 文件对齐
- [ ] 完整映射表（阶段↔方法论）是否完整

### 6. 更新 `implementation_plan.md`

- [ ] 标记已完成的构建项
- [ ] 新发现的待建项增补

### 7. 更新 `backlog.md`

- [ ] 对话中提到但未实现的想法 → 追加为待办
- [ ] 已完成的 backlog 项 → 标记完成
- [ ] 追加 changelog 条目

### 8. 一致性检查

- [ ] `find` 扫描实际文件 vs 文档中的目录结构
- [ ] 报告差异（不自动修复，只告知）

### 9. 追加进化记录

- [ ] 如本轮有交互进化 → 记录到 `evolution/interaction-rules.yaml`

### 10. 提取认知笔记

回顾本轮对话，提取用户可能不熟悉但重要的知识点。

- [ ] 识别对话中出现的**概念、原理、方法论、设计决策**
- [ ] 按 `entry-template.yaml` 格式生成条目（one_liner + analogy + key_insights）
- [ ] 展示给用户确认（用户可删除已掌握的）
- [ ] 确认后写入 `.aisep/knowledge/entries/learn-XXX.yaml`
- [ ] 更新 `.aisep/knowledge/index.yaml` 索引

**提取原则：**
- 只提取用户**新学到的**，不重复已有条目
- 每轮对话通常 1-3 条，宁少勿多
- 侧重「为什么」和「类比」，不记流水账

### 11. 上下文审计（Context Audit）

回顾本轮对话，分析文件使用情况（基于实际 `view_file`/`grep_search` 调用）。

- [ ] 列出本轮**实际访问过的文件**及访问次数
- [ ] 标注 verdict：`essential`（多次访问）/ `referenced`（1 次）/ `loaded_but_unused`（加载但未实际使用）
- [ ] 识别**应该早点加载但中途才发现需要的文件**（`late_discovery`）
- [ ] 将审计结果写入 `projects/{id}/_context_audit.yaml`（追加模式，保留最近 10 条）

```yaml
# 审计条目格式
- session_date: "2026-03-13"
  stage: "s5-implementation"
  slice: "slice-03"
  files:
    - { path: "design.yaml", times: 3, verdict: "essential" }
    - { path: "architecture.yaml", times: 1, verdict: "referenced" }
  late_discoveries:
    - { path: "slice-01/design.yaml", reason: "需要参考对称模块设计" }
```

**审计原则：**
- 只记录项目制品和系统文件，不记录临时文件 / 外部 URL
- verdict 判定标准：访问 2+ 次 = essential，1 次 = referenced，0 次但被声明加载 = loaded_but_unused
- `late_discovery` 是最有价值的信号——说明 Workflow 的 context 声明不够完善

### 12. 话题偏移评估（Topic Drift Assessment）

评估本轮对话是否偏离了预期锚点。

- [ ] 确定本轮**预期锚点**（当前 stage + slice，或对话开场时声明的目标）
- [ ] 回顾对话流，识别偏离锚点的讨论段
- [ ] 对每次偏移标注 severity：`minor`（合理的临时跨界）/ `major`（应该开新对话）
- [ ] 将评估写入 `_context_audit.yaml` 同一条目中

```yaml
  topic_drift:
    anchor: "S5 Slice-03 Purchase 实现"
    events:
      - { at: "中段", topic: "修复 Sale 模块 bug", severity: "minor" }
    recommendation: "minor 偏移可通过 change 日志记录；major 偏移建议提示用户开新对话"
```

**评估原则：**
- **不是所有偏移都是坏事** — 修 bug、回答用户临时问题属于正常
- 关注的是**系统性偏移**：如果半小时以上在讨论非锚点主题，就是 major
- 连续 2 次 /tidy 出现同类 minor 偏移 → 考虑是否应该调整 Workflow 的 scope

### 13. 生成会话交接清单

基于本轮工作和上下文审计，生成 `_next_session.yaml` 供新对话消费。

- [ ] 判断下一步最可能的任务（基于 pipeline 状态 + 本轮结束点）
- [ ] 生成推荐加载文件列表（分 `recommended` / `optional` / `excluded`）
- [ ] 附上推荐理由（`rationale`）
- [ ] 写入 `projects/{id}/_next_session.yaml`（覆盖式，只保留最新一份）

```yaml
# projects/{id}/_next_session.yaml
next_session:
  generated_at: "2026-03-13T08:30"
  predicted_task: "S5 Slice-04 MRP 模块代码实现"
  predicted_stage: "s5-implementation"

  recommended:                          # AI 推荐，新对话自动加载
    - path: "slices/slice-04/design.yaml"
      reason: "S4 设计产出，S5 主输入"
    - path: "architecture.yaml"
      reason: "架构约束（模块依赖图）"
    - path: "skills/odoo17/pitfalls.md"
      reason: "避坑必读"

  optional:                             # 可能有用，展示给用户选择
    - path: "slices/slice-01/design.yaml"
      reason: "Sale 模块可作为参考模板"

  excluded:                             # 明确排除
    - pattern: "slices/slice-05~07/**"
      reason: "未来 Slice，避免上下文污染"
    - pattern: "history/gate-log.yaml"
      reason: "只需摘要版"

  rationale: |
    基于 pipeline 状态，下一步是 Slice 4 的 S5 实现。
    上一轮审计显示 architecture.yaml 每次 S5 都被访问（essential），
    且 Sale 设计曾作为 late_discovery 出现，故提升到 optional。
```

**生成原则：**
- `recommended` 基于两个信号：Workflow 的 context 声明 + 历史审计中的 essential 文件
- `optional` 来自历史审计中的 late_discovery（曾经迟到的，下次提前准备）
- `excluded` 来自 Workflow 的 exclude 声明 + 非活跃 Slice
- 如有 3+ 次审计数据，使用频率统计优化推荐（进化式学习）

### 14. 生成下一轮开场模板

**必须在 /tidy 最后输出。** 根据本轮工作内容和交接清单，生成 1-3 个可直接粘贴的开场模板。

- [ ] 识别本轮的主要工作方向（项目开发 / 系统设计 / 探索研究）
- [ ] 根据后续自然走向，生成 1-3 个方向选项
- [ ] **引用交接清单**：在模板的"需要延续的关键上下文"中包含 `_next_session.yaml` 路径
- [ ] 每个模板使用以下格式：

```
继续 [话题/项目] 探索。上一轮覆盖了：
- [关键成果 1]
- [关键成果 2]

本轮目标：[具体目标 或 选项 A/B/C]

需要延续的关键上下文：
- 交接清单：projects/{id}/_next_session.yaml
- [其他关键文件]
```

**生成原则：**
- 包含足够上下文让新对话的 AI 快速接续（关键文件路径、项目 ID、阶段状态）
- 每个模板不超过 10 行
- 至少一个选项是「继续当前方向」，至少一个是「转向新方向」

## 不做的事

- ❌ 不修改 Workflow / Skill / Schema 的**业务内容**
- ❌ 不修改 `constitution.md`
- ❌ 不删除任何文件

## 核心原则

> **/tidy 的目标是「描述的一致性」**：所有文档中对系统结构的描述（目录树、命令列表、方法论映射）必须与实际文件一致。它不改变系统行为，只确保"文档说的"和"实际有的"一样。

## 自我进化

当 `/tidy` 执行中发现了**当前清单未覆盖的不一致类型**时：

1. 修复该不一致
2. 将新检查项追加到上方清单中
3. 在 backlog.md changelog 中记录："tidy 规则进化：新增 [检查项描述]"

无需人工审批（属于 L2 自动沉淀——仅影响描述一致性，不改系统行为）。
