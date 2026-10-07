# 回归协议

将改稿版本与上一次会诊记录比较。如果该记录不可用，请求用户提供，或运行 `COMPREHENSIVE` 会诊；绝不要假装知道既往决策。

## 回归记录

填充固定的 `regression` 契约：

- `prior_consultation`：绑定既往会诊 ID、既往剧本版本、既往源文本哈希、必需问题 ID/优先级/状态快照，以及字符串值的创作锁快照。改稿复审之外为 null。
- `required_issue_ids`：精确复制 `prior_consultation.required_issues` 的 ID。每个快照问题都必须存在于当前问题列表中，且优先级不变。
- `checked_issue_ids`：包含每个已检查历史问题，包括仍保持 `accepted` 的问题。
- `issue_results`：为每个必需且已检查 ID 创建且只创建一个结果。三个 ID 集合必须相同、唯一且完整覆盖。
- `creative_lock_checks`：为每个顶层创作锁键创建且只创建一个检查，不得有未知或重复 `lock_item`；只有当创作锁为空时才使用空数组。
- `escalated_dispute_ids`：精确列出有意升级到聚焦会诊的未解决争议。
- `final_result`：设置且只设置一个改稿复审结果。

当前 `script.parent_version` 必须等于快照剧本版本，当前 `script_version` 必须不同于该快照版本，当前会诊 ID 必须不同于快照会诊 ID。改稿复审之外，所有回归数组为空，`prior_consultation` 和 `final_result` 为 null。

对每个已接受问题，记录：

- `issue_id` 和非空 `accepted_decision`。
- 每个结果都要有非空 `reviewed_locations` 和 `comparison_evidence`。
- 根据下方证据规则记录实际 `changed_locations` 和 `change_evidence`。
- 机器观察：`FIXED`、`PARTIALLY_FIXED`、`UNFIXED` 或 `REGRESSED`。
- 使用问题生命周期状态枚举记录 `prior_status` 和 `status_after`。`prior_status` 是本次复审前的生命周期尾项；校验器会审计其在 `status_history` 中最后一次出现后的精确后缀。
- 独立 `verification_evidence`；没有独立验证时为 null。
- `linked_new_issue_id`，通常为 null。

观察结果是对比结论；它不是问题生命周期状态，也不自动断言本次复审改动了文本。即使是仅验证复审，`reviewed_locations` 和 `comparison_evidence` 仍然必填。

应用以下变更证据规则：

- `UNFIXED` 始终使用空 `changed_locations` 和 null `change_evidence`。
- 由既往 `accepted`、`partially_fixed` 或 `regressed` 得到的 `FIXED` 需要非空变更位置和变更证据。
- 由既往 `fixed` 或 `closed` 得到的 `FIXED` 可以仅验证，使用空变更位置和 null 变更证据。如果本次复审又做了变更，则两个字段都要提供。
- `PARTIALLY_FIXED` 和 `REGRESSED` 需要两个变更字段；例外是既往 `closed` 问题若仅凭对比发现旧修复失效，可以使用空/null，但仍必须链接下方要求的新问题。
- 绝不要只提供一个变更字段。每个变更位置都必须出现在 `reviewed_locations` 中，任何非空 `changed_locations` 都要求当前源文本哈希不同于既往源文本哈希。

## 观察到状态的转换

| 既往生命周期状态 | `FIXED` | `PARTIALLY_FIXED` | `UNFIXED` | `REGRESSED` |
| --- | --- | --- | --- | --- |
| `accepted` | 设为 `fixed`。如果同次复审也有独立验证证据，则可随后设为 `closed`。 | 保持 `accepted`。 | 保持 `accepted`。 | 保持 `accepted`；如果回归形成新问题，创建 `NEW-SC-NNN` 问题。 |
| `fixed` | 有独立验证证据时设为 `closed`；否则保持 `fixed`。 | 设为 `partially_fixed`。 | 设为 `regressed`。 | 设为 `regressed`。 |
| `partially_fixed` | 设为 `fixed`；有独立验证证据时可随后设为 `closed`。 | 保持 `partially_fixed`。 | 保持 `partially_fixed`。 | 设为 `regressed`。 |
| `regressed` | 设为 `fixed`。 | 保持 `regressed`。 | 保持 `regressed`。 | 保持 `regressed`。 |
| `closed` | 带验证保持 `closed`。 | 保持 `closed` 并链接新问题。 | 保持 `closed` 并链接新问题。 | 保持 `closed` 并链接新问题。 |

对既往 `regressed` 得到的任何非 `FIXED` 观察，保持 `regressed`；如果新的修复方向需要用户接受，则在后续修复工作前合法追加 `accepted`。

每次状态更新都必须遵循既有合法转换。当状态不变时，不要向 `status_history` 追加重复值。绝不要改写早先历史。

只有原文回归证据可以支持 `fixed`、`partially_fixed`、`regressed` 或 `closed`。`closed` 需要非空独立 `verification_evidence`。同一次复审中的 `accepted` → `fixed` → `closed` 序列，必须在 `change_evidence` 中记录文本变更，并在 `verification_evidence` 中记录单独关闭检查；同一段落不能默默同时代替两种检查。无论结果状态如何，都要把所有已检查历史 ID 加入 `regression.checked_issue_ids`。

绝不要重开已关闭的历史问题。`closed` + `FIXED` 后续检查保持问题 closed，不追加历史后缀，链接为 null；它可以是仅验证。任何其他观察都保持它 closed，并必须链接到一个不同的现有 `NEW-SC-NNN` 问题，用于表示新观察到的失效，无论本次复审是否改动文本。所有非 closed 的既往状态都要求链接为 null。

## 创作锁与新问题

独立检查每个创作锁条目并记录：

- `PRESERVED`：引用证据证明锁定值保持完好。
- `APPROVED_CHANGE`：引用证据，并记录非空 `approval_reference`、`old_value`、`new_value` 和 `effective_version`。
- `VIOLATED`：引用未经批准的冲突。

对 `PRESERVED`，当前值必须等于快照。对 `APPROVED_CHANGE`，`old_value` 等于快照值，`new_value` 等于当前值，`effective_version` 等于当前剧本版本；保留旧锁和批准审计。非批准结果可以让四个批准字段为 null。

为每个新问题创建 `NEW-SC-NNN`。当证据支持因果关系时，将其链接到引入它的改动。任何新 P0 或 P1 都会阻止 `PASS`。

## 最终结果决策树

校验器推导 `final_result`；报告不得自行选择或降级。按以下顺序评估，并在第一个匹配分支停止：

1. `REVISION_REQUIRED`：任一必需 P0/P1 观察不是 `FIXED`，存在任一 `NEW-SC-NNN` P0/P1，或任一锁结果为 `VIOLATED`。
2. `FOCUSED_REVIEW_REQUIRED`：分支 1 不适用，且存在升级争议、必需 P2/P3 观察不是 `FIXED`、任一结果停在 `fixed` 等待关闭验证，或存在任一 `NEW-SC-NNN` P2/P3。
3. `PASS`：前两个分支均不适用。

已确认的实质性 `NEW-SC-NNN` P0/P1 总是走分支 1，绝不走分支 2。只返回一个 `final_result`。

改稿复审不是重新对整部剧本做泛化审查。它必须检查改动影响半径，并发现由改稿造成或暴露的 `NEW-SC-NNN` 问题。
