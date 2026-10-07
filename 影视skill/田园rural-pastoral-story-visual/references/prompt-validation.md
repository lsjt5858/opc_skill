# 提示词复制前校验

本校验用于减少“复制后格式不被接受”与“提示词过度约束”的问题，不模拟或承诺任何生成平台的在线审核结果。

## 分级

- **error**：确定性格式问题或与已指定平台明确冲突。交付前必须修复。
- **warning**：可能影响兼容性、可控性或触发误判。默认仍可交付，由创作目标决定是否修改。
- **info**：优化建议，不影响通过。

默认模式下只有 error 会导致失败；不要把 warning 自动升级为 error。只有用户明确要求严格模式时才使用 `--strict`。

## 必检项

1. 提示词非空，不含控制字符、模板占位符或 Markdown 包装残留。
2. 明确目标平台：
   - 未指定平台：使用 `generic`，输出纯文本，不附私有参数。
   - Midjourney：允许 `--ar`、`--style`、`--stylize` 等已知参数。
   - Seedream / Seedance：不附 Midjourney 的 `--...` 参数。
3. 人物年龄表达清楚。`女孩 / 少女 / girl` 仅提示 warning；若本意是成年人，改成“二十岁以上成年女性 / young adult woman”，不要机械删除人物年龄。
4. 单条过长、否定词过多、动作过密时提示 warning，不阻断。
5. 涉及雨水、湿衣或赤足等普通生活细节时不单独拦截；只有与身体聚焦措辞叠加时提示兼容性 warning，并建议把重点改回动作、服装材质或环境。

## 运行

校验单条纯文本：

```bash
python3 scripts/check_prompts.py prompt.txt --platform generic
```

校验 JSON 中的一条或多条提示词：

```bash
python3 scripts/check_prompts.py prompts.json --platform midjourney
```

支持的平台值：`generic`、`midjourney`、`seedream`、`seedance`。

默认退出码：有 error 时为 1；仅有 warning 时仍为 0。用户明确要求零告警时才追加 `--strict`。

## 修改原则

- 优先删除不属于目标平台的参数和 Markdown 标签。
- 优先缩短重复的风格词与否定词，不删除主体、动作、地域、服装和光线锚点。
- 一条提示词只保留一个主要动作和最多一个直接结果；长镜头叙事拆分为多条。
- 对 warning 做最小改写，不因无法确认的平台误判而大面积删词。
- 输出校验摘要：`通过 / 通过但有提醒 / 未通过`，列出定位和建议；不要宣称“保证平台一定通过”。
