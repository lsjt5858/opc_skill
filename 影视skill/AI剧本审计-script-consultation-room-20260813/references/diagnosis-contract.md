# 诊断契约

## 证据类型

- `TEXT`：供应稿件中明确出现的对白、动作、场景内容或信息。
- `INFERENCE`：对文本的合理解读。措辞必须带有“不确定性标记”，例如“可能”“暗示”“也许意味着”，并说明文本依据。
- `UNKNOWN`：供应稿件既不能支持也不能排除该主张。

绝不要把 `INFERENCE` 或 `UNKNOWN` 表述成 `TEXT`。`UNKNOWN` 不免除证据要求：必须引用已检查的段落或明确源文本范围，并说明具体还有什么无法支持。

## 必填问题字段

每个问题必须包含 `issue_id`、`priority`、`category`、`status`、`location`、`anchor`、`evidence`、`evidence_type`、`problem`、`impact`、`root_cause`、`recommendation`、`expected_effect`、`risk`、`scope`、`fix_cost`、`confidence`、`confidence_reason` 和 `status_history`。`parent_issue` 可选。

如果问题缺少具体位置、缺少稿件证据、只陈述泛化影响，或没有可执行建议，就驳回该问题。当稿件没有可靠时间码或场号时，分配临时场景或节拍 ID，并包含原文锚点。绝不要估算或声称精确时间。

## 优先级

- `P0`：破坏核心因果、动机、主钩子、高潮或结尾，并实质性损害成片。
- `P1`：显著损害理解、留存、共情、张力或人物可信度。
- `P2`：在资源允许时提升完成度、精确度或视听执行。
- `P3`：偏好级润色项。默认保持不变并建议搁置；只有用户可以将其设为 `deferred` 或提升优先级。

## 范围与成本

必须且只能使用一个范围：`LINE`、`BEAT`、`SCENE`、`EPISODE`、`ARC` 或 `GLOBAL`。

必须且只能使用一个 `fix_cost`：`S` 表示一两行，`M` 表示一个场景，`L` 表示多个场景，`XL` 表示结构性工作。

`fix_cost` 衡量文字修改跨度。物料制作成本要单独评估；绝不要把制作成本编码或表述为 `fix_cost`。

## 状态

必须且只能使用一个状态：`detected`、`verified`、`disputed`、`accepted`、`rejected`、`deferred`、`fixed`、`partially_fixed`、`regressed` 或 `closed`。`status_history` 必须以 `detected` 开始；`status` 必须等于最后一项；每个相邻转换必须遵循此列表：

- `detected` → `verified`、`rejected` 或 `deferred`
- `verified` → `disputed`、`accepted`、`rejected` 或 `deferred`
- `disputed` → `accepted`、`rejected` 或 `deferred`
- `accepted` → `fixed` 或 `deferred`
- `fixed` → `partially_fixed`、`regressed` 或 `closed`
- `partially_fixed` → `fixed`、`regressed` 或 `deferred`
- `regressed` → `accepted`、`fixed` 或 `deferred`
- `deferred` → `accepted` 或 `rejected`
- `rejected` 和 `closed` 是终态

只有用户可以把问题设为 `accepted`、`rejected` 或 `deferred` 并授权改写。用户接受不代表问题已 `fixed`；只有改稿后的源文本验证才能确立该状态。只有已修复问题通过回归复审后，才能使用 `closed`。`rejected` 和 `deferred` 问题不得进入改写。

凡 `status` 为 `fixed`、`partially_fixed`、`regressed` 或 `closed` 的问题，其 `issue_id` 必须出现在 `regression.checked_issue_ids` 中。`regression.checked_issue_ids` 中的每个 ID 必须指向现有问题，且数组不得有重复项。

## 根因

用 `parent_issue` 将症状链接到其因果问题。先修父问题，再在编辑子问题前重新评估每个子问题。根因图不得包含循环。

## 创作锁

创作锁包含主题、预期观众体验、标志性反转、受保护的人物特质、核心物件和已被证明有效的场景。没有用户明确批准时，不要推荐或应用任何违反锁定元素的改动。
