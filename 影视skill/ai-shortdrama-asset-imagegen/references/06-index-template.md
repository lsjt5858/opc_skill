# 06_资产索引.md 模板

> 本文件为 AI 短剧资产库的三向映射索引表模板。**实体名 ↔ 文件名 ↔ 平台角色库标识** 一一对应，命名遵循 `UPPERCASE + 下划线 + 版本号` 规范。

## 使用说明

- **实体名**：中文名，来自剧本解析。
- **类型**：角色 / 场景 / 道具。
- **UPPERCASE ID**：唯一稳定 ID，例：`LIN_XIA_V1`、`RAINY_ALLEY_S1_V1`、`JADE_SWORD_V1`。改版号时递增（V2、V3），不可复用旧号覆盖。
- **文件名**：本 UPPERCASE ID 关联的**所有**产出文件，斜杠分隔。命名格式建议：`<UPPERCASE_ID>__<资产类别>.<ext>`（双下划线分隔 ID 与后缀）。
- **平台角色库标识**：上传到平台素材库 / 角色库时的稳定引用地址，默认按 `lib://characters/<UPPERCASE_ID>`、`lib://scenes/<UPPERCASE_ID>`、`lib://props/<UPPERCASE_ID>` 组织。

## 命名对照（推荐）

| 资产类别 | 建议文件名后缀 |
|---|---|
| 角色 · DNA Lock 文本 | `__dna.txt` |
| 角色 · 三视图·正面 | `__front.png` |
| 角色 · 三视图·侧面 | `__side.png` |
| 角色 · 三视图·背面 | `__back.png` |
| 角色 · 三视图·合并版 | `__three_view_merged.png` |
| 角色 · T-pose | `__tpose.png` |
| 角色 · 色卡 | `__palette.png` |
| 角色/道具 · 交互参考图（可选） | `<CHARACTER_ID>__with_<PROP_ID>.png` |
| 场景 · 全景 | `__establishing.png` |
| 场景 · 多机位 | `__camA.png` / `__camB.png` / `__camC.png` |
| 场景 · Depth | `__depth.png` |
| 场景 · HDRI | `__hdri.exr` |
| 道具 · Turnaround 正面 | `__turnaround_front.png` |
| 道具 · Turnaround 45° | `__turnaround_45.png` |
| 道具 · Turnaround 侧面 | `__turnaround_side.png` |

## 主表模板

| 实体名 | 类型 | UPPERCASE ID | 文件名 | 平台角色库标识 |
|---|---|---|---|---|
| <中文角色名> | 角色 | `<CHARACTER_UPPER_V1>` | `<CHARACTER_UPPER_V1>__dna.txt` / `<CHARACTER_UPPER_V1>__front.png` / `<CHARACTER_UPPER_V1>__side.png` / `<CHARACTER_UPPER_V1>__back.png` / `<CHARACTER_UPPER_V1>__three_view_merged.png` / `<CHARACTER_UPPER_V1>__tpose.png` / `<CHARACTER_UPPER_V1>__palette.png` | `lib://characters/<CHARACTER_UPPER_V1>` |
| <中文场景名> | 场景 | `<SCENE_UPPER_S1_V1>` | `<SCENE_UPPER_S1_V1>__establishing.png` / `<SCENE_UPPER_S1_V1>__camA.png` / `<SCENE_UPPER_S1_V1>__camB.png` / `<SCENE_UPPER_S1_V1>__camC.png` / `<SCENE_UPPER_S1_V1>__depth.png` / `<SCENE_UPPER_S1_V1>__hdri.exr` | `lib://scenes/<SCENE_UPPER_S1_V1>` |
| <中文道具名> | 道具 | `<PROP_UPPER_V1>` | `<PROP_UPPER_V1>__turnaround_front.png` / `<PROP_UPPER_V1>__turnaround_45.png` / `<PROP_UPPER_V1>__turnaround_side.png` | `lib://props/<PROP_UPPER_V1>` |

## 示例（供参考，实际按剧本替换）

| 实体名 | 类型 | UPPERCASE ID | 文件名 | 平台角色库标识 |
|---|---|---|---|---|
| 林夏 | 角色 | `LIN_XIA_V1` | `LIN_XIA_V1__dna.txt` / `LIN_XIA_V1__front.png` / `LIN_XIA_V1__side.png` / `LIN_XIA_V1__back.png` / `LIN_XIA_V1__three_view_merged.png` / `LIN_XIA_V1__tpose.png` / `LIN_XIA_V1__palette.png` | `lib://characters/LIN_XIA_V1` |
| 沈砚 | 角色 | `SHEN_YAN_V1` | `SHEN_YAN_V1__dna.txt` / `SHEN_YAN_V1__front.png` / `SHEN_YAN_V1__side.png` / `SHEN_YAN_V1__back.png` / `SHEN_YAN_V1__three_view_merged.png` / `SHEN_YAN_V1__tpose.png` / `SHEN_YAN_V1__palette.png` | `lib://characters/SHEN_YAN_V1` |
| 雨夜巷 | 场景 | `RAINY_ALLEY_S1_V1` | `RAINY_ALLEY_S1_V1__establishing.png` / `RAINY_ALLEY_S1_V1__camA.png` / `RAINY_ALLEY_S1_V1__camB.png` / `RAINY_ALLEY_S1_V1__camC.png` / `RAINY_ALLEY_S1_V1__depth.png` / `RAINY_ALLEY_S1_V1__hdri.exr` | `lib://scenes/RAINY_ALLEY_S1_V1` |
| 律所办公室 | 场景 | `LAW_OFFICE_S2_V1` | `LAW_OFFICE_S2_V1__establishing.png` / `LAW_OFFICE_S2_V1__camA.png` / `LAW_OFFICE_S2_V1__camB.png` / `LAW_OFFICE_S2_V1__camC.png` / `LAW_OFFICE_S2_V1__depth.png` / `LAW_OFFICE_S2_V1__hdri.exr` | `lib://scenes/LAW_OFFICE_S2_V1` |
| 玉剑 | 道具 | `JADE_SWORD_V1` | `JADE_SWORD_V1__turnaround_front.png` / `JADE_SWORD_V1__turnaround_45.png` / `JADE_SWORD_V1__turnaround_side.png` | `lib://props/JADE_SWORD_V1` |
| 红外套徽章 | 道具 | `REDCOAT_BADGE_A_V1` | `REDCOAT_BADGE_A_V1__turnaround_front.png` / `REDCOAT_BADGE_A_V1__turnaround_45.png` / `REDCOAT_BADGE_A_V1__turnaround_side.png` | `lib://props/REDCOAT_BADGE_A_V1` |

## 硬性规范

1. UPPERCASE ID 全片唯一，一旦确定不得改写；如需修改（比如换发型），版本号递增（`V1 → V2`），不覆盖旧号。
2. 场景 ID 需带场景编号（`_S1_`、`_S2_`），道具 ID 无场景编号但可含变体标记（`_A`、`_B`），变体标记放在版本号前，如 `REDCOAT_BADGE_A_V1`。
3. 平台角色库标识默认 `lib://characters/<UPPERCASE_ID>`、`lib://scenes/<UPPERCASE_ID>`、`lib://props/<UPPERCASE_ID>`，如上传后平台返回其他 ID，需回填此表。
4. 文件名与 prompt 内的资产引用 ID 完全一致，跨文件跨镜头保证可检索。
