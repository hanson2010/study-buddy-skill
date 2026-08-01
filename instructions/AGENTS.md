# StudyBuddy - 项目说明（AGENTS）

本仓库是 **StudyBuddy** 的学习助手项目。主 skill 被调用时的完整行为规范、子命令、教学流程、核心规则与视频推荐策略，统一以 [`skills/studybuddy/SKILL.md`](skills/studybuddy/SKILL.md) 及其 `references/` 下各 workflow 文件为**权威来源**。

## 给 Agent 的仓库级约定（skill 之外也适用）

- **环境变量 `STUDYBUDDY_DATA_DIR`**：所有学习数据（profile、`_index`、subjects、output 等）均存储在该变量指定的目录；任何读写学习数据前必须确认该变量已设置。可选 `STUDYBUDDY_REPORT_WEBHOOK`：设置后报告生成会推送到该地址，未设置则安静跳过。
- **本 skill 不分发脚本**：只处理文本内容，OCR / 格式转换交由环境中已有的能力或其他 skill 完成。边界定义见 `skills/studybuddy/references/ingest_workflow.md` 的「非文本内容转换」章节。

## 一致性检查

本仓库没有代码，**文档即 prompt**——任意两份文件之间的矛盾都是一个真实的行为缺陷。修改任何 `.md` 后请运行：

```bash
python tools/check_docs.py     # 无依赖，仅用标准库；退出码 0 表示通过
```

它会检查：链接与脚本引用是否存在、章节编号是否连续（跳过代码围栏）、`subject:` 是否取自六科枚举、原始文件路径键名是否统一为 `source_path`、日志路径（`output/YYYY/MM/`）与原始资料路径（`raw/YYYY/MM/`）是否唯一、同名平台是否出现多个域名。

## 文档入口

- skill 入口与完整规则：`skills/<skill_name>/SKILL.md`
- 安装与数据存储：`README.md`
