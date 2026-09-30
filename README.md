# opc_skill

长期维护的 AI 技能仓库。

## Skills

- `skill/ai-film-production-director`：AI 电影制片导演，面向跨平台电影制片与提示词包交付。
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

在项目根目录执行：

```bash
# 仅预览当前子模块，不修改仓库
./scripts/update-submodules.sh

# 实际同步全部子模块的远程最新代码
./scripts/update-submodules.sh --execute
```

脚本会动态读取 `.gitmodules`，同步 URL、递归初始化并更新全部子模块。后续通过
`git submodule add <仓库地址> <目录>` 添加新子模块后，无需修改同步脚本。

如果任一子模块存在未提交修改，脚本会停止更新，避免覆盖本地工作。同步完成后，
主仓库会显示子模块版本引用发生变化，需要按需提交这些变更。
