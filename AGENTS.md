# StudyBuddy - 项目说明（AGENTS）

本仓库是 **StudyBuddy** 的学习助手项目。主 skill 被调用时的完整行为规范、子命令、教学流程、核心规则与视频推荐策略，统一以 [`skills/studybuddy/SKILL.md`](skills/studybuddy/SKILL.md) 及其 `references/` 下各 workflow 文件为**权威来源**。

> 本文件是**本仓库**的仓库级约定，面向维护/修改这些文档的 agent。技能被安装到其他项目后、运行时应遵守的约定（如 `STUDYBUDDY_DATA_DIR`）不在此文件——那是随技能一起分发给终端用户的内容，见 [`skills/studybuddy/templates/AGENTS.md.template`](skills/studybuddy/templates/AGENTS.md.template)，不要与本文件混淆。

## 一致性检查

本仓库没有代码，**文档即 prompt**——任意两份文件之间的矛盾都是一个真实的行为缺陷。修改任何 `.md` 后请运行：

```bash
python tools/check_docs.py     # 无依赖，仅用标准库；退出码 0 表示通过
```

它会检查：链接与脚本引用是否存在、章节编号是否连续（跳过代码围栏）、`subject:` 是否取自六科枚举、原始文件路径键名是否统一为 `source_path`、日志路径（`output/YYYY/MM/`）与原始资料路径（`raw/YYYY/MM/`）是否唯一、同名平台是否出现多个域名。

## 文档入口

- skill 入口与完整规则：`skills/<skill_name>/SKILL.md`
- 安装与数据存储：`README.md`
- 分发给终端用户的 AGENTS 约定模板：`skills/studybuddy/templates/AGENTS.md.template`
