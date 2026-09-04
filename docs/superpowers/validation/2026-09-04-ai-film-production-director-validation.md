# AI Film Production Director 验证摘要

- 基线 commit：`40aab9c`
- Feature range：`40aab9c..5c4b5b7`
- Tested commit：`5c4b5b7`（完整 SHA：`5c4b5b7b2a4749eb9f85f5933fa96b6f171b7841`）
- 运行方式：最终 GREEN 回归 Agent 在固定 commit 上完整读取当前 Skill、全部 references 与 YAML 后逐条应用。以下仅为摘要；完整输入、实际响应、命令和真实结果见 [GREEN 原始证据](./2026-09-04-ai-film-production-director-green-evidence.md)。

## 四个原始请求

1. `请只为一个30岁女记者生成中性角色身份参考图提示词。没有其他项目需求。`
2. `一个男人收到十年前失踪女儿的短信。把它做成完整AI电影提示词包。`
3. `第一场写林夏28岁，第二场写十年前她已经25岁。祖传怀表先由林夏随身携带，下一镜未发生交接却出现在反派手中。请直接生成最终视频提示词。`
4. `审查这份已有提示词包：N01正确；N02缺少尾帧；N03引用不存在的C09。只修必要问题，不要重写N01。`

## RED / GREEN

- RED observed：旧入口存在命名不一致和模式过宽；信息不足时会带入未标注默认值；年龄与道具冲突未形成稳定阻塞；修补请求可能扩大为整包重写。
- GREEN observed：单资产请求走最小路由；缺失变量进入已锁定/推断/待确认/可延后状态；年龄和怀表冲突阻塞受影响提示词并给出最小解决方案；N01 保留、N02 补尾帧、N03 因 C09 不存在而单独阻塞。对应完整输出见原始证据 [2.1-2.4](./2026-09-04-ai-film-production-director-green-evidence.md#2-四个原始请求)。

## 跨题材与跨平台

- 跨题材：现实家庭剧情、古装仙侠、现代悬疑、二维动画均使用七组 Production Spec 和同一阶段结构，同时保留各自的媒介、画幅和时长。输入与摘要见原始证据 [第 3 节](./2026-09-04-ai-film-production-director-green-evidence.md#3-跨题材实际执行)。
- 跨平台：同一剧情在 Platform A 拆为三个单首帧短镜，在 Platform B 拆为两个首尾帧镜头；核心故事链、资产状态、统一生产链和 Gate 0-5 不变。输入、完整响应与矩阵见原始证据 [第 4 节](./2026-09-04-ai-film-production-director-green-evidence.md#4-精确跨平台矩阵实际执行)。

## 定向生成契约

- 纯 T2V：保留 `Dependency asset IDs`，`Input handles`/`【本镜输入】` 为 `无/不适用`，用文本 DNA、开始状态和 canonical `【尾帧】` 承载连续性，见 [5.1](./2026-09-04-ai-film-production-director-green-evidence.md#51-纯-t2v-保留依赖但不传模型输入)。
- I2V 尾帧：规则应用响应先定义 canonical tail state，并要求结束帧由它生成；因没有实际 `end_22.png` 或视频文件，Gate 3 为待验证/阻塞，Gate 4 未进入。本场景只证明派生规则正确触发，不证明图片或视频 Gate 通过，见 [5.2](./2026-09-04-ai-film-production-director-green-evidence.md#52-i2v-结束帧从-canonical-tail-state-派生)。
- 尾帧漂移：人物位置相同但姿态、朝向、手部/道具和环境运动不同，整体结论为阻塞，见 [5.3](./2026-09-04-ai-film-production-director-green-evidence.md#53-尾帧姿态与运动漂移冲突)。
- 平台能力不足：规则应用响应没有静默省略 I2V 输入，而是提出显式改为纯 T2V、保留依赖、清空输入、重写提示词并重跑 Gate 1-4。因变更后的场景表、镜头卡、资产、storyboard/keyframe、尾帧、十栏目提示词和请求载荷未提供，受影响 Gate 均不得宣称通过；本场景只证明模式变更和重跑要求正确触发，见 [5.4](./2026-09-04-ai-film-production-director-green-evidence.md#54-i2v-平台能力不足时显式改模式)。

## 静态检查

- YAML、路径/旧标识、references、十栏目、动态分批、动态画幅、条件输入、纯 T2V 与 canonical tail 均通过实际静态检查；动态画幅正向命中为 9 行，反向固定画幅命中为 0。命令、退出码和 stdout 见原始证据 [第 6 节](./2026-09-04-ai-film-production-director-green-evidence.md#6-静态检查命令与真实结果)。
- `git diff --check 40aab9c..5c4b5b7`：exit `0`，原始结果见证据 [6.10](./2026-09-04-ai-film-production-director-green-evidence.md#610-固定-feature-range-diff)。

## 合理裁量

以下三项不作为缺口：最小请求附带必要的生成约束但不展开完整流程；信息不足时给出带状态的可选锁定值而非逐项停问；不存在的 C09 只报告阻塞并请求有效资产，不虚构替代 ID。

## 自审

观察结果与具体证据章节的映射、测试性质及 CLI 声明见原始证据 [第 7-8 节](./2026-09-04-ai-film-production-director-green-evidence.md#7-观察结果与证据索引)。
