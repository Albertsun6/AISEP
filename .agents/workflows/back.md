---
description: 回退 — 将当前项目 pipeline 回退一步或到指定阶段
---

# /back — Pipeline 回退

> 触发：`/back` 或 `/back <stage>`
> 详细逻辑见 `pipeline.md` 中「主动回退」章节

## 语法

```
/back          → 回退一步（如 S1 → S0）
/back s0       → 回退到指定阶段
```

## 执行流程

1. 读取 `project.yaml` → `current_stage`
2. 确定目标：无参 → 前一阶段 | 有参 → 指定阶段
3. ⚠️ 确认回退（展示影响范围）
4. 更新 `project.yaml` + `registry.yaml` + `gate-log.yaml`
5. 输出：「⏪ 已回退到 {target_stage}。输入 /pipeline 继续」
