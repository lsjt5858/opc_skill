# 万物生视频提示词包模板

当需要为万物生/万物生 AI 电影组装“剧本 + 资产”的视频提示词包时，使用这个模板。

## 1. 全局章节

```markdown
# 《{title}》万物生视频提示词优化版 {aspect_ratio}

成片规格：{total_duration_if_known}，{aspect_ratio}，{visual_style}。
平台单次生成范围：{clip_duration_range}。该范围只约束单条视频；不得据此推断成片总时长、固定镜头数或统一单镜时长。
使用方式：每个镜头生成前，先上传对应参考图；把本文中的 `@[C01_NAME]` 这类占位符替换成万物生实际素材引用 ID。

## 0. 全局锁定

【影像风格】
{realistic style lock; film grain; lighting; genre; forbidden styles}

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

## 2. 单镜头提示词块

每个镜头使用一个独立块。镜头数量、成片总时长和每条生成时长根据项目决定；不要继承其他项目的固定数值。所有栏目必须独立保留，字段无内容时写“无”，不要省略或合并。

````markdown
### N{number}｜{generation_duration}｜{story_function}

```text
{scene type and duration}单镜头，{visual style}，{genre tone}，{camera/film texture}，{aspect ratio} cinematic frame，{camera character}，photorealistic live-action。

@[S01_TOKEN] 作为{style/reference role}视觉锚定：{only the transferable style, palette, texture and lighting traits}。

@[C01_TOKEN] 作为{character}视觉锚定：{identity, age, facial anchors, wardrobe, current state and restrained performance}。

@[P01_TOKEN] 作为{prop}视觉锚定：{shape, material, wear, current state, owner, screen/readability rule}。

@[E01_TOKEN] 作为{environment}视觉锚定：{layout, light direction, time, weather, period details and spatial mood}。

【场景】
{where and when the shot happens; spatial layout; story function; emotional situation; what the image should emphasize and avoid}。

【运镜】
{generation_duration}单镜头，{aspect_ratio}。{shot size, lens, camera height/angle, one main camera movement, foreground/midground/background, focus rules, screen direction}。不自动切镜；若用户明确要求镜内剪辑或蒙太奇，才改写此约束。

【动作】
0-{x}s：{opening subject action and environment motion}。
{x}-{y}s：{middle action or emotional turn}。
{y}-{end}s：{ending action and exact stopping point}。

【尾帧】
{exact final visual state; character position and eyeline; prop holder, state and direction; lighting; edit handoff}。

【音效】
Sound design only，{background room tone/environment sound}；{time-coded event sounds}；{dialogue/voice treatment}；{music policy}。

【影像调性】
{palette, contrast, film stock/grain, physical light, skin/material texture, realism level and forbidden commercial/CG look}。

【表演要求】
{emotion expressed through breath, gaze, jaw, posture and small hand movement; explicit performance limits; who must not overact}。

【对白】
{exact dialogue/voice-over, speaker, timing and lip-sync policy; or 无对白}。无生成字幕；关键文字按后期政策处理。

【反向锚定】
NOT {wrong aspect ratio}，NOT {wrong style}，NOT {identity drift}，NOT {prop/state error}，NOT {performance error}，NOT {camera error}，NOT readable text，NOT subtitles，NOT logos，NOT watermark。

【后期与 QC】
后期：{subtitles, UI, numbers, messages, exact text, controlled compositing and sound handoff}。
QC：{observable pass/fail checks for identity, action count/order, camera, prop state, text, continuity and exact tail frame}。
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

## 4. 常用跑歪修复句

- 身份漂移：`preserve the exact same individual and mandatory facial anchors from the provided identity reference.`
- 画幅漂移：`{aspect_ratio} final video frame, not vertical, not square, not cropped portrait composition.`
- 文字漂移：`no readable text, no numbers, no app interface, no subtitles, no logos; all critical text will be composited in post.`
- 道具漂移：`preserve the exact {prop} shape, material, scratches, worn edges, and current state from the prop reference.`
- 表演过度：`restrained realistic acting, quiet grief, no melodramatic crying or shouting.`
- 类型错误：`realistic live-action film, not horror, not comedy, not influencer short-video filter, not animation, not CGI.`
