# AISEP 研究沉淀机制设计

> 解决问题：调研/探索产出如何从「对话临时产物」变为「系统持久化知识」

## 问题背景

| 现状 | 问题 |
|------|------|
| 调研报告存在对话 artifact `~/.gemini/.../brain/<id>/` | 对话结束后难以发现和复用 |
| KI 自动提取可能遗漏完整调研上下文 | 精度不可控 |
| note.md 是临时记录区 | 没有结构化管理 |

## 设计方案

### 存储结构

```
.aisep/docs/research/
├── index.yaml                              # 调研索引
└── {date}-{topic-slug}/                    # 按日期+主题组织
    ├── report.md                           # 调研报告（主文档）
    ├── sources.yaml                        # 来源引用 + 决策记录
    └── attachments/                        # 可选：附件（截图、原始数据等）
```

### 索引文件 `index.yaml`

```yaml
research_index:
  items:
    - id: "research-001"
      title: "AI 辅助系统逆向工程行业调研"
      date: "2026-03-15"
      path: "2026-03-15-ai-reverse-engineering/"
      tags: ["onboard", "reverse-engineering", "ai", "knowledge-graph"]
      status: "completed"           # draft | completed | superseded
      applied_to:                   # 调研成果应用到了哪里
        - "onboard.md V2 重写"
      conversation_id: "0b998d9e-fade-452c-b2c8-9fb78230f897"
```

### 沉淀触发机制

| 触发方式 | 场景 | 动作 |
|----------|------|------|
| **自动** | 对话中产出 artifact 类型为 research | AI 提示沉淀到 `.aisep/docs/research/` |
| **命令** | `/tidy` 工作流的一部分 | 检查对话 artifact，识别可沉淀内容 |
| **手动** | 用户指定 | 直接复制并索引 |

### 与知识层的关系

```
对话 artifact → 沉淀到 research/ → 可能提取为 KI
                    ↓
              .aisep/knowledge/ → 认知笔记（高密度精炼）
```

> [!IMPORTANT]
> `research/` 保留**完整调研上下文**（来源、论证、对比），`knowledge/` 保留**精炼结论**。两者不互斥。

## 本体论视角（Palantir Ontology 启发）

Palantir Foundry 用 Object Types + Link Types 组织信息的方式，可以推广到 AISEP 整个知识体系：

### AISEP 信息本体论

```yaml
ontology:
  object_types:
    # 项目层
    - type: "project"
    - type: "slice"
    - type: "change"
    
    # 知识层
    - type: "research"          # 调研报告
    - type: "cognitive_note"    # 认知笔记
    - type: "decision"          # 决策记录
    
    # 制品层
    - type: "domain_model"
    - type: "glossary_term"
    - type: "business_rule"
    - type: "architecture_component"
    
    # 过程层
    - type: "gate_record"
    - type: "reasoning_trace"
    - type: "qa_interaction"

  link_types:
    - type: "informs"           # research → decision
    - type: "produces"          # project → artifact
    - type: "evolves_from"      # research_v2 → research_v1
    - type: "applies_to"       # decision → project/workflow
    - type: "references"        # any → any
    - type: "supersedes"        # new_version → old_version
```

### 这种思维方式的价值

1. **可发现性**：通过 link_types 找到相关联的知识
2. **可追溯性**：每个决策都能追溯到调研来源
3. **可演进性**：supersedes 关系记录知识的版本演进
4. **AI 友好**：结构化的本体论让 AI 更容易理解和导航知识库

## runtime → 静态文件的沉淀模式

> 对应 note.md 中的「如何把 runtime 沉淀成静态文件」

| runtime 类型 | 沉淀为 | 沉淀时机 | 存储位置 |
|-------------|--------|----------|----------|
| 对话中的调研 | `report.md` + `sources.yaml` | 对话结束时（/tidy） | `.aisep/docs/research/` |
| AI 推理过程 | `reasoning-trace.yaml` | 每次 Gate 通过后 | `artifacts/onboard/` |
| 用户决策 | `decision-log.yaml` | 每次交互节点后 | `artifacts/onboard/` |
| 问答交互 | `qa-summary.md` | 每个阶段结束后 | `artifacts/onboard/` |
| 项目经验 | 认知笔记 | S8 复盘时 | `.aisep/knowledge/` |

### 与 /tidy 工作流的整合

在 `/tidy` 的 step 中增加：

```
Step N: 研究沉淀检查
  - 扫描对话 artifact 目录
  - 识别 research 类型的文件
  - 如发现 → 提示用户：「检测到调研报告，是否沉淀到 .aisep/docs/research/？」
  - 如确认 → 复制文件 + 更新 index.yaml
```

## 实施计划

| 优先级 | 任务 | 工作量 |
|--------|------|--------|
| P0 | 创建 `research/index.yaml` 模板 | ~5m |
| P0 | 在 `/tidy` 中添加研究沉淀检查步骤 | ~10m |
| P1 | 本体论 schema 正式化 | ~30m |
| P2 | 知识图谱可视化（全局） | ~1h |
