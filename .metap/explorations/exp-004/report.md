# exp-004: Explore 与 Deliberate 的组合模式

## 元数据
```yaml
id: exp-004
direction: "explore 和 deliberate 是否应该结合使用"
status: concluded
started_date: "2026-03-15"
scouts: 3
```

## 核心发现

### 发现 1：认知科学——「双钻石」模型（confidence: 0.9）

**Explore = 发散思维（Divergent）, Deliberate = 收敛思维（Convergent）**

英国设计委员会的 Double Diamond 模型精确描述了这种组合：

```
   发散          收敛          发散          收敛
    ◇              ◇              ◇              ◇
  /    \         /    \         /    \         /    \
 / 发现  \      / 定义  \      / 发展  \      / 交付  \
/________\    /________\    /________\    /________\
 Discover      Define       Develop       Deliver
 (explore)   (deliberate)  (explore)   (deliberate)
```

**关键洞察**：发散和收敛必须**交替进行**，不是一次发散到底再一次收敛。每个阶段都是一个 explore→deliberate 的小循环。

### 发现 2：AI 领域——Post-Research Debate 模式（confidence: 0.85）

多篇论文（NeurIPS 2024、ACL 2025）验证了一个模式：

```
独立探索（多 Agent 并行搜索）
    ↓
结构化辩论（Agent 之间交叉质疑）
    ↓
共识提炼
```

**效果数据**：
- 多 Agent 辩论 vs 单 Agent 思考链：数学推理准确率 +15-23%
- 辩论后的 hallucination 率显著下降
- 关键原因：**独立探索保证信息多样性，辩论保证结论可靠性**

### 发现 3：AISEP 已有的组合机制（confidence: 1.0）

`explore.md` 第 157-163 行已定义自动触发规则：

```yaml
# 当 Step 4 发现以下情况时，自动建议发起 /deliberate：
- 核心发现的 confidence < 0.5
- Scout 之间存在显著矛盾
- 行动建议涉及高风险（risk > medium）
```

**问题**：这只是**单向触发**（explore → deliberate），缺少：
- 反向路径（deliberate → explore）
- 组合模式（explore + deliberate 作为一个原子操作）
- 迭代循环（多轮 explore↔deliberate 直到 confidence 达标）

### 发现 4：CrewAI 等框架的实现模式（confidence: 0.75）

多 Agent 编排框架（CrewAI、AutoGen）普遍采用的模式：
- **Advocate-Critic-Judge** 三角色辩论
- **Research Planner → Source Finder → Reviewer → Synthesizer** 流水线
- 辩论不是替代探索，而是探索的**质量保证层**

## 综合分析

### 交叉验证

| 结论 | Scout-A (认知科学) | Scout-B (AI 研究) | Scout-C (AISEP 现状) | 置信度 |
|------|---|---|---|---|
| 应该组合使用 | ✅ 双钻石模型 | ✅ post-debate 提升准确率 | ✅ 已有触发规则 | **高** |
| 应该是迭代的 | ✅ 交替发散/收敛 | ✅ multi-round debate | ⚠️ 当前是单向 | **高** |
| 需要自动编排 | — | ✅ orchestrator pattern | ⚠️ 当前需手动触发 | **中** |

### 矛盾点

**无显著矛盾**。三个 Scout 的发现高度一致：explore 和 deliberate 就像吸气和呼气——天然成对。

## 行动建议

### prop-007: 新增 `/deepdive` 组合命令（P1 · ~20m · 2 files · mid）

**理由**：将 explore + deliberate 封装为一个原子操作，用户说一句话就触发完整的「发散→收敛」循环。

```
/deep-dive 线上拍卖竞价引擎技术方案
    ↓
Phase 1: /explore（多 Scout 并行搜索）→ 报告
    ↓ 自动判断
Phase 2: /deliberate（对探索发现辩论）→ 共识 + 修正
    ↓ 自动判断
Phase 3: 如 confidence 仍 < 0.7 → 再次 /explore（补充搜索）
    ↓
最终报告：探索 + 辩论 + 行动建议
```

**风险**：低——是现有两个命令的编排，不改底层

### prop-008: 增强 explore↔deliberate 双向触发（P2 · ~10m · 2 files · low）

**理由**：当前只有 explore→deliberate 的单向触发。补充 deliberate→explore 的反向路径。

```yaml
# deliberate.md 新增触发规则
auto_trigger_explore:
  - condition: "辩论中发现信息盲区（所有角色都缺少数据支撑）"
    action: suggest_explore
  - condition: "分歧点 > 共识点 且无法收敛"
    action: suggest_targeted_explore  # 针对分歧点定向探索
```

### prop-009: 记到 backlog，暂不实现（P3）

**理由**：当前 AISEP 的 explore 和 deliberate 使用频率还不高（3 次 explore + 1 次 deliberate），先积累更多实战数据再决定组合模式是否值得工程化。
