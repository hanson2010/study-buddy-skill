# StudyBuddy - 面向高中生的 AI 学习助手

## 简介

StudyBuddy 是一个面向高中生的 AI 学习助手，专注于作业批改、错题分析、知识点讲解和个性化复习。支持语文、数学、英语、物理、化学、生物六大学科，通过长期记忆系统实现个性化学习。

---

## 🚀 快速开始

### 子命令使用

本助手提供 6 个子命令，用于启动不同的工作流程：

| 子命令 | 功能 | 适用场景 |
|--------|------|----------|
| `aim` | 目标对齐 | 设定学习目标、上传高校资料、制定学习规划 |
| `ingest` | 学习资料导入 | 导入课本资料、讲义、笔记、参考材料，按学科分类归档 |
| `learn` | 知识点学习与巩固 | 学习知识点、复习薄弱点、古诗文学习 |
| `eval` | 作业批改与错题归档 | 上传作业/试卷照片、请求批改错题 |
| `feedback` | 成绩反馈 | 上传成绩分析报告、单科卷面分析报告 |
| `report` | 学情追踪 | 生成学习周报/月报、分析学习趋势 |

**使用方式**：
- **命令形式**：直接输入子命令，如 `aim`、`ingest`、`learn`、`eval`、`feedback`、`report`
- **自然语言形式**：用自然语言描述需求，如"帮我导入学习资料"、"我要学习导数"、"帮我批改作业"、"分析我的成绩"、"生成学习周报"
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

```
<STUDYBUDDY_DATA_DIR>/
├── profile.md                 # 学习背景档案（姓名、年级、文理科、教材版本、学习目标）
├── _index.md                  # 学习总览（六科状态汇总、历次考试成绩、全局薄弱点）
├── colleges/                  # 高校资料（目标院校专业组、投档数据、分数分布）
│   ├── _index.md              # 高校资料索引
│   └── YYYY/                  # 按年份归档
│       └── YYYY-MM-DD-<slug>.md # 示例：2026-07-12-peking-university.md
├── raw/                       # 原始数据（按年月归档）
│   ├── YYYY/MM/              # 图片文件（使用原始文件名）
│   └── YYYY/MM/YYYY-MM-DD-log.md  # 会话日志
├── subjects/                  # 学科数据（错题、练习，按科目+年月归档）
│   ├── 语文/_index.md         # 语文学科索引
│   └── 语文/YYYY/MM/YYYY-MM-DD-descriptive-slug.md
└── output/                    # 学习产出（学情报告等，按年月归档）
```

---

## 📝 核心规则

| 序号 | 规则名称 | 说明 |
|------|----------|------|
| 1 | 智能辅导六步法 | 辅导与学习必须按「诊断/识别 → 错因/盲区分析 → 分步讲解 → 视频推荐 → 举一反三 → 归档/同步」顺序执行（根据场景适配或跳过部分步骤） |
| 2 | 视频推荐不能漏 | 每次错题讲解后必须推荐 1-2 个优质视频 |
| 3 | 长期记忆驱动个性化 | 批改和讲解前先读取学生档案，命中薄弱点即高亮提示 |
| 4 | 参考材料隔离 | 标准答案、范文等通过 frontmatter 字段标识，不影响学生学情记录 |
| 5 | 图片存储规则 | 用户上传的图片存入 `raw/YYYY/MM/`，使用原始文件名，同名文件添加数字后缀 |
| 6 | 操作概要记入 log | 每次操作概要必须记入 `YYYY-MM-DD-log.md` 文件 |

---

## 📖 参考文档

- [SKILL.md](skills/studybuddy/SKILL.md) — 完整教学规则
- [aim_workflow.md](skills/studybuddy/references/aim_workflow.md) — 目标对齐工作流
- [ingest_workflow.md](skills/studybuddy/references/ingest_workflow.md) — 学习资料导入工作流
- [learn_workflow.md](skills/studybuddy/references/learn_workflow.md) — 知识点学习工作流
- [eval_workflow.md](skills/studybuddy/references/eval_workflow.md) — 作业批改工作流
- [feedback_workflow.md](skills/studybuddy/references/feedback_workflow.md) — 成绩反馈工作流
- [report_workflow.md](skills/studybuddy/references/report_workflow.md) — 学情追踪工作流
