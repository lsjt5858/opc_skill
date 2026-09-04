# AI 电影制片导演 视频提示词包模板

当需要为 AI 电影组装“剧本 + 资产”的视频提示词包时，使用这个模板。

## 1. 全局章节

```markdown
# 《{title}》视频提示词优化版 {aspect_ratio}      

成片规格：{total_duration_if_known}，{aspect_ratio}，{visual_style}。
平台单次生成范围：{clip_duration_range}。该范围只约束单条视频；不得据此推断成片总时长、固定镜头数或统一单镜时长。
使用方式：仅当 Production Spec 已确认目标平台支持参考输入且当前镜头需要参考资产时，上传对应参考资产，并把本文中的 `@[C01_NAME]` 这类占位符替换成实际素材引用 ID；纯 T2V 或目标平台不支持参考输入时，省略资产引用，改用已锁定的文本连续性 DNA。

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

## 1. 资产锚定表

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

## 2. 镜头提示词
```

## 输入资产就绪检查

生成任何单镜提示词前逐项确认：

- Production Spec 变量已锁定；尚未锁定的变量必须明确标注状态和责任方，不得静默猜测。
- 当前镜头引用的全部资产 ID 均存在且可访问；不适用的资产类型可不引用。
- 角色身份、服装/状态、道具状态和环境状态与镜头表一致。
- 画面中的关键文字已有明确后期合成、校对和替换策略。
- 镜头的动作、运镜、状态变化和声音复杂度适合目标平台的单次生成能力；超出时先拆镜。

## 2. 单镜头提示词块

每个镜头使用一个独立块，一镜只有一个主要叙事节拍；若有多个独立节拍，必须拆镜。镜头数量、成片总时长和每条生成时长根据项目决定；不要继承其他项目的固定数值。所有栏目必须独立保留，字段无内容时写“无”，不要省略或合并。

````markdown
### N{number}｜{generation_duration}｜{story_function}

```text
{scene type and duration}单镜头，{visual style}，{genre tone}，{image texture}，{aspect ratio} frame，{camera character}，{rendering medium}。

@[S01_TOKEN] 作为{style/reference role}视觉锚定：{only the transferable style, palette, texture and lighting traits}。

@[C01_TOKEN] 作为{character}视觉锚定：{identity, age, facial anchors, wardrobe, current state and restrained performance}。

@[P01_TOKEN] 作为{prop}视觉锚定：{shape, material, wear, current state, owner, screen/readability rule}。

@[E01_TOKEN] 作为{environment}视觉锚定：{layout, light direction, time, weather, period details and spatial mood}。

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
{exact final visual state; every character's position and eyeline; prop holder, state and direction; lighting state and direction; next-shot edit handoff}。

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
QC：{observable pass/fail checks with visible or audible evidence for identity, action count/order and timing, the single main camera movement, prop state, text policy, continuity, sound layers and exact tail frame}。
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
- 每个镜头都有用于剪辑连续性的最终状态。
- 声音设计服务故事，不添加不需要的背景音乐。
- 每个镜头完整保留 `【场景】【运镜】【动作】【尾帧】【音效】【影像调性】【表演要求】【对白】【反向锚定】【后期与 QC】` 十个独立栏目。
- 平台单次生成范围只用于校验每条提示词时长；没有用户要求时，不推断成片总时长、镜头总数或统一单镜时长。

## 4. 包级质量标准

- **生产一致性**：全包遵守已锁定的 Production Spec，资产状态与镜头表一致。
- **资产可追踪**：每个实际引用都能追溯到存在且就绪的资产 ID。
- **镜头可执行**：每个单镜头只有一个主要叙事节拍和一个主要摄影机运动，单次复杂度适配目标平台，并完整保留十个独立栏目。
- **时间可验证**：动作时间段连续覆盖生成时长，关键动作和声音有可观察时间点。
- **剪辑可衔接**：尾帧明确人物位置、视线、道具状态、光线和剪辑接口。
- **后期可落地**：关键文字、合成项和声音交接均有明确策略。

## 5. 常用跑歪修复句

- 身份漂移：`preserve the exact same individual and mandatory facial anchors from the provided identity reference.`
- 画幅漂移：`{aspect_ratio} final video frame, not {wrong_aspect_ratios}, no unintended crop or reframing.`
- 文字漂移：`no readable text, no numbers, no app interface, no subtitles, no logos; all critical text will be composited in post.`
- 道具漂移：`preserve the exact {prop} shape, material, scratches, worn edges, and current state from the prop reference.`
- 表演过度：`follow the locked performance direction; remove unrequested exaggeration in voice, face, posture, and gesture.`
- 类型错误：`preserve the locked rendering medium, genre, and visual style; exclude only the conflicting styles listed in the Production Spec.`
