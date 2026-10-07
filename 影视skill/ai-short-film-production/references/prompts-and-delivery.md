# 提示词构建、依赖与交付

## Asset Dependency

默认顺序：

```text
Visual Bible
→ Character identity
→ Character looks / costume / accessories
→ Scene layout / fixed dressing
→ Object identity / states
→ Character sheets
→ Scene plates
→ Object sheets
→ Story keyframes / close-ups
→ Storyboard frames
→ Pre-video shot prompts
```

剧情图依赖角色、场景、道具和剧情状态。分镜依赖剧情图规则和镜头策略。前置资产未锁定时，可以输出“探索版”，但必须标注未锁项。

## Consistency Lock

为每项可复用资产生成简短锁：

```yaml
continuity_lock:
  id: LOCK-CHAR-01
  invariants: []
  allowed_changes: []
  forbidden_drift: []
  current_state: null
```

提示词应复述最关键的视觉锚点，不只写 `@[CHAR-01]`。若目标工具支持引用图、种子、角色参考或 LoRA，可以另列使用建议，但不要假设功能必然存在。

## 通用 Prompt Formula

按以下顺序组织，不必机械保留标签：

1. **用途**：角色设定图/场景概念图/道具设定图/剧情关键帧/分镜。
2. **主体锚点**：身份、外观、不变量、当前状态。
3. **动作与关系**：可见动作、人物距离、视线、道具交互。
4. **环境锚点**：Scene Bible 固定结构、时间、天气、生活痕迹。
5. **叙事意图**：观众此刻必须理解或感受到什么。
6. **情绪表演**：Level、表层/底层状态、具体身体证据。
7. **镜头语言**：景别、机位、视角、焦段意图、景深、运动起点/终点。
8. **视觉规则**：光线、颜色、材质、构图、画幅、后期。
9. **连续性状态**：服装、伤痕、道具状态、站位和动作接点。
10. **负面约束**：禁止漂移、错误时代元素、无动机美化、结构错误、文字乱码等。

## 提示词类型

### 角色设定图

Priority A 默认包含：正面全身、3/4 身、侧面、面部近景、行为签名、基础服装和关键剧情阶段造型。保持中性背景和可比较光线，避免概念图氛围遮蔽身份细节。

### 场景设定图

包含：建立视图、关键方位、固定家具/门窗、材质近景、主要昼夜状态。先保证空间连续性，再追求氛围。

### 道具设定图

包含：正反侧三视图或等效视角、手持比例、磨损细节、屏幕/按钮状态、状态变化。对于界面文字，优先把内容作为后期排版说明，避免生成模型随机文字。

### 剧情关键帧

引用明确的 `beat_id`、角色 look、scene state 和 object state。五星节点生成主构图，并在需要时给 1–2 个叙事目的不同的备选，不做纯审美变体。

### 特写

明确特写的叙事信息，例如“看见未接来电姓名为空”或“看见父亲拇指停在拨号键上”，而不是只写“电影感特写”。

### 分镜图

每条包含镜头 ID、时长建议、景别、角度、构图、动作、台词/声音提示、情绪、镜头衔接、连续性和图像提示词。分镜图以叙事清晰为先，可以比最终画面更简洁。

### 视频生成前镜头提示词

本 Skill 不生成视频，但可以交付单镜头提示词。每条应描述：

- 起始画面和结束画面。
- 单个主要动作与次要环境运动。
- 摄影机运动、速度、方向和停止点。
- 人物表演的微变化。
- 哪些元素必须静止或保持不变。
- 时长建议、画幅、帧率/运动质感（用户需要时）。
- 禁止瞬移、身份漂移、道具变形、额外人物、无动机镜头运动。

避免在一个短镜头中塞入多个场景切换或不可实现的连续事件。

## Prompt Package

标准交付：

```yaml
prompt_packages:
  character_prompts: []
  scene_prompts: []
  object_prompts: []
  keyframe_prompts: []
  closeup_prompts: []
  storyboard_prompts: []
  pre_video_shot_prompts: []
```

每条 Prompt 建议字段：

```yaml
- prompt_id: PROMPT-KF-001
  target: keyframe
  dependencies: [CHAR-01-LOOK-01, SCENE-01-STATE-NIGHT, OBJ-01-STATE-02]
  priority: A
  story_importance: 5
  narrative_goal: null
  positive_prompt_zh: null
  negative_prompt_zh: null
  continuity_checks: []
  unresolved: []
```

## Production Orchestrator

### 生成预算分配

- A 级 + 五星：完整设定、多视角、局部细节、状态变化和备选构图。
- A 级或四星：完整主视图与关键状态。
- B 级：标准主视图和必要引用。
- C 级：并入场景/镜头，不单独成包。

### 修改传播

当用户修改：

- Visual Bible：检查所有 Prompt 的摄影、颜色、光线、材质和后期。
- Character Bible：检查角色图、与其互动的道具图、关键帧与分镜。
- Scene Bible：检查场景图、其中所有关键帧、人物方位和光源。
- Object Bible：检查手持比例、状态变化、插入镜头和伏笔回收。
- 剧情节拍：重算重要度、情绪曲线和镜头顺序。

只重写受影响内容，并列“保留不变项”和“已更新项”。

## 最终交付清单

制作包模式检查：

1. 项目摘要与创作意图。
2. Script Breakdown 和时间线。
3. Visual Bible。
4. Character / Scene / Object Bible。
5. Asset Priority 与理由。
6. Story Importance 与关键观众信息。
7. Emotion Curve 与角色表演证据。
8. Shot Strategy 与完整镜头表。
9. 各类图像提示词。
10. 视频生成前单镜头提示词。
11. Consistency Locks、未解决项和连续性检查。
12. 推荐的资产生产顺序。

本 Skill 到此停止，不声称已出图或已生成视频。
