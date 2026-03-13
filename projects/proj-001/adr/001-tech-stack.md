# ADR-001: 技术栈选择 — Odoo 17 Community Edition

## 状态

已接受

## 上下文

制造业ERP (proj-001) 需要支持生产管理、采购管理、库存管理、销售管理四大模块。
项目约束：AI 辅助开发、无专职开发团队、中小型制造企业场景。

需要选择一个能快速实现 ERP 功能的技术方案。

### 备选方案

| 方案 | 优势 | 劣势 |
|------|------|------|
| **Odoo 17 CE** | 内置 MRP/Sales/Purchase/Inventory 标准模块；Python 生态；继承扩展机制成熟 | 学习曲线；Community 版无企业级功能 |
| **ERPNext** | 开源免费；UI 现代 | 制造模块功能弱于 Odoo；Frappe 框架生态较小 |
| **从零构建 (Django/FastAPI)** | 完全自主控制 | 开发周期极长；需构建所有基础设施 |

## 决策

选择 **Odoo 17 Community Edition** 作为技术栈。

## 理由

1. **内置领域模块** — Odoo 的 `mrp`、`sale`、`purchase`、`stock` 标准模块覆盖 80%+ 需求，无需从零构建
2. **继承扩展** — 通过 `_inherit` 在标准行业功能基础上做定制，开发量最小
3. **AI 友好** — Odoo 的声明式 View（XML）+ Model（Python）模式结构化程度高，适合 AI 生成
4. **社区生态** — 17.0 版本有活跃的社区和丰富的文档
5. **部署成熟** — 官方 Docker 镜像，开箱即用

## 影响

- **正面**：开发周期缩短 60%+；标准模块经过充分测试
- **负面**：受限于 Odoo ORM 和架构约束；Community 版无工作流引擎（Studio）
- **风险**：Odoo 版本升级时继承模块可能需要适配
- **约束**：所有后续代码须遵循 Odoo 模块规范（`__manifest__.py`、ACL、XML ID 规范）

## 关联

- Pipeline 阶段：S3
- 相关制品：`architecture.yaml`
- 相关 ADR：ADR-002（模块策略）
