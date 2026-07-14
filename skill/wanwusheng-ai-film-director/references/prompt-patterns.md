# 万物生提示词模式

仅在交付规格和关键连续性锚点一致后使用这些模式。

## 目录

1. 核心提示词结构
2. 交付格式
3. 角色资产
4. 道具资产
5. 环境资产
6. 分镜与关键帧
7. 视频镜头
8. 配色/风格设定集
9. 质量控制与重抽修复

## 1. 核心提示词结构

每个提示词资产都应包含：

- `资产 ID/标题`：稳定 ID、项目/段落、主体、版本；
- `用途/依赖`：使用它的下游镜头/资产；
- `格式`：参考设定表格式或最终交付比例；
- `主体`：身份、轮廓、比例、材质、颜色、故事角色；
- `连续性 DNA`：重复的身份、标记、服装、配色和参考；
- `构图`：视角、取景、布局、背景、位置；
- `布光`：方向、质感、色温；
- `风格/质量`：可见的制作特征；
- `约束条件`：可能出错的类别或不需要的元素；
- `质量控制`：可检查的验收标准；
- `重抽修复`：仅针对可能失败的强化语句。

## 2. 标准交付格式

````text
=== {模型/任务} 提示词 - {资产 ID} {资产名称} v1 ===

【用途与依赖】
- {为何存在；哪些资产/镜头引用它}

【格式】
- {画幅比例、面板布局、输出类型}

【连续性】
- {锁定的身份/材质/状态/光线锚点和参考资产 ID}

【prompt】
```text
{英文可执行提示词}
```

【QC】
- {可观察的通过/失败检查}

【跑歪修复】
- {失败类型} -> "{英文强化语句}"
````

## 3. 角色资产

不要将所有角色需求合并到一张设定表中。

### 中性身份 / 转面设定表

用于锁定角色身份。

必需项：

- 中性站姿和中性表情；
- 正面、正侧面、背面、3/4 全身视角；
- 布局允许时，面部特写或识别细节面板；
- 每个面板中都是同一个人，比例、头发、服装和标记一致；
- 素净摄影棚背景和受控中性布光；
- 无戏剧性故事动作。

```text
a production identity turnaround sheet for {角色 ID/姓名}. {参考设定表比例和网格}. same individual in every panel with identical facial structure, body proportions, hairstyle, costume, accessories, and recognition marks. panels show front full body, true side full body, back full body, and right-front 3/4 full body; include a separate neutral face close-up if requested. neutral standing pose, arms relaxed and visible, plain studio backdrop, soft neutral reference lighting.

Identity: {年龄、出身、体型、面部锚点、头发、皮肤、职业线索}. Mandatory recognition features: {特征}. Costume/state: {服装 ID 和精确材质/颜色}.

Constraints: no sitting, no crying, no running, no cinematic scene, no pose change between orthographic views, no identity drift, no extra text, no watermark.
```

### 表情设定表

仅在身份锁定后使用。

- 固定头部角度或受控的正面/3/4 面对组合；
- 4-6 种与剧本节奏点关联的命名情绪；
- 相同的头发、衣领、光线和面部比例；
- 避免与故事无关的通用情绪网格。

```text
an expression reference sheet for the exact same {角色 ID/姓名} from the provided identity reference. {面板数量} equal face close-up panels: {剧本特定表情}. preserve identical facial structure, age, hairstyle, skin texture, costume collar, camera distance, and neutral studio lighting. expressions are natural and restrained unless the script requires otherwise. no identity drift, no different person, no full-body action, no text except optional panel labels.
```

### 姿势 / 动作设定表

用于高难度或反复出现的动作，而非每个细微手势。

```text
an action-pose reference sheet for the exact same {角色 ID/姓名} in {服装 ID}. panels show {不同的剧动作，具有清晰的起始/结束身体力学}. preserve identity, proportions, costume, dominant hand, carried props, and injury side. clean neutral background, readable full body and hands, practical anatomy. no environment storytelling, no costume change, no extra limbs.
```

### 服装 / 状态设定表

用于服装、年龄、受伤、天气、污渍或转变变体。

说明什么保持不变，什么变化。为每个状态分配稳定 ID，如 `C01-W01` 或 `C01-ST02`。

### 细节设定表

用于必须在特写镜头中保留的面部锚点、手部、疤痕、珠宝、妆容、鞋类或操作细节。

### 覆盖优先级

- 主角：完整身份、面部/细节、服装/状态、表情、高难度动作。
- 反复出现的配角：正面/3/4 面、面部、主要服装、所需表情/动作。
- 一次性角色：紧凑选角卡。

## 4. 道具 / 设备设定表

当一个物品反复出现、改变状态、承载证据或必须一致使用时使用。

必需项：

- 精确尺寸和持有者/使用逻辑；
- 正面/侧面/顶面/3/4 面或相关正交视图；
- 固定的材质、扣件、磨损、污渍、铭文、可动部件；
- 打开、破损、湿润、包扎或损坏时的独立状态变体；
- 与相似故事物品的明确对比。

```text
a production prop reference sheet for {道具 ID/名称}. {布局}. same exact object in every panel. dimensions: {尺寸}. owner and handling: {逻辑}. materials/colors: {锁定值}. mandatory recognition marks: {精确位置}. state: {状态 ID}. show {视图/细节}. practical prop photography, neutral background, controlled light. not {易混淆物品}, no changed damage placement, no extra text, no watermark.
```

对于精确的收据、信件、屏幕、标签或证据文字：生成没有关键文字的物理表面，然后合成经过验证的排版。提示词可以预留干净的文字区域，但绝不能假装生成的文字是可靠的。

## 5. 环境设定表

在有人物的故事帧之前，将反复出现的地点作为空场景创建。

必需项：

- 比例与功能；
- 主全景和主要/反打覆盖；
- 几何关系重要时的俯视/空间关系；
- 入口、出口、窗户、门、家具、危险区域、核心道具区域；
- 材质、时期、年代、天气和光线方向；
- 跨面板的相同布局。

```text
a production environment reference sheet for {环境 ID/名称}, empty set with no story characters. {布局}: master wide, primary shooting direction, reverse direction, and key-zone detail/top-down relation. preserve identical architecture, door/window/furniture positions, materials, period details, and navigation paths in all panels. scale/function: {细节}. lighting/weather state: {状态 ID 和方向}. practical cinematic production design, spatially coherent, no unexplained layout changes, no readable incidental text, no watermark.
```

## 6. 分镜与关键帧

### 分镜面板

使用低成本面板验证覆盖、调度、视线、画面方向和剪辑节奏。身份完美不是必需的，除非影响理解。

### 关键帧静帧

在参考锁定后用于最终镜头时刻。

必需项：

- 镜头 ID 和故事目的；
- 最终交付比例；
- 身份、服装/状态、道具和环境的参考 ID；
- 摄影机/镜头感觉、角度、距离、取景、景深；
- 演员调度、视线、动作状态和屏幕位置；
- 环境、天气和明确的光线方向；
- 成对使用时的起始或结束标记。

```text
cinematic keyframe for {镜头 ID}, {最终画幅比例}. Story purpose: {节奏点}. Preserve the exact identity and recognition features from {角色参考}, wardrobe/state from {状态 ID}, prop design/state from {道具 ID}, and environment geometry/light direction from {环境 ID}. Camera: {取景/镜头/角度}. Blocking: {位置、视线、手部、动作状态}. Environment: {时间/天气/背景}. Lighting: {光源/方向/质感}. {风格/质量}. no extra characters, no identity drift, no costume or prop-state change, no unintended text, no watermark.
```

## 7. 图生视频 / 文生视频镜头

明确区分运动维度。

```text
cinematic {时长}s video shot for {镜头 ID}, {最终画幅比例}. Starting from {起始帧 ID}; end on {结束帧 ID 如使用}. Preserve exact character identity, wardrobe/state, prop marks/state, environment geometry, palette, and lighting direction from {参考 ID}.

Subject motion: {一个清晰的动作序列}.
Camera motion: {推轨/摇摄/俯仰/环绕/手持/固定}.
Environment motion: {雨/灰尘/布料/人群/光线}.
Timing: {0-1秒}, {1-3秒}, {最后一秒}.
End state: {可编辑的最终状态}.
Constraints: no identity drift, no costume change, no prop morphing, no extra limbs, no camera teleport, no unrequested scene cut, no text, no logo.
```

优先使用 3-6 秒。拆分多节奏动作。对于强烈的状态或调度变化使用起始/结束帧。

## 8. 配色 / 风格设定集

当许多资产共享一种视觉语言时使用。

- 定义故事控制的颜色、材质、对比度、颗粒感、镜头行为、皮肤处理和光线规则。
- 当不同叙事时期或地点的配色不同时进行区分。
- 保持色板平整和标签受控；如果精确可读性很重要，手动创建标签。
- 不要让风格设定集覆盖最终镜头画幅比例。

## 9. 质量控制与重抽修复

仅检查可观察的标准：

- 身份与家族相似性；
- 年龄与时期；
- 比例与尺度；
- 服装/状态 ID；
- 材质、配色和精确标记位置；
- 环境几何与光线方向；
- 布局/画幅；
- 相邻镜头连续性；
- 关键文字准确性/合成就绪度。

常见强化语句：

- 身份漂移：`preserve the exact same individual and mandatory facial anchors from the provided identity reference`.
- 设定表不一致：`same individual/object in every panel, identical placement of every recognition mark`.
- 比例/持有者错误：重复精确尺寸、持有者和使用方式；禁止易混淆物品。
- 过于现代/干净：`period-accurate, weathered, repaired, practical, not factory-new`.
- 缺少标志性标记：将其移到主体第一句中并称之为强制性。
- 视频漂移：`no identity, wardrobe, material, color, damage-placement, or environment-layout changes`.
- 多余文字：`no text, labels, subtitles, logos, or watermark`；为受控合成预留文字。
