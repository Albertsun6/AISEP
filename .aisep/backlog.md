# AISEP Backlog

> 新想法和待办项。按优先级排列，想到就记，定期审视。

## 🔴 高优先级

- [x] **深入讨论进化机制**：递归问题、进化系统设计（已完成：规则生命周期 + 分层审批）
- [x] 认知知识库：/tidy 时提取学习笔记（已完成：knowledge/ 目录 + schema + tidy 集成）
- [x] 实战验证：用 `/idea promote` 创建第一个项目，走 S0→S1（已完成：proj-001 制造业ERP）
- [x] 上下文归档机制：Slice 之间阶段切换时的归档策略（已完成：机制八 + pipeline 5 步归档清单）
- [x] **S8 复盘进化**：项目完成后的经验提取 + 知识沉淀 + 流程进化（workflow 已创建，proj-001 已执行）
- [x] **Project Map (`_map.yaml`)** — Gate 通过时自动生成的低 token 项目概览（类似 Aider Repo Map）（已完成：proj-001 首个实例生成）
- [x] **context_fence 排除规则** — 在 AISEP.md 中声明非活跃项目的排除目录，防止上下文污染（已完成：AISEP.md 区块 + 机制七注册）

## 🟡 中优先级

- [ ] 制品摘要化的具体规则（`_summary_rules.yaml`）
- [ ] `capabilities.md` 动态生成的具体实现逻辑
- [x] 自进化 L2 知识沉淀到 `~/.aisep/skills/` 的具体流程（已完成：两条路径 + Readiness 评估 + 5 步晋升协议）
- [x] 补充 optional 方法论 SKILL.md：`moscow`、`given-when-then`、`design-patterns`、`tdd`、`bdd`
- [ ] 补充 Gate 验证器：`crud-matrix`、`process-coverage`
- [ ] 每次项目结束的经验分层沉淀机制（L2→L1→L0）
- [x] **registry 冷热分区** — 归档项目迁移到 `registry-archive.yaml`，保持主注册表轻量（已完成：冷热分区结构 + archive/ 目录）
- [x] **Skills `_summary.yaml`** — 框架知识 auto-generated 摘要索引，避免知识库膨胀（已完成：odoo17/_summary.yaml）
- [x] **知识库倒排索引** — `.aisep/knowledge/index.yaml` 增加 `by_tag` / `by_framework` 倒排索引（已完成：4 个维度）

## 🟢 低优先级 / 远期

- [ ] 项目类型按需加载模板（Profile 机制，后期讨论）
- [ ] 技能市场（install/share 机制）
- [ ] 多 Agent 并行化（Slice 间并行执行）
- [ ] 数据驱动需求发现流程
- [ ] `proposal.yaml` 的 schema 验证规则
- [ ] `changes/` 与 `slices/` 混合模式下的依赖管理
- [ ] **静态 HTML 报告生成** — Gate 通过时自动生成 project-dashboard.html（参考 allure-report）
- [ ] **VS Code Extension** — 侧栏展示项目列表/Gate 时间线/一键 pipeline 按钮
- [ ] **Continue Context Provider 融合** — 研究其声明式上下文注册架构，作为 AISEP VS Code Extension 技术底座
- [x] **GitHub 代码管理集成** — 项目代码的版本控制（已完成：Git 初始化 + GitHub private 仓库 + /tidy Git 同步步骤）

## Changelog

| 日期 | 变更 |
|------|------|
| 2026-03-12 | 初始构建：50+ 文件（入口 + 配置 + 脚手架 + 11 Skills + 13 Workflows + 规范） |
| 2026-03-12 | ACES → AISEP 全局改名 |
| 2026-03-12 | 创建 system-guide.md + backlog.md + /tidy workflow |
| 2026-03-12 | 交互进化 6 条规则（evo-001 ~ evo-006） |
| 2026-03-12 | 进化机制深化：规则生命周期 + 分层审批 + 认知知识库 |
| 2026-03-12 | S1-S7 Workflow 充实为可执行级（311→1178 行）+ 9 个制品 Schema（1234 行）+ Odoo17 知识库充实（153→802 行）|
| 2026-03-12 | S0/Pipeline/Idea/Project/Onboard 5 个管理级 Workflow 充实为可执行级（168→1099 行，+554%）|
| 2026-03-12 | 补充 5 个 optional 方法论 Skill（moscow/gwt/design-patterns/tdd/bdd），方法论总数 11→16 |
| 2026-03-12 | S1 Gate 通过：domain-model.yaml + capability-map.yaml + glossary.yaml（24 术语）|
| 2026-03-12 | S2 Gate 通过：functional.yaml（40 stories）+ slice-plan.yaml（7 slices, MVP=1-5）|
| 2026-03-12 | S3 Gate 通过：architecture.yaml（4 模块/12 Models/安全模型/Docker 部署）+ ADR-001/002 |
| 2026-03-12 | S4+S5 SLICE-01 完成：sale_mfg 模块（10 文件，delivery_status + qty_positive） |
| 2026-03-12 | S4+S5 SLICE-02 完成：stock_mfg 模块（8 文件，全标准复用零自定义） |
| 2026-03-12 | S4+S5 SLICE-03 完成：purchase_mfg 模块（10 文件，receipt_status + qty/price 约束） |
| 2026-03-12 | S4+S5 SLICE-04 完成：mrp_mfg 模块（12 文件，BOM state 生命周期 + qty_variance + action_confirm 校验） |
| 2026-03-12 | Docker 部署验证通过：Odoo 17 + PG 16，mrp_mfg 模块零错误安装，浏览器功能测试通过 |
| 2026-03-13 | S5 SLICE-05 完成：生产执行（领料+报工+执行详情）+ Odoo 17 P1-05 兼容修复 + 浏览器自动验收 |
| 2026-03-13 | S5 SLICE-06 完成：MRP 生产建议向导（TransientModel）+ sale 依赖 |
| 2026-03-13 | S5 SLICE-07 完成：调拨/盘点/价目表菜单快捷入口 |
| 2026-03-13 | E2E 端到端演示通过：销售→MRP建议→生产→库存完整闭环 |
| 2026-03-13 | 创建 deployment-guide.md + gate-log 追加 Slice 4-7 |
| 2026-03-13 | 创建 S8-Retrospective workflow（项目复盘进化阶段）|
| 2026-03-13 | 架构探讨：用户呈现形式（混合增强方案）+ 上下文体积控制（四个方案）|
| 2026-03-13 | /tidy 升级 11→14 步：新增上下文审计 + 话题偏移评估 + 会话交接清单 |
| 2026-03-13 | context-loading-protocol.md 新增机制六：审计闭环流程图 + 进化路径 |
| 2026-03-13 | architecture.md 注册 3 个新文件（_map.yaml / _context_audit.yaml / _next_session.yaml）|
| 2026-03-13 | 新增 backlog 项：Project Map、context_fence、registry 冷热分区、Skills 摘要、知识库倒排索引、静态报告、GitHub 集成 |
| 2026-03-13 | 落地 3 个高优先级方案：Project Map(_map.yaml) + context_fence(AISEP.md) + registry 冷热分区(archive/) |
| 2026-03-13 | 落地 2 个中优先级方案：Skills _summary.yaml(odoo17) + 知识库倒排索引(4维度) |
| 2026-03-13 | 落地上下文归档机制（机制八）：阶段/Slice 过渡归档协议 + pipeline 5 步归档清单 |
| 2026-03-13 | 🔴 高优先级 backlog 全部清零（8/8 完成） |
| 2026-03-13 | Git 版本管理建立：.gitignore + Git 初始化 + GitHub 远程仓库(Albertsun6/AISEP) + /tidy Step 15 版本同步 |
