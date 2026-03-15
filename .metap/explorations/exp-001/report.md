# 探索报告：Ontology 是否可以作为系统中间层

**探索 ID**: exp-001 | **日期**: 2026-03-15 | **状态**: concluded | **结论信心**: 78%

---

## 核心发现

### 发现 1：Ontology 作为系统中间层——可行且有成熟先例 (confidence: 88%)

Palantir Foundry 已经验证了这条路径。其 Ontology 采用三层架构：

| 层 | 职责 | 对应你的问题 |
|---|------|-------------|
| **Semantic** (名词) | 定义实体、属性、关系 | "需求沉淀到 Ontology" |
| **Kinetic** (动词) | 定义操作、数据管道、写回 | "用 Ontology 构建系统" |
| **Dynamic** (智能) | AI 推理、自动化决策、应用构建 | "管理系统" |

> 来源: [Palantir Foundry 官方文档](https://www.palantir.com/docs/foundry/ontology) (credibility: 0.9)

### 发现 2：Ontology 是描述性的，需要与规定性工具（MDD）结合 (confidence: 82%)

学术界区分了两种互补的范式：
- **Ontology (ODIS)** = 描述性 → 描述"世界是什么样"
- **Model-Driven (MDD)** = 规定性 → 规定"系统怎么建"

**对你的关键启示**：Ontology 不能独立完成"构建管理系统"。它需要一个 **生成层/执行层** 将 Ontology 定义转化为可运行的代码/UI/API。

> 来源: [academia.edu - ODIS vs MDD](https://www.academia.edu) (credibility: 0.8)

### 发现 3：从 Ontology 自动生成应用在学术上已验证 (confidence: 72%)

有研究成功从 Enterprise Ontology 自动生成 Mendix low-code 应用。但存在 **30-40% 定制化缺口**——Ontology 难以完整表达业务逻辑的边界条件和 UX 细节。

> 来源: [ResearchGate](https://www.researchgate.net) (credibility: 0.8)

### 发现 4：Semantic Layer 正在成为产业标准 (confidence: 85%)

dbt Semantic Layer (2024 GA) 是 Ontology 思想在数据工程领域的实用化。Gartner 将语义技术列为 2025 年 AI/元数据/决策智能核心。趋势：Semantic Layer 成为 LLM 与结构化数据的桥梁。

> 来源: [dbt Labs](https://www.getdbt.com/blog/semantic-layer), [Ontoforce/Gartner](https://www.ontoforce.com) (credibility: 0.8)

---

## 矛盾与不确定性

### 矛盾 1：中心化 vs 联邦化

- **Pro 中心化**：所有需求沉淀到单一 Ontology = 完美的 SSOT
- **Anti 中心化**：在大规模微服务架构中，中心化 Ontology 可能成为性能瓶颈和单点故障
- **折中方案**：联邦 Ontology（各域维护子 Ontology + 上层统一映射）

### 矛盾 2：自动生成的覆盖率上限

- 自动生成可覆盖 ~60-70% 的标准 CRUD 场景
- 剩余 30-40% 涉及业务逻辑边界条件和 UX 优化

---

## 知识空白

1. **MetaP/AISEP 自身的 Ontology 如何与"生成层"对接？**
2. **LLM 辅助 Ontology 构建的可靠性数据**
3. **联邦 Ontology 的实操经验**

---

## 新注册概念

| ID | 名称 | 成熟度 | 信心 |
|---|------|--------|------|
| concept-001 | ODIS（Ontology-Driven Information System） | growing | 82% |
| concept-002 | 三层 Ontology 架构（Semantic-Kinetic-Dynamic） | validated | 88% |
| concept-003 | Ontology→Application 自动生成 | growing | 72% |
| concept-004 | Semantic Layer 即 Ontology 的工程化落地 | validated | 85% |
| concept-005 | Ontology-as-SSOT 的三大结构性挑战 | growing | 85% |

---

## 行动建议

| # | 建议 | 优先级 | 工作量 | 风险 | 执行路径 |
|---|------|--------|--------|------|----------|
| prop-001 | **升级 MetaP Ontology 为三层架构** ✅ 已完成 | P0 | ~2d | 中 | 修改 `.metap/ontology/schema.yaml` |
| prop-002 | **构建 Ontology→Scaffold 原型** | P1 | ~3d | 中 | 创建 AISEP 项目 |
| prop-003 | **深挖联邦 Ontology + LLM 辅助构建** | P2 | ~1w | 低 | 继续 `/explore` |
