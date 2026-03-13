---
name: twelve-factor
description: "Twelve-Factor App — 现代应用部署原则"
category: deployment
applicable_stages: [s7]

requires:
  stage: [s7]

always: false
---

# Twelve-Factor App

## 核心指令

部署配置时逐项检查（选取最相关的 6 条）：

| 因子 | 要求 | 检查项 |
|------|------|--------|
| **III. Config** | 配置存环境变量 | 无硬编码密码/连接串 |
| **IV. Backing Services** | 数据库/缓存/邮件作为附加资源 | 可通过 URL 切换 |
| **VI. Processes** | 应用无状态 | Session 不存本地文件 |
| **VII. Port Binding** | 通过端口暴露服务 | 不依赖外部 Web 容器 |
| **X. Dev/Prod Parity** | 开发/生产环境一致 | 用 Docker 保证一致 |
| **XI. Logs** | 日志作为事件流 | 输出到 stdout |

## Gate 检查清单

- [ ] 所有敏感信息是否走环境变量？
- [ ] 数据库连接是否可通过环境切换？
- [ ] 是否有 Docker/docker-compose 配置？
- [ ] 日志是否输出到 stdout？
