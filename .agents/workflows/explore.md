---
description: 发起多Agent并行探索任务——从用户方向到结构化报告和行动建议
---

# /explore — 探索工作流 v2.0

> 触发方式：`/explore <方向描述>`
> 引擎配置：`.metap/engines/exploration.yaml`
> 自治级别：搜索 L2 / 建议 L1
> 版本：v2.0（升级自 v1.0：新增多 Scout 并行、Director-Scout-Synthesizer 三角色分工）

## 角色定义

| 角色 | 职责 | 数量 |
|------|------|------|
| **Director** | 接收方向、分解子问题、分配任务、生成行动建议 | 1 |
| **Scout** | 对分配的子问题进行信息检索和初步分析 | 1-3（按子问题数量动态分配） |
| **Synthesizer** | 汇总所有 Scout 发现、去重交叉验证、生成综合报告 | 1 |
| **Registrar** | 将发现注册为 Ontology 对象（Concept + Source + Link） | 1 |

## 前置条件

- MetaP.md 已加载
- `.metap/engines/exploration.yaml` 已加载

## 工作流步骤

### Step 1: 接收与确认方向 (Director)

1. 解析用户给出的探索方向
2. 如果方向过于模糊，提问澄清（最多 1 轮）
3. 创建 Exploration 对象：
   ```yaml
   # .metap/explorations/exp-{NNN}/meta.yaml
   id: exp-{NNN}
   direction: "<用户方向>"
   status: active
   started_date: <today>
   ```
4. 确认："探索方向已确认：{direction}。开始分解子问题。"

### Step 2: 分解子方向 (Director)

1. 将方向分解为 3-5 个子问题
2. 每个子问题标注：
   - **优先级**（core / supplementary / extended）
   - **搜索策略**（academic / industry / case_study / technical）
   - **搜索关键词**（英文优先）
3. 为每个 core 子问题分配一个 Scout（supplementary/extended 可合并）
4. 输出分解结果（自治级别 L2）:
   ```
   📋 子问题分解（共 N 个，分配 M 个 Scout）：
   Scout-A: [core] {question_1} — 策略: academic
   Scout-B: [core] {question_2} — 策略: industry
   Scout-C: [core+supplementary] {question_3 + question_4} — 策略: technical
   ```

### Step 3: 并行信息侦察 (Scout × N)

// turbo
**多 Scout 并行执行**（每个 Scout 独立搜索，互不干扰）：

每个 Scout 的执行流程：
1. 根据分配的子问题和搜索策略执行搜索
2. 每个子问题收集 3-5 个来源
3. 来源自动评分（参考 auto_credibility 规则）
4. 对每个来源提取关键发现
5. 生成 Scout 发现报告

**Scout 搜索策略差异化**：

| 策略 | 工具偏好 | 来源类型 |
|------|---------|---------| 
| academic | search_web (site:arxiv.org scholar.google.com) | 论文、学术综述 |
| industry | search_web (general), read_url_content | 行业报告、厂商方案、案例 |
| case_study | search_web (site:medium.com github.com) | 实践案例、开源项目 |
| technical | search_web, read_url_content (docs) | 技术文档、API 参考 |

**Scout 输出格式**：
```yaml
scout_id: A
sub_question: "..."
findings:
  - source: { title, url, credibility }
    key_points: [...]
    relevance: high | medium | low
confidence: 0.X
gaps: "未能覆盖的方面"
```

**并行调度**：
- 使用多轮并行 `search_web` 调用，每个 Scout 的搜索同时发起
- Scout 之间不共享中间结果（保持独立性，避免 confirmation bias）
- 所有 Scout 完成后，结果汇总到 Synthesizer

### Step 4: 综合分析 (Synthesizer)

1. **汇总**：合并所有 Scout 发现
2. **去重**：同一结论多源佐证 → 提升 confidence
3. **交叉验证**：不同 Scout 的独立发现互相印证 → 可信度更高
4. **矛盾检测**：不同 Scout/来源的冲突信息 → 标注为矛盾点
5. **提炼核心发现**：3-5 个关键洞察（排序：confidence × relevance）
6. **标注知识空白**：所有 Scout 都未能覆盖的盲区
7. **元分析**：哪些 Scout 策略最高效？记录供进化引擎学习

### Step 5: 知识注册 (Registrar)

按 Ontology schema v0.2.0 的 Kinetic 层 Action 定义注册：

1. **register_concept** (autonomy: L2)
   - 新发现 → 创建 Concept（maturity: seed）
   - 文件：`.metap/ontology/concepts/concept-{NNN}.yaml`

2. **source.verify** (autonomy: L3)
   - 新来源 → 创建 Source（含 credibility 评分）
   - 文件：探索目录下 `sources.yaml`

3. **concept.link** (autonomy: L2)
   - 建立 Concept ↔ Source 的 `derived_from` Link
   - 如果发现与现有 Concept 相关，建立 `relates_to` Link
   - 如果发现矛盾，建立 `contradicts` Link

4. 更新 `.metap/ontology/concepts/index.yaml`

### Step 6: 生成行动建议 (Director)

1. 基于综合分析报告生成 2-4 个 ActionProposal
2. 每个建议必须包含：
   - 标题和理由（引用具体发现）
   - 工作量估算
   - 风险评估
   - 优先级（P0-P3）
   - 执行路径（创建 AISEP 项目 / 继续探索 / 直接操作）
3. 建议之间应有优先级差异，避免全是 P0

### Step 7: 呈现报告 (Director) — ⚠️ 人类检查点

按 exploration.yaml 中的 report_template 格式输出。

**必须等待用户审批**（自治级别 L1）

### Step 8: 执行批准的建议

1. 对每个 approved 的 ActionProposal：
   - 需要 AISEP 项目 → 触发 `aisep.create_project` Action
   - 继续探索 → 创建新 Exploration（follows_up）
   - 直接操作 → 在自治级别允许范围内执行
2. 更新 Exploration 状态为 `concluded`

### Step 9: 事后记录与记忆流转

1. **Episodic memory**: 写入 `.metap/memory/episodes/ep-{NNN}.yaml`
2. **信任积分更新**: `trust.update_score(exploration_accepted)`
3. **进化引擎 L1**: 记录探索效率
4. **概念索引更新**: 确保 index.yaml 与新注册概念同步

## 自动触发博弈

当 Step 4 发现以下情况时，自动建议发起 `/deliberate`：
- 核心发现的 confidence < 0.5
- Scout 之间存在显著矛盾
- 行动建议涉及高风险（risk > medium）

## 文件产出

```
.metap/explorations/exp-{NNN}/
├── meta.yaml              # 探索元数据（含 Scout 分配信息）
├── report.md              # 结构化探索报告
├── sources.yaml           # 来源清单及评分
└── scout_logs/            # 各 Scout 原始发现
    ├── scout_a.yaml
    ├── scout_b.yaml
    └── scout_c.yaml
.metap/ontology/concepts/
├── concept-{NNN}.yaml     # 新概念
.metap/memory/episodes/
├── ep-{NNN}.yaml          # 事件记忆
```
