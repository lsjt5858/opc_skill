# 报告模板

## 正式争议与不确定性通则

诊断专家可以提交 candidate `uncertainty note`；主代理负责聚合、去重、写入报告正文，并判断补证后是否升级为正式争议。剧本总监只接收已经正式开启的争议，或 `REVISION_REVIEW` 中既有正式未决争议；不接收尚未正式开启的候选分歧，也不负责报告普通 note。

最终开启检查必须在分配 `dispute_id` 和写入 `disputes[]` 之前完成。每个选项必须有具体方案（proposal）、原文 `anchor`（raw-text anchor）、`evidence` 与 `evidence_type`、收益、`fix_cost`、单独的物料制作成本和风险；至少存在一项能区分选项优劣的已核验 `TEXT`，或有明确文本依据的 `INFERENCE`，并能对故事目标、观众信息、因果公平、情绪效果、创作锁或物料制作成本之一形成比较。`UNKNOWN` 可以记录缺口，但不得作为区分选项优劣或选中方案的唯一证据。未通过检查就降回报告正文 `uncertainty note`，不创建机器争议。

## 全面会诊

必须按以下精确顺序输出：

1. **一句话判断：** 说明当前稿件的戏剧状态和最高杠杆风险。
2. **会诊记录：** 说明 `COMPREHENSIVE`、深度、实际使用的专家、剧本版本、源文本范围和明确假设。
3. **剧本画像与核心承诺：** 识别格式、平台、类型、预期观众体验、戏剧问题和核心承诺。
4. **受保护优点与创作锁：** 列出有证据支撑且需要保留的优点，以及锁定的主题、观众体验、标志性反转、人物特质、核心物件和已验证场景。
5. **健康表：** 对每个健康维度展示分数或 `N/A`、证据、权重和权重理由；只有评分量表允许时才包含总分。
6. **情绪曲线：** 展示相关节拍、主导情绪、强度、触发因素、新信息、活跃观众问题和进入下一节拍的推动力。
7. **P0/P1 问题看板：** 展示 P0 和 P1 的完整问题卡。P2 和 P3 放入附录，除非用户要求放在主看板中。
8. **根因图：** 用 `parent_issue` 将症状链接到因果问题；父问题修复必须排在子问题复评之前，并保持图无环。
9. **重大争议与剧本总监裁决：** 只记录通过最终开启检查的正式争议，以及剧本总监从已提交选项中作出的唯一专家层建议、依据和所有主要未选方案的拒绝理由。每个 `disputes[]` 记录必须有同一 `dispute_id` 的完整 `decisions[]`，否则不能交付机器记录；剧本总监不得再以证据不足或选项不可比回避裁决。未通过检查的候选分歧不得称为正式未决争议；紧接本节以 **不确定性/待补材料** 列出主代理聚合、去重后的 `uncertainty note`，包含精确问题、已检查证据、缺失材料或约束和下一步，且不分配 `dispute_id`，不写入 `disputes[]` 或 `decisions[]`。
10. **有序修改路线图：** 按依赖和杠杆排序已接受或待决策的修复；说明范围、文字 `fix_cost`、预期效果、风险和单独的物料制作成本。
11. **用户决策：** 请用户接受、拒绝、搁置、重启争议，或请求三个真正替代方案。改写授权需单独记录。

裁决与授权边界：所有模式中，证据充分、选项可比较且达到重大争议阈值时，剧本总监仅从已提交选项中选择一个，写入同一 `dispute_id` 的 `decisions[]`，并给出依据和所有主要未选方案的拒绝理由；不得投票或强行折中。报告以诊断和用户决策为止，没有用户明确授权时不要改写任何源文本；剧本总监不得代用户接受、拒绝或搁置，只有用户可以接受、拒绝、搁置、重启争议或授权改写。无重大争议时，`disputes[]` 和 `decisions[]` 为空数组。

## 聚焦会诊

将模式声明为 `FOCUSED`。报告聚焦问题、所选专家、必要上下文和源文本范围、相关问题卡、重大争议、剧本总监裁决和局部修复选项。每个问题都必须绑定证据，并使用与全面会诊相同的正式开启门槛、机器记录配对、**不确定性/待补材料**、用户决策和改写授权边界。未通过最终开启检查的候选分歧只由主代理聚合为 `uncertainty note`，不分配 `dispute_id`，不创建正式 `disputes[]` 或 `decisions[]`；材料补齐并重新通过检查后才正式开启。一旦写入 `disputes[]`，必须生成同一 `dispute_id` 的完整 `decisions[]` 才能交付。如果答案会改变全局故事方向，停止并升级为 `COMPREHENSIVE`。

## 改稿复审

将模式声明为 `REVISION_REVIEW`。不要重复泛化梗概。将 `prior_consultation` 绑定到上一次会诊 ID、剧本版本、源文本哈希、必需问题快照和创作锁快照。当前 `parent_version` 必须指向该既往剧本版本，当前 `script_version` 必须与其不同。严格根据快照构建 `required_issue_ids`；每个必需问题必须仍然存在、优先级相同，并有一个 `prior_status` 与快照匹配的结果。

将机器观察结果与问题生命周期状态分开。观察结果只能使用 `FIXED`、`PARTIALLY_FIXED`、`UNFIXED` 或 `REGRESSED`；这些值不是问题状态。展示两列：

| 问题 | 已接受决策 | 已复审位置 | 已变更位置 | 对比证据 | 变更证据 | 观察结果 | 既往生命周期状态 | 当前生命周期状态 | 验证证据 | 关联新问题 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SC-NNN` | 用户批准方向 | 每个已检查位置 | 实际变更位置或空 | 原文对比 | 变更证据或 null | 观察枚举 | 快照状态 | 当前 schema 状态 | 独立证据或 null | `NEW-SC-NNN` 或 null |

应用回归协议中的生命周期转换表。特别注意，`UNFIXED` 是观察结果，不是状态；既往状态为 `accepted` 的未修复问题仍保持 `accepted`。当状态不变时，不要追加重复历史条目。

观察结果是对比结论，不自动声称本次复审改动了文本。始终引用非空 `reviewed_locations` 和 `comparison_evidence`。`UNFIXED` 使用空 `changed_locations` 和 null `change_evidence`。由既往 `accepted`、`partially_fixed` 或 `regressed` 得到的 `FIXED` 需要两个变更字段。由既往 `fixed` 或 `closed` 得到的 `FIXED` 可以仅验证，变更字段为空/null。`PARTIALLY_FIXED` 和 `REGRESSED` 需要变更字段，除非仅凭对比发现既往 `closed` 修复失效，且结果链接到新问题。绝不要只提供一个变更字段。每个变更位置都必须被复审，任何声称有变更的结果都要求当前源文本哈希不同于快照哈希。

将每个创作锁快照条目独立检查为 `PRESERVED`、`APPROVED_CHANGE` 或 `VIOLATED`。被保留的值必须完全相同。对已批准变更，将 `old_value` 绑定到快照，`new_value` 绑定到当前锁，`effective_version` 绑定到当前剧本版本；保留旧锁和批准审计。为新问题创建 `NEW-SC-NNN` 问题卡。

如果既往 `closed` 问题仍保持修复，则保持 closed 并验证。若它再次失效，保持历史问题 closed，并把结果链接到现有 `NEW-SC-NNN` 问题。

`REVISION_REVIEW` 中新出现且未通过开启检查的候选冲突与首诊相同：只由主代理聚合为报告正文 `uncertainty note`，不分配 `dispute_id`，不写入 `disputes[]`，也不写入 `regression.escalated_dispute_ids`。新冲突通过检查后可以正式开启，并由剧本总监从已提交选项中裁决；写入 `disputes[]` 后必须有同一 `dispute_id` 的完整 `decisions[]` 才能交付。

只有 prior/current 已经正式存在且仍未裁决的争议，才可以保留在 `disputes[]` 而不生成虚假的 `decisions[]`。在 `regression.escalated_dispute_ids` 中精确列出每个此类既有正式未决争议的 `dispute_id`；该集合必须精确等于既有正式未决争议，已裁决争议和新出现但未通过检查的候选冲突都不得列入。将这些既有争议路由到后续 `FOCUSED` 会诊补证；剧本总监可以指出仍缺少的证据、材料或约束，但不得强选。

校验器会根据结构化证据推导唯一有效结果。按以下有序决策树执行，命中第一项后停止：

1. `REVISION_REQUIRED`（需要再次修改）：任一必需 P0/P1 观察不是 `FIXED`，存在任一 `NEW-SC-NNN` P0/P1，或任一创作锁结果为 `VIOLATED`。
2. `FOCUSED_REVIEW_REQUIRED`（需要聚焦会诊）：分支 1 不适用，且存在升级争议、任一必需 P2/P3 观察不是 `FIXED`、任一结果停在 `fixed` 等待关闭验证，或存在任一 `NEW-SC-NNN` P2/P3。
3. `PASS`（通过）：前两个分支均不适用。

结尾必须且只能给出一个机器结果及其人类可读标签。`NEW-SC-NNN` P0/P1 总是选择分支 1，绝不选择分支 2。

## 问题卡

```text
[issue_id] [priority] [status] [category]
location: <具体位置>
anchor: <原文锚点>
evidence: <基于源文本的证据>
evidence_type: <TEXT | INFERENCE | UNKNOWN>
problem: <具体失效>
impact: <戏剧或观众后果>
root_cause: <因果诊断>
recommendation: <可执行修复方向>
expected_effect: <可测试的预期结果>
risk: <修改风险>
scope: <LINE | BEAT | SCENE | EPISODE | ARC | GLOBAL>
fix_cost: <S | M | L | XL>
confidence: <high | medium | low>
confidence_reason: <置信理由>
parent_issue: <issue_id 或 null>
status_history: <以 detected 开始的合法历史>
```

如果问题卡缺少精确位置、原文锚点、证据、具体影响或可执行建议，就驳回。`fix_cost` 是文字修改跨度，不是物料制作成本。
