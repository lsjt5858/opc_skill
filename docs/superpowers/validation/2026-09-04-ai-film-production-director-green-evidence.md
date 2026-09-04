# AI Film Production Director GREEN 原始证据

## 1. 固定元数据

- Workspace：`/Users/bytedance/zimeiti/opc_skill/.worktrees/ai-film-production-director`
- Branch：`feature/ai-film-production-director`
- Tested commit：`5c4b5b7`（完整 SHA：`5c4b5b7b2a4749eb9f85f5933fa96b6f171b7841`）
- Runner：最终 GREEN 回归 Agent
- Skill 入口：`skill/ai-film-production-director/SKILL.md`
- 已按路由加载：
  - `skill/ai-film-production-director/references/continuity-audit.md`
  - `skill/ai-film-production-director/references/output-batching.md`
  - `skill/ai-film-production-director/references/production-workflow.md`
  - `skill/ai-film-production-director/references/prompt-patterns.md`
  - `skill/ai-film-production-director/references/video-prompt-pack-template.md`
- 执行方法：当前 Agent 在 tested commit 上完整读取入口、全部五份 references 与 `agents/openai.yaml` 后，将下列每条输入彼此独立地重新应用当前 Skill；响应均为本次回归实际生成的完整响应或按要求保留的 Production Spec/结构摘要，不沿用未复核结论。
- 证据性质：人工场景执行与 shell 静态检查，不声称存在自动化测试框架，也未调用或伪造 Skill 专用 CLI。

## 2. 四个原始请求

### 2.1 最小资产请求

**原始输入**

> 请只为一个30岁女记者生成中性角色身份参考图提示词。没有其他项目需求。

**本次实际响应全文**

仅输出所请求的中性角色身份参考图提示词，不展开制片计划、镜头或视频提示词。

=== image prompt - C01-ID01 30岁女记者中性身份参考 v1 ===

【用途与依赖】
- 锁定角色身份；没有其他项目依赖。

【格式】
- 4:3 横向角色转面参考图，五个等宽 panel：正面全身、真侧面全身、背面全身、右前 3/4 全身、正面面部近景。

【连续性】
- 已锁定：女性、30岁、记者职业身份。
- 推断：当代日常职业装、自然妆发、无剧情状态；依据是“中性角色身份参考图”，可由用户覆盖。

【prompt】

```text
a production identity turnaround sheet for C01, a 30-year-old female journalist. 4:3 horizontal reference-sheet grid with five equal panels. the exact same individual in every panel with identical facial structure, body proportions, hairstyle, costume, and recognition features. panels show front full body, true side full body, back full body, right-front 3/4 full body, and a separate neutral front face close-up. neutral standing pose, arms relaxed with both hands visible, calm neutral expression, natural contemporary grooming, practical understated journalist workwear with no logos, plain pure white studio background, soft neutral reference lighting, even exposure, clear production-reference detail.

Constraints: no camera, no microphone, no notebook, no press badge, no bag, no handheld props, no sitting, no crying, no running, no cinematic location, no dramatic action, no pose change between orthographic views, no identity drift, no extra person, no text, no logo, no watermark.
```

【QC】
- 五个 panel 必须是同一人，年龄观感约 30 岁，脸型、五官比例、发型、身材和服装一致。
- 正面、真侧面、背面、3/4 与面部近景齐全；站姿和表情中性。
- 纯白背景、受控中性光、双手可见；画面中没有职业道具、剧情动作、文字、logo 或水印。

【跑歪修复】
- 身份漂移 -> `preserve the exact same individual and identical facial anchors in all five panels.`
- 混入剧情或道具 -> `strict neutral production reference only, empty hands, pure white studio background, no story action and no props.`

### 2.2 信息不足的完整提示词包

**原始输入**

> 一个男人收到十年前失踪女儿的短信。把它做成完整AI电影提示词包。

**本次实际响应全文**

当前不能直接生成“最终完整提示词包”：故事核心已给出，但身份、短信事实、交付规格和平台能力仍会改变镜头、关键资产与文字合成方案。先锁定到可安全推进的范围。

**Production Spec**

| 变量组 | 变量 | 值 | 状态 | 来源 |
|---|---|---|---|---|
| 故事 | 核心事件 | 男人收到十年前失踪女儿发来的短信 | 已锁定 | 用户指令 |
| 故事 | 父女当前年龄与失踪时年龄 | 未提供 | 待确认 | 用户未提供 |
| 故事 | 短信是否确由女儿发送 | 未提供 | 待确认 | 会改变真相与结局 |
| 故事 | 地点与后续节拍 | 未提供 | 待确认 | 会改变场景和镜头 |
| 交付 | 用途、画幅、总时长、分辨率、帧率、格式 | 未提供 | 待确认 | 用户未提供 |
| 视觉 | 写实/风格化、时代、色彩、光线、摄影语言 | 未提供 | 待确认 | 用户未提供 |
| 表演 | 男人身份、年龄、状态、对白与口型 | 未提供 | 待确认 | 用户未提供 |
| 声音 | 对白/旁白、环境音、动作音、强调音、音乐 | 先保留手机提示音这一故事声音 | 推断 | 核心事件需要可听触发；其余可延后 |
| 生成 | 平台、输入类型、单次时长、参考能力 | 未提供 | 待确认 | 决定拆镜和参考策略 |
| 后期 | 短信文字 | 受控后期合成，不交给生成模型直接写 | 已锁定 | 关键文字政策 |
| 后期 | 剪辑、调色、字幕、最终 QC | 未提供 | 可延后 | 首次成为依赖前锁定 |

**Gate 0 结论：阻塞**

阻塞项：父女年龄与时间线、短信真伪和后续故事节拍、最终交付规格、视觉方向、目标平台能力未锁定。

下游影响：角色资产、短信内容、场景表、镜头卡、最终画幅、镜头时长、参考图策略及全部最终视频提示词。

最小解决方案：请一次确认四项：`父女当前/失踪时年龄`、`短信真伪与结局方向`、`成片画幅和总时长`、`目标平台的单次时长及首/尾帧能力`；视觉方向可同时指定，或授权我给出一项可逆推断。

仍可继续完成的部分：

1. 故事事实台账可先锁定“父亲收到来自失踪十年的女儿号码/账号的短信”。
2. 短信画面统一生成干净手机屏幕，准确内容在后期排版、校对和合成。
3. 暂定叙事骨架可登记为“日常状态 -> 短信触发 -> 身份核验 -> 行动选择 -> 真相/悬念”，但在短信真伪确认前不转成最终镜头。

收到上述最少信息后，按 `Production Spec -> 连续性审计 -> 场景/镜头卡 -> 资产依赖 -> storyboard/keyframe -> 十栏目视频提示词 -> 后期与 QC` 输出完整包。

### 2.3 连续性冲突阻塞

**原始输入**

> 第一场写林夏28岁，第二场写十年前她已经25岁。祖传怀表先由林夏随身携带，下一镜未发生交接却出现在反派手中。请直接生成最终视频提示词。

**本次实际响应全文**

不能直接生成受影响的最终视频提示词。年龄算术和核心道具归属同时冲突，均会污染角色资产、镜头 keyframe 与相邻镜头衔接。

Audit scope: 第一场、十年前的第二场及怀表跨镜连续性

Overall conclusion: 阻塞

Conditions / blocking summary: 林夏年龄时间线与怀表持有链必须先锁定。

ID: CONT-01

Severity: Blocker

Source facts: 第一场林夏 28 岁；第二场发生在十年前却写林夏 25 岁。若两场相差十年且为同一人，第二场应为 18 岁。

Downstream impact: 林夏当前/年轻版身份资产、服装状态、表演、第二场 keyframe、所有引用年龄的最终视频提示词。

Recommended lock: 保留“第一场 28 岁”和“十年前”，将第二场改为 18 岁。

Alternative: 若第二场必须为 25 岁，则第一场应为 35 岁，或把时间差改为 3 年。

Recommended action: 在三个自洽组合中确认一个。

Status: 待确认

ID: CONT-02

Severity: Blocker

Source facts: 怀表先由林夏随身携带；下一镜未发生交接，却由反派持有。

Downstream impact: 两镜尾帧/首帧、手部动作、道具状态、屏幕方向、反派 keyframe 和剪辑逻辑。

Recommended lock: 在两镜之间补一个可见交接、夺取或遗失节拍，并明确怀表离开林夏及进入反派手中的时点。

Alternative: 若不增加交接镜，则下一镜仍由林夏持有，反派只能看到或试图夺取。

Recommended action: 确认“补交接/夺取镜”或“反派尚未持有”。

Status: 待确认

阻塞项：CONT-01 年龄时间线；CONT-02 核心道具持有链。

下游影响：第二场及后续所有依赖林夏年龄或怀表状态的最终提示词。

最小解决方案：回复一个年龄组合，并选择怀表通过何种可见动作转移。

仍可继续完成的部分：可先建立林夏身份锚点、怀表材质/磨损锚点和不依赖冲突的场景环境；不得生成受影响镜头的最终 keyframe 或视频提示词。

### 2.4 最小修补

**原始输入**

> 审查这份已有提示词包：N01正确；N02缺少尾帧；N03引用不存在的C09。只修必要问题，不要重写N01。

**本次实际响应全文**

Audit scope: N01-N03 最小修补

Overall conclusion: 阻塞

Conditions / blocking summary: N02 可做局部结构补丁；N03 的 C09 不存在，修复前不得进入生成。

- `N01`：保持原文，不重写、不重排。
- `N02`：只在原块中补入以下独立栏目，其余内容保持原文：

```text
【尾帧】
保持 N02 最后一段动作结束时的既有人物位置、视线、道具持有者与状态、环境布局和光线方向；动作完全停住并稳定保持 0.5 秒，作为下一镜剪辑接口。不得新增动作、人物、道具转移或光线变化。
```

- `N03`：不改写其余栏目，暂时阻塞。删除或替换 `C09` 前不能把该镜提交生成。

ID: ASSET-01

Severity: Blocker

Source facts: N03 引用了不存在的 `C09`。

Downstream impact: N03 的角色身份/状态无法追踪，生成会产生未受控身份。

Recommended lock: 若该人物已有正确资产，提供其真实稳定 ID 并仅替换 `C09`；若资产缺失，先创建并验收该角色资产，再恢复引用。

Recommended action: 提供有效资产 ID 或补齐资产。

Status: 待确认

最小变更结果：N01 零改动；N02 仅新增 `【尾帧】`；N03 仅隔离无效引用并等待有效 ID，不虚构替代资产。

## 3. 跨题材实际执行

以下四条输入彼此独立执行。每条响应均保留七组 Production Spec 和相同的依赖/Gate 骨架，但使用输入指定的媒介、画幅与时长。

### 3.1 现实家庭剧情

**完整输入**

> 为一部现实家庭剧情制定 AI 电影制片计划：离家多年的女儿在父亲手术前夜回到县城老屋，两人一起修好坏掉的收音机。成片 6 分钟，4:3，克制自然主义，普通话对白。请给出 Production Spec 和生产结构摘要。

**本次实际响应的 Production Spec/结构摘要**

| 变量组 | 锁定或推断结果 |
|---|---|
| 故事 | 父女重逢与修收音机为双线动作；手术前夜、县城老屋、收音机为核心道具均已锁定 |
| 交付 | 6 分钟、4:3、普通话已锁定；分辨率/帧率/文件格式待确认 |
| 视觉 | 克制自然主义已锁定；推断低饱和室内实景、固定机位与轻微手持，不强加商业写实模板 |
| 表演 | 少台词、停顿和手部协作承载关系变化；角色精确年龄与服装待确认 |
| 声音 | 普通话对白、老屋环境音、工具动作音、收音机电流强调音；音乐可延后 |
| 生成 | 平台与单次能力待确认；平台锁定前只做镜头卡，不锁单镜时长 |
| 后期 | 收音机刻度等非关键文字不可读；字幕、调色和混音在 Gate 5 锁定 |

结构：Gate 0 锁定父女年龄、手术事实和收音机状态；Gate 1 以“归来、共处、修理、响起、未说出口的和解”建立场景表与 animatic；Gate 2 先做父女身份、老屋空景和收音机正常/损坏状态；Gate 3 做 4:3 storyboard/keyframe；Gate 4 依平台能力拆片；Gate 5 完成对白、拟音、调色和交付 QC。立即行动依次为确认角色年龄与平台、建立道具状态台账、制作临时对白 animatic、生成复用资产、再进入关键帧。

### 3.2 古装仙侠

**完整输入**

> 为一部古装仙侠短片制定 AI 电影制片计划：被逐出师门的剑修在云海断桥上归还本命剑，剑灵化成纸鹤飞走。成片 90 秒，2.39:1，水墨与剪纸融合的高度风格化视觉，无对白。请给出 Production Spec 和生产结构摘要。

**本次实际响应的 Production Spec/结构摘要**

| 变量组 | 锁定或推断结果 |
|---|---|
| 故事 | 逐出师门、归还本命剑、剑灵化纸鹤为已锁定节拍；剑与纸鹤状态变化需单独台账 |
| 交付 | 90 秒、2.39:1、无对白已锁定；分辨率/帧率/格式待确认 |
| 视觉 | 水墨与剪纸融合、高度风格化已锁定；明确排除自动写实化，不套用真人电影皮肤与镜头质感 |
| 表演 | 以剪影、袖摆、持剑和停顿表达；无口型需求 |
| 声音 | 风声、衣料、剑鸣、纸张振翅为三层声音；音乐风格待确认 |
| 生成 | 工具与首尾帧能力待确认；变形镜头优先要求起止关键帧 |
| 后期 | 水墨粒子、纸鹤合成、无意文字清理与宽银幕 QC |

结构：Gate 0 审计剑的归属与变形逻辑；Gate 1 以“登桥、奉剑、剑灵脱离、纸鹤远去”建立场景/镜头卡和节奏 animatic；Gate 2 制作角色剪影身份、剑的正交/状态资产、断桥空景和风格 bible；Gate 3 全部按 2.39:1 构图；Gate 4 将剑灵变形按平台能力决定单镜或拆镜；Gate 5 完成水墨/剪纸合成和声音。该响应未改写为写实视觉，也未套用固定竖屏或固定单镜时长。

### 3.3 现代悬疑

**完整输入**

> 为一部现代悬疑微电影制定 AI 电影制片计划：夜班保安在监控里看见五分钟前的自己走进一部停运电梯。成片 45 秒，1:1，冷色监控质感与少量主观镜头，无台词。请给出 Production Spec 和生产结构摘要。

**本次实际响应的 Production Spec/结构摘要**

| 变量组 | 锁定或推断结果 |
|---|---|
| 故事 | 夜班、停运电梯、监控延迟悖论和“另一个自己”为核心事实；五分钟时间差与出入方向需连续性台账 |
| 交付 | 45 秒、1:1、无台词已锁定；平台与编码待确认 |
| 视觉 | 冷色监控质感加少量主观镜头已锁定；监控画面和现实画面分别设光线/噪点锚点 |
| 表演 | 克制警觉，以视线、呼吸和手停在按钮前表达；无口型 |
| 声音 | 值班室底噪、电梯继电器、脚步、一次低频强调；不默认持续配乐 |
| 生成 | 需确认平台是否支持画中画、首尾帧和精确时长；关键监控 UI 留后期 |
| 后期 | 时间戳、电梯状态等关键文字受控合成；监控画面嵌套、声音和 1:1 交付在 Gate 5 |

结构：Gate 0 校验“五分钟前”与人物动线；Gate 1 用现实/监控两条可辨时间线做 shot cards；Gate 2 建立同一保安身份、值班室/电梯环境和服装状态；Gate 3 以 1:1 验证屏幕内外视线；Gate 4 依据平台拆分现实与监控片段；Gate 5 合成准确时间戳并做音画 QC。该响应未替换用户的方形画幅或 45 秒时长。

### 3.4 二维动画

**完整输入**

> 为一部二维动画制定 AI 电影制片计划：纸片小狐狸沿着会折叠的城市地图寻找回家的红线。成片 70 秒，9:16，平涂赛璐璐、有限动画、无对白，面向儿童。请给出 Production Spec 和生产结构摘要。

**本次实际响应的 Production Spec/结构摘要**

| 变量组 | 锁定或推断结果 |
|---|---|
| 故事 | 小狐狸、折叠城市地图、回家红线和儿童受众已锁定；地图折叠规则需建立空间台账 |
| 交付 | 70 秒、9:16、无对白已锁定；分辨率/帧率/格式待确认 |
| 视觉 | 平涂赛璐璐、有限动画、纸片角色已锁定；不增加写实毛发、体积皮肤或真人摄影语言 |
| 表演 | 依靠轮廓 squash/stretch、耳尾姿态和停顿；动作幅度适合儿童阅读 |
| 声音 | 纸张折叠、轻脚步、红线弹拨和环境层；音乐待确认 |
| 生成 | 优先支持风格/角色参考和可控关键帧的流程；具体平台待确认 |
| 后期 | 红线轨迹、地图折叠遮罩、色彩一致性和竖屏安全区在后期锁定 |

结构：Gate 0 锁定地图折叠的可见规则；Gate 1 以“迷路、发现红线、地图折叠阻断、跨越、到家”做 animatic；Gate 2 生成角色转面、表情、地图模块和红线状态；Gate 3 全程使用 9:16 storyboard/keyframe；Gate 4 按动作容量生成有限动画片段；Gate 5 完成遮罩、音效和儿童可读性 QC。该响应保持二维媒介，没有强加写实、横屏或其他固定时长。

## 4. 精确跨平台矩阵实际执行

### 4.1 共同剧情与不变项

共同剧情：**女人推门进入空房，发现桌上怀表后停住。**

两次执行共同锁定：

- 故事链：门外起始 -> 推门并进入空房 -> 发现桌上怀表 -> 停住。
- 连续性：同一女人、同一服装、同一房间布局；怀表始终位于桌面且无人持有；主光从房间左窗进入。
- 关键资产：`C01` 女人身份/服装、`E01` 空房、`P01` 桌上怀表。
- Production chain：Production Spec -> 连续性审计 -> shot cards -> 资产依赖 -> storyboard/keyframe -> video generation -> 后期/QC。
- Gate：Gate 0-5 均适用；退出标准不因平台改变。

### 4.2 Platform A

**完整输入**

> Platform A：每次 3-5 秒，只支持一张首帧。对共同剧情“女人推门进入空房，发现桌上怀表后停住”制定镜头拆分与参考策略。只调整平台相关策略，保持核心故事链与 Gate 不变。

**本次实际响应全文**

Production Spec 平台增量锁定：单次生成 `3-5 秒`；输入为 `一张首帧`；不支持尾帧约束。核心故事、资产状态、画幅、风格与声音规则保持共同锁定值，其中未提供的画幅和风格仍为待确认，不作默认。

镜头拆分：

| Shot | 时长 | 单一主要节拍 | 首帧策略 | 尾帧交接 |
|---|---:|---|---|---|
| A-N01 | 3 秒 | 女人从门外推开门 | 使用一张合成首帧 `KF-A01-S`：C01 位于门外、手触门把，E01 门内布局可见，P01 尚不可见 | 门打开，C01 停在门槛，左手仍接触门 |
| A-N02 | 4 秒 | 女人跨入空房并抬眼 | 使用一张合成首帧 `KF-A02-S`，严格复现 A-N01 尾帧；不额外上传角色/环境分图 | C01 进入房内，视线落向桌面方向，P01 仅进入视野 |
| A-N03 | 4 秒 | 女人看见怀表并停住 | 使用一张合成首帧 `KF-A03-S`：C01 已在房内、P01 在桌面、左窗光方向不变 | C01 完全停住，视线锁定 P01；P01 原位无人持有，保持 0.5 秒 |

参考策略：Platform A 每镜只提供一张已经合成身份、服装、环境几何和道具状态的首帧；不上传尾帧，也不同时塞入多张独立参考。A-N02、A-N03 的首帧由前镜已验收尾帧状态制作并在 Gate 3 核对，生成提示词仍重复稳定的文本连续性 DNA。

Gate 保持不变：Gate 0 锁定 Spec/连续性；Gate 1 验证三张 shot card 与动作容量；Gate 2 验收 C01/E01/P01；Gate 3 验收三张首帧及跨镜接口；Gate 4 逐镜生成并以实际尾帧 QC；Gate 5 剪辑、声音和交付。平台限制只导致较细拆镜和单首帧策略。

### 4.3 Platform B

**完整输入**

> Platform B：每次 8-12 秒，支持首尾帧。对共同剧情“女人推门进入空房，发现桌上怀表后停住”制定镜头拆分与参考策略。只调整平台相关策略，保持核心故事链与 Gate 不变。

**本次实际响应全文**

Production Spec 平台增量锁定：单次生成 `8-12 秒`；支持 `首帧 + 尾帧`。核心故事、资产状态、画幅、风格与声音规则保持共同锁定值，其中未提供的画幅和风格仍为待确认，不作默认。

镜头拆分：

| Shot | 时长 | 单一主要节拍 | 首尾帧策略 |
|---|---:|---|---|
| B-N01 | 8 秒 | 女人推门并完成进入空房 | 首帧 `KF-B01-S`：C01 门外手触门把；尾帧 `KF-B01-E`：C01 已跨入房内、门在身后半开、视线尚未锁定怀表 |
| B-N02 | 8 秒 | 女人发现桌上怀表并停住 | 首帧 `KF-B02-S` 复现 B-N01 尾帧；尾帧 `KF-B02-E`：C01 完全停住并看向 P01，P01 原位无人持有，左窗光方向不变 |

参考策略：每镜使用一对经 Gate 3 验收的首尾帧，首帧锁定起始 blocking，尾帧锁定状态变化和剪辑接口；B-N01 尾帧与 B-N02 首帧使用同一连续性状态。提示词仍重复 C01/E01/P01 的文本 DNA，不把首尾帧能力误当成可省略资产和连续性检查。

Gate 保持不变：Gate 0 锁定 Spec/连续性；Gate 1 验证两张 shot card 与动作容量；Gate 2 验收 C01/E01/P01；Gate 3 验收两对首尾帧；Gate 4 逐镜生成并检查是否准确到达尾帧；Gate 5 剪辑、声音和交付。平台能力只把 Platform A 的三个短片段合并为两个较长片段，并增加尾帧约束；故事链、资产状态和 Gate 0-5 未改变。

### 4.4 矩阵结论

| 项目 | Platform A | Platform B | 不变核心 |
|---|---|---|---|
| 单次时长 | 3-5 秒 | 8-12 秒 | 总故事顺序不变 |
| 拆分 | 3 镜 | 2 镜 | 每镜保持一个主要叙事节拍/动作目的 |
| 图像输入 | 每镜一张合成首帧 | 每镜一对首尾帧 | C01/E01/P01 与文本连续性 DNA 不变 |
| 尾帧控制 | 生成后 QC，并转成下一镜首帧 | 生成前作为 end frame 锁定，生成后再 QC | 人物、怀表、房间、光线和剪辑接口标准不变 |
| 流程/Gate | 统一生产链，Gate 0-5 | 统一生产链，Gate 0-5 | 完全不变 |

## 5. 新增定向场景实际执行

以下四条输入彼此独立应用当前 Skill，专门验证 `5c4b5b7` 所固定的生成模式所有权、输入契约和 canonical tail state。

### 5.1 纯 T2V 保留依赖但不传模型输入

**完整输入**

> 镜头 N21 已锁定为纯 T2V：一名穿深蓝雨衣的短发女人在旧车站候车厅停在黄色安全线前，右手握一只磨损黄铜怀表；冷白顶灯，雨水沿右侧玻璃向下流。请给出镜头卡关键字段和提示词连续性部分。规划依赖为 C01-W02、P01-ST01、E03-L02。不要传任何参考图。

**本次实际响应全文**

镜头实际模式以镜头卡为唯一真源；纯 T2V 仍保留规划依赖，但不把任何资产作为模型输入。

```text
Shot ID: N21
Duration: 5s
Story purpose: 女人走到安全线前，握紧怀表并停住
Generation mode: pure T2V
Start state: 中景；C01 位于候车厅画面左后方，朝画面右前方行走，右手在腰侧握住 P01；黄色安全线横贯前景；冷白顶灯稳定，雨水沿右侧玻璃向下流。
Subject motion: C01 向前两步，在安全线前停下，右手收紧怀表。
Camera motion: 缓慢向右前方平移一次。
Environment motion: 仅右侧玻璃雨水持续向下；顶灯不闪烁。
Canonical tail state / 权威尾帧定义:
  Camera/composition:
    Shot size: 中景
    Camera position/angle: 与人物眼高，位于安全线外侧，正侧前 3/4
    Frame layout: C01 位于左侧三分线，黄色安全线横贯下前景，右侧玻璃占右三分之一
  Character terminal state:
    Position: 双脚停在黄色安全线后
    Pose: 身体微前倾后稳定直立
    Facing: 朝画面右前方
    Expression: 克制警觉
    Hands: 右手在腰侧握紧 P01，左手自然垂下
    Action completion: 两步行走和握紧动作均已完成，静止 0.5 秒
  Environment terminal state:
    Motion: 仅雨水沿右侧玻璃向下
    Weather: 室外持续下雨
    Particles: 无
    Lighting: 冷白顶灯稳定，方向与亮度不变
  Prop holder/state/direction: C01 右手持有 P01；表盖闭合；表冠朝上
  Eyelines: C01 看向画面右前方站台入口
  Next-shot edit handoff: 静止尾帧硬切至站台入口反打
Dependency asset IDs: C01-W02, P01-ST01, E03-L02
Input handles: 无/不适用
```

```text
【依赖资产 IDs】
C01-W02, P01-ST01, E03-L02

【本镜输入】
无/不适用

【文本连续性 DNA】
角色：同一名约 30 岁短发女人，窄长脸、左眉尾浅疤，深蓝哑光连帽雨衣，黑色直筒裤，无随机饰品；道具：同一只掌心大小的磨损黄铜怀表，闭合表盖，表冠朝上，右手持有；环境：同一旧车站候车厅，黄色安全线横贯前景，右侧整面玻璃，冷白顶灯；影像：低饱和冷色、克制写实、细雨夜景。
【开始状态】
中景，人物位于左后方并朝右前方行走，右手在腰侧握住闭合怀表；黄色安全线在前景，右侧玻璃雨水向下，冷白顶灯稳定。

【尾帧】
- Camera/composition：中景；与人物眼高、安全线外侧、正侧前 3/4；人物在左侧三分线，安全线横贯下前景，右侧玻璃占右三分之一。
- Character terminal state：人物双脚停在线后，身体稳定直立并朝右前方，克制警觉；右手腰侧握紧怀表，左手垂下；动作完成并静止 0.5 秒。
- Environment terminal state：仅玻璃雨水向下；室外持续下雨；无粒子；冷白顶灯稳定。
- Prop holder/state/direction：C01 右手持有，表盖闭合，表冠朝上。
- Eyelines：看向画面右前方站台入口。
- Next-shot edit handoff：静止尾帧硬切至站台入口反打。
```

结论：通过。`Dependency asset IDs` 完整保留；`Input handles` 与 `【本镜输入】` 均为 `无/不适用`；没有 token、附件、URL、来源帧或结束帧资产。连续性由文本 DNA 与开始状态承载，`【尾帧】` 逐项映射权威尾帧。

### 5.2 I2V 结束帧从 canonical tail state 派生

**完整输入**

> 镜头 N22 为 I2V，平台支持首尾帧。首帧句柄 `start_22.png`，结束帧候选 `end_22.png`。镜头内容是女人把闭合怀表放到木桌中央后松手。请先锁定 canonical tail state，再说明结束帧如何派生，并给出 Gate 3/4 校验结果。依赖为 C01-W02、P01-ST01、E04-L01。

**本次实际响应全文**

```text
Shot ID: N22
Duration: 6s
Generation mode: I2V/reference-driven
Start state: C01 站在木桌近侧，右手持闭合 P01 悬于桌面上方；左手扶桌沿。
Canonical tail state / 权威尾帧定义:
  Camera/composition:
    Shot size: 腰部中近景
    Camera position/angle: 桌面高度略上方，人物右前 3/4
    Frame layout: C01 上身在左半幅，木桌中央与 P01 在右下视觉中心
  Character terminal state:
    Position: C01 仍站在木桌近侧
    Pose: 上身轻微前倾
    Facing: 朝桌面
    Expression: 克制、决断
    Hands: 右手已松开并停在怀表上方约 5 厘米；左手仍扶桌沿
    Action completion: 放置和松手完成，保持 0.5 秒
  Environment terminal state:
    Motion: 窗帘轻微向左摆动
    Weather: 室外小雨
    Particles: 无
    Lighting: 左窗暖灰侧光稳定
  Prop holder/state/direction: 无人持有；P01 闭合，位于木桌正中央，表冠朝画面右侧
  Eyelines: C01 看向 P01
  Next-shot edit handoff: 可切怀表顶视特写，保持表冠朝右
Dependency asset IDs: C01-W02, P01-ST01, E04-L01, END-N22
Input handles:
  C01-W02: start_22.png → start_frame
  P01-ST01: start_22.png → start_frame
  E04-L01: start_22.png → start_frame
  END-N22: end_22.png → end_frame
```

`end_22.png` 不作为第二套创作定义。它必须在上述 canonical tail state 锁定后生成：腰部中近景、人物右前 3/4、C01 在桌近侧微前倾、右手松开并悬停 5 厘米、左手扶桌、怀表无人持有且在桌中央闭合并表冠朝右、视线落在怀表、窗帘轻微向左、左窗侧光稳定。`END-N22` 是从权威尾帧派生的镜头资产，已加入 `Dependency asset IDs` 并映射到 `end_22.png → end_frame`；它不定义第二套结束状态。

Gate 3 校验：

- 画幅与起始帧符合 Production Spec：通过。
- `end_22.png` 与 canonical `Camera/composition`：通过。
- `Character terminal state` 的位置、姿态、朝向、表情、双手与动作完成状态：逐项通过。
- `Environment terminal state` 的运动、天气、粒子和光线：逐项通过。
- 道具持有者/状态/方向、视线、下一镜接口：逐项通过。
- Gate 3 结论：通过，可使用首尾帧。

Gate 4 进入校验：

- 镜头卡模式为 I2V/reference-driven，平台支持首尾帧：通过。
- 依赖与实际输入映射已明确，结束帧有 canonical 派生证明：通过。
- 十栏目 `【尾帧】` 已逐项复制上述 canonical 值，没有另立终态：通过。
- Gate 4 进入结论：通过；生成后仍须逐项检查结果是否落到同一 canonical tail state，未实际生成前不宣称 Gate 4 退出通过。

### 5.3 尾帧姿态与运动漂移冲突

**完整输入**

> 审查 N23：canonical tail state 写人物站在门左侧、双臂下垂、右手空置、门帘完全静止；生成结果中人物仍在门左侧，但右手抬到胸前抓住围巾，身体转向门口，门帘持续向右摆动。能否因为人物位置相同而判通过？

**本次实际响应全文**

不能。人物位置相同只满足 `Character terminal state.Position`，不覆盖姿态、朝向、手部、动作完成状态和环境运动。

```text
Audit scope: N23 Gate 4 生成结果与权威尾帧逐项核验
Overall conclusion: 阻塞
Conditions / blocking summary: 终止姿态、朝向、手部/道具状态和环境运动均偏离 canonical tail state；返修前不得进入相邻镜头衔接或 Gate 5。

ID: TAIL-01
Severity: Blocker
Source facts: canonical 要求人物双臂下垂、右手空置、身体维持原朝向；结果为右手抬至胸前抓住围巾并转向门口。
Downstream impact: N23 尾帧、下一镜开始状态、手部与围巾状态、视线和屏幕方向。
Recommended lock: 保持 canonical 原值，返修结果使双臂下垂、右手空置、身体恢复锁定朝向。
Recommended action: 返修 N23，不得用生成结果覆盖镜头卡。
Status: 待处理

ID: TAIL-02
Severity: Blocker
Source facts: canonical 要求门帘完全静止；结果中门帘持续向右摆动。
Downstream impact: 环境运动终态和下一镜静止剪辑接口。
Recommended lock: 尾帧门帘完全静止。
Recommended action: 返修环境运动并重新执行 Gate 4 尾帧核验。
Status: 待处理
```

结论：阻塞。位置一致不构成整体尾帧一致；canonical 的所有结构化字段均是验收条件。

### 5.4 I2V 平台能力不足时显式改模式

**完整输入**

> N24 镜头卡原定 I2V，依赖 C02-W01、P04-ST02、E06-L01，并计划传首帧和尾帧。执行前发现平台不支持任何参考输入。不要换平台，请给出合规处理与受影响 Gate 重跑结果。

**本次实际响应全文**

不能删除输入后仍把 N24 当作 I2V 生成。先进行生产契约变更，再重新准入。

```text
Shot ID: N24
Generation mode: pure T2V
Dependency asset IDs: C02-W01, P04-ST02, E06-L01
Input handles: 无/不适用
```

变更内容：

1. 在镜头卡中把唯一真源 `Generation mode` 从 `I2V/reference-driven` 显式改为 `pure T2V`。
2. 保留全部 `Dependency asset IDs`，清空首帧与尾帧句柄；生成请求不得传入来源帧或结束帧资产。
3. 重写 N24 的生成模式连续性段，完整写入 C02-W01 的身份/服装 DNA、P04-ST02 的形状/材质/状态/归属 DNA、E06-L01 的布局/光线 DNA，以及镜头开始状态。
4. 保持镜头卡既有 canonical tail state 不变；十栏目 `【尾帧】` 逐项映射该值。
5. 此次仅改变 N24 单镜模式，不改变 Production Spec 的平台能力、允许模式集合或全局默认策略。

受影响 Gate 重跑：

| Gate | 重跑原因 | 实际结果 |
|---|---|---|
| Gate 1 | 镜头卡模式、输入字段及动作容量改变 | 通过：模式唯一，依赖保留，输入为无/不适用；单镜动作在纯 T2V 能力内，无需再拆镜 |
| Gate 2 | 资产从模型输入改为文本规划依赖 | 通过：C02-W01、P04-ST02、E06-L01 均保留稳定 ID 和完整文本 DNA，不删除资产依赖 |
| Gate 3 | 原首尾输入策略失效 | 通过：不再把首/尾 keyframe 作为模型输入；storyboard 仅用于审阅，canonical tail state 保持唯一且与相邻镜头开始状态一致 |
| Gate 4 | 生成模式和请求载荷改变 | 进入通过：提示词已改为纯 T2V，`Input handles`/`【本镜输入】` 为无/不适用，无伪引用，`【尾帧】` 映射 canonical；实际生成后才能判定退出 |

Gate 0 的平台事实本来已锁定为“不支持参考输入”，没有被这次单镜模式变更改写；Gate 5 尚未进入。若 Gate 1 发现动作容量超限，必须先拆镜并再次重跑其后受影响 Gate，而不是继续提交生成。

结论：有条件通过至 Gate 4 入口。条件是实际请求载荷不含任何参考输入，生成结果仍须按 canonical tail state 逐项验收；未静默省略输入，也未伪造平台能力。

## 6. 静态检查命令与真实结果

所有命令均在固定 workspace、branch 和 `HEAD=5c4b5b7b2a4749eb9f85f5933fa96b6f171b7841` 上实际执行。没有专用测试 CLI；以下均为通用 shell、Ruby YAML 解析和 Git 检查。

### 6.1 YAML

```bash
ruby -e 'require "yaml"; p=ARGV.fetch(0); d=YAML.safe_load(File.read(p), permitted_classes: [], aliases: false); abort "root must be mapping" unless d.is_a?(Hash); i=d["interface"]; abort "missing interface" unless i.is_a?(Hash); %w[display_name short_description default_prompt].each { |k| abort "missing #{k}" unless i[k].is_a?(String) && !i[k].empty? }; puts "YAML OK: #{p}"' skill/ai-film-production-director/agents/openai.yaml
```

真实结果：exit `0`。

```text
YAML OK: skill/ai-film-production-director/agents/openai.yaml
```

### 6.2 路径与旧标识

```bash
test -f skill/ai-film-production-director/SKILL.md && test -f skill/ai-film-production-director/agents/openai.yaml && test ! -e skill/quan_zhan_dao_yan && test ! -e skill/ai-film-production-director/.DS_Store; printf 'path_check_exit=0\n'; if rg -n 'quan_zhan_dao_yan|wanwusheng-ai-film-director|\$wanwusheng-ai-film-director' skill/ai-film-production-director; then exit 1; else printf 'legacy_identifier_matches=0\n'; fi
```

真实结果：exit `0`。

```text
path_check_exit=0
legacy_identifier_matches=0
```

### 6.3 References 完整性

```bash
expected='continuity-audit.md output-batching.md production-workflow.md prompt-patterns.md video-prompt-pack-template.md'; actual=$(find skill/ai-film-production-director/references -maxdepth 1 -type f -name '*.md' -exec basename {} \; | sort | tr '\n' ' ' | sed 's/ $//'); test "$actual" = "$expected"; printf 'references_count=%s\nreferences=%s\n' "$(find skill/ai-film-production-director/references -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')" "$actual"
```

真实结果：exit `0`。

```text
references_count=5
references=continuity-audit.md output-batching.md production-workflow.md prompt-patterns.md video-prompt-pack-template.md
```

### 6.4 十栏目

```bash
for heading in 场景 运镜 动作 尾帧 音效 影像调性 表演要求 对白 反向锚定 '后期与 QC'; do rg -q "【${heading}】" skill/ai-film-production-director/references/video-prompt-pack-template.md || exit 1; done; rg -n '十个独立栏目|【场景】【运镜】【动作】【尾帧】【音效】【影像调性】【表演要求】【对白】【反向锚定】【后期与 QC】' skill/ai-film-production-director/references/video-prompt-pack-template.md
```

真实结果：exit `0`。

```text
164:- 每个镜头完整保留 `【场景】【运镜】【动作】【尾帧】【音效】【影像调性】【表演要求】【对白】【反向锚定】【后期与 QC】` 十个独立栏目。
174:- **镜头可执行**：每个单镜头只有一个主要叙事节拍和一个主要摄影机运动，单次复杂度适配目标平台，并完整保留十个独立栏目。
```

### 6.5 动态分批

```bash
rg -n '共同判断是否需要分批|不设固定镜头数或资产数阈值|批次数量与覆盖范围按项目实际复杂度确定|不套用默认镜头分组' skill/ai-film-production-director/references/output-batching.md; if rg -n 'N01-N05|N06-N10|N11-N16' skill/ai-film-production-director/references/output-batching.md; then exit 1; else printf 'fixed_batch_matches=0\n'; fi
```

真实结果：exit `0`。

```text
7:根据以下因素共同判断是否需要分批，不设固定镜头数或资产数阈值：
27:批次数量与覆盖范围按项目实际复杂度确定，不套用默认镜头分组。
fixed_batch_matches=0
```

### 6.6 动态画幅

```bash
rg -n '\{aspect_ratio\}|\{wrong_aspect_ratios\}|最终交付比例|不继承其他项目的风格、画幅、时长、镜头数' skill/ai-film-production-director/SKILL.md skill/ai-film-production-director/references/*.md; if rg -n 'not vertical, not square|固定(为|：| )?(16:9|9:16|1:1|4:3|2\.39:1)' skill/ai-film-production-director; then exit 1; else printf 'fixed_aspect_matches=0\n'; fi
```

真实结果：exit `0`；命中动态占位与最终比例规则共 10 行，末行：

```text
fixed_aspect_matches=0
```

关键命中包括：

```text
skill/ai-film-production-director/SKILL.md:24:- 不继承其他项目的风格、画幅、时长、镜头数或平台限制。
skill/ai-film-production-director/references/production-workflow.md:80:参考图可以使用便于审阅的临时网格。所有 storyboard panel、keyframe 和视频镜头必须使用 Production Spec 锁定的最终交付比例。
skill/ai-film-production-director/references/video-prompt-pack-template.md:8:# 《{title}》视频提示词优化版 {aspect_ratio}
skill/ai-film-production-director/references/video-prompt-pack-template.md:24:所有最终关键帧与视频镜头统一为 {aspect_ratio}. 禁止 {wrong_aspect_ratios}.
```

### 6.7 条件输入

```bash
rg -l '平台不支持参考输入|平台不支持所需输入' skill/ai-film-production-director/references/*.md | sort
```

真实结果：exit `0`。

```text
skill/ai-film-production-director/references/output-batching.md
skill/ai-film-production-director/references/production-workflow.md
skill/ai-film-production-director/references/prompt-patterns.md
skill/ai-film-production-director/references/video-prompt-pack-template.md
```

### 6.8 纯 T2V

```bash
rg -l '纯 T2V.*Dependency asset IDs|纯 T2V.*Input handles|Input handles.*无/不适用|【本镜输入】：无/不适用' skill/ai-film-production-director/references/*.md | sort
```

真实结果：exit `0`。

```text
skill/ai-film-production-director/references/output-batching.md
skill/ai-film-production-director/references/production-workflow.md
skill/ai-film-production-director/references/prompt-patterns.md
skill/ai-film-production-director/references/video-prompt-pack-template.md
```

### 6.9 Canonical tail

```bash
rg -l 'Canonical tail state|canonical tail state|权威尾帧定义|单一尾帧真源' skill/ai-film-production-director/references/*.md | sort
```

真实结果：exit `0`，全部五份 reference 均命中：

```text
skill/ai-film-production-director/references/continuity-audit.md
skill/ai-film-production-director/references/output-batching.md
skill/ai-film-production-director/references/production-workflow.md
skill/ai-film-production-director/references/prompt-patterns.md
skill/ai-film-production-director/references/video-prompt-pack-template.md
```

### 6.10 固定 feature range diff

```bash
git diff --check 40aab9c..5c4b5b7; rc=$?; printf 'diff_check_exit=%s\n' "$rc"; exit "$rc"
```

真实结果：exit `0`。

```text
diff_check_exit=0
```

## 7. 观察结果与证据索引

- 最小模式未扩写为完整制片流程，见 [2.1](#21-最小资产请求)。
- 缺失阻塞变量没有被静默猜测，关键文字进入后期，见 [2.2](#22-信息不足的完整提示词包)。
- 年龄算术和怀表持有链分别形成 Blocker，见 [2.3](#23-连续性冲突阻塞)。
- N01 保留，N02 局部补尾帧，N03 因无效资产隔离，见 [2.4](#24-最小修补)。
- 四种题材均保留用户给定媒介、画幅和时长，见 [第 3 节](#3-跨题材实际执行)。
- Platform A/B 只改变拆分和参考策略，核心故事、资产状态、生产链和 Gate 不变，见 [第 4 节](#4-精确跨平台矩阵实际执行)。
- 纯 T2V 的依赖、输入和连续性载体均符合契约，见 [5.1](#51-纯-t2v-保留依赖但不传模型输入)。
- I2V 结束帧在 Gate 3/4 被证明派生自 canonical tail state，见 [5.2](#52-i2v-结束帧从-canonical-tail-state-派生)。
- 人物位置相同但姿态、手部和环境运动漂移仍被判为阻塞，见 [5.3](#53-尾帧姿态与运动漂移冲突)。
- 平台不支持 I2V 输入时显式更新镜头卡并重跑所有受影响 Gate，见 [5.4](#54-i2v-平台能力不足时显式改模式)。
- YAML、路径/旧标识、references、十栏目、动态分批、动态画幅、条件输入、纯 T2V、canonical tail 和固定 feature range diff 的命令结果见 [第 6 节](#6-静态检查命令与真实结果)。

## 8. 自审

- 本文所有观察结果均链接到本文件的具体响应或命令章节。
- 行为验证如实描述为当前 Agent 逐条应用 Skill 的人工场景回归；没有声称自动化测试框架。
- 静态检查只记录实际运行的通用 shell、Ruby YAML 解析与 Git 命令；没有声称或伪造专用 CLI。
- 四个原始中文请求均逐字保留，其响应已在本次回归中重新生成和逐项复核。
- 四题材和两个平台输入均独立重跑；平台矩阵保持同一剧情和统一 Gate。
- 新增四个定向场景均记录本次实际响应，其中 Gate 4 只在具有输入契约证据时判“进入通过”，未把未执行的视频生成伪报为“退出通过”。
- Tested commit、完整 SHA 与 `HEAD` 一致；静态 feature range 严格使用用户指定的 `40aab9c..5c4b5b7`。
