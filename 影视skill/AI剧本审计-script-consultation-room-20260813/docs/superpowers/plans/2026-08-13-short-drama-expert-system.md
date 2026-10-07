# 短剧商业增长专家体系实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将当前泛化的七角色简介升级为“4 个核心席 + 5 个条件席 + 1 个裁决席”的专业短剧商业增长会诊体系，并保持现有机器契约兼容。

**Architecture:** 角色定义集中在 `references/expert-roles.md`，每个岗位使用统一契约描述任务授权、方法、证据、交付和越权边界。`SKILL.md` 只负责按模式和问题选择岗位，不重复角色方法论；JSON Schema 继续把实际专家名称存为字符串，因此无需迁移历史记录。

**Tech Stack:** Markdown、Python 3、JSON Schema Draft 2020-12、现有 `scripts/validate_consultation.py`

**Design Spec:** `docs/superpowers/specs/2026-08-13-short-drama-expert-system-design.md`

**Repository Note:** 当前目录不是 Git 仓库，执行时跳过 commit 步骤，不得为满足计划而自行初始化仓库。

---

### Task 1: 建立旧角色体系的行为基线

**Files:**
- Create: `docs/superpowers/baselines/2026-08-13-expert-role-baseline.md`
- Read: `references/expert-roles.md`
- Read: `references/diagnosis-contract.md`

- [ ] **Step 1: 用旧角色文件运行“无时间码开场”场景**

向独立诊断代理提供旧版 `expert-roles.md`、`diagnosis-contract.md` 和以下材料：

```text
任务：审查短剧开场留存。
已知条件：没有成片、没有时间码、没有平台数据。
原文：
【第一场 客厅 日】
林妍盯着离婚协议，门外传来钥匙声。
她把协议压进茶几抽屉，起身迎向刚进门的丈夫。
丈夫：今天怎么这么安静？

请分别以编剧、增长专家、观众代表身份输出问题。每个问题必须给出位置、原文锚点、证据类型、问题、影响和建议。
```

记录三个角色是否重复给出“钩子不足/节奏慢”，是否编造前三秒或十秒结论，观众代表是否用主观感受替代文本证据。

- [ ] **Step 2: 用旧角色文件运行“无付费模型集尾”场景**

```text
任务：判断这一集结尾能否承担付费卡点。
已知条件：项目只说明是连载短剧，没有提供免费集数、付费边界、平台或商业模式。
原文：
【第八场 医院走廊 夜】
护士把亲子鉴定递给周岚。
周岚翻到最后一页，脸色骤变。
电梯门打开，失踪三年的陈默走出来。
切黑。
```

记录旧体系是否把“切黑”直接等同于有效卡点，是否虚构付费转化效果，是否说明缺失条件。

- [ ] **Step 3: 用旧角色文件运行“高成本高潮降本”场景**

```text
任务：评估 AI 制作可行性并提出降本方向。
原文：
暴雨夜，五十辆摩托围住跨江大桥。男女主在疾驰货车顶搏斗，
无人机群坠落爆炸，桥面断裂，男主抓住女主悬在江面上。
创作锁：男女主必须共同完成一次不可逆的信任选择。
```

记录旧 AI 制片是否只罗列“群演、爆炸、复杂动作难生成”，是否提供保留“共同信任选择”戏剧功能的替代方案，是否分开文字修改成本与物料制作成本。

- [ ] **Step 4: 写入基线结果**

`docs/superpowers/baselines/2026-08-13-expert-role-baseline.md` 必须包含：

```markdown
# 旧专家体系行为基线

## 场景一：无时间码开场
- 重复结论：
- 伪精确判断：
- 无证据观众代言：

## 场景二：无付费模型集尾
- 被虚构的商业前提：
- 悬念与硬断是否区分：

## 场景三：高成本高潮降本
- 是否保留戏剧功能：
- 是否分开两类成本：

## 必须由新角色体系修复的失败
1.
2.
3.
```

预期：至少复现一项角色重复、一项缺失信息未声明，以及一项专业交付不完整。若旧体系意外全部满足，则记录真实结果，不得编造失败。

---

### Task 2: 重写专业专家角色契约

**Files:**
- Modify: `references/expert-roles.md:1-36`
- Read: `docs/superpowers/specs/2026-08-13-short-drama-expert-system-design.md`
- Read: `docs/superpowers/baselines/2026-08-13-expert-role-baseline.md`

- [ ] **Step 1: 写入全局执业规则**

文件开头必须明确：

```markdown
# 短剧商业增长会诊专家

## 共同执业规则

- 独立诊断前不得查看其他专家结论。
- 每位诊断专家最多提交五个高价值问题、三个受保护优点和一个最大不确定性。
- 每个问题必须满足诊断契约，缺少可靠时长、平台、商业模型或制作方案时使用 `INFERENCE` 或 `UNKNOWN`。
- 专家只能在岗位授权范围内诊断；发现跨岗位根因时标记移交，不得自行扩权。
- 允许没有 P0/P1，不得为显示专业而制造问题。
```

- [ ] **Step 2: 写入四个核心席**

按以下顺序写入，名称必须完全一致：

```text
短剧故事架构师
留存与信息策略师
人物关系与情绪回报编辑
场景与对白执行编辑
```

每个角色必须包含七个二级字段：

```markdown
### 任务授权
### 必须回答的问题
### 专业方法
### 证据门槛
### 标准交付件
### 禁止越权
### 交叉质询触发条件
```

内容逐项落实设计规格中的审查对象、方法和约束。尤其要明确：

- 故事架构师输出因果根节点和修复依赖，不润色对白。
- 留存与信息策略师无时间码时只用场景/节拍锚点，不使用伪秒数。
- 人物关系与情绪回报编辑区分刺激强度与挣得的情绪回报。
- 场景与对白执行编辑先检查场景状态变化，再处理台词。

- [ ] **Step 3: 写入五个条件席**

按以下顺序写入，名称必须完全一致：

```text
集尾钩子与商业转化策划
竖屏视听导演
AI 制片与可生成性监制
平台策略与内容风险顾问
逻辑连续性审计师
```

每个条件席在七字段之前增加 `### 触发条件`。必须包含以下防误判条款：

- 商业转化策划：无付费边界时不得宣称转化效果；必须区分悬念、扣留和硬断。
- 竖屏视听导演：不把镜头数量或快剪当作节奏。
- AI 制片：分别报告 `fix_cost` 与物料制作成本；降本不得破坏创作锁。
- 平台顾问：无法确认的政策判断标为 `UNKNOWN`，不把偏好包装成规则。
- 逻辑审计师：只报告可证明的连续性或信息权限问题，不把不喜欢的选择判成漏洞。

- [ ] **Step 4: 写入裁决席**

`剧本总监` 必须使用以下结构：

```markdown
## 裁决席

### 剧本总监

#### 输入
#### 裁决职责
#### 必须输出
#### 禁止事项
```

必须输出一个专家层建议、裁决依据、主要替代方案拒绝理由和修复顺序。禁止新增诊断、投票、代用户修改状态或授权改写。

- [ ] **Step 5: 运行静态结构检查**

Run:

```bash
rg -n '^## |^### |^#### ' references/expert-roles.md
```

Expected:

- 出现 4 个核心席、5 个条件席和 1 个裁决席。
- 每个诊断席都有任务授权/必须回答的问题/专业方法/证据门槛/标准交付件/禁止越权/交叉质询触发条件。
- 条件席额外具有触发条件。

---

### Task 3: 同步主技能的专家选择与降级流程

**Files:**
- Modify: `SKILL.md:53-72`
- Modify: `SKILL.md:80-90`
- Read: `references/expert-roles.md`

- [ ] **Step 1: 替换深度选择规则**

将“DEEP 全面会诊使用全部七个诊断角色”替换为：

```markdown
按模式、深度、格式、商业模型和问题选择专家：

- `LIGHT`：至少两个核心席；只运行与问题直接相关的条件席。
- `STANDARD`：四个核心席中至少三个，加必要条件席；复杂因果、反转或修改复审加入逻辑连续性审计师。
- `DEEP` 全面会诊：四个核心席全部运行；条件席根据平台、付费模型、制作方式和剧情复杂度触发。

剧本总监不计入独立诊断专家数量。不得为凑齐人数运行无关岗位，必须报告实际运行的岗位。
```

- [ ] **Step 2: 替换聚焦会诊面板**

写入以下组合：

```markdown
- **开场留存：** 留存与信息策略师、短剧故事架构师、场景与对白执行编辑；按需加入竖屏视听导演和逻辑连续性审计师。
- **集尾追更/付费卡点：** 集尾钩子与商业转化策划、留存与信息策略师、人物关系与情绪回报编辑；按需加入短剧故事架构师和平台策略与内容风险顾问。
- **爽点或情绪回报：** 人物关系与情绪回报编辑、短剧故事架构师、场景与对白执行编辑；按需加入留存与信息策略师和竖屏视听导演。
- **反转可预测或不可信：** 短剧故事架构师、逻辑连续性审计师、留存与信息策略师；按需加入人物关系与情绪回报编辑。
- **AI 制作可行性：** AI 制片与可生成性监制、竖屏视听导演、场景与对白执行编辑；按需加入逻辑连续性审计师和短剧故事架构师。
```

- [ ] **Step 3: 替换无子代理降级方案**

降级为四次隔离诊断，不得冒充真实多专家会诊：

```markdown
1. 故事与因果：短剧故事架构师。
2. 留存与商业：留存与信息策略师；有明确商业模型时加入集尾钩子与商业转化策划。
3. 人物与执行：人物关系与情绪回报编辑加场景与对白执行编辑。
4. 制作与审计：按需组合竖屏视听导演、AI 制片、平台顾问和逻辑连续性审计师。
```

- [ ] **Step 4: 同步总编剧称谓**

在 `SKILL.md` 的裁决流程中把自然语言角色名“总编剧”统一改为“剧本总监”；机器字段、`decisions[]` 结构和用户权限边界不变。

- [ ] **Step 5: 检查旧角色名是否残留**

Run:

```bash
rg -n '导演加 AI 制片|增长、编剧、观众|情绪、观众|红队|七个诊断角色|总编剧' SKILL.md references/expert-roles.md
```

Expected: no matches.

---

### Task 3b: 对齐争议未决路径与机器契约

**Files:**
- Modify: `SKILL.md`
- Modify: `references/expert-roles.md`
- Modify: `references/dispute-protocol.md`
- Modify: `references/report-template.md`
- Verify only: `scripts/validate_consultation.py`
- Verify only: `references/consultation.schema.json`

- [ ] **Step 1: 保持现有 validator 契约**

不得修改 validator 或 schema。确认：

```bash
python3 - <<'PY'
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "validator", Path("scripts/validate_consultation.py")
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
data = {
    "mode": {"user_mode": "COMPREHENSIVE"},
    "issues": [],
    "disputes": [
        {
            "dispute_id": "D-001",
            "options": [{"option_id": "A"}, {"option_id": "B"}],
        }
    ],
    "decisions": [],
    "creative_lock": {},
    "health": {"dimensions": [], "overall_score": None},
    "regression": {
        "prior_consultation": None,
        "required_issue_ids": [],
        "checked_issue_ids": [],
        "issue_results": [],
        "creative_lock_checks": [],
        "escalated_dispute_ids": [],
        "final_result": None,
    },
}
print(
    "\n".join(
        error
        for error in module.semantic_errors(data)
        if "争议" in error or "dispute" in error
    )
)
PY
```

Expected:

```text
争议未解决: D-001
```

- [ ] **Step 2: 定义模式化未决处理**

四个文档统一使用：

```text
COMPREHENSIVE / FOCUSED：
  证据不足或选项不可比 → 不创建 disputes[] / decisions[]；
  记录为专家阶段 uncertainty note，在报告正文列出待补材料；
  材料补齐后才开启正式争议。

REVISION_REVIEW：
  已存在但暂不可裁决的争议可保留在 disputes[]；
  不生成虚假 decisions[]；
  dispute_id 必须进入 regression.escalated_dispute_ids。

所有模式：
  证据充分、选项可比且达到重大争议阈值 → 创建 disputes[]，
  剧本总监必须写同 dispute_id 的唯一 decisions[] 裁决。
```

- [ ] **Step 3: 同步剧本总监称谓**

把 `references/dispute-protocol.md` 和 `references/report-template.md` 中自然语言“总编剧”统一为“剧本总监”。机器字段不变。

- [ ] **Step 4: 验证跨文件规则**

Run:

```bash
rg -n '总编剧|Head Writer' \
  SKILL.md \
  references/expert-roles.md \
  references/dispute-protocol.md \
  references/report-template.md
```

Expected: no matches.

Run:

```bash
rg -n 'COMPREHENSIVE|FOCUSED|REVISION_REVIEW|uncertainty note|escalated_dispute_ids' \
  SKILL.md \
  references/expert-roles.md \
  references/dispute-protocol.md \
  references/report-template.md
```

Expected: 四份文件中的模式化未决处理不互相冲突。

---

### Task 4: 运行新角色体系行为复测

**Files:**
- Create: `docs/superpowers/baselines/2026-08-13-expert-role-green.md`
- Read: `references/expert-roles.md`
- Read: `references/diagnosis-contract.md`
- Read: `docs/superpowers/baselines/2026-08-13-expert-role-baseline.md`

- [ ] **Step 1: 重跑无时间码开场场景**

使用 Task 1 的原文，分别运行：

```text
留存与信息策略师
短剧故事架构师
场景与对白执行编辑
```

Expected:

- 不出现未经来源支持的精确秒数。
- 三个岗位分别聚焦信息策略、因果承诺和场景执行。
- 每条问题均有位置、锚点和证据类型。

- [ ] **Step 2: 重跑无付费模型集尾场景**

运行：

```text
集尾钩子与商业转化策划
留存与信息策略师
人物关系与情绪回报编辑
```

Expected:

- 明确缺少付费边界和平台模型。
- 商业效果使用 `INFERENCE` 或 `UNKNOWN`。
- 区分“陈默出现带来的新问题”与“切黑本身”。

- [ ] **Step 3: 重跑高成本高潮降本场景**

运行：

```text
AI 制片与可生成性监制
竖屏视听导演
短剧故事架构师
```

Expected:

- AI 制片提供至少一个保留“共同信任选择”的低成本机制。
- 分开文字修改跨度和物料制作成本。
- 导演与架构师不越权代替 AI 制片估算生成难度。

- [ ] **Step 4: 写入 GREEN 结果并对照基线**

`docs/superpowers/baselines/2026-08-13-expert-role-green.md` 必须逐场景记录：

```markdown
## 观察结果
- 岗位输出是否可区分：
- 缺失条件是否显式：
- 是否存在伪精确：
- 是否保留创作锁：
- 是否出现越权：

## 与旧体系对比
- 已修复：
- 仍存在：
- 需要补强的角色条款：
```

若仍存在重复、越权或伪精确，回到 Task 2 最小化补强对应角色条款，并重新运行该失败场景。

---

### Task 5: 回归验证完整 skill 包

**Files:**
- Verify: `SKILL.md`
- Verify: `references/expert-roles.md`
- Verify: `references/consultation.schema.json`
- Verify: `scripts/stabilize_script_index.py`
- Verify: `scripts/validate_consultation.py`

- [ ] **Step 1: 检查角色名称一致性**

Run:

```bash
for role in \
  '短剧故事架构师' \
  '留存与信息策略师' \
  '人物关系与情绪回报编辑' \
  '场景与对白执行编辑' \
  '集尾钩子与商业转化策划' \
  '竖屏视听导演' \
  'AI 制片与可生成性监制' \
  '平台策略与内容风险顾问' \
  '逻辑连续性审计师' \
  '剧本总监'; do
  rg -q \"$role\" references/expert-roles.md || exit 1
done
```

Expected: exit 0.

- [ ] **Step 2: 编译现有 Python 脚本**

Run:

```bash
python3 -m py_compile scripts/stabilize_script_index.py scripts/validate_consultation.py
```

Expected: exit 0 with no output.

- [ ] **Step 3: 验证 JSON Schema 未被破坏**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator

schema = json.loads(
    Path("references/consultation.schema.json").read_text(encoding="utf-8")
)
Draft202012Validator.check_schema(schema)
print("schema valid")
PY
```

Expected:

```text
schema valid
```

- [ ] **Step 4: 运行索引脚本冒烟测试**

Run:

```bash
python3 scripts/stabilize_script_index.py <<'JSON'
{"script_id":"demo","source_text":"开场。她推门。","segments":[{"level":"scene","episode":1,"scene":1,"anchor":"开场"},{"level":"beat","episode":1,"scene":1,"beat":1,"anchor":"她推门"}]}
JSON
```

Expected: 输出包含 `"segment_id": "E001-S001"` 和 `"segment_id": "E001-S001-B001"`。

- [ ] **Step 5: 检查本次修改范围**

Run:

```bash
find . -maxdepth 4 -type f | sort
```

Expected: 除设计、计划和行为基线文档外，只修改 `SKILL.md` 与 `references/expert-roles.md`；不得修改 `consultation.schema.json` 或校验算法。
