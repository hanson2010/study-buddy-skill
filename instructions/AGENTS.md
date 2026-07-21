# StudyBuddy - 项目说明（AGENTS）

本仓库是 **StudyBuddy** 的学习助手 skill 项目。skill 被调用时的完整行为规范、子命令、教学流程、核心规则与视频推荐策略，统一以 [`skills/studybuddy/SKILL.md`](skills/studybuddy/SKILL.md) 及其 `references/` 下各 workflow 文件为**权威来源**，本文件不再重复维护这些行为细则，避免两处内容漂移。

## 给 Agent 的仓库级约定（skill 之外也适用）

- **环境变量 `STUDYBUDDY_DATA_DIR`**：所有学习数据（profile、`_index`、subjects、output 等）均存储在该变量指定的目录；运行任何 Python 脚本前必须确认该变量已设置。可选 `STUDYBUDDY_REPORT_WEBHOOK`：设置后报告生成会推送到该地址，未设置则安静跳过。
- **Python 虚拟环境**：脚本统一使用 `$STUDYBUDDY_DATA_DIR/.venv/Scripts/python.exe`（Windows PowerShell），禁止使用系统 Python。
- **QoderWork 项目路径提醒**：QoderWork 的项目级 skill 路径应为 **`.qoder/skills/studybuddy`**（注意是 `.qoder/`，不是 `.qoderwork/`）。其他平台的项目级路径见 `README.md` 的安装指南。

## 文档入口

- skill 入口与完整规则：`skills/studybuddy/SKILL.md`
- 视频推荐细则：`skills/studybuddy/references/video_resources.md`
- 学情报告与 Webhook：`skills/studybuddy/references/report_workflow.md`
- 安装与数据存储：`README.md`
