---
description: 帮助 — 显示所有可用命令（/help 或 /? 均可触发）
---

# /help — 命令速查

> 触发：`/help` 或 `/?`

收到此命令时，输出以下命令表：

```
📋 AISEP 命令速查

Pipeline 执行
  /pipeline              执行当前项目 pipeline（自动路由到当前阶段）
  /s0 ~ /s8              直接进入指定阶段
  /back                  回退一步（/back s0 回退到指定阶段）
  /onboard               逆向接管现有模块

项目管理
  /idea add|list|refine|promote|archive    想法管理
  /project list|switch|status|archive      项目管理

探索与博弈
  /explore <方向>         多 Scout 并行探索
  /deliberate <议题>      4 角色 3 轮辩论
  /deepdive <方向>        explore + deliberate 一步到位
  /approve prop-XXX      批准行动建议
  /reject prop-XXX       拒绝行动建议

系统维护
  /tidy                  对话收尾整理
  /evolve                触发自进化分析
  /help 或 /?            显示本命令表

用户快捷词
  深挖 / 拉远 / 总结 / 转向 / 全做 / 验收 / 进化 / 状态
```

同时附加当前项目状态快照（读取 registry.yaml + project.yaml）。
