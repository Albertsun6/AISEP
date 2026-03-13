# AISEP — AI-Integrated Software Engineering Process

> 系统导航入口。AI 在每次交互开始时首先读取此文件。
> 📖 **人类用户请看** [系统指南](.aisep/docs/system-guide.md) — 一站式了解全局

## 当前活跃项目

<!-- 由 /project switch 命令自动更新 -->
```yaml
active_project: "proj-002"    # 拍卖模块
```

## 上下文围栏（Context Fence）

<!-- 由 /project switch 和 /project archive 命令自动更新 -->
```yaml
context_fence:
  active: "proj-002"
  excluded_dirs:
    - "projects/proj-001/**"    # 已归档
  cross_project_allowed:
    - ".aisep/knowledge/**"       # 认知知识库始终可访问
    - ".aisep/evolution/**"       # 进化数据始终可访问
    - ".aisep/docs/**"            # 系统文档始终可访问
```

> **解析规则**：`excluded_dirs` 中的路径即使被 AI 请求也**不加载**（硬排除）。`cross_project_allowed` 是白名单例外。`/project switch` 时自动将旧项目加入 excluded，`/project archive` 时永久加入。

## 系统文件索引

### 始终加载（L0 常驻层）

| 文件 | 职责 |
|------|------|
| `AISEP.md`（本文件） | 系统导航 + 当前活跃项目 |
| `constitution.md` | 全局铁律（不可违反） |
| 活跃项目的 `glossary.yaml` | 术语一致性 |

### 按需加载

| 路径 | 内容 | 加载条件 |
|------|------|---------|
| `.aisep/config.yaml` | 全局配置 | 需要 pipeline 信息时 |
| `.aisep/ideas.yaml` | 想法池 | `/idea` 命令时 |
| `.aisep/registry.yaml` | 项目注册表 | `/project` 命令时 |
| `.agents/workflows/` | 工作流定义 | 进入具体阶段时 |
| `.agents/skills/` | 方法论 + 框架知识 | 经 Gating 过滤后加载 |

### 设计文档

详见 [implementation_plan.md](.aisep/docs/implementation_plan.md) 中的文档索引。

## 命令速查

```
# 想法管理
/idea add <描述>          记录想法
/idea list                列出所有想法
/idea refine <id>         AI 辅助分析
/idea promote <id>        提升为项目 → S0
/idea archive <id>        归档

# 项目管理
/project list             列出所有项目
/project switch <id>      切换活跃项目
/project status           查看进度
/project status --full    聚合视图
/project archive <id>     归档项目

# Pipeline 执行
/pipeline                 执行当前项目 pipeline
/s0-init ~ /s8-retrospective 直接进入指定阶段
/onboard --source <path>  逆向接管现有模块

# 系统维护
/tidy                     对话窗口收尾整理
/evolve                   触发自进化分析
```

## 上下文加载协议

此系统实施三层上下文预算控制（详见 [context-loading-protocol.md](.aisep/docs/context-loading-protocol.md)）：
- **L0 常驻层**：< 2K tokens（本文件 + constitution + glossary）
- **L1 阶段层**：< 5K tokens（当前 Workflow + Skills）
- **L2 按需层**：单次请求 < 3K tokens
