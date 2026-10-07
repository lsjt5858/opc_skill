# 争议协议

## 先判定候选分歧是否可正式开启

不要先分配 `dispute_id` 或写入机器数组。主代理必须逐项检查候选分歧同时满足以下条件，才可正式开启：

- 选择会改变故事方向、观众认知、人物含义、情绪回报或物料制作成本，达到重大争议阈值。
- 每个选项都已提交具体方案（proposal）、原文 `anchor`（raw-text anchor）、`evidence` 与 `evidence_type`、收益、`fix_cost`、单独的物料制作成本和风险。
- 至少存在一项能区分选项优劣的已核验 `TEXT`，或有明确文本依据的 `INFERENCE`，并能对故事目标、观众信息、因果公平、情绪效果、创作锁或物料制作成本之一形成比较。
- `UNKNOWN` 可以记录证据、材料或约束缺口，但不得作为区分选项优劣或选中方案的唯一证据。
- 至少两个已提交选项通过上述检查且可以比较。

最终开启检查发生在写入 `disputes[]` 之前。任何一项未通过，都把候选分歧降回 `uncertainty note`。诊断专家可以提交 candidate `uncertainty note`；主代理负责聚合、去重、写入报告正文，并判断补证后是否重新检查并升级。不要把普通 note 交给剧本总监。

按模式处理未通过开启检查的候选分歧：

- **`COMPREHENSIVE` / `FOCUSED`：** 未通过开启检查时，不分配 `dispute_id`，不创建正式 `disputes[]` 或 `decisions[]`。主代理将其作为 `uncertainty note` 写入报告正文“不确定性/待补材料”，列出精确问题、已检查证据、缺失材料或约束和下一步；它不是 consultation schema 根字段。材料补齐并重新通过检查后才正式开启。一旦写入 `disputes[]`，必须由剧本总监生成同一 `dispute_id` 的完整 `decisions[]` 后才能交付机器记录；剧本总监不得再以证据不足或选项不可比回避裁决。
- **`REVISION_REVIEW` 新冲突：** 新出现且未通过开启检查的候选冲突与首诊相同，只由主代理聚合为报告正文 `uncertainty note`；不分配 `dispute_id`，不写入 `disputes[]`，也不写入 `regression.escalated_dispute_ids`。新冲突通过检查后可以正式开启，并必须由剧本总监裁决，生成同一 `dispute_id` 的完整 `decisions[]`。
- **`REVISION_REVIEW` 既有争议：** 只有 prior/current 已经正式存在且仍未裁决的争议，才可以保留在 `disputes[]` 而不生成虚假 `decisions[]`。每个此类 `dispute_id` 必须精确列入 `regression.escalated_dispute_ids`，并路由到后续 `FOCUSED` 会诊补证；已裁决争议不得列入。剧本总监可以指出仍缺少的证据、材料或约束，但不得强选。
- **所有模式：** 无重大争议时，`disputes[]` 和 `decisions[]` 为空数组。

剧本总监只接收已经正式开启的争议，或 `REVISION_REVIEW` 中既有正式未决争议。它不接收尚未正式开启的候选分歧，也不负责聚合、去重或报告普通 `uncertainty note`。

## 正式争议的机器映射

以下七条只适用于通过开启检查、可以裁决的正式争议，或 `REVISION_REVIEW` 中既有正式未决争议。后者若当前不能裁决，只保留既有 `disputes[]` 记录并按升级路径处理，不得为满足第 5 至 7 条而制造 `decisions[]`。除这一既有未决例外外，写入 `disputes[]` 的记录必须有同一 `dispute_id` 的完整 `decisions[]` 才能交付。

1. **`dispute_id` 与精确问题：** 向 `disputes[]` 写入一个可回答的问题。
2. **选项 A：** 向 `disputes[]` 写入具体方案，并包含原文 `anchor`、`evidence`、`evidence_type`、收益、`fix_cost`、独立物料制作成本评估和风险。
3. **选项 B：** 向 `disputes[]` 写入具体方案，并包含原文 `anchor`、`evidence`、`evidence_type`、收益、`fix_cost`、独立物料制作成本评估和风险。
4. **选项 C，仅在真实存在时：** 只有当它是具有独立机制的真正综合方案时，才写入 `disputes[]`。字段与 A、B 相同。如果不存在真正 C，在协议记录中说明，但不要创建选项 C 对象。绝不要为了回避裁决而编造折中方案。
5. **剧本总监建议：** 除 `REVISION_REVIEW` 中既有正式未决争议外，剧本总监只能从该争议已提交选项中选择一个，在同一 `dispute_id` 下把所选选项和唯一专家层裁决写入 `decisions[]`，不得以证据不足或选项不可比回避。这不是用户接受，也不是改写授权。
6. **裁决依据：** 在同一 `decisions[]` 记录中，评估故事目标、观众信息、因果公平性、情绪效果、创作锁和物料制作成本。
7. **主要拒绝理由：** 在同一 `decisions[]` 记录中，明确说明为什么所有主要未选方案被拒绝。

不要投票，也不要强行折中或选择“中间意见”。剧本总监提供唯一专家层建议和裁决，但不得把任何问题设为 `accepted`、`rejected` 或 `deferred`，不得代用户接受、拒绝或搁置，也不得触发改写。只有用户可以做出这些用户决策并授权改写。

争议没有问题式 `status`。当出现新的稿件证据、制作约束变化或用户目标变化时，在同一 `dispute_id` 下新增或更新裁决审计记录；将原建议、依据和拒绝理由作为历史保留。
