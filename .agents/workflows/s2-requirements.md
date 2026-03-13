---
description: "S2 需求规格 + Slice 规划"
context:
  always:
    - "AISEP.md"
    - "constitution.md"
    - "glossary.yaml"
  load:
    - "artifacts/global/domain-model.yaml"
    - "artifacts/global/capability-map.yaml"
    - "artifacts/global/gap-analysis.yaml"
    - ".aisep/templates/artifacts/s2-functional.tmpl.yaml"
  exclude:
    - "history/**"
    - "artifacts/slices/**"
    - "artifacts/changes/**"
---

# S2: 需求规格 + Slice 规划

## 前置条件

- S1 Gate 已通过（`pipeline_state.stages.s1.gate_passed == true`）
- `domain-model.yaml` 和 `capability-map.yaml` 存在
- `glossary.yaml` 已填充核心术语

## 输入

- `domain-model.yaml`（S1 输出）— 限界上下文、聚合、实体
- `capability-map.yaml`（S1 输出）— 业务能力树
- `gap-analysis.yaml`（如有）— Baseline/Target/Gap

## 加载方法论

- **必须**：User Story Mapping（`.agents/skills/methodologies/requirements/user-story-mapping/SKILL.md`）
- **必须**：INVEST（`.agents/skills/methodologies/requirements/invest/SKILL.md`）
- **可选**：MoSCoW, Given-When-Then

---

## 活动

### 步骤 1: 领域模型 → Story Map 转化

**AI 执行指引**：
1. 从 `capability-map.yaml` 的 L1 能力节点提取**用户活动**（Story Map 的 Backbone）
2. 从 L2/L3 能力节点提取**用户任务**（Story Map 的 Walking Skeleton）
3. 每个任务下展开为具体 User Stories

**交互节点**：
- 🗣️ 先展示 Story Map 的 Backbone（核心活动列表），用户确认后再展开

### 步骤 2: Story 编写 + INVEST 校验

**AI 执行指引**：
1. 按模块逐个编写 User Story，格式：`As a <角色>, I want <目标>, so that <价值>`
2. 每个 Story 附加验收标准（AC），推荐 Given-When-Then 格式
3. 每个 Story 自查 INVEST 6 要素：
   - **I**ndependent — 与其他 Story 可独立交付？
   - **N**egotiable — 可与用户协商范围？
   - **V**aluable — 对用户/业务有直接价值？
   - **E**stimable — 能估算工作量？
   - **S**mall — 300-800 行代码可实现？
   - **T**estable — 验收标准可测试？

**交互节点**：
- 🗣️ 按模块分批展示（每批 5-8 个 Story），用户逐批确认
- 用户可能补充 AI 遗漏的异常流程（"如果数量为负呢？""审批被拒怎么办？"）

**异常处理**：
- Story 不满足 INVEST → 拆分或合并，标注原因
- 发现领域模型缺失 → 建议回退 S1 补充（需用户确认）

### 步骤 3: MoSCoW 优先级排序

**AI 执行指引**：
1. AI 提出初步优先级建议 + 理由
2. 用户确认或调整
3. 检查 Must 比例：**Must 不应超过 60%**（超过则与用户讨论降级）

**交互节点**：
- 🗣️ 展示优先级分布饼图/表格 → 用户确认

### 步骤 4: Slice 划分

**AI 执行指引**：
1. 按 Story Map 水平切分，每层 = 一个 Slice
2. 每个 Slice 的粒度标准：
   - **1-3 个 Model** + 完整的 Views + Security + Tests
   - **300-800 行代码**
   - **一个可独立演示的业务场景**
3. 确定 Slice 间依赖关系（拓扑序）

**Slice 1 选择决策指引**：
- ✅ 选最核心 + 依赖最少的功能（能独立运行）
- ✅ 选能快速验证技术栈可行性的功能
- ❌ 不选依赖其他 Slice 的功能作为 Slice 1

**交互节点**：
- 🗣️ 展示 Slice 划分方案（表格：Slice → Models → Stories → 估算行数 → 依赖）
- 用户可调整粒度和顺序

### 步骤 5: CRUD 覆盖矩阵验证

**AI 执行指引**：
1. 对每个 Model，检查是否有 Create / Read / Update / Delete 对应的 Story
2. 生成 CRUD 矩阵表格
3. 缺失项标记为 ⚠️，AI 提出补充建议

```
          | Create | Read | Update | Delete |
BOM       |  US-01 | US-02|  US-03 |   ⚠️   |
BOM Line  |  US-01 | US-02|  US-03 |  US-04 |
...
```

**异常处理**：
- 发现遗漏的 CRUD → 补充 Story 或明确标注为 Won't（需用户确认）

### 步骤 6: 最终整合

**AI 执行指引**：
1. 整合所有 Story 到 `functional.yaml`
2. 整合 Slice 划分到 `slice-plan.yaml`
3. 更新 `glossary.yaml`（如有新术语）

---

## 输出

- `artifacts/global/functional.yaml`（必须）— 按 `s2-functional.tmpl.yaml` 格式
- `artifacts/global/slice-plan.yaml`（必须）— 含 Slice 列表、依赖图、估算
- 更新 `glossary.yaml`

## Gate 检查清单

### Story 质量
- [ ] 所有 Story 是否通过 INVEST 6 要素检查？
- [ ] 每个 Story 是否有 ≥ 1 条验收标准（AC）？
- [ ] MoSCoW 分布是否合理？（Must ≤ 60%）
- [ ] 异常流程是否覆盖？（不只是 Happy Path）

### Slice 质量
- [ ] 每个 Slice 是否满足粒度标准？（1-3 models, 300-800 行）
- [ ] Slice 1 是否可独立运行？
- [ ] Slice 间依赖关系是否清晰？无环形依赖？
- [ ] 依赖拓扑序是否确定？

### 完整性
- [ ] CRUD 覆盖矩阵是否完整？遗漏项是否有处理策略？
- [ ] 所有 Model 是否至少有 Read Story？
- [ ] `glossary.yaml` 是否与新增术语同步？

## Gate 通过后

1. **Compaction**：生成 `functional.summary.yaml`（保留 Story 数量、每模块覆盖度、MoSCoW 分布）
2. **状态更新**：`pipeline_state.stages.s2.status = "completed"`, `gate_passed = true`
3. **推进**：`current_stage` → `s3-architecture`
4. **Gate 日志**：追加记录到 `history/gate-log.yaml`
