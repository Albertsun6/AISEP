---
description: "S7 部署配置"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
  load:
    - "artifacts/global/architecture.yaml"
  load_summary:
    - "artifacts/global/slice-plan.yaml"
  exclude:
    - "history/**"
    - "artifacts/slices/**/code/**"
    - "changes/**"
---

# S7: 部署配置

> [!IMPORTANT]
> S7 在所有 Slice 的 S6 Gate 通过后执行。这是整个 Pipeline 的最终阶段。

## 前置条件

- 所有 Slice 的 S6 Gate 均已通过
- 所有模块代码已通过测试
- `architecture.yaml` 中的部署方案已定义（S3）

## 输入

- `architecture.yaml`（部署方案 + 模块列表）
- 所有 Slice 的代码（聚合使用）
- Framework Skill（部署相关知识）

## 加载方法论

- **必须**：Twelve-Factor App（`.agents/skills/methodologies/deployment/twelve-factor/SKILL.md`）

---

## 活动

### 步骤 1: Twelve-Factor 逐条检查

**AI 执行指引**：
逐条对照 12 Factor 原则，确认项目合规：

| # | Factor | 检查内容 |
|---|--------|---------|
| I | 基准代码 | 一份代码 → 多份部署（dev/staging/prod） |
| II | 依赖 | 显式声明（requirements.txt / manifest depends） |
| III | 配置 | 环境变量存储（无硬编码密码/Key） |
| IV | 后端服务 | 数据库等作为附加资源对待 |
| V | 构建/发布/运行 | 严格分离（build → release → run） |
| VI | 进程 | 无状态进程（session 不存本地） |
| VII | 端口绑定 | 通过端口暴露服务 |
| VIII | 并发 | 可水平扩展 |
| IX | 快速启动/优雅终止 | 容器快速启停 |
| X | 环境等价 | dev ≈ staging ≈ prod |
| XI | 日志 | 写入 stdout，由平台收集 |
| XII | 管理进程 | 一次性任务（数据迁移、初始化）独立脚本 |

### 步骤 2: 生成 Docker 配置

**AI 执行指引**：
1. `Dockerfile`：
   - 基于 Framework 官方镜像（Odoo: `odoo:17.0`）
   - COPY 自定义模块到 `extra-addons`
   - 设置正确的文件权限
2. `docker-compose.yml`：
   - Odoo 服务 + PostgreSQL 服务
   - Volume 映射（数据持久化）
   - 环境变量引用（`.env` 文件）
   - 端口映射

### 步骤 3: 生成环境配置

**AI 执行指引**：
1. `.env.example`：列出所有需要的环境变量（含注释说明）
2. `odoo.conf`（或等效配置）：
   - 数据库连接信息（引用环境变量）
   - `addons_path` 包含自定义模块路径
   - Workers / 内存限制 / 日志级别

**安全检查**：
- ❌ `.env` 不入版本管理（确保 `.gitignore` 包含 `.env`）
- ✅ `.env.example` 入版本管理（无真实密码）

### 步骤 4: 生成初始化脚本

**AI 执行指引**：
1. 数据库初始化命令
2. 模块安装命令（按依赖拓扑序安装所有自定义模块）
3. 管理员密码修改提示

### 步骤 5: 最终集成验证

**AI 执行指引**：
1. 在 Docker 环境中验证所有模块同时安装无冲突
2. 验证跨 Slice 的功能交互（如不同 Slice 的 Model 引用是否正常）
3. 验证安全规则在真实环境中的行为

**交互节点**：
- 🗣️ 提供完整的启动命令序列，提示用户执行：
  ```bash
  cp .env.example .env
  # 编辑 .env 填入真实配置
  docker-compose up -d
  docker-compose exec web odoo -u all_custom_modules -d mydb
  ```
- 🗣️ 用户验证：登录 → 检查所有模块菜单可见 → 执行关键操作

### 步骤 6: 编写部署文档

**AI 执行指引**：
生成 `README.md` 或 `DEPLOY.md`，包含：
1. 系统要求（Docker 版本、内存、磁盘）
2. 快速启动步骤（5 步以内）
3. 环境变量说明
4. 数据库备份/恢复方法
5. 常见问题排查

---

## 输出

- `artifacts/global/deployment.yaml`（部署配置元数据）
- 部署文件（直接写入项目根目录或指定位置）：
  - `Dockerfile`
  - `docker-compose.yml`
  - `.env.example`
  - `odoo.conf`（或等效配置）
  - `scripts/init.sh`（初始化脚本）
  - `DEPLOY.md`（部署文档）

## Gate 检查清单

### Twelve-Factor 合规
- [ ] 所有配置是否通过环境变量管理？（Factor III）
- [ ] `.env` 是否在 `.gitignore` 中？（Factor III）
- [ ] 进程是否无状态？（Factor VI）
- [ ] 日志是否写入 stdout？（Factor XI）

### Docker 配置
- [ ] Dockerfile 是否基于官方镜像？
- [ ] docker-compose 是否包含所有必要服务？
- [ ] Volume 是否正确映射？（数据持久化）
- [ ] 端口映射是否正确？

### 安全
- [ ] 无硬编码密码/API Key？（constitution 第 6 条）
- [ ] 默认管理员密码是否有修改提示？
- [ ] 数据库访问是否有网络隔离？

### 集成
- [ ] 所有模块是否可同时安装？
- [ ] 跨 Slice 功能是否正常交互？
- [ ] 部署文档是否完整可用？

## Gate 通过后

1. **状态更新**：`pipeline_state.stages.s7.status = "completed"`, `gate_passed = true`
2. **项目状态**：项目标记为 `completed`（或 `deployed`）
3. **Gate 日志**：追加最终记录
4. **Compaction**：为整个项目生成 project-overview（只读快照）
5. **🎉 Pipeline 完成**：通知用户，提供后续选项：
   - 进入增量演进模式（使用 `changes/`）
   - 归档项目（`/project archive`）
   - 开始新项目
