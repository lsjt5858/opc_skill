# 完整交付 Schema

仅在用户要求结构化项目文件、完整制作包或交接其他工具时使用。字段为空且对当前阶段无用时可省略。

```yaml
project_state:
  project:
    title: null
    logline: null
    theme: null
    format: short_film
    genre: []
    duration: null
    episode_count: 1
    aspect_ratio: null
    language: zh-CN
    target_audience: null

  source_material:
    - source_id: SRC-01
      type: concept|outline|script|reference|revision
      summary: null

  confirmed_facts: []
  assumptions: []
  open_questions: []

  script_breakdown:
    characters:
      - id: CHAR-01
        name: null
        role: null
        relationships: []
        goal: null
        obstacle: null
        secret: null
        arc: null
    scenes:
      - scene_instance_id: SCENEINST-01
        scene_id: SCENE-01
        heading: null
        interior_exterior: INT|EXT
        time: null
        weather: null
        characters: []
        objects: []
        dramatic_function: null
    objects:
      - id: OBJ-01
        name: null
        owner: null
        narrative_function: null
        first_appearance: null
        state_changes: []
    beats:
      - id: BEAT-01
        scene_instance_id: SCENEINST-01
        event: null
        cause: null
        consequence: null
        audience_information: null
    timeline: []
    emotion_beats: []
    key_moments: []

  visual_bible:
    world:
      era: null
      country: null
      region: null
      season: null
      weather: null
      time_pattern: null
    genre:
      primary: null
      secondary: []
      realism_level: null
    camera:
      lens_tendency: []
      depth_of_field: null
      camera_height: null
      stability: null
      movement_rule: null
      viewpoint: null
    composition:
      rules: []
      recurring_motifs: []
    color:
      primary: []
      secondary: []
      accent: []
      saturation: null
      contrast: null
      narrative_arc: []
    lighting:
      source: null
      direction: null
      softness: null
      color_temperature: null
      day_night_rules: []
    material:
      dominant: []
      texture_rules: []
    aspect_ratio: null
    post_process:
      medium: film|digital|documentary|news
      grain: null
      sharpness: null
      black_level: null
      highlight_rolloff: null
    do: []
    avoid: []

  character_bibles:
    - id: CHAR-01
      identity: {}
      appearance: {}
      behavior_signature: {}
      speech: {}
      psychology: {}
      arc_states: []
      looks:
        - look_id: CHAR-01-LOOK-01
          costume: {}
          accessories: []
          grooming: null
          story_range: []
      invariants: []
      allowed_changes: []
      forbidden_drift: []

  scene_bibles:
    - id: SCENE-01
      identity: {}
      dimensions: null
      layout: {}
      fixed_landmarks: []
      furniture: []
      materials: []
      palette: []
      practical_lights: []
      natural_light_direction: null
      ambient_sound: []
      age_marks: []
      states:
        - state_id: SCENE-01-STATE-01
          time: null
          weather: null
          condition: null
      invariants: []
      forbidden_drift: []

  object_bibles:
    - id: OBJ-01
      identity: {}
      era: null
      brand_style: null
      dimensions: null
      material: []
      color: []
      structure_details: []
      wear_marks: []
      owner: null
      states:
        - state_id: OBJ-01-STATE-01
          condition: null
          visible_content: null
      required_views: []
      invariants: []
      forbidden_drift: []

  narrative_plan:
    asset_priority:
      A: []
      B: []
      C: []
    story_importance:
      - beat_id: BEAT-01
        stars: 5
        reason: null
        audience_payload: null
    emotion_curve:
      - beat_id: BEAT-01
        character_id: CHAR-01
        surface_emotion: null
        underlying_emotion: null
        level: 1
        visible_cues: []
    shot_strategy: []

  shot_plan:
    - shot_id: SHOT-001
      scene_instance_id: SCENEINST-01
      beat_id: BEAT-01
      duration_seconds: null
      importance: null
      size: null
      angle: null
      viewpoint: null
      lens_intent: null
      movement: null
      composition: null
      action: null
      dialogue: null
      sound: null
      emotion: null
      dependencies: []
      continuity_in: []
      continuity_out: []
      transition: null

  prompt_packages:
    character_prompts: []
    scene_prompts: []
    object_prompts: []
    keyframe_prompts: []
    closeup_prompts: []
    storyboard_prompts: []
    pre_video_shot_prompts: []

  continuity_locks:
    - id: LOCK-01
      target_id: null
      invariants: []
      allowed_changes: []
      forbidden_drift: []
      current_state: null

  revision_log:
    - revision_id: REV-01
      request: null
      changed: []
      preserved: []
      impacted_outputs: []
```
