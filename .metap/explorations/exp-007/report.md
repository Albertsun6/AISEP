# 📊 Deep Dive 报告：进化引擎自动发现机制

> exp-007 | type: deepdive | 2026-03-15 | 3 Scout · 9 来源 · 辩论触发

## 探索发现

### 核心发现（3 Scout 交叉验证，confidence: 0.85）

| # | 发现 | 来源 | AISEP 映射 |
|---|------|------|-----------|
| F1 | **Reflexion 模式**已被验证：Act→Evaluate→Reflect→Store→Retry 提升编码正确率 11% | NeurIPS 2023 [arxiv] | Auto-Observation = Reflect + Store |
| F2 | Schön 区分 **reflection-on-action**（事后）vs **reflection-in-action**（即时）| Schön 经典著作 | 当前 = on-action；远期目标 = in-action |
| F3 | AI 应作为**认知脚手架**"外化隐性知识"，而非替代反思 | Arizona Research + ResearchGate | Auto-Observation = 外化, /evolve = 人类审视 |
| F4 | DevOps 行业标准：**"自动收集 + 人工审批"**模式（Google SRE, Blameless, Rootly） | sre.google + rootly.com | prop-013 完全吻合 |
| F5 | Zalando 用 LLM 分析大量 post-mortem **发现跨事故系统性模式** | zalando.com | /evolve 可做类似的跨 Gate 批量模式识别 |

### 知识空白（所有 Scout 共同盲区）

- **成功模式检测缺失**：现有研究和实践主要针对"故障/问题"，缺少对"正常成功流程"的经验提取
- **process-level learning**：学术界对 task-level self-correction 研究充分，但对跨任务的过程模式积累研究较少

---

## 辩论结论

**议题**：Auto-Observation 的自治程度——AI 应静默记录一切，还是应有选择性？

| 角色 | 最终立场 |
|------|---------|
| 🟢 倡导者 | 坚持当前设计，接受 3 个补充改进 |
| 🔴 质疑者 | 0 致命风险 · 2 可管理风险（噪声堆积 + 检测质量）· 1 已解决（成功模式） |
| 🟡 务实者 | 推荐 MVP：先加"观察合并"到 evolve.md（~5min） |
| 🔵 远见者 | 长期价值确认：Auto-Observation 是系统从"工具"到"学习型系统"的转折点 |

**共识**（4/4 + Devil's Advocate 验证通过）：prop-013 方向和已落地改动有效。

**Devil's Advocate 提出的系统性偏差风险**：LLM 可能系统性忽略某类模式 → 缓解措施：
- /evolve 时展示检测维度分布
- 定期校准（obs 采纳率作为反馈信号）
- nudge_mode 切到 inline 作为质量审计期

---

## 行动建议

| # | 级别 | 提案 | 工作量 | 风险 | 状态 |
|---|------|------|--------|------|------|
| prop-013 | L3 | Auto-Observation 重构（已执行） | 已完成 | 低 | ✅ applied |
| prop-014 | L3 | evolve.md 加"观察合并"规则 | ~5m · 1 file | 低 | ⏳ 待批准 |
| prop-015 | L3 | evolution.yaml 加第5维"成功模式"检测 | ~3m · 1 file | 低 | ⏳ 待批准 |
