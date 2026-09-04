# AI Film Production Director Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename and refocus the existing director skill into a platform-neutral, variable-driven AI film production and executable video prompt-pack workflow.

**Architecture:** Keep one lightweight `SKILL.md` as the routing layer and retain five focused references for continuity, production planning, prompt patterns, prompt-pack structure, and batching. Use Production Spec variables and explicit stage gates to prevent unsupported assumptions from reaching final prompts.

**Tech Stack:** Markdown skill documents, YAML agent metadata, shell-based static checks, agent scenario tests.

**Acceptance focus:** 十个独立栏目、跨题材适配、跨平台变量适配，以及小请求的最小模式路由。

---

## File Map

- Rename: `skill/quan_zhan_dao_yan/` -> `skill/ai-film-production-director/`
- Modify: `skill/ai-film-production-director/SKILL.md`
- Modify: `skill/ai-film-production-director/agents/openai.yaml`
- Modify: `skill/ai-film-production-director/references/continuity-audit.md`
- Modify: `skill/ai-film-production-director/references/production-workflow.md`
- Modify: `skill/ai-film-production-director/references/prompt-patterns.md`
- Modify: `skill/ai-film-production-director/references/video-prompt-pack-template.md`
- Modify: `skill/ai-film-production-director/references/output-batching.md`
- Delete: `skill/ai-film-production-director/.DS_Store`
- Preserve: `剧本/` and every unrelated skill directory

### Task 1: Capture RED Behavior Baseline

**Files:**
- Read: `skill/quan_zhan_dao_yan/SKILL.md`
- Read: `skill/quan_zhan_dao_yan/references/*.md`
- Temporary evidence: `/tmp/ai-film-production-director-baseline.md`

- [ ] **Step 1: Run the minimal-request scenario without the revised skill**

Use the current skill instructions with this exact request:

```text
请只为一个30岁女记者生成中性角色身份参考图提示词。没有其他项目需求。
```

Record whether the response unnecessarily expands into a full production plan or prompt pack.

- [ ] **Step 2: Run the missing-variable scenario**

```text
一个男人收到十年前失踪女儿的短信。把它做成完整AI电影提示词包。
```

Record whether the response invents aspect ratio, style, platform, total duration, character identity facts, or exact text without labeling assumptions.

- [ ] **Step 3: Run the continuity-conflict scenario**

```text
第一场写林夏28岁，第二场写十年前她已经25岁。祖传怀表先由林夏随身携带，下一镜未发生交接却出现在反派手中。请直接生成最终视频提示词。
```

Record whether the response blocks affected downstream prompts and reports both conflicts.

- [ ] **Step 4: Run the repair scenario**

```text
审查这份已有提示词包：N01正确；N02缺少尾帧；N03引用不存在的C09。只修必要问题，不要重写N01。
```

Record whether correct content is preserved.

- [ ] **Step 5: Save baseline evidence**

Write concise observations to `/tmp/ai-film-production-director-baseline.md`:

```markdown
# Baseline

## Minimal request
- Result:
- Failure:

## Missing variables
- Result:
- Failure:

## Continuity conflict
- Result:
- Failure:

## Repair
- Result:
- Failure:
```

Expected: at least the metadata-name mismatch and one behavioral gap are observable before implementation.

### Task 2: Rename the Skill and Fix Discovery Metadata

**Files:**
- Rename: `skill/quan_zhan_dao_yan/` -> `skill/ai-film-production-director/`
- Modify: `skill/ai-film-production-director/SKILL.md`
- Modify: `skill/ai-film-production-director/agents/openai.yaml`
- Delete: `skill/ai-film-production-director/.DS_Store`

- [ ] **Step 1: Verify the new path and identifier are absent**

Run:

```bash
test ! -e skill/ai-film-production-director
rg -n 'name: ai-film-production-director|\\$ai-film-production-director' skill/quan_zhan_dao_yan
```

Expected: the path test passes and `rg` returns no matches.

- [ ] **Step 2: Rename the tracked directory**

Run:

```bash
git mv skill/quan_zhan_dao_yan skill/ai-film-production-director
rm -f skill/ai-film-production-director/.DS_Store
```

- [ ] **Step 3: Replace the frontmatter and title**

Set the start of `skill/ai-film-production-director/SKILL.md` to:

```yaml
---
name: ai-film-production-director
description: Use when 用户需要规划或审查 AI 电影制作，尤其涉及剧本可生产性、跨镜头连续性、资产依赖、关键帧或可执行视频提示词包。
---

# AI 电影制片导演
```

- [ ] **Step 4: Update agent metadata**

Set `skill/ai-film-production-director/agents/openai.yaml` to:

```yaml
interface:
  display_name: "AI 电影制片导演"
  short_description: "将剧本、素材与制作约束转成可执行的制片方案和视频提示词包"
  default_prompt: "使用 $ai-film-production-director，把这个剧本和素材目录转成可执行的 AI 电影制片方案与视频提示词包。"
```

- [ ] **Step 5: Verify naming consistency**

Run:

```bash
test -d skill/ai-film-production-director
test ! -e skill/quan_zhan_dao_yan
rg -n 'quan_zhan_dao_yan|wanwusheng-ai-film-director|\\$wanwusheng-ai-film-director' skill/ai-film-production-director
```

Expected: the first two checks pass and `rg` returns no matches.

- [ ] **Step 6: Commit the naming migration**

```bash
git add -A -- skill/quan_zhan_dao_yan skill/ai-film-production-director
git commit -m "refactor: rename ai film production director skill"
```

### Task 3: Refocus the Lightweight Skill Entry Point

**Files:**
- Modify: `skill/ai-film-production-director/SKILL.md`

- [ ] **Step 1: Define entry-point acceptance checks**

Before editing, run:

```bash
rg -n '^## (核心定位|非目标|Production Spec|请求路由|阶段准入)' skill/ai-film-production-director/SKILL.md
```

Expected: one or more required sections are absent.

- [ ] **Step 2: Replace broad purpose text with a focused contract**

The opening body must state:

```markdown
## 核心定位

把剧本、素材和制作约束转换成可执行的 AI 电影制片方案与视频提示词包。核心价值是生产决策、连续性、资产依赖、镜头可执行性和交付 QC，而不是文学创作。

## 非目标

- 不从零创作小说或完整文学剧本。
- 不做泛文案润色。
- 不绑定特定平台、题材或视觉风格。
- 不把未经审计的剧本直接机械转换成最终提示词。
```

- [ ] **Step 3: Add the Production Spec minimum contract**

Include these seven variable groups in compact form:

```markdown
## Production Spec

先锁定或标注：故事、交付、视觉、表演、声音、生成、后期变量。

- 阻塞变量：会改变故事或生产路径，先询问或给出待确认方案。
- 可推断变量：采用保守值并标注“推断”。
- 可延后变量：记录为待定，不阻塞当前阶段。
```

The body must explicitly forbid inheriting another project's style, aspect ratio, duration, shot count, or platform limits.

- [ ] **Step 4: Replace mode prose with a routing table**

The table must map:

```text
制片审计 -> continuity-audit.md
制片计划 -> production-workflow.md
资产提示词 -> prompt-patterns.md
完整提示词包 -> video-prompt-pack-template.md
提示词包修补 -> references selected by defect type
```

State that small requests use the smallest mode and do not trigger the full workflow.

- [ ] **Step 5: Add the production chain and compact blocking rule**

Use this sequence:

```text
输入与变量锁定
→ 可生产性与连续性审计
→ 场景表和镜头卡
→ 资产依赖与生成顺序
→ Storyboard / Keyframe
→ 视频提示词包
→ 后期交接与 QC
```

State that identity, timeline, core-prop, aspect-ratio, platform-capability, critical-text, or nonexistent-asset conflicts block affected final prompts.

- [ ] **Step 6: Remove duplicated heavy detail**

Keep detailed prompt templates, asset coverage lists, fixed ten-column definitions, and batching mechanics in references. Target a concise routing document rather than repeating reference content.

- [ ] **Step 7: Verify the entry point**

Run:

```bash
rg -n '^name: ai-film-production-director$|^# AI 电影制片导演$|^## (核心定位|非目标|Production Spec|请求路由|统一生产链|阶段准入)' skill/ai-film-production-director/SKILL.md
rg -n '固定.*(画幅|总时长|镜头数)|默认.*(写实|竖屏|横屏)' skill/ai-film-production-director/SKILL.md
```

Expected: every required section appears; the second command returns no platform/style defaults.

- [ ] **Step 8: Commit the entry-point refactor**

```bash
git add skill/ai-film-production-director/SKILL.md
git commit -m "refactor: focus ai film production skill routing"
```

### Task 4: Strengthen Production Audit and Stage Gates

**Files:**
- Modify: `skill/ai-film-production-director/references/continuity-audit.md`
- Modify: `skill/ai-film-production-director/references/production-workflow.md`

- [ ] **Step 1: Verify producibility checks are incomplete**

Run:

```bash
rg -n '不可视觉化|动作过载|台词容量|空间关系|结尾状态|Production Spec|有条件通过|需拆镜' \
  skill/ai-film-production-director/references/continuity-audit.md \
  skill/ai-film-production-director/references/production-workflow.md
```

Expected: several required concepts are absent.

- [ ] **Step 2: Add producibility audit categories**

Add a section to `continuity-audit.md` covering:

```markdown
## 剧本可生产性

- 不可直接视觉化的心理描写：转为可见动作、表演或声音线索。
- 动作过载：单镜包含多个独立动作、地点或身份变化时标记“需拆镜”。
- 台词容量：台词无法在计划镜头时长内自然完成时标记“阻塞”或建议拆分。
- 空间关系：缺失入口、出口、站位、视线或屏幕方向时，不生成依赖该关系的最终 keyframe。
- 关键文字：故事关键文字必须预留后期合成策略。
- 剪辑接口：每个镜头必须有可描述的开始状态和结束状态。
```

Extend the audit output with `状态：通过 / 有条件通过 / 阻塞 / 需拆镜`.

- [ ] **Step 3: Add the full Production Spec table**

In `production-workflow.md`, define the seven variable groups and classify each value as:

```text
已锁定 | 推断 | 待确认 | 可延后
```

Require source attribution for locked values: user instruction, source material, inspected asset, or platform constraint.

- [ ] **Step 4: Strengthen stage gates**

Each gate must include observable entry and exit conditions:

```text
Gate 0: Production Spec and continuity
Gate 1: Scene list, shot cards, and animatic
Gate 2: Reusable assets
Gate 3: Storyboard and keyframes
Gate 4: Video generation
Gate 5: Edit, sound, text, and delivery
```

At every failed gate, return blocking item, downstream impact, minimum resolution, and work that may continue.

- [ ] **Step 5: Verify audit and workflow rules**

Run:

```bash
rg -n '剧本可生产性|不可直接视觉化|动作过载|台词容量|剪辑接口|有条件通过|需拆镜' \
  skill/ai-film-production-director/references/continuity-audit.md
rg -n '故事变量|交付变量|视觉变量|表演变量|声音变量|生成变量|后期变量|已锁定|待确认' \
  skill/ai-film-production-director/references/production-workflow.md
```

Expected: all categories and statuses are present.

- [ ] **Step 6: Commit audit and workflow changes**

```bash
git add \
  skill/ai-film-production-director/references/continuity-audit.md \
  skill/ai-film-production-director/references/production-workflow.md
git commit -m "feat: add production variables and stage gates"
```

### Task 5: Strengthen Asset and Prompt-Pack Execution Rules

**Files:**
- Modify: `skill/ai-film-production-director/references/prompt-patterns.md`
- Modify: `skill/ai-film-production-director/references/video-prompt-pack-template.md`
- Modify: `skill/ai-film-production-director/references/output-batching.md`

- [ ] **Step 1: Verify quality-rule gaps**

Run:

```bash
rg -n '环境音|动作音|强调音|资产就绪|一个主要叙事节拍|一个主要摄影机运动|动态分批' \
  skill/ai-film-production-director/references
```

Expected: the complete quality contract is absent.

- [ ] **Step 2: Tighten reusable asset readiness**

In `prompt-patterns.md`, require:

```text
角色身份：中性姿势、完整身体、正面/侧面/背面/3/4、必要面部特写
环境：先空环境，包含主视角、反向覆盖和必要空间关系
道具：尺寸、归属、材质、状态和稳定识别标记
Keyframe：只在所引用身份、状态、道具和环境资产就绪后生成
```

Preserve separate subject motion, camera motion, environment motion, timing, and end state for video prompts.

- [ ] **Step 3: Add package-level readiness checks**

Before the single-shot template in `video-prompt-pack-template.md`, add:

```markdown
## 输入资产就绪检查

- Production Spec 已锁定或明确标注变量状态。
- 当前镜头引用的资产 ID 全部存在。
- 角色、服装、道具和环境状态与镜头表一致。
- 关键文字已有后期策略。
- 镜头复杂度适合平台单次生成能力。
```

- [ ] **Step 4: Strengthen the ten-column shot template**

Keep the existing columns and add these requirements:

```text
故事作用：每个镜头标题或正文明确叙事节拍。
运镜：一个主要摄影机运动。
动作：时间段连续覆盖生成时长。
尾帧：人物位置、视线、道具状态、光线、剪辑接口。
音效：环境音、动作音、强调音；音乐按 Production Spec。
后期与 QC：可观察的通过/失败检查。
```

- [ ] **Step 5: Replace fixed batching examples with dynamic batching**

In `output-batching.md`, remove default groups such as `N01-N05` and `N06-N10`. Define batch boundaries by:

```text
镜头数量
资产引用复杂度
动作与声音密度
单次输出能否保留完整 QC
```

Require each batch to declare its coverage and preserve locked values from previous batches.

- [ ] **Step 6: Verify prompt-pack structure**

Run:

```bash
for heading in 场景 运镜 动作 尾帧 音效 影像调性 表演要求 对白 反向锚定 '后期与 QC'; do
  rg -q "【${heading}】" skill/ai-film-production-director/references/video-prompt-pack-template.md || exit 1
done
rg -n '环境音|动作音|强调音|一个主要摄影机运动|输入资产就绪检查' \
  skill/ai-film-production-director/references/video-prompt-pack-template.md
! rg -n 'N01-N05|N06-N10|N11-N16' \
  skill/ai-film-production-director/references/output-batching.md
```

Expected: all commands exit successfully.

- [ ] **Step 7: Commit prompt quality changes**

```bash
git add \
  skill/ai-film-production-director/references/prompt-patterns.md \
  skill/ai-film-production-director/references/video-prompt-pack-template.md \
  skill/ai-film-production-director/references/output-batching.md
git commit -m "feat: strengthen executable video prompt packs"
```

### Task 6: Run GREEN Behavior and Regression Validation

**Files:**
- Read: `skill/ai-film-production-director/SKILL.md`
- Read: `skill/ai-film-production-director/references/*.md`
- Compare: `/tmp/ai-film-production-director-baseline.md`

- [ ] **Step 1: Re-run all four baseline scenarios**

Use the exact prompts from Task 1 with the revised skill. Confirm:

```text
Minimal request -> only the requested identity asset
Missing variables -> explicit variable states before final prompts
Continuity conflict -> affected downstream work blocked
Repair -> N01 preserved; only N02 and N03 repaired
```

- [ ] **Step 2: Run cross-genre regression**

Run the same production-plan request against:

```text
现实家庭剧情
古装仙侠
现代悬疑
二维动画
```

Expected: the production structure remains stable and the skill does not force photorealism, a fixed aspect ratio, or a fixed duration.

- [ ] **Step 3: Run cross-platform regression**

Use two hypothetical platform profiles:

```text
Platform A: 3-5 seconds per generation, one start image
Platform B: 8-12 seconds per generation, start and end images
```

Expected: shot splitting and reference use change, while the core production chain and quality gates remain stable.

- [ ] **Step 4: Run static checks**

```bash
test -f skill/ai-film-production-director/SKILL.md
test ! -e skill/quan_zhan_dao_yan
test ! -e skill/ai-film-production-director/.DS_Store
rg -q '^name: ai-film-production-director$' skill/ai-film-production-director/SKILL.md
rg -q '\\$ai-film-production-director' skill/ai-film-production-director/agents/openai.yaml
! rg -n 'quan_zhan_dao_yan|wanwusheng-ai-film-director|\\$wanwusheng-ai-film-director' \
  skill/ai-film-production-director
git diff --check
```

Expected: every command exits successfully with no stale identifier or whitespace error.

- [ ] **Step 5: Compare GREEN results to baseline**

Document in the working notes:

```text
Which baseline failures are fixed
Whether any new rationalization or overreach appeared
Which minimum wording change, if any, is required
```

If a new loophole appears, change only the responsible document and rerun the affected scenario.

- [ ] **Step 6: Verify repository scope**

Run:

```bash
git status --short
git diff --stat HEAD~3..HEAD
```

Expected: only the renamed skill and approved documentation are changed; `剧本/` remains untouched.

- [ ] **Step 7: Commit final refinements if needed**

If GREEN testing required wording changes:

```bash
git add skill/ai-film-production-director
git commit -m "test: close ai film production workflow gaps"
```

If no refinements were needed, do not create an empty commit.
