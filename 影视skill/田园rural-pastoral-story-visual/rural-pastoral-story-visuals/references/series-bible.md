# 系列资产与去重记忆

## 用途

跨集保持人物、地点、道具一致，并防止场景重复。建议在项目目录维护 `series-bible.json`，每完成一集更新一次。

## 结构

```json
{
  "series": "山村四时",
  "season": 1,
  "region": "江南水乡",
  "characters": [
    {
      "id": "pian_jiang",
      "role": "篾匠师傅",
      "age_range": "50-60",
      "gender": "男",
      "appearance": "花白短发，深褐皮肤，右手有旧疤",
      "costume": "靛蓝对襟粗布褂，深灰裤，草鞋",
      "skills": ["竹编", "扎灯"],
      "relations": {"xue_tu": "师徒"}
    }
  ],
  "locations": [
    {"id": "citang", "name": "祠堂晒场", "features": "石板地、旗杆、木梁"}
  ],
  "props": [
    {"id": "yu_deng", "name": "鱼灯", "state": "已修复点亮", "episode": 1}
  ],
  "episodes": [
    {
      "number": 1,
      "title": "灯火渡溪",
      "solar_term": "秋分",
      "hook": "水面漂来陌生小灯",
      "scenes": [
        {"id": "01", "location": "沿河街巷", "action": "雾中待集",
         "people": "0", "relationship": "无人空镜", "prop": "未点街灯"}
      ]
    }
  ]
}
```

## 更新规则

1. 人物首次出现时登记，后续只引用不重写设定。
2. 道具状态只能按剧情前进，不得无故回退。
3. 地点特征变化必须写明原因，例如修缮、洪水、新建。
4. 每集登记 `hook`，下一集必须回应或明确延后。
5. 季末检查未回收的钩子。

## 去重检查

新集规划完成后，与历史 `scenes` 比对四元组：`location + action + relationship + prop`。

- 四项全同：必须更换。
- 三项相同：需更换主动作或人物关系。
- 两项相同：允许，但要求景别或时间不同。

使用 `scripts/check_storyboard.py` 校验单集，使用 `--history` 参数传入历史剧集文件可自动比对跨集重复。

## 人物出场平衡

- 主角连续出场不超过5集不变化状态；应安排学习、失败、成长或关系变化。
- 每季至少引入2位新角色，并给出明确来意。
- 群像集需给3位以上可辨识配角安排具体动作，而非纯背景。
