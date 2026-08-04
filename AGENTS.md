# StudyBuddy - 项目说明（AGENTS）

本仓库是 **StudyBuddy** 的学习助手项目。主 skill 被调用时的完整行为规范、子命令、教学流程、核心规则与视频推荐策略，统一以 [`skills/studybuddy/SKILL.md`](skills/studybuddy/SKILL.md) 及其 `references/` 下各 workflow 文件为**权威来源**。

> 本文件是**本仓库**的仓库级约定，面向维护/修改这些文档的 agent。技能被安装到其他项目后、运行时应遵守的约定（如 `STUDYBUDDY_DATA_DIR`）不在此文件——那是随技能一起分发给终端用户的内容，见 [`skills/studybuddy/templates/AGENTS.md.template`](skills/studybuddy/templates/AGENTS.md.template)，不要与本文件混淆。

## 一致性检查

本仓库没有代码，**文档即 prompt**——任意两份文件之间的矛盾都是一个真实的行为缺陷。修改任何 `.md` 后请运行：

```bash
python tools/check_docs.py     # 无依赖，仅用标准库；退出码 0 表示通过
```

它会检查：

- 链接与脚本引用是否存在
- 章节编号是否连续（跳过代码围栏）
- `subject:` 是否取自九科枚举
- 原始文件路径键名是否统一为 `source_path`
- **学科编译连接键是否统一为数组 `topics:`**（单值 `topic:` 会让命中多个知识点的记录只编译进一个档案，其余档案永远收不到——最难肉眼发现的一类缺陷；知识点档案模板豁免）
- **编译层是否混入日期目录**（`subjects/` 下的学科目录后面、或 `colleges/` 后面直接跟年份或 `YYYY` 占位符，即违反「源层与编译层分离」不变式，通常是迁移遗漏或规则回潮）

  > 注意：本检查按字面匹配路径，因此**文档里不能写出该反例的字面形式**，否则会检查到自己。需要举例时改用 `<年>/<月>` 这类中文占位符。
- 日志路径（`output/YYYY/MM/`）与源层路径（`raw/sources/YYYY/MM/`、`raw/notes/YYYY/MM/`）是否唯一
- 同名平台是否出现多个域名

## 架构不变式（改文档时最容易违反的两条）

数据分为**源层**与**编译层**，这是理解全部规则的前提：

```
input/  →  raw/（源层：只追加，不修改）  →  编译  →  subjects/（编译层：可全量重建）
```

1. **`raw/` 只追加，不改写**。`raw/sources/YYYY/MM/` 存原始上传件（原文件名），`raw/notes/YYYY/MM/` 存按日期归档的加工记录。
2. **编译层只由编译生成**，且必须满足「全部删除后能从 `raw/` 完整重建」。编译层有两个：`subjects/`（学科：`_index.md` + `topics/<知识点>.md`）与 `colleges/`（升学：`_index.md` + `groups/` + `majors/` + `scores-distribution.md`）。两者**均严禁出现按年月分的日期目录**——凡按日期归档的东西一律属于 `raw/notes/`。

两族编译的**触发方向不同**：学科族是记录驱动（写入记录 → 编译它命中的 `topics`），升学族是目标驱动（`profile.md` 的目标列表 → 从全部资料中提取）。原因见 `references/compile_admission_workflow.md` 第一节。

### 两族文件完全平铺

`references/` 下**不设父子层级**——两族各有一份自足的完整流程，分流由 `SKILL.md` 判定，agent 识别出资料族后只读对应那一份：

| | 学科族 | 升学族 |
|---|---|---|
| 导入 | `ingest_subject_workflow.md`（完整：识别 → 存储 → 解析 → 归档 → 编译触发 → log → `input/` 清理） | `ingest_admission_workflow.md`（同样完整，各步骤自己写一遍） |
| 编译 | `compile_subject_workflow.md`（完整：输入 → 增量编译 → 四段正文 → 状态重算 → 前置 → 本族重放 → log） | `compile_admission_workflow.md`（同样完整） |

**这是刻意接受重复换来的**：两族只有存储脊柱相同，解析、连接键、编译目标、触发方向全都不同。为共用那点脊柱做成父子结构，代价是每次导入一份讲义都要连带读完投档线规则。平铺后每份自足、按需加载。

**防漂移约定（改文档时必须遵守）**：

1. **允许重复的只有「操作步骤」**——原件归档、日期口径、log 格式、`input/` 清理这类**怎么做**的描述，两族各写一遍是正常的。
2. **判定口径绝不重复**——建档粒度三问、状态流转、证据强度、复习优先级公式、两条架构不变式，一律只在唯一权威处定义（`SKILL.md` / `topic_templates.md`），两族文件只引用、不复述。**这类重复才是真正的行为缺陷**：两处各自演化，agent 会照着过时的那份执行。
3. **重编的编排在 `maintain_workflow.md`**（范围确定、用户确认、log），两族各自只写「本族被重放时怎么放」。两族的重放规则本就不同——学科族必须按 `date` 升序，升学族顺序无关。
4. 新增一条规则前先判断它属于哪一族：**只对学科成立**（`topics`、知识点档案、错因史）→ 学科文件；**只对升学成立**（`scope`、选科校验、位次）→ 升学文件；**两族都成立且属于判定口径** → 写进 `SKILL.md`，两族文件各留一条指针；**两族都成立但属于操作步骤** → 两边各写一遍。

这四条 `tools/check_docs.py` 断言不了，只能靠人工守。

写文档时若要新增一个"保存到某处"的规则，先判断它属于哪一层：**学生做了什么记在 `raw/`，学生掌握了什么、够不够得着目标算在编译层**。这两条已由 `tools/check_docs.py` 机械断言，写错会直接报错。

## 文档入口

skill 的完整行为规范以 `skills/<skill_name>/SKILL.md` 为唯一权威来源（见本文件开头），此处不重复列出其下各 `references/`、`templates/` 文件，避免与 SKILL.md 自身的「参考文档」章节产生第二份索引、互相漂移。

唯一需要在此单独强调的是：

- 随技能分发给终端用户的 AGENTS 约定模板（不要与本文件混淆）：`skills/studybuddy/templates/AGENTS.md.template`
