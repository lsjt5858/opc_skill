# 万物生视频提示词包模板

在为万物生组装剧本+资产视频提示词包时使用此模板。

## 1. 全局部分

```markdown
# 《{标题}》万物生视频提示词优化版 {画幅比例}

成片规格：{时长} 秒左右，{画幅比例}，{视觉风格}。
使用方式：每个镜头生成前，先上传对应参考图；把本文中的 `@[C01_NAME]` 这类占位符替换成万物生实际素材引用 ID。

## 0. 全局锁定

【影像风格】
{写实风格锁定；电影颗粒；布光；类型；禁止风格}

【画幅】
所有最终关键帧与视频镜头统一为 {画幅比例}. 禁止 {错误画幅比例}.

【表演】
{表演规则、情绪克制、类型特定的表演限制}

【文字政策】
所有故事关键文字一律后期合成，不交给视频模型生成：
- {关键文字项 1}
- {关键文字项 2}

AI 画面统一约束：no readable text, no numbers, no app interface, no subtitles, no logos, no watermark.

## 1. 资产锚定表

【角色】
- C01 {角色}：`@[C01_TOKEN]`
  `{本地路径}`

【场景】
- E01 {场景}：`@[E01_TOKEN]`
  `{本地路径}`

【道具】
- P01 {道具}：`@[P01_TOKEN]`
  `{本地路径}`

【色卡/关系参考】
- S01 {参考}：`@[S01_TOKEN]`
  `{本地路径}`

## 2. 镜头提示词
```

## 2. 镜头提示词块

每个镜头使用一个块。

```markdown
### N{编号} | {时间范围} | {故事功能}

【上传参考图】{C/E/P/S ID}

```text
[STYLE LOCK]
{视觉风格} + {类型基调} + {摄影机/胶片质感} + {画幅比例} + {布光} + {景深} + photorealistic live-action film + not a 3D render.

Sound design only: {环境音}, {动作音}, {对白/旁白处理}, no background music.

@[C01_TOKEN] 作为{角色}视觉锚定+{身份/年龄/服装/当前状态}+严格按此图渲染。
@[P01_TOKEN] 作为{道具}视觉锚定+{材质/磨损/状态/持有者/屏幕状态}+{可读性规则}.
@[E01_TOKEN] 作为{环境}视觉锚定+{布局/光线/时间/天气}.

【镜头组织】
{时长}秒，{单镜头/硬切/蒙太奇/匹配剪辑/甩镜}。{时间线角色}。

【机位与构图】
{镜头景别}+{镜头}+{摄影机高度/角度}+{摄影机运动}+{前景/中景/背景}+{对焦规则}+{画面方向}.

【动作节奏】
0-{x}s：{开场动作与声音}.
{x}-{y}s：{中段动作/情绪转折}.
{y}-{结束}s：{结尾动作/对白/结束状态}.

【尾帧】
{确切的最终视觉状态；道具位置；谁拿着什么；视线；剪辑交接}.

【铁律】
{身份状态锁定}. {道具状态锁定}. {摄影机/画幅锁定}. {表演锁定}. {关键文字锁定}.

NOT {错误画幅} + NOT {错误风格} + NOT {身份漂移} + NOT {随机可读文字} + NOT subtitles + NOT logos + NOT watermark.
```

后期合成：{字幕、UI、数字、腕带文字、聊天信息、标题}.
声音：{如果尚未覆盖；确切对白/旁白台词}.
QC：{可观察的通过/失败检查}.
```

## 3. 连续性审计检查清单

在编写依赖提示词之前使用此检查清单：

- 画幅比例和时长与用户最新指令匹配。
- 角色身份和年龄变体不混淆。
- 每条时间线内的服装状态稳定。
- 反复出现的道具有确切的持有者、材质、损坏/磨损和屏幕状态。
- 手机/UI/腕带/收据/聊天/药品标签文字是后期合成。
- 场景顺序在物理和情绪上连贯。
- 每个镜头都有用于剪辑连续性的最终状态。
- 声音设计支持故事，不添加不需要的背景音乐。

## 4. 常见重抽修复

- 身份漂移：`preserve the exact same individual and mandatory facial anchors from the provided identity reference.`
- 画幅漂移：`{画幅比例} final video frame, not vertical, not square, not cropped portrait composition.`
- 文字漂移：`no readable text, no numbers, no app interface, no subtitles, no logos; all critical text will be composited in post.`
- 道具漂移：`preserve the exact {道具} shape, material, scratches, worn edges, and current state from the prop reference.`
- 表演过度：`restrained realistic acting, quiet grief, no melodramatic crying or shouting.`
- 类型错误：`realistic live-action film, not horror, not comedy, not influencer short-video filter, not animation, not CGI.`
