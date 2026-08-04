# StudyBuddy - 面向高中生的 AI 学习助手

## 简介

StudyBuddy 是一个面向高中生的 AI 学习助手，专注于作业批改、错题分析、知识点讲解和个性化复习。支持语文、数学、英语、物理、化学、生物、政治、历史、地理九大学科（按选科组合启用），通过长期记忆系统实现个性化学习。

---

## 🚀 快速开始

### 子命令使用

本助手提供 10 个子命令，用于启动不同的工作流程：

| 子命令 | 功能 | 适用场景 |
|--------|------|----------|
| `aim` | 目标对齐与生涯规划 | 编辑学生档案、生涯探索、**选科校验**、设定目标梯度、差距分析、学习规划 |
| `ingest` | 外部资料导入 | 导入学科资料（课本/讲义/笔记/参考材料）与升学资料（招生政策/简章/投档线/一分一段/就业年报）；非文本内容需先由其他工具转换为文本 |
| `learn` | 知识点学习与巩固 | 学习知识点、复习薄弱点（含视频推荐规则） |
| `classical` | 古诗文记忆与理解 | 古诗词、文言文的背诵、理解与鉴赏 |
| `eval` | 作业批改与错题归档 | 上传作业/试卷照片、请求批改错题 |
| `essay` | 语文作文批改 | 作文图片/文本的批改、评分与升格（北京卷：微写作 10 分 / 大作文 50 分） |
| `feedback` | 成绩反馈 | 上传成绩分析报告、单科卷面分析报告 |
| `report` | 学情追踪 | 生成学习周报/月报、分析学习趋势 |
| `ask` | 学情提问（只读） | 询问学习状况、薄弱点排序、历史错题回顾、目标差距 |
| `maintain` | 数据维护 | 数据体检、档案清理、重新编译、全量重编、学年归档 |

> 知识点档案的编译不是子命令——它隐式挂在各写入型子命令的最后一步，用户无需感知。只有重编（重新编译单一学科/目标，或全量重编）需要经由 `maintain`。

**使用方式**：
- **命令形式**：直接输入子命令，如 `aim`、`ingest`、`learn`、`classical`、`eval`、`essay`、`feedback`、`report`、`ask`、`maintain`
- **自然语言形式**：用自然语言描述需求，如"帮我导入学习资料"、"我要学习导数"、"学习《登高》"、"帮我批改作业"、"批改这篇作文"、"分析我的成绩"、"生成学习周报"、"我最近数学怎么样"、"给学习数据做个体检"
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

```text
我现在哪些知识点最该补？给我排个序。
```

```text
我想学医或者计算机，选科该怎么选？
```

---

## 🧠 数据是怎么组织的

StudyBuddy 的数据分为**源层**与**编译层**：

```
input/  →  raw/（源层：只追加，不修改）  →  编译  →  subjects/（编译层：可全量重建）
```

- **源层 `raw/`**：`raw/sources/` 存原始上传件（原文件名不变），`raw/notes/` 存按日期归档的加工记录（错题、资料、学习记录、升学资料）。只追加，永不改写。
- **编译层**：每次写入源层后自动编译，把散落在各日期文件里的信息收敛成档案。

一句话：**学生做了什么记在 `raw/`，学生掌握了什么、够不够得着目标算在编译层。**

编译分两族，触发方向不同：

| 编译族 | 产出 | 触发 |
|--------|------|------|
| **学科族** | `subjects/<学科>/topics/<知识点>.md` | **记录驱动**：写入一条错题 → 编译它命中的知识点 |
| **升学族** | `colleges/groups/<院校专业组>.md`、`colleges/majors/<专业>.md` | **目标驱动**：由 `profile.md` 的目标列表决定编译谁 |

升学族之所以反过来，是因为一份全省投档线表含 800+ 个院校专业组，没法在记录里枚举，而学生只关心其中 10-30 个。

这两层的价值：半年后问"我为什么老是错导数应用"，助手能答出"三次里两次都是概念不清（极值点判别），一次才是计算失误"；问"我的选科能报临床医学吗"，助手能直接校验并告诉你目标是否可达——**而选科在高一下之后基本不可逆**。编译层可随时删除并从源层完整重建，因此它是数据的**视图**而非权威存放地。

升学域另有两条不可退让的边界：**位次优先于分数**（分数随试题难度波动，位次跨年可比，档案以位次为主指标）；**不做录取概率预测、不代填志愿**（位次法有系统误差，给出"78% 概率被录取"是虚假精确，只呈现位次差距这一事实，梯度是否合理由学生和家长结合官方渠道判断）。

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

### 建议：合并 AGENTS 约定

安装完成后，建议将 [`skills/studybuddy/templates/AGENTS.md.template`](skills/studybuddy/templates/AGENTS.md.template) 的内容合并进你项目根目录的 `AGENTS.md`（或 `CLAUDE.md`）。这样 agent 在 StudyBuddy 被显式触发之前也能了解 `STUDYBUDDY_DATA_DIR` 等约定，例如被要求直接读写学习数据目录时。

---

## 💾 数据存储

数据存储在环境变量 `STUDYBUDDY_DATA_DIR` 指定的目录中。必须设置该环境变量，否则会提醒用户设置后再继续使用。

 可选环境变量 `STUDYBUDDY_REPORT_WEBHOOK`：设置后，生成的学情报告（日报 / 周报 / 月报 / 专项报告）会在落盘后自动 POST 到该地址（请求体为 `{"content": "<报告正文 Markdown>"}`，**不含 Frontmatter**）；**不设置则安静跳过**，不影响报告生成。详见 [report_workflow.md](skills/studybuddy/references/report_workflow.md) 的「报告推送」章节。

数据目录的完整结构（`profile.md`、`_index.md`、`input/`、`raw/`、`subjects/`、`colleges/`、`archive/`、`output/`）定义在 [SKILL.md 的「数据目录结构」](skills/studybuddy/SKILL.md) 一节。

---

## 📝 核心规则

完整的 16 条核心规则（智能辅导六步法与交互确认、视频推荐、参考材料隔离、日期口径、原始资料存储、源层与编译层分离、编译连接键、证据强度、升学数据的位次优先与选科校验、日志记录等）以 [SKILL.md 的「一页核心规则」](skills/studybuddy/SKILL.md) 为**唯一权威来源**，本文不复述，以免与之产生分歧。

---

## 📖 参考文档

- [SKILL.md](skills/studybuddy/SKILL.md) — 完整教学规则
- [aim_workflow.md](skills/studybuddy/references/aim_workflow.md) — 目标对齐工作流
- [topic_vocabulary.md](skills/studybuddy/templates/topic_vocabulary.md) — 九科知识点受控词表（470 条，建档命名与前置关系派生的权威来源）
- [ingest_subject_workflow.md](skills/studybuddy/references/ingest_subject_workflow.md) — **学科资料导入**完整流程（与 eval 的边界、资料类型切分表、建档粒度三问）
- [ingest_admission_workflow.md](skills/studybuddy/references/ingest_admission_workflow.md) — **升学资料导入**完整流程（`scope` 判定、归档模板、就业数据分级）
- [learn_workflow.md](skills/studybuddy/references/learn_workflow.md) — 知识点学习工作流（含视频推荐规则）
- [classical_workflow.md](skills/studybuddy/references/classical_workflow.md) — 古诗文记忆与理解工作流
- [eval_workflow.md](skills/studybuddy/references/eval_workflow.md) — 作业批改工作流
- [essay_workflow.md](skills/studybuddy/references/essay_workflow.md) — 语文作文批改工作流
- [feedback_workflow.md](skills/studybuddy/references/feedback_workflow.md) — 成绩反馈工作流
- [report_workflow.md](skills/studybuddy/references/report_workflow.md) — 学情追踪工作流
- [ask_workflow.md](skills/studybuddy/references/ask_workflow.md) — 学情提问工作流（只读）
- [compile_subject_workflow.md](skills/studybuddy/references/compile_subject_workflow.md) — **学科族编译**完整流程（知识点档案，记录驱动 push）
- [compile_admission_workflow.md](skills/studybuddy/references/compile_admission_workflow.md) — **升学族编译**完整流程（院校专业组／专业档案，目标驱动 pull）
- [maintain_workflow.md](skills/studybuddy/references/maintain_workflow.md) — 数据维护工作流（体检 / 档案清理 / 重编 / 归档）
- [index_templates.md](skills/studybuddy/templates/index_templates.md) — 索引文件模板
- [topic_templates.md](skills/studybuddy/templates/topic_templates.md) — 知识点档案模板
- [college_templates.md](skills/studybuddy/templates/college_templates.md) — 升学档案模板（院校专业组 / 专业）
- [AGENTS.md.template](skills/studybuddy/templates/AGENTS.md.template) — 安装后建议合并进你项目 AGENTS.md 的技能约定
