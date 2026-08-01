# StudyBuddy - 面向高中生的 AI 学习助手

## 简介

StudyBuddy 是一个面向高中生的 AI 学习助手，专注于作业批改、错题分析、知识点讲解和个性化复习。支持语文、数学、英语、物理、化学、生物六大学科，通过长期记忆系统实现个性化学习。

---

## 🚀 快速开始

### 子命令使用

本助手提供 8 个子命令，用于启动不同的工作流程：

| 子命令 | 功能 | 适用场景 |
|--------|------|----------|
| `aim` | 目标对齐 | 设定学习目标、上传高校资料、制定学习规划 |
| `ingest` | 学习资料导入 | 导入课本资料、讲义、笔记、参考材料，按学科分类归档（非文本内容需先由其他工具转换为文本） |
| `learn` | 知识点学习与巩固 | 学习知识点、复习薄弱点（含视频推荐规则） |
| `classical` | 古诗文记忆与理解 | 古诗词、文言文的背诵、理解与鉴赏 |
| `eval` | 作业批改与错题归档 | 上传作业/试卷照片、请求批改错题 |
| `essay` | 语文作文批改 | 作文图片/文本的批改、评分与升格（北京卷：微写作 10 分 / 大作文 50 分） |
| `feedback` | 成绩反馈 | 上传成绩分析报告、单科卷面分析报告 |
| `report` | 学情追踪 | 生成学习周报/月报、分析学习趋势 |

**使用方式**：
- **命令形式**：直接输入子命令，如 `aim`、`ingest`、`learn`、`classical`、`eval`、`essay`、`feedback`、`report`
- **自然语言形式**：用自然语言描述需求，如"帮我导入学习资料"、"我要学习导数"、"学习《登高》"、"帮我批改作业"、"批改这篇作文"、"分析我的成绩"、"生成学习周报"
- **图片触发**：上传图片时自动识别内容类型并匹配对应的工作流程

### 典型用法

```text
帮我批改这份数学作业。
[上传图片]
```

```text
孩子高一，物理"牛顿第二定律"总错。请先讲明白，再出练习。
```

```text
请帮我生成本周的学习周报。
```

---

## 📁 安装指南

> 以下均为**项目级别**安装：将 skill 复制到当前项目根目录下的对应目录中，随项目一起管理（推荐，便于版本控制与团队共享）。

### QoderWork 用户

```bash
mkdir -p .qoder/skills/studybuddy
cp -r skills/studybuddy/* .qoder/skills/studybuddy/
```

### WorkBuddy 用户

```bash
mkdir -p .workbuddy/skills/studybuddy
cp -r skills/studybuddy/* .workbuddy/skills/studybuddy/
```

### Trae Work 用户

```bash
mkdir -p .trae/skills/studybuddy
cp -r skills/studybuddy/* .trae/skills/studybuddy/
```

---

## 💾 数据存储

数据存储在环境变量 `STUDYBUDDY_DATA_DIR` 指定的目录中。必须设置该环境变量，否则会提醒用户设置后再继续使用。

 可选环境变量 `STUDYBUDDY_REPORT_WEBHOOK`：设置后，生成的学情报告（日报 / 周报 / 月报 / 专项报告）会在落盘后自动 POST 到该地址（请求体为 `{"content": "<报告正文 Markdown>"}`，**不含 Frontmatter**）；**不设置则安静跳过**，不影响报告生成。详见 [report_workflow.md](skills/studybuddy/references/report_workflow.md) 的「报告推送」章节。

数据目录的完整结构（`profile.md`、`_index.md`、`colleges/`、`raw/`、`subjects/`、`output/`）定义在 [SKILL.md 的「数据目录结构」](skills/studybuddy/SKILL.md) 一节。

---

## 📝 核心规则

完整的 12 条核心规则（智能辅导六步法与交互确认、视频推荐、参考材料隔离、原始资料存储、日志记录等）以 [SKILL.md 的「一页核心规则」](skills/studybuddy/SKILL.md) 为**唯一权威来源**，本文不复述，以免与之产生分歧。

---

## 📖 参考文档

- [SKILL.md](skills/studybuddy/SKILL.md) — 完整教学规则
- [aim_workflow.md](skills/studybuddy/references/aim_workflow.md) — 目标对齐工作流
- [ingest_workflow.md](skills/studybuddy/references/ingest_workflow.md) — 学习资料导入工作流
- [learn_workflow.md](skills/studybuddy/references/learn_workflow.md) — 知识点学习工作流（含视频推荐规则）
- [classical_workflow.md](skills/studybuddy/references/classical_workflow.md) — 古诗文记忆与理解工作流
- [eval_workflow.md](skills/studybuddy/references/eval_workflow.md) — 作业批改工作流
- [essay_workflow.md](skills/studybuddy/references/essay_workflow.md) — 语文作文批改工作流
- [feedback_workflow.md](skills/studybuddy/references/feedback_workflow.md) — 成绩反馈工作流
- [report_workflow.md](skills/studybuddy/references/report_workflow.md) — 学情追踪工作流
