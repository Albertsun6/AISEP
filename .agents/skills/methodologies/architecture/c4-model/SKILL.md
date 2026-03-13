---
name: c4-model
description: "C4 Model — 四层架构可视化"
category: architecture
applicable_stages: [s3]

requires:
  stage: [s3]

always: false
---

# C4 Model

## 核心指令

按四层递进描述系统架构：

| 层级 | 描述 | 输出 |
|------|------|------|
| **C1 Context** | 系统与外部角色/系统的关系 | 系统上下文图 |
| **C2 Container** | 系统内部的技术容器（应用、数据库、消息队列） | 容器图 |
| **C3 Component** | 每个容器内的组件/模块 | 组件图 |
| **C4 Code** | 关键组件的类/接口设计 | 类图（仅核心聚合） |

## 执行要点

1. **C1 必做**：识别所有外部用户角色和集成系统
2. **C2 必做**：明确技术容器边界（Odoo Server / PostgreSQL / Nginx 等）
3. **C3 按需**：对复杂模块展开组件划分
4. **C4 按需**：仅对核心 Aggregate Root 展开类图

## Gate 检查清单

- [ ] C1 是否覆盖所有外部角色和系统集成？
- [ ] C2 容器边界是否清晰？通信协议是否标注？
- [ ] 模块边界是否与 DDD Bounded Context 对齐？
