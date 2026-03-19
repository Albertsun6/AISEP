# MetaP — AISEP 元认知协作层

> **版本**: 0.2.0 (Phase 2)
> **角色**: AISEP 的"大脑皮层"——负责思考、探索、辩论和自进化
> **关系**: MetaP 不替代 AISEP，而是在其之上提供方向探索和知识积累

## 与 AISEP 的关系

```
用户
 ↓ 探索方向
MetaP (思考层)   ←→  Ontology (语义中间层: Semantic → Kinetic → Dynamic)
 ↓ 行动建议
AISEP (执行层)   ←→  Pipeline S0-S8 + Gates
 ↓ 项目产出
MetaP (反馈回路) ←   经验提炼回 Ontology
```

## 系统文件索引

### L0: 立即加载
- `MetaP.md` — 本文件（入口）
- `constitution.md` — 共享铁律（§1-16）

### L1: 按需加载
- `.metap/config.yaml` — 全局配置（v0.2.0）
- `.metap/ontology/schema.yaml` — 三层 Ontology（Semantic + Kinetic + Dynamic）

### L2: 深度加载
- `.metap/engines/exploration.yaml` — 探索引擎（多 Scout 并行）
- `.metap/engines/deliberation.yaml` — 博弈引擎（4 角色 3 轮）
- `.metap/engines/autonomy.yaml` — 自治引擎（信任积分 + 三维评估）
- `.metap/engines/evolution.yaml` — 进化引擎（**已委托给底层 AIEC OS 处理**）
- `.metap/engines/memory.yaml` — 记忆引擎（工作/事件/语义三级）
- `.metap/state/trust.yaml` — 当前信任积分

### L3: 知识库
- `.metap/ontology/concepts/` — 语义记忆（Concept 实例 = 通用知识）
- `.metap/memory/episodes/` — 事件记忆（Episode 实例 = 具体经验）
- `.metap/explorations/` — 历史探索记录
- `.metap/evolution/` — 进化观察和不可变审计日志

## 命令速查

| 命令 | 功能 | 引擎 | 自治级别 |
|------|------|------|---------|
| `/explore <方向>` | 多 Scout 并行探索，生成报告和建议 | 探索 + 本体 | 搜索 L2 / 建议 L1 |
| `/deliberate <议题>` | 4 角色 3 轮结构化辩论 | 博弈 + 本体 | 辩论 L3 / 结论 L1 |
| `/deliberate --on exp-XXX` | 对探索发现发起辩论 | 博弈 + 探索 | 同上 |
| `/approve prop-XXX` | 批准行动建议 | 自治 | L0 |
| `/reject prop-XXX: 理由` | 拒绝行动建议 | 自治 | L0 |
| `/tidy` | 记忆流转 + 索引同步 + 信任更新 | 记忆 + 进化 | 记录 L3 / 提升 L1 |
| `/evolve` | 触发自进化分析 | 进化 | 观察 L3 / 变更 L0 |

## 三层 Ontology 架构

| 层 | 职责 | 内容 |
|---|------|------|
| **Semantic** 📐 | 描述"是什么" | 5 Object Type: Concept / Source / Exploration / ActionProposal / Project |
| **Kinetic** ⚡ | 定义"能做什么" | 11 Action: concept.refine / proposal.approve / aisep.create_project / ... |
| **Dynamic** 🧠 | 实现"如何智能" | 4 推理规则 + 2 Agent 接口 + 5 自动化触发器 + Scaffold 预留 |

## 信任积分

当前积分：`见 .metap/state/trust.yaml`
级别阈值：L0(0) → L1(1.0) → L2(3.0) → L3(6.0) → L4(10.0)

## 上下文加载协议

1. **对话起始**：L0 自动加载（MetaP.md + constitution.md）
2. **用户输入 /explore**：加载 L1（config）+ L2（exploration.yaml）
3. **用户输入 /deliberate**：加载 L1（config）+ L2（deliberation.yaml）
4. **需要知识引用**：按需加载 L3 的特定 Concept/Episode
5. **上下文紧张时**：压缩 L3，保留 L0+L1
