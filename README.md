# opc_skill

长期维护的 AI 技能仓库。

## Skills

- `skill/wanwusheng-ai-film-director`：万物生 AI 电影端到端导演技能。
- `skill/ai-loop-orchestrator`：有边界、可验证的 AI Agent 循环与工作流设计。
- `skill/aigc-rapid-workflow-explainer`：AIGC 工具实测与工作流内容生产。
- `skill/article-to-sop-manualizer`：将文章转化为零基础可执行 SOP。
- `skill/ebook-maker`：从调研、写作、插图到 PDF 导出的电子书工作流。
- `skill/hv-analysis`：横纵分析法深度研究与 PDF 报告生成。
- `skill/khazix-writer`：数字生命卡兹克风格的公众号长文写作。
- `skill/khazix-skills`：[Git Submodule] 卡兹克官方技能包（包含 aihot、hv-analysis、khazix-writer、leader、neat-freak、storage-analyzer 等），上游仓库：https://github.com/KKKKhazix/khazix-skills
- `skill/seedance-2.0`：[Git Submodule] Seedance 2.0 视频生成技能，上游仓库：https://github.com/Emily2040/seedance-2.0

## Git Submodule 使用说明

### 克隆项目

首次克隆时需要带上 `--recurse-submodules` 参数以自动拉取子模块内容：

```bash
git clone --recurse-submodules git@github.com:lsjt5858/opc_skill.git
```

如果已经克隆了项目但未拉取子模块，执行：

```bash
git submodule update --init --recursive
```

### 更新子模块

当任一子模块上游有更新时（如 [khazix-skills](https://github.com/KKKKhazix/khazix-skills) 或 [seedance-2.0](https://github.com/Emily2040/seedance-2.0)），按以下步骤同步（以 khazix-skills 为例，替换为对应子模块路径即可）：

```bash
# 1. 进入子模块目录，拉取最新代码
cd skill/khazix-skills
git pull origin main

# 2. 回到主项目根目录，提交子模块版本引用
cd ../../
git add skill/khazix-skills
git commit -m "chore: 更新 khazix-skills 到最新版本"
git push
```

更新 seedance-2.0 时，将路径替换为 `skill/seedance-2.0` 即可。
