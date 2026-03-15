---
description: "AISEP Pipeline 主编排器 — 按阶段推进项目"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
  load:
    - ".aisep/config.yaml"
    - ".aisep/registry.yaml"
  exclude:
    - ".aisep/docs/**"
    - ".aisep/templates/**"
---

# Pipeline 编排

## 启动检查

**AI 执行指引**：

1. 读取 `registry.yaml` → 获取 `active_project`
2. 如 `active_project == null` → 提示：「当前无活跃项目。请先用 `/idea promote <id>` 创建项目，或用 `/project switch <id>` 切换」→ **中止**
3. 读取 `projects/{active_project}/project.yaml` → 获取 `pipeline_state`
4. 如文件不存在 → 提示：「项目 {id} 的 project.yaml 缺失，项目可能未正确初始化」→ **中止**
5. 读取 `pipeline_state.current_stage` → 确定当前应执行的阶段

### 异常状态恢复

| 状态 | 处理 |
|------|------|
| `current_stage` 的当前阶段 status = `"in_progress"` | 正常 — 继续执行该阶段 |
| `current_stage` 的当前阶段 status = `"rejected"` | 恢复模式 — 告知用户上次 Gate 被拒绝的原因（从 `gate-log.yaml`），询问是否重新执行 |
| `current_stage` 的当前阶段 status = `"completed"` 且 `gate_passed = true` | 自动推进到下一阶段 |
| 所有 S0-S7 status = `"completed"` | 项目已完成 — 展示恭喜信息 + 概览 |

---

## 执行流程

### 步骤 1: 状态快照

**AI 执行指引**：
进入阶段前，输出状态快照：

```
📊 项目: {project.name}
📍 当前阶段: {current_stage} — {stage_name}
✅ 已完成: S0, S1, ...
⏳ 当前: {current_stage}
⏹️ 待执行: ...
```

### 步骤 2: 上下文加载

**AI 执行指引**（严格遵循 context-loading-protocol.md）：

1. **L0 常驻层**（自动加载）：
   - `AISEP.md` — 系统导航
   - `constitution.md` — 全局铁律
   - `glossary.yaml` — 术语一致性

2. **L1 阶段层**（按当前阶段加载）：
   - 读取当前阶段 Workflow 的 `context.load` frontmatter → 加载指定文件
   - 读取 `config.yaml` 中该阶段的 `methodologies.required` → 加载对应 Skill
   - **Gating 规则**：`methodologies.optional` 的 Skill **不自动加载**，仅在 AI 判断需要或用户要求时加载
   - **框架知识 Gating**：仅当 `project.yaml.tech_stack` 非空且匹配时，才加载 `skills/frameworks/{tech_stack}/SKILL.md`

3. **L2 按需层**（执行中按需加载）：
   - 历史制品摘要（`.summary.yaml` 优先于原始文件）
   - 其他 Slice 的摘要（当前 Slice 加载原始文件，其他 Slice 仅加载摘要）

**预算检查**：
- L0: ≤ 2K tokens
- L1: ≤ 5K tokens
- L2: 单次请求 ≤ 3K tokens
- 总软限: ≤ 10K tokens

### 步骤 3: 执行阶段 Workflow

**AI 执行指引**：
1. 加载当前阶段的 Workflow 文件（如 `.agents/workflows/s1-domain.md`）
2. 严格按照 Workflow 中定义的**步骤**执行
3. 在 Workflow 的每个**交互节点 (🗣️)** 处暂停等待用户确认
4. 按 Workflow 的**输出**节要求生成制品

### 步骤 4: Gate 审查

**AI 执行指引**：
1. 读取当前阶段 Workflow 的 **Gate 检查清单**
2. AI 自检每个清单项，标注是否满足
3. 展示自检结果给用户：

```
🚪 Gate 审查 — {stage_name}

✅ [规则 1]
✅ [规则 2]
⚠️ [规则 3] — [不满足原因]
❌ [规则 4] — [不满足原因]

总结：N/M 项通过 | 需处理 K 项
```

4. **用户决定**（constitution 第 1 条——所有 Gate 必须经人确认）：
   - **通过** → 步骤 5
   - **修正** → 回到步骤 3，按修正意见调整制品
   - **拒绝** → 记录原因，标记 status = `"rejected"`，询问回退目标

### 步骤 5: Gate 通过处理

**AI 执行指引**：
Gate 通过后执行以下 **4 个自动动作**（无需人工确认）：

#### 5a. 状态更新
```yaml
# 更新 project.yaml
pipeline_state:
  stages:
    {current_stage}:
      status: "completed"
      gate_passed: true
      completed_at: "{timestamp}"
  current_stage: "{next_stage}"    # 推进到下一阶段
```

#### 5b. Compaction（摘要生成）
为本阶段产出的每个制品生成摘要：
- 文件名：`{artifact}.summary.yaml`
- 摘要内容：保留结构骨架 + 关键决策 + 统计数字，去除详细描述
- 摘要行数：≤ 30 行
- 放在制品同目录下

#### 5c. Gate 日志
```yaml
# 追加到 history/gate-log.yaml
- stage: "{current_stage}"
  action: "passed"
  timestamp: "{timestamp}"
  artifacts_produced:
    - "{artifact_path}"
  notes: "{用户确认时的备注（如有）}"
```

#### 5d. 推进
- 更新 `current_stage` 到下一阶段
- 输出推进信息：「✅ {stage_name} Gate 通过。推进到 {next_stage_name}」
- 自动加载下一阶段的 Workflow（回到步骤 2）

#### 5e. Project Map 更新
- 读取/创建 `projects/{id}/_map.yaml`
- 根据本次 Gate 通过的阶段，更新对应区段：
  - S0-S3 Gate → 更新 `map.stage` + `map.modules`（如适用）
  - S4-S6 Gate → 更新 `map.slices` 完成度
  - S8 Gate → 更新 `map.knowledge`
- 同步 `map.gates.total` / `map.gates.passed` 计数
- **设计原则**：`_map.yaml` 是低 token 骨架（< 500 tokens），只保留结构和关键 ID，不复制制品详情

---

## S4-S6 Slice 循环

S4-S6 阶段按 **逐 Slice 迭代**执行：

### 循环编排

```
读取 slice-plan.yaml → 获取 Slice 列表和优先级

for each slice in prioritized_slices:
    显示: "📦 Slice {n}/{total}: {slice.name}"

    S4: 加载 slice 上下文 → 执行设计 → Gate
    S5: 加载 slice 设计 → 执行实现 → Gate
    S6: 加载 slice 实现 → 执行测试 → Gate

    标记 slice.status = "completed"
    生成 slice 级摘要

推进到 S7
```

### Slice 上下文隔离与归档（关键）

- **当前 Slice**：加载完整制品（`artifacts/slices/{current_slice}/`）
- **其他 Slice**：仅加载摘要（`.summary.yaml`），**不加载原始制品**
- **Slice 完成归档清单**（Slice N 的 S6 Gate 通过后执行）：

  1. **Compaction**：生成 `slices/slice-N/` 下的 `design.summary.yaml`（代码和测试文件保留但不加载）
  2. **上下文卸载**：从 L1 阶段层移除 Slice N 的完整制品
  3. **_map.yaml 同步**：更新 `map.slices.completed` 计数和对应 Slice 状态
  4. **上下文加载**：将 Slice N+1 的完整制品加载到 L1（历史 Slice 仅通过 `.summary.yaml` 可访问）
  5. **进度展示**：输出更新后的 Slice 进度条

> [!NOTE]
> 归档 ≠ 删除。已归档 Slice 的完整制品仍在磁盘上，AI 通过 L2 按需层显式请求时可回溯完整版。

### Slice 进度展示

每个 Slice 完成后展示进度：

```
📊 Slice 进度
[████████░░░░] 3/5 Slices 完成

✅ slice-01: 用户管理        (S4✓ S5✓ S6✓)
✅ slice-02: 物料管理        (S4✓ S5✓ S6✓)
✅ slice-03: 采购订单        (S4✓ S5✓ S6✓)
⏳ slice-04: 生产工单        (S4⏳)
⏹️ slice-05: 库存管理
```

---

## Gate 修正与拒绝处理

### Gate 修正流程

1. 记录修正原因到 `gate-log.yaml`（action: `"revision"`）
2. 保留用户的修正意见
3. 回到当前阶段的 Workflow，按修正意见调整制品
4. 调整后重新触发 Gate 审查
5. **进化植入（Auto · 修正模式检测）**：
   - 每次 revision 后，扫描 `gate-log.yaml` 中所有 revision 记录
   - 如果**同类修正累计 ≥ 2 次**（按 stage 或 修正原因关键词分组），自动提醒：
     ```
     ⚡ 进化提醒：{stage_name} 已被修正 N 次，共同原因是 "{pattern}"。
     建议：将此经验沉淀为 Skill 或更新 Workflow 步骤指引。
     → /approve 执行沉淀 | /reject 跳过（记录到 observations）
     ```
   - 如果无重复模式 → 不触发，无感通过

### Gate 拒绝流程

1. 记录拒绝原因到 `gate-log.yaml`（action: `"rejected"`）
2. 标记 `stages.{current_stage}.status = "rejected"`
3. 询问用户希望回退到哪个阶段：

```
当前阶段 {stage_name} Gate 被拒绝。
请选择：
  1. 重做本阶段 → 清空本阶段制品，重新执行
  2. 回退到 {prev_stage} → 重新执行上一阶段及后续
  3. 暂停 → 保留现状，下次 /pipeline 继续
```

4. 执行用户选择的动作

---

## 主动回退：`/back`

> 用于**已通过 Gate 后**主动回退到之前的阶段重做。
> 独立命令入口：`.agents/workflows/back.md`

### 语法

```
/back          → 回退一步（如 S1 → S0）
/back <stage>  → 回退到指定阶段（如 /back s0）
```

### 执行流程

**AI 执行指引**：

1. **确定目标阶段**：
   - 无参数 → `target = previous_stage(current_stage)`
   - 有参数 → `target = <stage>`
   - 如果 target 阶段 status ≠ `"completed"` → 拒绝：「该阶段还未完成过，无法回退」

2. **确认回退**（⚠️ 人类检查点）：
   ```
   ⚠️ 回退确认
   当前: {current_stage}
   目标: {target_stage}
   影响: {target} 到 {current} 之间的制品将保留但标记为 stale
   
   确认回退？(y/n)
   ```

3. **执行回退**：
   ```yaml
   # 更新 project.yaml
   pipeline_state:
     current_stage: "{target_stage}"
     stages:
       {target_stage}: { status: "in_progress", gate_passed: false }
       # target 之后的阶段状态不变（保留 completed，方便对比）
   ```

4. **gate-log 记录**：
   ```yaml
   - stage: "{target_stage}"
     action: "rollback"
     timestamp: "{timestamp}"
     from_stage: "{original_current_stage}"
     reason: "{用户说明}"
   ```

5. **registry 同步**：更新 `current_stage`

### 制品处理

- **不删除**任何制品——回退后可参考旧版本
- 重做阶段时生成的新制品会**覆盖**旧制品
- 旧版本可通过 git 历史回溯（如已提交）

---

## 异常处理

| 异常 | 处理 |
|------|------|
| 对话中断（用户离开） | 制品保存在 `artifacts/` 中，下次 `/pipeline` 从 `current_stage` 恢复 |
| AI 无法完成某步骤 | 标注 `confidence: low`，告知用户需要人工补充 |
| 制品不符合 Schema | 告知用户具体违规项，尝试自动修复，修复失败则请用户协助 |
| 上下文超出预算 | 触发额外 Compaction，将低优先级制品替换为摘要 |
