# AI 电影制片导演 视频提示词包模板

当需要为 AI 电影组装“剧本 + 资产”的视频提示词包时，使用这个模板。

## 1. 全局章节

```markdown
# 《{title}》视频提示词优化版 {aspect_ratio}      

成片规格：{total_duration_if_known}，{aspect_ratio}，{visual_style}。
平台单次生成范围：{clip_duration_range}。该范围只约束单条视频；不得据此推断成片总时长、固定镜头数或统一单镜时长。
使用方式：先按 Production Spec 和镜头卡为每镜锁定一种生成模式，再只输出对应分支，禁止同时输出两种写法：
- **I2V/参考驱动**：目标平台支持参考输入；每镜只传入实际存在、平台支持且当前镜头需要的资产子集，并只在单镜提示词中以 `{input_handle}` 列出该子集；`{input_handle}` 可映射为 token、附件、URL 或 API 字段，不得把资产锚定表整表当作传入清单，也不得为不需要或不可用的资产保留占位符。允许使用结束帧，但结束帧资产必须从镜头卡已锁定的 `Canonical tail state / 权威尾帧定义` 派生，并保持人物位置、视线、道具持有/状态/方向、光线、景别、机位、画面布局和下一镜剪辑接口一致；无法保证时只允许起始帧输入或阻塞修正，不得另设结束状态。
- **纯 T2V**：不传入任何输入句柄、来源帧、资产引用或结束帧资产；单镜提示词删除全部资产引用行，以完整文本写明连续性 DNA 和开始状态。十栏目 `【尾帧】` 同样忠实映射镜头卡 canonical tail state，不得另创结束状态。

若原定 I2V/参考驱动镜头遇到平台不支持参考输入，不得静默省略引用继续生成。只能二选一：先更新 Production Spec 与镜头卡，将该镜生成模式显式改为纯 T2V、按纯 T2V 重写提示词，并重跑所有受生成模式、拆镜、资产依赖、storyboard/keyframe 策略影响的 Gate；任一受影响 Gate 未通过则阻塞。或保持阻塞并更换为支持参考输入的平台。

## 0. 全局锁定

【影像风格】
{visual style lock; texture; lighting; genre; forbidden styles}

【画幅】
所有最终关键帧与视频镜头统一为 {aspect_ratio}. 禁止 {wrong_aspect_ratios}.

【表演】
{acting rules, emotional restraint, genre-specific performance limits}

【文字政策】
所有故事关键文字一律后期合成，不交给视频模型生成：
- {critical text item 1}
- {critical text item 2}

AI 画面统一约束：no readable text, no numbers, no app interface, no subtitles, no logos, no watermark.

## 1. 资产锚定表（设计/追踪台账）

本表用于包级资产设计、就绪状态和引用能力追踪，不等于任何单镜的传入清单。I2V/参考驱动镜头只能从中选择当前镜头实际需要、资产实际存在且平台支持的子集，并将其可用引用方式规范化为 `{input_handle}`；纯 T2V 镜头不得从本表传入任何输入句柄或引用 ID。

【角色】
- C01 {character}: `@[C01_TOKEN]`
  `{local path}`

【场景】
- E01 {environment}: `@[E01_TOKEN]`
  `{local path}`

【道具】
- P01 {prop}: `@[P01_TOKEN]`
  `{local path}`

【色卡/关系参考】
- S01 {reference}: `@[S01_TOKEN]`
  `{local path}`

以上 token 仅为 `{input_handle}` 的示例形式，不是必选契约。每项同时记录其完整文本连续性 DNA、当前状态/用途、资产是否存在、目标平台是否支持及可用引用方式；不存在、不支持或无可用句柄时明确写“无/不适用”，不得伪造 token、UUID、附件、URL 或 API 字段。

## 2. 镜头提示词
```

## 输入资产就绪检查

生成任何单镜提示词前逐项确认：

- Production Spec 变量已锁定；尚未锁定的变量必须明确标注状态和责任方，不得静默猜测。
- 当前镜头已在 Production Spec 和镜头卡中锁定为 I2V/参考驱动或纯 T2V，且提示词只使用对应分支。
- 镜头卡已在 Gate 3 前锁定 `Canonical tail state / 权威尾帧定义`，完整包含人物位置、视线、道具持有/状态/方向、光线、景别、机位、画面布局和下一镜剪辑接口；它是结束状态的唯一真源。
- I2V/参考驱动镜头 `【本镜输入】` 中的每个传入项均实际存在、平台支持、当前镜头需要且可访问，并已写明平台字段映射；不适用的资产类型不引用。若包含结束帧，已证明该资产从镜头卡 canonical tail state 派生并逐项一致；否则删除结束帧、只保留起始帧，或阻塞修正。
- 纯 T2V 镜头的 `【本镜输入】` 写 `无/不适用`，不包含也不传入任何输入句柄、来源帧、资产引用或结束帧资产；已完整写明文本连续性 DNA 和开始状态，十栏目 `【尾帧】` 忠实映射镜头卡 canonical tail state。
- 角色身份、服装/状态、道具状态和环境状态与镜头表一致。
- 已锁定且需保持连续性的固定饰品可保留；禁止随机饰品和未锁定职业道具。
- 画面中的关键文字已有明确后期合成、校对和替换策略。
- 镜头的动作、运镜、状态变化和声音复杂度适合目标平台的单次生成能力；超出时先拆镜。

## 2. 单镜头提示词块

每个镜头使用一个独立块，一镜只有一个主要叙事节拍；若有多个独立节拍，必须拆镜。镜头数量、成片总时长和每条生成时长根据项目决定；不要继承其他项目的固定数值。所有栏目必须独立保留，字段无内容时写“无”，不要省略或合并。

````markdown
### N{number}｜{generation_duration}｜{story_function}

```text
{scene type and duration}单镜头，{visual style}，{genre tone}，{image texture}，{aspect ratio} frame，{camera character}，{rendering medium}。

【本镜输入】
以下写法严格二选一；本栏目独立放在十栏目之前，不计入也不替代后续十个栏目。
I2V/参考驱动：逐项填写 `{传入项名称/用途}: {input_handle} → {目标平台字段}`；`{input_handle}` 可映射为 token、附件、URL 或 API 字段，只能列实际存在且平台支持的当前镜头输入。结束帧用途必须注明“由镜头卡 canonical tail state 派生”，不得在输入栏另写结束状态。
纯 T2V：无/不适用（不得传入输入句柄、来源帧或其他资产引用）。

以下“生成模式连续性段”严格二选一，只保留当前镜头对应写法；它不新增或替代后续十个栏目。I2V/参考驱动的每条锚定行必须与 `【本镜输入】` 中的实际传入项逐项一致，不得多列或漏列。

I2V/参考驱动写法（仅在平台支持且引用实际存在、当前镜头需要时保留需要的行；每个 `{input_handle}` 必须与 `【本镜输入】` 一致）：
{input_handle} 作为{style/reference role}视觉锚定：{only the transferable style, palette, texture and lighting traits}。

{input_handle} 作为{character}视觉锚定：{identity, age, facial anchors, wardrobe, current state and restrained performance}。

{input_handle} 作为{prop}视觉锚定：{shape, material, wear, current state, owner, screen/readability rule}。

{input_handle} 作为{environment}视觉锚定：{layout, light direction, time, weather, period details and spatial mood}。

纯 T2V 写法（删除以上全部资产引用行，不得传入输入句柄）：
【文本连续性 DNA】角色：{完整身份、年龄、面部锚点、服装，以及已锁定且需保持连续性的固定饰品}；道具：{完整形状、材质、磨损、归属与当前状态}；环境：{完整空间布局、光线方向、时代细节、材质与氛围}；影像：{完整风格、色彩、纹理与照明约束}。
【开始状态】{镜头开始时每个角色的位置、朝向、视线、姿态和表情；道具持有者、位置、方向和状态；环境、光线与摄影机状态}。
纯 T2V 的结束状态由下方十栏目 `【尾帧】` 映射镜头卡 canonical tail state；不需要结束帧资产，也不得在文本连续性块中重复定义或另创。

【场景】
{where and when the shot happens; spatial layout; this shot's explicit story function and the change it contributes; emotional situation; what the image should emphasize and avoid}。

【运镜】
{generation_duration}单镜头，{aspect_ratio}。只安排一个主要摄影机运动：{shot size, lens, camera height/angle, main camera movement, foreground/midground/background, focus rules, screen direction}。不自动切镜；若用户明确要求镜内剪辑或蒙太奇，才改写此约束。

【动作】
0-{x}s：{opening subject action and environment motion}。
{x}-{y}s：{middle action or emotional turn}。
{y}-{end}s：{ending action and exact stopping point}。
以上时间段首尾相接、无重叠无空档，连续覆盖完整生成时长；主体动作、环境运动和状态变化均在对应时间段内可观察。

【尾帧】
忠实映射镜头卡 `Canonical tail state / 权威尾帧定义`：{every character's position and eyeline; prop holder, state and direction; lighting state and direction; framing; camera position/angle; frame layout; next-shot edit handoff}。不得删改或另创。

【音效】
环境音：{background room tone/environment sound or 无}；动作音：{time-coded action sounds or 无}；强调音：{time-coded emphasis sounds or 无}；对白/人声：{dialogue/voice treatment or 无}；音乐：{follow the locked Production Spec music policy or 无}。

【影像调性】
{palette, contrast, medium, texture, lighting, subject/material treatment, rendering style, realism/stylization level and forbidden styles from the Production Spec}。

【表演要求】
{emotion expressed through breath, gaze, jaw, posture and small hand movement; explicit performance limits; who must not overact}。

【对白】
{exact dialogue/voice-over, speaker, timing and lip-sync policy; or 无对白}。无生成字幕；关键文字按后期政策处理。

【反向锚定】
NOT {wrong aspect ratio}，NOT {wrong style}，NOT {identity drift}，NOT {prop/state error}，NOT {performance error}，NOT {camera error}，NOT readable text，NOT subtitles，NOT logos，NOT watermark。

【后期与 QC】
后期：{subtitles, UI, numbers, messages, exact text, controlled compositing and sound handoff}。
QC：{observable pass/fail checks with visible or audible evidence for identity, action count/order and timing, the single main camera movement, prop state, text policy, continuity, sound layers and exact tail frame; 【尾帧】 must faithfully map the shot card canonical tail state; for I2V/reference-driven shots, every anchor must match 【本镜输入】 and any end-frame input must be derived from that canonical tail state; for every generation mode, the generated result must land on that same state}。
```
````

## 3. 连续性审计清单

写依赖提示词前，使用这份清单：

- 画幅和时长符合用户最新指令。
- 角色身份和年龄变体没有混用。
- 每条时间线内服装状态稳定。
- 反复出现的道具有精确归属者、材质、损坏/磨损和屏幕状态。
- 手机/UI/腕带/收据/聊天/药品标签文字采用后期合成。
- 场景顺序在物理和情绪上自洽。
- 每个镜头卡都在 Gate 3 前锁定完整的 `Canonical tail state / 权威尾帧定义`，作为结束状态唯一真源。
- 声音设计服务故事，不添加不需要的背景音乐。
- 每个镜头完整保留 `【场景】【运镜】【动作】【尾帧】【音效】【影像调性】【表演要求】【对白】【反向锚定】【后期与 QC】` 十个独立栏目。
- 每个镜头在十栏目之前独立保留 `【本镜输入】`；该栏目不计入十栏目。I2V/参考驱动以 `{input_handle}` 列实际传入项及平台字段映射，且正文锚定与 QC 只检查是否逐项与 `【本镜输入】` 一致；结束帧输入只能从镜头卡 canonical tail state 派生，不一致时只保留起始帧输入或阻塞修正。纯 T2V 写 `无/不适用`，不传任何输入句柄或结束帧资产。
- 平台单次生成范围只用于校验每条提示词时长；没有用户要求时，不推断成片总时长、镜头总数或统一单镜时长。
- 每镜只输出一种生成模式连续性段：I2V/参考驱动只保留与 `【本镜输入】` 一致的实际使用 `{input_handle}` 行；纯 T2V 无输入句柄或结束帧资产，以完整文本连续性 DNA 和开始状态承载起始连续性；两种模式的十栏目 `【尾帧】` 都忠实映射镜头卡 canonical tail state。
- 原定 I2V/参考驱动镜头的平台不支持参考输入时，必须更新 Production Spec 与镜头卡，重跑所有受生成模式、拆镜、资产依赖、storyboard/keyframe 策略影响的 Gate；任一受影响 Gate 未通过则阻塞，或更换平台。不得静默省略引用继续生成。

## 4. 包级质量标准

- **生产一致性**：全包遵守已锁定的 Production Spec，资产状态与镜头表一致。
- **资产可追踪**：每个实际引用都能追溯到存在且就绪的资产 ID。
- **镜头可执行**：每个单镜头只有一个主要叙事节拍和一个主要摄影机运动，单次复杂度适配目标平台，并完整保留十个独立栏目。
- **时间可验证**：动作时间段连续覆盖生成时长，关键动作和声音有可观察时间点。
- **剪辑可衔接**：尾帧明确人物位置、视线、道具持有/状态/方向、光线、景别、机位、画面布局和下一镜剪辑接口。
- **单一尾帧真源**：镜头卡 `Canonical tail state / 权威尾帧定义` 是唯一真源；I2V 结束帧资产与两种生成模式的十栏目 `【尾帧】` 都从它派生或映射，生成结果落在同一状态。任何逐项差异都必须返修，不能形成第二套结束状态。
- **后期可落地**：关键文字、合成项和声音交接均有明确策略。

## 5. 常用跑歪修复句

- 身份漂移（I2V/参考驱动）：`preserve the exact same individual and mandatory facial anchors from the provided identity reference.`
- 身份漂移（纯 T2V）：`preserve the exact same individual using the locked textual identity anchors: {complete facial structure, age, hair, skin, fixed accessories, wardrobe and distinguishing details}.`
- 画幅漂移：`{aspect_ratio} final video frame, not {wrong_aspect_ratios}, no unintended crop or reframing.`
- 文字漂移：`no readable text, no numbers, no app interface, no subtitles, no logos; all critical text will be composited in post.`
- 道具漂移（I2V/参考驱动）：`preserve the exact {prop} shape, material, scratches, worn edges, and current state from the provided prop reference.`
- 道具漂移（纯 T2V）：`preserve the exact {prop} using the locked textual anchors repeated in this shot: {shape, dimensions, material, color, scratches, worn edges, damage placement, owner and current state}.`
- 表演过度：`follow the locked performance direction; remove unrequested exaggeration in voice, face, posture, and gesture.`
- 类型错误：`preserve the locked rendering medium, genre, and visual style; exclude only the conflicting styles listed in the Production Spec.`
