# AISEP 逆向 Onboard 设计（V2）

> [!NOTE]
> 基于 2026-03-15 行业调研结果重新设计。
> 调研报告：`.aisep/docs/research/2026-03-15-ai-reverse-engineering/report.md`

## 定位

独立的 Onboard 流程，将现有系统模块逆向为 AISEP 标准制品，纳入项目管理。

```
/onboard --source ./path/to/modules
  → R0 鸟瞰 → R1 扫描 → R2 领域还原 → R3 对齐 → R4 补全 → R5 Slice → R6 注册
  → 项目出现在 registry.yaml，可用 /pipeline 继续正向演进
```

## 核心架构

### 三层渐进分析（Multi-Pass Progressive Disclosure）

| 层级 | 名称 | 做什么 | 涉及阶段 |
|------|------|--------|----------|
| **L0 鸟瞰** | Architecture Scan | 文件树 + 框架检测 + 规模评估 | R0 |
| **L1 结构** | Structural Extract | AST → 知识图谱（确定性） | R1 + R2 第一轮 |
| **L2 语义** | Semantic Inference | LLM 推断业务意图（论述+选择） | R2 第二轮 |

### 知识图谱中间层（Ontology Schema）

参考 Palantir Foundry 的 Object Types + Properties + Link Types：

- **Object Types**：module, model, field, view, menu_item, security_rule, method
- **Link Types**：depends_on, defines, has_field, inherits_from, references, triggers, constrains, computes

> [!IMPORTANT]
> 知识图谱是**确定性提取**的产物（不依赖 LLM），存储在 `knowledge-graph.yaml` 中，作为后续 LLM 推理的上下文基础（GraphRAG 模式）。

### 论述+选择模式

对于业务意图（WHY），AI 不标注「未知」：
```
❌ 旧模式：AI 提取 WHAT → 标注「意图未知」→ 人从零填写
✅ 新模式：AI 提取 WHAT → AI 论述多种可能的 WHY → 人选择/修正/补充
```

## 逆向准确度

| 层级 | 准确度 | 来源 | V1→V2 变化 |
|------|--------|------|-----------|
| 模块元数据 | 100% | `__manifest__.py` 直接提取 | 不变 |
| 数据模型 + 字段 | 100% | 知识图谱（AST 解析） | ↑ 从 LLM 读代码改为确定性 KG |
| 视图结构 | 100% | XML 解析 | 不变 |
| 安全规则 | 100% | CSV/XML 解析 | 不变 |
| 计算逻辑 / 业务规则 | ~85-90% | LLM + KG 上下文（GraphRAG） | ↑ 有 KG 上下文辅助 |
| 业务需求（WHY） | ~60-70% | 论述+选择 | ↑ 从 0% 提升到有假设 |

## 框架适配器

通用流程 + 框架特化插件设计：

| 框架 | 状态 | 检测条件 |
|------|------|----------|
| Odoo 17 | ✅ 已实现 | `__manifest__.py` 存在 |
| Django | 📋 待实现 | `manage.py + settings.py` |
| Next.js | 📋 待实现 | `next.config.* + pages/` |
| 通用模式 | ✅ 已实现 | fallback |

## 增量演进机制

与 V1 保持一致。Onboard 完成后进入增量模式：

- `slices/`：逆向还原的原有功能切片
- `changes/`：后续新增的功能变更，需 `proposal.yaml` 影响分析

## 过程沉淀

V2 新增：逆向过程自身的记录沉淀

| 产出 | 内容 | 价值 |
|------|------|------|
| `reasoning-trace.yaml` | AI 推理链记录 | 可追溯、可审计 |
| `decision-log.yaml` | 用户选择决策 | 知识沉淀 |
| `qa-summary.md` | 交互记录摘要 | 经验复用 |

## 后续行动

- [ ] 实际执行一次完整 Onboard → 验证 V2 流程
- [ ] 添加 Django 框架适配器
- [ ] 添加 Next.js 框架适配器
- [ ] 知识图谱可视化（Mermaid 架构图自动生成）
- [ ] 论述+选择模式的 UX 优化
- [ ] 运行时辅助分析的实际集成
