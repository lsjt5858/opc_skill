---
name: ai-shortdrama-asset-imagegen
description: Use when a completed short-drama script, story outline, or shot list needs core still-image assets or image-generation prompts, including character sheets, story keyframes, emotional close-ups, detail inserts, scenes, or key props.
---

# AI 短剧核心图片资产生成

## 核心原则

在剧本完成后，把叙事信息转成可生成、可复用、可追踪的核心图片资产。

**故事决定资产，剧本决定风格。** 不预设仙侠、写实、动漫、电影感、冷暖色、媒介、画幅、镜头、颗粒或清晰度；把视觉风格统一写入 `STYLE_PROFILE`，根据剧本与用户要求逐项解析。

本 Skill 只负责静态图片资产规划与提示词，不负责改写剧本、设计完整视频分镜或生成剪辑方案。

## 输入边界

需要以下任一种输入：完整剧本、完整故事梗概、已完成的分镜文本或镜头清单。

可选输入：目标生图平台、发布平台、画幅、分辨率、已有角色参考图、品牌或艺术指导、禁用元素。

若没有任何故事文本，先索取剧本。剧本已足够时，不因次要外貌、材质、光源或镜头参数反复追问；做最小必要推断，并在资产表中标记 `推断`。影响全片视觉方向的重大缺口才询问用户。

## 强制规则

1. 禁止设置固定风格后缀。不得自动加入具体艺术流派、题材风格、冷暖倾向、渲染媒介、胶片颗粒、镜头语言、画幅、分辨率或质量词。
2. 每个风格结论必须能追溯到用户要求、剧本文本或明确标注的制作推断。
3. 题材不等于视觉风格。例如古代题材不自动等于水墨，科幻题材不自动等于写实，爱情题材不自动等于暖色。
4. 全片共用 `STYLE_PROFILE`；单张资产只能通过 `ASSET_STYLE_OVERRIDE` 增补本图需要的变化，不能悄悄改写全片风格。
5. 角色、场景和关键道具必须建立一致性锁。重复出现时逐字复用，不改写同义词、顺序和关键特征。
6. 剧情关键帧必须表现一个明确事件、动作、冲突或信息变化，不能只生成无叙事作用的海报。
7. 特写与细节图必须绑定剧情功能，例如情绪转折、线索揭示、伤痕、材质、符号或角色关系。
8. 三视图、T-pose、Depth、HDRI、白底 turnaround 都是选配技术资产；只有用户或后续制作流程需要时才生成。
9. 输出中的提示词必须展开所有变量，不得保留 `{{PLACEHOLDER}}`。
10. 提示词语言跟随用户或平台要求；未指定时使用中文结构化提示词，必要的行业术语可保留英文。

## 1. 剧本解析

先提取：

- 故事类型、时代、地域、世界规则、核心冲突、情绪曲线。
- 主要角色、关系、外观证据、服装变化、标志性特征。
- 主要场景、时间、天气、空间关系、重复出现的视觉锚点。
- 关键道具、线索、伤痕、服装部件、环境细节及其剧情功能。
- 起因、升级、转折、高潮、结果中的关键视觉时刻。

每项信息标记来源：

- `明确`：剧本或用户直接给出。
- `推断`：为可生成性做的最小补全。
- `待确认`：会显著改变世界观、人物身份或全片视觉方向。

## 2. 构建视觉方向变量

先输出一份 `STYLE_PROFILE`，按以下字段填写。字段无依据时写 `未指定`，不要用个人偏好补成固定风格。

```text
STYLE_PROFILE
- Narrative genre: {{故事类型与叙事情绪}}
- World and period: {{时代、地域、文化与世界规则}}
- Visual medium: {{摄影、插画、绘画、三维渲染、拼贴等}}
- Art direction: {{整体美术方向}}
- Realism and stylization: {{写实程度与造型夸张度}}
- Color system: {{主色、辅色、强调色、饱和度与对比关系}}
- Lighting system: {{光源逻辑、光质、方向、明暗关系}}
- Texture and material language: {{材质、表面、颗粒、介质特征}}
- Atmosphere: {{天气、空气、空间与情绪氛围}}
- Composition language: {{构图密度、留白、秩序、视觉重心}}
- Camera language: {{视角、景别、镜头感与运动暗示}}
- Graphic and layout language: {{设定集、档案板等平面版式规则}}
- Delivery spec: {{横竖版、比例、分辨率及平台限制}}
- Global negative constraints: {{根据目标风格与模型风险生成的负面约束}}
- Evidence: {{对应的用户要求或剧本证据；推断必须注明}}
```

解析优先级：

1. 用户明确的视觉要求。
2. 剧本明确描写。
3. 跨场景可验证的叙事情绪和世界规则。
4. 为制作连续性做的最小推断，并标记原因。

不要把示例提示词中的具体风格词复制进 `STYLE_PROFILE`。示例只提供结构，不提供默认审美。

## 3. 建立一致性锁

### Character DNA

每个主要或重复角色只写一次，后续逐字复用：

```text
CHARACTER_DNA: {{性别与年龄感}}, {{脸型与五官}}, {{发型与发色}}, {{肤色与皮肤特征}}, {{体型与姿态}}, {{本阶段固定服装}}, {{长期标志性特征}}
```

一次性手持物、临时伤势和单场服装变化不写入基础 DNA，改写入对应资产的 `STORY_STATE`。

### Scene DNA

```text
SCENE_DNA: {{空间类型与结构}}, {{时代地域特征}}, {{固定陈设与地标}}, {{材质系统}}, {{固定光源逻辑}}, {{空间色彩关系}}
```

### Prop DNA

```text
PROP_DNA: {{道具类型与比例}}, {{轮廓}}, {{材质}}, {{颜色}}, {{固定标记}}, {{磨损与状态}}, {{剧情识别点}}
```

## 4. 规划核心资产

根据剧本价值选择资产，不按固定数量机械凑图。

| 资产类型    | 何时生成                   | 核心目的                                     |
| ------- | ---------------------- | ---------------------------------------- |
| 角色设定集   | 主要角色或需保持一致的角色          | 锁定身份、造型、服装、表情、材质和道具关系                    |
| 剧情关键帧   | 起因、转折、高潮、揭示或关系变化       | 呈现故事事件与情绪变化                              |
| 情绪特写    | 表情、眼神、伤势或反应承担叙事时       | 锁定微表情与心理状态                               |
| 动作/手部特写 | 触碰、抓握、交换、书写、操作等动作关键时   | 呈现动作信息与角色关系                              |
| 细节图     | 线索、服饰、伤痕、纹样、材质或环境细节重要时 | 让观众看清剧情信息                                |
| 场景锚点图   | 场景重复出现或决定叙事气氛时         | 锁定空间、时间、天气和光源                            |
| 关键道具图   | 道具推动情节、承载情感或反复出现时      | 锁定外观、状态及识别点                              |
| 技术参考图   | 三维、合成或角色库流程明确需要时       | 提供三视图、T-pose、Depth、HDRI、turnaround 等制作资料 |

资产优先级：

- `P0`：缺失会导致故事读不懂或角色无法保持一致。
- `P1`：显著增强情绪、线索或空间连续性。
- `P2`：用于后续制作便利，可选。

每项资产都写明：`资产 ID / 类型 / 优先级 / 对应剧情 / 生成目的 / 一致性锁 / 画幅 / 状态变化`。

## 5. 通用提示词框架

所有提示词按下列模块组装。模块可按资产需要增减，但顺序保持清晰：

```text
{{ASSET_TYPE_AND_PURPOSE}}

主体与叙事：{{SUBJECT}}, {{STORY_EVENT}}, {{ACTION}}, {{EMOTION}}, {{RELATIONSHIP}}, {{STORY_STATE}}

一致性：{{CHARACTER_DNA / SCENE_DNA / PROP_DNA，逐字复用}}

造型与材质：{{COSTUME}}, {{HAIR_AND_MAKEUP}}, {{PROPS}}, {{MATERIALS}}, {{WEAR_AND_DAMAGE}}

构图与镜头：{{ORIENTATION}}, {{ASPECT_RATIO}}, {{SHOT_SIZE}}, {{ANGLE}}, {{LENS_OR_PERSPECTIVE}}, {{FOCAL_HIERARCHY}}, {{NEGATIVE_SPACE}}

环境与光线：{{LOCATION}}, {{TIME}}, {{WEATHER}}, {{BACKGROUND}}, {{LIGHT_SOURCE}}, {{LIGHT_DIRECTION}}, {{LIGHT_QUALITY}}

风格变量：{{完整展开 STYLE_PROFILE}}

本图变化：{{ASSET_STYLE_OVERRIDE；没有则省略}}

交付参数：{{PLATFORM}}, {{RESOLUTION}}, {{SAFE_AREA}}, {{TEXT_POLICY}}, {{QUALITY_REQUIREMENTS}}

Negative: {{GLOBAL_NEGATIVE_CONSTRAINTS + 本图特有风险；不得用负面词偷偷指定另一种风格}}
```

不要堆叠空泛质量词。每个词都应服务于叙事、连续性、可读性或交付要求。

## 6. 资产模板

以下模板抽取自复杂角色设定集提示词的结构。占位符必须根据当前剧本重写；不得继承示例题材或风格。

### A. 完整角色设定集

```text
一张完整的 {{CHARACTER_NAME}} 角色设定集，{{ORIENTATION}} {{ASPECT_RATIO}} 构图，professional character design sheet，{{PROJECT_USE}}。

角色设定：{{CHARACTER_DNA}}。本阶段状态：{{STORY_STATE}}。补充体态、气质、表情基线与角色关系造成的可见影响。

服装与材质：{{COSTUME_LAYERS}}，{{COLOR_RELATIONSHIP}}，{{FABRICS_AND_MATERIALS}}，{{CONSTRUCTION_DETAILS}}，{{WEAR_STATE}}。

版式结构：主视觉区展示 {{HERO_PORTRAIT_OR_FULL_BODY}}；视图区展示 {{REQUIRED_VIEWS}}；表情区展示 {{SCRIPT_RELEVANT_EXPRESSIONS}}；服饰拆解区展示 {{COSTUME_COMPONENTS}}；配饰与道具区展示 {{SIGNATURE_ITEMS}}；色彩区展示 {{SCRIPT_DERIVED_PALETTE}}；材质区展示 {{MATERIAL_CLOSEUPS}}；预留 {{TITLE_AND_INFO_POLICY}}。

环境与光线：{{BACKGROUND_LOGIC}}，{{LIGHTING_LOGIC}}。

风格变量：{{EXPANDED_STYLE_PROFILE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

设定集不强制左/右版式、三视图、T-pose、色卡数量或文字标签；根据角色复杂度和用途决定。若精确文字不是重点，使用干净标签区并建议后期排字，避免让生图模型承担大量准确文字。

### B. 剧情关键帧

```text
剧情关键帧，表现“{{BEAT_NAME}}”：{{CHARACTER_OR_SUBJECT}} 在 {{LOCATION}} 中 {{DECISIVE_ACTION}}，事件发生前的状态是 {{BEFORE_STATE}}，画面瞬间发生的变化是 {{TURNING_POINT}}，可见结果是 {{AFTER_STATE}}。角色核心情绪为 {{EMOTION}}，通过 {{FACE_BODY_GESTURE}} 呈现；关键剧情信息 {{STORY_CLUE}} 必须清晰可读。

一致性：{{EXACT_DNA_LOCKS}}。

构图与镜头：{{SHOT_SIZE_AND_ANGLE}}，{{FOCAL_HIERARCHY}}，前景 {{FOREGROUND}}，中景 {{MIDGROUND}}，背景 {{BACKGROUND}}，{{SPATIAL_RELATIONSHIP}}。

光线与环境：{{TIME_WEATHER_LIGHTING}}。

风格变量：{{EXPANDED_STYLE_PROFILE}}。本图变化：{{ASSET_STYLE_OVERRIDE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

### C. 面部情绪特写

```text
{{CHARACTER_NAME}} 的面部情绪特写，发生在 {{BEAT_NAME}}，{{SHOT_SIZE}}，{{VIEW_ANGLE}}。必须保持：{{EXACT_CHARACTER_DNA}}。当前情绪不是抽象标签，而是 {{INNER_CONFLICT}} 造成的 {{MICRO_EXPRESSION}}：{{EYES}}，{{BROWS}}，{{MOUTH}}，{{BREATHING}}，{{TEARS_SWEAT_DUST_OR_INJURY}}。视线落点为 {{GAZE_TARGET}}，背景只保留 {{MINIMUM_CONTEXT}}，焦点落在 {{NARRATIVE_FOCUS}}。

光线：{{FACE_LIGHTING}}。风格变量：{{EXPANDED_STYLE_PROFILE}}。本图变化：{{ASSET_STYLE_OVERRIDE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

### D. 手部、服饰、线索与材质细节图

```text
剧情细节图，展示 {{DETAIL_SUBJECT}} 在 {{BEAT_NAME}} 中的 {{CURRENT_STATE}}。画面必须清楚呈现 {{NARRATIVE_EVIDENCE}}、{{MATERIAL_STRUCTURE}}、{{SURFACE_TEXTURE}}、{{WEAR_DAMAGE_STAIN}}、{{CONTACT_OR_FORCE}} 及其与 {{RELATED_CHARACTER_OR_PROP}} 的关系。{{MACRO_OR_INSERT_COMPOSITION}}，{{DEPTH_AND_FOCUS_LOGIC}}，保留足够环境线索以说明它为何重要，但不喧宾夺主。

一致性：{{EXACT_DNA_LOCKS}}。光线：{{DETAIL_LIGHTING}}。风格变量：{{EXPANDED_STYLE_PROFILE}}。本图变化：{{ASSET_STYLE_OVERRIDE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

### E. 场景锚点图

```text
{{SCENE_NAME}} 场景锚点图，叙事功能是 {{SCENE_FUNCTION}}。一致性：{{EXACT_SCENE_DNA}}。展示 {{SPATIAL_LAYOUT}}、{{ENTRANCES_EXITS}}、{{LANDMARKS}}、{{MATERIAL_SYSTEM}}、{{TIME_WEATHER}} 与 {{FIXED_LIGHT_SOURCES}}。构图必须为后续角色调度保留 {{BLOCKING_SPACE}}，并让 {{STORY_RELEVANT_ZONE}} 成为视觉锚点。

风格变量：{{EXPANDED_STYLE_PROFILE}}。本图变化：{{ASSET_STYLE_OVERRIDE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

### F. 关键道具图

```text
{{PROP_NAME}} 关键道具资产图，剧情功能为 {{PROP_FUNCTION}}。一致性：{{EXACT_PROP_DNA}}。重点展示 {{IDENTIFYING_FEATURES}}、{{MATERIALS}}、{{CONSTRUCTION}}、{{CURRENT_DAMAGE_OR_CHANGE}} 与 {{CLUE}}。视图采用 {{VIEW_SET}}，比例参照 {{SCALE_REFERENCE}}；如需角色交互，增加 {{HAND_OR_BODY_INTERACTION}}，并逐字复用对应 Character DNA。

风格变量：{{EXPANDED_STYLE_PROFILE}}。本图变化：{{ASSET_STYLE_OVERRIDE}}。

交付要求：{{EXPANDED_DELIVERY_SPEC}}。

Negative: {{RESOLVED_NEGATIVE_CONSTRAINTS}}
```

## 7. 输出结构

按以下顺序交付：

1. `===== 剧本视觉解析 =====`：故事、角色、场景、关键道具、视觉时刻及信息来源。
2. `===== STYLE_PROFILE =====`：完整视觉变量与推断依据。
3. `===== 核心资产清单 =====`：资产 ID、类型、优先级、对应剧情、用途、画幅、状态。
4. `===== 一致性锁 =====`：Character DNA、Scene DNA、Prop DNA。
5. `===== 图片资产提示词 =====`：每项资产一个独立提示词代码块。
6. `===== 资产索引 =====`：覆盖所有已规划资产。

资产 ID 使用大写字母、数字、下划线和版本号：

- 角色：`CHAR_<NAME>_V1`
- 剧情关键帧：`STORY_<BEAT>_V1`
- 特写：`CLOSEUP_<SUBJECT>_<BEAT>_V1`
- 细节：`DETAIL_<SUBJECT>_<BEAT>_V1`
- 场景：`SCENE_<NAME>_V1`
- 道具：`PROP_<NAME>_V1`

资产索引列名：

| 资产 ID  | 类型     | 优先级    | 对应剧情   | 一致性锁   | 画幅     | 文件名    | 用途     |
| ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| <br /> | <br /> | <br /> | <br /> | <br /> | <br /> | <br /> | <br /> |

## 常见错误

| 错误                         | 修正                                        |
| -------------------------- | ----------------------------------------- |
| 把示例中的仙侠、国风、冷色或水墨词沿用到新项目    | 只复用模板结构，重新从剧本解析 `STYLE_PROFILE`           |
| 所有项目统一加电影感、胶片颗粒、暖色或固定清晰度   | 删除固定后缀，把媒介、色彩、质感和交付规格变量化                  |
| 所有资产统一使用同一画幅               | 根据发布平台和资产用途解析 `Delivery spec`             |
| 角色设定集只换姓名，其他外貌仍来自示例        | 从当前剧本重建 Character DNA、服装、材质和版式内容          |
| 关键帧像海报，没有事件变化              | 写清 before / turning point / after 与可见剧情信息 |
| 情绪特写只写“悲伤、愤怒”              | 拆成眼神、眉、嘴、呼吸、视线和身体反应                       |
| 细节图只是漂亮微距                  | 明确线索、材质、破损、接触关系及剧情功能                      |
| 未经要求强制输出 T-pose、Depth、HDRI | 仅在后续制作流程明确需要时作为 P2 资产加入                   |
| 提示词仍保留占位符                  | 输出前把所有变量展开；无内容的可选模块直接删除                   |

## 最终自检

- [ ] `STYLE_PROFILE` 的每项结论都有用户、剧本或已标注推断作为依据。
- [ ] 没有把任何示例风格当作全局默认值。
- [ ] 没有固定画幅、分辨率、镜头、后处理或质量后缀。
- [ ] 每个主要角色、重复场景和关键道具都有唯一一致性锁。
- [ ] 每个关键剧情转折至少由一个核心资产承载。
- [ ] 情绪特写和细节图都能指出明确剧情功能。
- [ ] 技术资产只在确有制作需求时生成。
- [ ] 所有提示词已展开变量，没有遗留 `{{...}}`。
- [ ] 所有资产均进入索引，文件名和 ID 唯一。

