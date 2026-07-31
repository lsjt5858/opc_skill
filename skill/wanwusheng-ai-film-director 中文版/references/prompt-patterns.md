# 万物生提示词模式

只有在交付规格和关键连续性锚点已经自洽后，才使用这些模式。

## 目录

1. 核心提示词结构
2. 标准交付格式
3. 角色资产
4. 道具
5. 环境
6. Storyboard 与 keyframe
7. 视频镜头
8. 色卡/风格 bible
9. QC 与跑歪修复

## 1. 核心提示词结构

每个提示词资产都应包含：

- `asset ID/title`：稳定 ID、项目/段落、主体、版本；
- `purpose/dependencies`：用途，以及下游哪些镜头/资产会引用它；
- `format`：参考图格式或最终交付比例；
- `subject`：身份、轮廓、尺寸、材质、颜色、故事作用；
- `continuity DNA`：重复身份、标记、服装、色卡和参考；
- `composition`：视角、景别、布局、背景、位置；
- `lighting`：方向、质感、色温；
- `style/quality`：可见制作特征；
- `constraints`：容易跑偏的类别或不需要的元素；
- `QC`：可观察的验收检查；
- `reroll fixes`：只针对高概率失败写强化句。

## 2. 标准交付格式

````text
=== {model/task} prompt - {asset ID} {asset name} v1 ===

【用途与依赖】
- {为什么需要这个资产；哪些资产/镜头会引用它}

【格式】
- {画幅、panel 布局、输出类型}

【连续性】
- {锁定身份/材质/状态/光线锚点和参考资产 ID}

【prompt】
```text
{English executable prompt}
```

【QC】
- {可观察的通过/失败检查}

【跑歪修复】
- {failure} -> "{English strengthening line}"
````

## 3. 角色资产

不要把所有角色需求合进一张图。

### 中性身份/转面图

用于锁定角色是谁。

必备：

- 中性站姿和中性表情；
- 正面、真侧面、背面、3/4 全身视图；
- 布局允许时加入面部 close-up 或识别细节 panel；
- 每个 panel 中保持同一个人、同一比例、发型、服装和标记；
- 纯 studio 背景和受控中性光；
- 不要包含戏剧性剧情动作。

```text
a production identity turnaround sheet for {character ID/name}. {reference-sheet ratio and grid}. same individual in every panel with identical facial structure, body proportions, hairstyle, costume, accessories, and recognition marks. panels show front full body, true side full body, back full body, and right-front 3/4 full body; include a separate neutral face close-up if requested. neutral standing pose, arms relaxed and visible, plain studio backdrop, soft neutral reference lighting.

Identity: {age, origin, build, face anchors, hair, skin, occupation cues}. Mandatory recognition features: {features}. Costume/state: {wardrobe ID and exact materials/colors}.

Constraints: no sitting, no crying, no running, no cinematic scene, no pose change between orthographic views, no identity drift, no extra text, no watermark.
```

### 表情图

只在身份锁定后使用。

- 固定头部角度，或受控的正面/3/4 组合；
- 4-6 个与剧本节拍绑定的命名情绪；
- 保持同一发型、服装领口、光线和脸部比例；
- 避免与故事无关的泛泛情绪九宫格。

```text
an expression reference sheet for the exact same {character ID/name} from the provided identity reference. {panel count} equal face close-up panels: {script-specific expressions}. preserve identical facial structure, age, hairstyle, skin texture, costume collar, camera distance, and neutral studio lighting. expressions are natural and restrained unless the script requires otherwise. no identity drift, no different person, no full-body action, no text except optional panel labels.
```

### 姿势/动作图

用于困难或重复动作，不要给每个小手势都做。

```text
an action-pose reference sheet for the exact same {character ID/name} in {wardrobe ID}. panels show {distinct script actions with clear start/end body mechanics}. preserve identity, proportions, costume, dominant hand, carried props, and injury side. clean neutral background, readable full body and hands, practical anatomy. no environment storytelling, no costume change, no extra limbs.
```

### 服装/状态图

用于服装、年龄、伤痕、天气、污渍或变身变体。

写清什么保持不变、什么发生变化。给每个状态分配稳定 ID，例如 `C01-W01` 或 `C01-ST02`。

### 细节图

用于必须在 close-up 中保持的面部锚点、手部、疤痕、首饰、妆容、鞋履或拿取细节。

### 覆盖优先级

- 主角：完整身份、脸部/细节、服装/状态、表情、困难动作。
- 反复出现的配角：正面/3/4、脸部、主服装、必要表情/动作。
- 一次性角色：紧凑 casting card。

## 4. 道具/设备图

当物体会重复出现、改变状态、承载证据或需要稳定拿取时使用。

必备：

- 精确尺寸和归属/拿取逻辑；
- 正面/侧面/顶面/3/4 或相关正交视图；
- 固定材质、扣件、磨损、污渍、刻字、可动部件；
- 打开、损坏、潮湿、包裹或破损时，要做独立状态变体；
- 明确区别于故事里相似的物品。

```text
a production prop reference sheet for {prop ID/name}. {layout}. same exact object in every panel. dimensions: {size}. owner and handling: {logic}. materials/colors: {locked values}. mandatory recognition marks: {exact locations}. state: {state ID}. show {views/details}. practical prop photography, neutral background, controlled light. not {confusable object}, no changed damage placement, no extra text, no watermark.
```

对精确收据、信件、屏幕、标签或证据文字：生成不含关键字样的物理表面，再后期合成校对过的排版。提示词可以预留干净文字区域，但不能假装生成文字可靠。

## 5. 环境图

重复地点要先创建空场景，再创建带人物的剧情帧。

必备：

- 尺寸与功能；
- 主视角大远景和主要/反向覆盖；
- 几何关系重要时提供俯视/空间关系；
- 入口、出口、窗、门、家具、危险点、核心道具区域；
- 材质、年代、老化程度、天气和光线方向；
- 所有 panel 中保持同一布局。

```text
a production environment reference sheet for {environment ID/name}, empty set with no story characters. {layout}: master wide, primary shooting direction, reverse direction, and key-zone detail/top-down relation. preserve identical architecture, door/window/furniture positions, materials, period details, and navigation paths in all panels. scale/function: {details}. lighting/weather state: {state ID and direction}. practical cinematic production design, spatially coherent, no unexplained layout changes, no readable incidental text, no watermark.
```

## 6. Storyboard 与 Keyframe

### 故事板画面（Storyboard Panel）

使用低成本 panel 验证覆盖、blocking、视线、屏幕方向和剪辑节奏。除非影响理解，不要求身份完美。

### 关键帧静帧（Keyframe Still）

参考图锁定后，用于最终镜头瞬间。

必备：

- 镜头 ID 和故事作用；
- 最终交付比例；
- 身份、服装/状态、道具和环境的参考 ID；
- 摄影机/镜头感觉、角度、距离、景别、景深；
- 演员 blocking、视线、动作状态和画面位置；
- 环境、天气和明确光线方向；
- 成对使用时标明 start 或 end。

```text
cinematic keyframe for {shot ID}, {final aspect ratio}. Story purpose: {beat}. Preserve the exact identity and recognition features from {character references}, wardrobe/state from {state IDs}, prop design/state from {prop IDs}, and environment geometry/light direction from {environment IDs}. Camera: {framing/lens/angle}. Blocking: {positions, gaze, hands, action state}. Environment: {time/weather/background}. Lighting: {source/direction/quality}. {style/quality}. no extra characters, no identity drift, no costume or prop-state change, no unintended text, no watermark.
```

## 7. Image-to-Video / Text-to-Video 镜头

明确分开运动维度。

```text
cinematic {duration}s video shot for {shot ID}, {final aspect ratio}. Starting from {start-frame ID}; end on {end-frame ID if used}. Preserve exact character identity, wardrobe/state, prop marks/state, environment geometry, palette, and lighting direction from {reference IDs}.

Subject motion: {one clear action sequence}.
Camera motion: {dolly/pan/tilt/orbit/handheld/static}.
Environment motion: {rain/dust/cloth/crowd/light}.
Timing: {0-1s}, {1-3s}, {final second}.
End state: {editable final state}.
Constraints: no identity drift, no costume change, no prop morphing, no extra limbs, no camera teleport, no unrequested scene cut, no text, no logo.
```

优先 3-6 秒。拆分多节拍动作。对强状态变化或 blocking 变化使用 start/end frames。

## 8. 色卡/风格 Bible

当许多资产共享同一种视觉语言时使用。

- 定义故事控制的颜色、材质、反差、颗粒、镜头行为、皮肤处理和光线规则。
- 当叙事时期或地点色彩不同，分开说明。
- 色块保持平面，标签受控；如果需要精确可读，手动创建标签。
- 不要让风格 bible 覆盖最终镜头画幅。

## 9. QC 与跑歪修复

只检查可观察标准：

- 身份和家庭相似性；
- 年龄与年代；
- 比例与尺寸；
- 服装/状态 ID；
- 材质、色卡和精确标记位置；
- 环境几何和光线方向；
- 布局/画幅；
- 相邻镜头连续性；
- 关键文字准确性/合成准备度。

常用强化句：

- Identity drift: `preserve the exact same individual and mandatory facial anchors from the provided identity reference`.
- Inconsistent sheet: `same individual/object in every panel, identical placement of every recognition mark`.
- Wrong scale/owner: 重复精确尺寸、归属者和拿取方式；禁止混淆物品。
- Too modern/clean: `period-accurate, weathered, repaired, practical, not factory-new`.
- Missing signature mark: 把标志性特征移到主体第一句，并声明 mandatory。
- Video drift: `no identity, wardrobe, material, color, damage-placement, or environment-layout changes`.
- Extra text: `no text, labels, subtitles, logos, or watermark`; 把文字留给受控后期合成。
