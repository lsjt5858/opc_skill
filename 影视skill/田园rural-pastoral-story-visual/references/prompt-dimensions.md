# 提示词维度体系

每条提示词都按固定六维度组装，保证同一系列可控、可替换、可批量。

## 维度总表

| 序号 | 维度 | 作用 | 示例 |
|---|---|---|---|
| 1 | 民族 | 决定服饰、建筑、礼俗系统 | 汉族、白族、侗族、藏族 |
| 2 | 地域 | 决定地貌、建筑、水土、物产 | 江南水乡、西南山地、关中平原 |
| 3 | 着装 | 决定形制、材质、颜色 | 宋制交领上襦配长裙、短褐、褙子 |
| 4 | 风俗与场景 | 决定空间和文化背景 | 江南的村庄、河埠头、社戏台、赶集 |
| 5 | 事件 | 决定动作与情绪 | 河流嬉戏玩耍、采莲、围炉夜话 |
| 6 | 人物结构 | 决定人数与关系 | 少女三人、母女、祖孙、村中群像 |

再叠加三项固定层：**氛围（惬意松弛）＋ 视觉（见 visual-style.md）＋ 参数**。

## 组装顺序

```
时间与季节 → 地域与具体空间 → 人物结构与着装 → 事件动作与受力 → 关键道具状态
→ 天气风向与光源 → 景别机位与前景遮挡 → 材质与空气感 → 情绪 → 色调 → 风格与负面约束 → 参数
```

中文提示词按此顺序写成一段；英文提示词按同一顺序自然重写，不逐字硬译。

## 民族与着装对应

| 民族 | 着装写法要点 | 注意 |
|---|---|---|
| 汉族 | 交领上襦、长裙、短褐、褙子、直裾；棉麻粗布 | 明确形制，不写"古装" |
| 其他民族 | 需指明具体民族与场合，区分日常装与节庆装 | 不混搭不同民族元素 |

未指定民族时默认汉族；未指定朝代时用"日常汉服"而非具体年号，避免形制错误。

## 地域与空间对应

| 地域 | 可用空间 |
|---|---|
| 江南水乡 | 河埠头、石拱桥、乌篷船、白墙黛瓦、莲塘、竹林、廊桥 |
| 西南山地 | 吊脚楼、梯田、山溪、竹桥、云雾山道、寨门 |
| 关中／华北 | 土院、晒场、麦田、砖窑、老槐树、集市 |
| 岭南 | 骑楼、榕树、河涌、荔枝园、龙舟埠 |
| 高原牧区 | 草场、经幡、石屋、河谷、羊群 |

## 事件库（惬意向）

优先使用有动作但无压迫感的事件：

- **水边**：河流嬉戏玩耍、浅溪泼水、洗菜淘米、采莲摘菱、垂足听风、放纸船、river 边洗发
- **田园**：采茶、摘果、晒谷、拾稻穗、喂鸡鹅、牵牛过田埂、追蝴蝶
- **市井**：赶集挑选、试戴头饰、买糖人、看杂耍、河埠交易
- **家常**：围坐吃饭、灶前添柴、廊下饮茶、缝补、编竹篮、剥莲子
- **节庆**：扎灯、放河灯、看社戏、荡秋千、簪花、投壶
- **休憩**：树下打盹、竹椅摇扇、雨天檐下看雨、夜里数星、并肩看晚霞

## 人物结构库

| 结构 | 适用 | 关系写法 |
|---|---|---|
| 空镜 | 空间、时间、余韵 | 无人物，写痕迹 |
| 单人 | 情绪高潮、独处惬意 | 明确动作与视线 |
| 双人 | 互动、说笑、协作 | 写清谁主动、谁反应 |
| 三人 | 群体轻松感最佳 | 三角构图，一人回头 |
| 母女／祖孙 | 温情 | 写年龄差与照护动作 |
| 孩童加成人 | 生活气息 | 孩童承担动态，成人承担情绪 |
| 村落群像 | 集市、节庆 | 主动作一个，辅助两三个，背景若干 |

## 中文提示词模板

```
[季节与时段]的[地域]，[民族]传统生活场景；[具体空间与建筑]，[人物结构、年龄、着装形制与颜色、材质]，[动作起点与受力过程]，[事件结果与情绪]，[关键道具状态]，[天气、风向、光源方向]，[景别、机位、前景遮挡、背景纵深]，[材质与空气感]，[色调]，惬意松弛的生活气息，东方古典美学，真实实拍电影感，自然柔光，浅景深，真实皮肤纹理，无文字，无水印[仅在目标平台明确且支持时追加平台参数]
```

## 英文提示词模板

```
[Subject with age, ethnicity, garment type, fabric and color] [specific action caught mid-motion] in [specific rural location with regional architecture], [time of day and light direction], [environmental motion: wind, mist, smoke, water], [foreground occlusion and depth], [emotion described through face and body], [color palette], authentic ancient Chinese countryside, natural skin texture, handmade fabric with real weight, cinematic live-action period film still, subtle film grain, shallow depth of field, soft volumetric sunlight, realistic photography, no text, no watermark [append platform parameters only when the target platform is known and supports them]
```

## 参考范例

用户已验证可用的写法，作为英文语感基准：

```
A young adult Chinese woman in a simple oatmeal linen hanfu pushes open an old wooden lattice window at dawn, seen from outside a rustic whitewashed farmhouse, cool morning mist drifting through a bamboo grove, warm sunrise touching her relaxed face, loose strands of black hair moving in the breeze, linen curtain billowing outward, dew sparkling on leaves in the foreground, quiet pastoral intimacy, muted sage green, warm ivory and pale gold color palette, authentic ancient Chinese countryside, natural skin texture, weathered wood and handmade fabric, cinematic live-action period film still, subtle film grain, shallow depth of field, soft volumetric sunlight, realistic photography, no fantasy effects, no modern objects, no text, no watermark --ar 16:9 --style raw --stylize 175
```

可复用要点：主体动作前置、地点紧随、环境流动元素、前景细节、情绪短语、色板、真实材质、电影感、负面约束、参数收尾。

## 禁写清单

- 不写"美丽的女子""仙气飘飘""绝美画面"等无画面信息的形容。
- 不写"古装""古代衣服"，必须给形制。
- 不写"很有生活气息"，必须给具体动作。
- 不用现代词汇如 photoshoot、model、fashion editorial。
- 不在一条提示词里堆超过三个主要动作。
