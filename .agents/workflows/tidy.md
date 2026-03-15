---
description: "收尾整理 — 对话窗口结束前同步所有变更"
---

# /tidy 收尾整理

## 触发时机

### 应该触发 /tidy 的 3 个条件（任一满足即触发）

| # | 条件 | 信号 |
|---|------|------|
| **1** | **对话轮次过长**（≥ 50 轮交互） | 上下文退化风险，早期信息可能丢失 |
| **2** | **一个完整 Gate 通过且用户准备离开** | 自然切割点——制品已固化 |
| **3** | **话题发生重大偏移** | 如从项目执行转到系统进化研究，上下文被不相关信息稀释 |

### 不需要触发 /tidy 的情况

- 连续在同一阶段或相邻阶段内工作（如 S1→S2 一气呵成）
- 上下文没有明显退化迹象（AI 仍能准确引用早期信息）
- 只做了简单问答或小修改，没有产生系统级变更

### AI 主动提醒规则

当检测到以下信号时，AI 应在 Next step 中**建议**（非强制）执行 /tidy：
- 对话中出现 3 次以上"对了""还有""另外"等话题跳转词
- 已完成 2 个以上 Gate 且未执行过 /tidy
- 用户说"今天先到这里""下次继续"等收尾意向词

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

- [ ] 如本轮有交互进化 → 记录到 `.metap/evolution/interaction-rules.yaml`

### 10. 提取认知笔记 + 结晶成熟度评估

回顾本轮对话，提取用户可能不熟悉但重要的知识点，并评估现有知识的成熟度晋升。

**A. 提取新笔记：**
- [ ] 识别对话中出现的**概念、原理、方法论、设计决策**
- [ ] 按 `entry-template.yaml` 格式生成条目（含 `_type` + `maturity` 字段）
- [ ] 为新条目设定初始 `maturity.level: "note"` + `validation_count: 1`
- [ ] 展示给用户确认（用户可删除已掌握的）
- [ ] 确认后写入 `.aisep/knowledge/entries/learn-XXX.yaml`
- [ ] 更新 `.aisep/knowledge/index.yaml` 索引

**B. 结晶成熟度评估：**
- [ ] 扫描本轮对话是否**再次验证了已有知识条目**（类似场景、相同模式再现）
- [ ] 如是 → 更新该条目的 `maturity.validation_count += 1` + `maturity.last_validated`
- [ ] 检查晋升条件：
  - `note` + 第 2 次验证 → 晋升为 `decision`
  - `decision` + 第 3+ 次验证 → 晋升为 `skill_draft`（建议创建 SKILL.md 草案）
  - `skill_draft` + 跨项目验证 → 晋升为 `skill`（正式 SKILL.md）
- [ ] 如有晋升 → 添加 `crystallized_as` Link + 更新 `crystallization_paths`

**提取原则：**
- 只提取用户**新学到的**，不重复已有条目
- 每轮对话通常 1-3 条，宁少勿多
- 侧重「为什么」和「类比」，不记流水账

### 11. 研究沉淀检查（Research Precipitation）

回顾本轮对话，识别可沉淀的调研/探索产出。

- [ ] 扫描对话 artifact 目录中是否有调研类文件（含 research、report、analysis 等关键词）
- [ ] 如发现 → 提示用户：「检测到调研报告，是否沉淀到 .aisep/docs/research/？」
- [ ] 如确认 → 创建 `{date}-{topic}/` 目录，复制报告 + 生成 `sources.yaml`
- [ ] 更新 `.aisep/docs/research/index.yaml` 索引

**沉淀原则：**
- 详见 `.aisep/docs/research-precipitation-design.md`
- `research/` 保留完整调研上下文，`knowledge/` 保留精炼结论
- 只沉淀有价值的调研，不是每次对话都需要

### 12. 本体论一致性检查 + 决策沉淀 + 成熟度同步（Ontology Check）

回顾本轮对话中的设计决策、本体论标注完整性、以及知识成熟度跨系统同步。

- [ ] 扫描对话中是否有**重要设计决策**（技术选型、架构取舍、方案比较）
- [ ] 如发现 → 追加到 `history/decision-log.yaml`（使用 `decision-log.tmpl.yaml` 格式）
- [ ] 检查已标注的 `_type` 值是否属于 `ontology-conventions.yaml` 定义的 19 种 Object Types
- [ ] 检查新创建的制品是否已增加 `_type` 标注
- [ ] 报告**孤立 Object**（有 `_type` 但无 `_links` 的条目）— 提醒而非强制修复
- [ ] **成熟度同步检查（maturity_mapping）**：
  - 扫描 `.aisep/knowledge/index.yaml` 中 maturity.level = `skill` 的条目
  - 检查其对应的 `.metap/ontology/concepts/` 中是否存在 Concept
  - 如缺失 → 建议创建（autonomy L1，需用户确认）
  - 如存在但 maturity < `established` → 建议提升
  - 反向检查：MetaP `established` Concept 是否在 AISEP 中有对应 `skill`

**检查原则：**
- 详见 `.aisep/conventions/ontology-conventions.yaml`
- 渐进标注：不要求一次补全所有 `_links`，优先标注新增制品
- 孤立 Object 是 red flag 但不是 error — 可在后续逐步补全
- 成熟度同步只检查 `skill` ↔ `established` 的对应，不强制低级别同步

### 13. 上下文审计（Context Audit）

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

### 14. 话题偏移评估（Topic Drift Assessment）

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

### 15. 生成会话交接清单

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

### 16. 生成下一轮开场模板

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

### 17. 版本同步（Git Checkpoint）

AI 在完成上述所有步骤后，评估是否有需要版本控制的变更。

- [ ] 执行 `git status --short` 检查是否有未提交变更
- [ ] **AI 判断**：基于变更内容决定是否建议 commit
  - 建议 commit 的情况：系统文件更新、新增制品、代码变更、配置修改
  - 不建议 commit 的情况：仅临时文件变更、无实质内容变化
- [ ] 如建议 commit，向用户展示变更摘要：
  ```
  📝 Git 变更检测
  变更文件: N 个（新增 A / 修改 M / 删除 D）
  建议提交消息: tidy({date}): {stage} — {一行摘要}
  
  是否提交并推送？(y/n)
  ```
- [ ] 用户确认后自动执行：
  ```bash
  git add -A
  git commit -m "tidy({date}): {stage} — {摘要}"
  git push
  ```
- [ ] 展示结果：`git diff --stat HEAD~1`

**设计决策**：
- commit + push 均自动执行，但需**人工审核确认**后才触发
- 提交消息格式统一：`tidy({date}): {stage} — {一行摘要}`
- 如用户拒绝，变更保留在工作区，不丢失

---

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

---

## MetaP 元认知层整理（如存在 `.metap/` 时执行）

### 18. 记忆流转（Working → Episodic）

- [ ] 扫描本次对话中的关键事件（探索结论、辩论共识、用户决策、概念验证）
- [ ] 过滤纯过程性信息（搜索中间结果、格式调整）
- [ ] 按 episode schema 格式化，写入 `.metap/memory/episodes/ep-{NNN}.yaml`
- [ ] 更新 `.metap/memory/index.yaml`

### 19. 概念索引同步

- [ ] 扫描 `.metap/ontology/concepts/*.yaml` 实际文件
- [ ] 与 `concepts/index.yaml` 对比，自动修复不一致
- [ ] 重建倒排索引（by_maturity, by_tag, by_exploration）

### 20. 信任积分更新

- [ ] 汇总本次对话的信任事件（exploration_accepted, proposal_approved 等）
- [ ] 更新 `.metap/state/trust.yaml`
- [ ] 如积分跨越阈值 → 建议自治级别调整

### 21. 进化引擎 L1 观察

- [ ] 记录观察到的模式（用户偏好、探索效率、辩论表现）追加到 `.metap/evolution/observations.yaml`

### 22. Ontology 一致性检查

- [ ] Concept.derived_from 引用的 Source 是否存在
- [ ] Concept.relates_to 引用的 Concept 是否存在
- [ ] Exploration.meta 中的 concept ID 与实际文件是否匹配

### 23. Antigravity KI 桥接扫描（Knowledge Item Bridge）

扫描本 agent 的 Knowledge Items 系统，识别与当前项目相关的知识条目。

- [ ] 扫描 `~/.gemini/antigravity/knowledge/` 目录（如存在）
- [ ] 识别与当前项目/话题相关的 KI（基于 tags/summary 匹配）
- [ ] 对每个相关 KI，检查 `.aisep/knowledge/` 和 `.metap/ontology/concepts/` 中是否已有对应条目
- [ ] 如发现新的、AISEP 未覆盖的知识 → 提示用户是否提炼到 AISEP 体系
- [ ] 已有对应条目的 → 检查是否需要更新（KI 可能有更新的信息）

**桥接原则：**
- 选择性桥接，不是全量导入——只桥接与当前项目/系统相关的 KI
- KI 的格式（markdown/JSON）需转化为 AISEP 的格式（YAML）
- 保持 KI 系统的独立性——桥接是读取，不修改 KI 源文件

### 24. 上下文工程审计（Context Engineering Audit）

在现有 Step 13（上下文审计）基础上，增加**上下文效率**维度的评估。

- [ ] **加载效率**：本轮加载的总 token 估算 vs 实际使用到的信息比例
- [ ] **重复加载检测**：识别被多次加载但从未在输出中引用的文件
- [ ] **层级错配检测**：
  - 应在 L0 但被放在 L2 的高频文件（每次都需要 → 应升到 L0）
  - 应在 L2 但被放在 L0 的低频文件（占用常驻空间但很少使用 → 应降级）
- [ ] **上下文预算遵守度**：L0 < 2K / L1 < 5K / L2 < 3K 的实际遵守情况

**审计输出**：
```yaml
context_engineering_audit:
  session_date: "YYYY-MM-DD"
  estimated_total_tokens: N
  utilization_ratio: 0.X  # 实际引用的 token / 加载的 token
  level_mismatches:
    - { file: "X", current_level: "L2", recommended: "L0", reason: "..." }
  repeated_unused:
    - { file: "Y", load_count: N, reference_count: 0 }
```

### 25. 反向同步检查（Reverse Sync）

确保 AISEP.md 和 MetaP.md 中的"系统状态快照"与实际数据一致。

- [ ] 统计实际 cognitive_notes 数量 vs AISEP.md 中声明的数量
- [ ] 统计实际 Concepts/Episodes 数量 vs AISEP.md 中声明的数量
- [ ] 统计实际 Object Types / Link Types / Action Types vs 声明数量
- [ ] 如不一致 → 自动更新 AISEP.md 的"当前系统状态快照"区块（autonomy L2）
- [ ] 检查 MetaP.md 的概念统计是否与 concepts/index.yaml 一致


