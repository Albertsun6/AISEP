---
description: "S8 复盘进化 — 项目完成后的经验提取、知识沉淀和系统进化"
---

# S8 复盘进化（Retrospective & Evolution）

> **定位**：Pipeline 的最后一个阶段。每个项目完成后（S7 Gate 通过）执行一次。
> 目标：**让系统在每次项目后变得更聪明**。

## 触发条件

- 所有 Slice 完成，S7-deployment Gate 通过
- 或用户手动执行 `/s8-retrospective`

## 输入

| 来源 | 内容 |
|------|------|
| `history/gate-log.yaml` | 所有 Gate 通过/失败/回退记录 |
| `artifacts/slices/*/` | 每个 Slice 的设计 + 实现制品 |
| 项目代码 (`addons/`) | 实际交付的代码 |
| 对话历史 | 开发过程中的决策、踩坑、修复 |
| `.agents/skills/frameworks/` | 当前框架知识库 |

## 执行流程

### Step 1: 项目度量收集

```yaml
# 自动从 gate-log 和代码中提取
project_metrics:
  total_slices: 7
  total_stories: 40
  total_files: ~50
  total_custom_lines: ~500
  gate_passes: 11
  gate_failures: 0
  rollbacks: 0
  bugs_found: 1  # P1-05 quantity_done
  time_span: "2026-03-12 ~ 2026-03-13"
```

### Step 2: 经验提取（Experience Extraction）

回顾整个项目，按三个维度提取经验：

#### 2a. 踩坑记录（Pitfalls Encountered）
- 哪些地方踩了坑？
- 修复成本多大？
- 是否已沉淀到框架知识库？

**输出**：检查 `pitfalls.md` 是否已覆盖所有踩坑

#### 2b. 模式识别（Pattern Recognition）
- 哪些代码模式被反复使用？（如 TransientModel 向导、View 继承）
- 是否可以抽象为 Skill 或模板？

**输出**：建议新增的 Skill 或代码模板

#### 2c. 决策回顾（Decision Review）
- 架构决策（ADR）哪些被验证为正确？
- 哪些决策如果重来会改变？

**输出**：ADR 状态更新（Accepted / Deprecated / Superseded）

### Step 3: 知识分层沉淀

将提取的经验按层级沉淀：

```
L2 项目级（最具体）
  └→ pitfalls.md 新增条目
  └→ 项目特有的模板/配置

L1 框架级（跨项目可用）  ← 重点关注
  └→ .agents/skills/frameworks/{name}/ 更新
  └→ 新增 Skill（如"Odoo TransientModel 向导模式"）
  └→ 更新 best-practices.md / pitfalls.md

L0 通用级（跨框架/跨技术栈）
  └→ .agents/skills/methodologies/ 改进
  └→ constitution.md 新增铁律（极少触发）
  └→ Workflow 流程改进
```

**沉淀规则**：
- 项目中出现 **2 次及以上**的模式 → 提升到 L1
- 涉及**安全或数据完整性**的教训 → 评估是否进入 L0
- **仅出现 1 次**且高度项目特定 → 保留在 L2

### Step 4: 认知笔记提取

从开发过程中提取用户（和 AI）学到的关键概念：

1. 识别对话中出现的**新概念、原理、设计模式**
2. 按 `entry-template.yaml` 格式生成条目
3. **展示给用户确认**（用户可删除已掌握的）
4. 写入 `.aisep/knowledge/entries/learn-XXX.yaml`
5. 更新 `.aisep/knowledge/index.yaml`

### Step 5: 系统自进化

基于本项目经验，评估 AISEP 系统本身是否需要改进：

| 检查项 | 动作 |
|--------|------|
| Gate 检查清单是否完备 | 追加遗漏的检查项 |
| Workflow 步骤是否高效 | 精简或重排步骤 |
| 制品模板是否够用 | 新增或修改模板 |
| /tidy 清单是否遗漏项 | 追加新检查项 |
| 命令列表是否需要新增 | 评估并追加 |

**限制**：
- ❌ 不修改 `constitution.md`（需人类显式批准）
- ❌ 不删除任何 Skill 或 Workflow
- ✅ 可新增 Skill、模板、检查项
- ✅ 可更新 backlog.md

### Step 6: 生成复盘报告

输出 `artifacts/global/retrospective.yaml`：

```yaml
retrospective:
  project_id: "proj-001"
  timestamp: "2026-03-13T07:45:00+08:00"

  metrics: { ... }  # Step 1 数据

  pitfalls_added:
    - { id: "P1-05", desc: "stock.move.quantity_done → quantity" }

  patterns_identified:
    - { name: "TransientModel 向导", frequency: 1, promoted_to: null }
    - { name: "View 继承 + 中文菜单", frequency: 4, promoted_to: "L1" }

  decisions_reviewed:
    - { adr: "001", status: "validated" }
    - { adr: "002", status: "validated" }

  knowledge_entries:
    - { id: "learn-XXX", topic: "..." }

  system_evolutions:
    - { type: "workflow", desc: "新增 S8 阶段" }

  next_actions:
    - "考虑将 View 继承模式抽象为 Skill"
    - "多级 BOM 展开功能迭代"
```

## Gate 通过条件

- [ ] 项目度量已收集
- [ ] 踩坑记录已沉淀到知识库
- [ ] 模式识别至少评估 3 个候选
- [ ] 认知笔记已展示给用户确认
- [ ] 复盘报告已生成
- [ ] backlog.md 已更新

## Pipeline 更新

```
S0 → S1 → S2 → S3 → [S4→S5→S6]×N → S7 → S8 复盘进化
                                              ↓
                                        知识沉淀 → L1/L0
                                        系统进化 → Workflows/Skills
                                        ↓
                                        下一个项目更强
```
