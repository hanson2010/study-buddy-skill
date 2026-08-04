# 升学资料导入（ingest_admission_workflow）

本文件定义**升学资料**（招生政策、招生简章、投档线、一分一段、就业年报）的完整导入流程，从原件归档一直到触发编译。

> [!IMPORTANT]
> **学科资料**（课本、讲义、笔记、题源、参考材料）走 [ingest_subject_workflow.md](ingest_subject_workflow.md)，那是一份**平级的完整流程**，不是本文件的父文档。分流在 SKILL.md 完成——agent 识别出资料族后直接读对应的那一份。
>
> 两族的存储规则（原件归档、日期口径、log、`input/` 清理）刻意在两份文件里**各写一遍**：这样每份都自足。代价是重复，收益是不必为了导入一份投档线去翻两百行课本切分规则。
>
> 用户从来不需要知道这个区分：`ingest` 识别出资料族后自动走对应规则。

**编译规则见** [compile_admission_workflow.md](compile_admission_workflow.md)——本文件负责"怎么存"，那份负责"怎么编"。

---

## 一、识别线索与流程概览

出现以下任一特征即判为升学资料：院校名称与招生代码、专业组代码、投档线／最低位次、分数段与累计人数、批次控制线、选科要求、就业率／深造率；或用户明确说明是"招生简章／投档线／一分一段／就业报告"。

升学资料**不属于任何学科**，不设 `subject` 与 `topics`，学科短码固定用 `admission`。

**输入来源**（两种）：
- **GUI 直接上传**：用户在对话中直接上传图片、文档或输入文字
- **`input/` 目录扫描**：Agent 扫描 `<STUDYBUDDY_DATA_DIR>/input/`（扁平，无日期层），逐个处理待导入文件。触发方式为用户明确要求，不主动轮询

**本流程的步骤**：

```
输入来源（GUI 上传 / input/ 目录扫描）
  → 2. 原件存入 raw/sources/YYYY/MM/
  → 2.5 非文本转换（如需）
  → 3. 解析（先判 scope）
  → 4. 归档进 raw/notes/
  → 5. 触发目标驱动（pull）编译
  → 6. 记入 log
  → 7. 清理 input/（仅当来源为 input/）
```

---

## 二、原件存储与非文本转换

### 2. 原始资料存储

按核心规则 2，将原件存入 `raw/sources/YYYY/MM/`：

- **存储时机**：文件接收后**立即存储**，且**只存储一次**，后续步骤直接引用，不重复拷贝
- **年月取值**：按核心规则 1 取**事件日期**（资料的发布或适用日期，如"2025 年投档线"取 2025 年的发布月），无法识别时才用当前时间
- **文件命名**：使用原始文件名，冲突时加数字后缀
- **去重检查**：拷贝前检查目标目录是否已有同名文件，已存在则跳过拷贝、直接引用
- **路径引用**：在 `raw/notes/` 记录的 `source_path` 中写相对路径

**来源为 `input/` 目录时**：先**复制**到 `raw/sources/YYYY/MM/`，`input/` 中的原件**暂不删除**——等第 7 步确认整个流程走完才移除，避免中途失败丢资料。

### 2.5 非文本内容转换（本 skill 不负责）

> [!NOTE]
> **本 skill 仅处理文本内容**。投档线表、一分一段表常以 PDF、图片或 Excel 形式提供，本 skill **不直接做 OCR / 格式转换**。
>
> - 由 Agent 选择当前环境中**其他可用的 skill 或工具**完成转换，变成文本后再交给本流程。
> - 原始非文本文件仍按上一步存入 `raw/sources/YYYY/MM/`，并在结果文件中引用其路径。
> - 若环境中无可用转换工具，提示用户以文本形式提供，再继续导入。
>
> **对 `bulk` 大表尤其重要**：转换必须保留**全部行**。表格被截断是最难发现的一类损坏——编译时查不到某个专业组，会被误当成"该校今年未在本省招生"。

---

## 三、解析（先判 `scope`）

**先判定 `scope`**——这决定后续怎么存、怎么编译：

| `scope` | 判定标准 | 典型资料 |
|---------|----------|----------|
| `entity` | 资料围绕**少数几个明确实体**展开 | 某校招生简章、某校就业质量年报、某专业介绍 |
| `bulk` | 资料是**覆盖大量实体的全量表** | 全省投档线表、一分一段表、各批次控制线 |

**为什么要区分**：一份全省投档线表包含 800+ 个院校专业组，无法在 frontmatter 里枚举，也没有必要——学生只关心其中 10-30 个。`bulk` 记录保留完整表格内容，编译时**按需查询**对应行。

**解析要求**：

- `entity` 资料：提取院校代码、专业组代码与名称、选科要求、包含专业、招生计划、历年投档数据、就业指标等
- `bulk` 资料：**完整保留表格**，不做裁剪或摘要——编译时要按行查询，裁掉的行就永久丢失了。表格过大时按分数段或批次拆成子文件，主文件保留目录

> **切分单元由 `scope` 决定，不套用学科族的「章/节/篇」口径**——[ingest_subject_workflow.md](ingest_subject_workflow.md) 第 4 步的资料类型切分表只管学科资料。

---

## 四、归档与命名

**归档位置**：`raw/notes/YYYY/MM/<YYYY-MM-DD>-admission-<descriptive-slug>.md`

升学资料不属于任何学科，学科短码固定用 `admission`。

**Frontmatter 模板（`scope: entity`）**：
```yaml
---
date: YYYY-MM-DD              # 事件日期（资料发布/适用日期），决定目录与文件名
ingested_at: YYYY-MM-DD       # 导入日期，仅作审计，不参与路径
doc_type: admission_data      # 不属于任何学科，故不设 subject 与 topics
scope: entity
data_type: admission_info     # admission_info / employment / major_info / policy
title: [资料名称]
colleges:                      # 涉及的院校代码
  - "10001"
groups:                        # 涉及的院校专业组代码
  - "1000101"
majors:                        # 涉及的专业名称
  - 计算机科学与技术
academic_year: 2026            # 该资料适用的招生年度
credibility: authoritative     # authoritative / reference；questionable 不得入库
source_path: raw/sources/YYYY/MM/<原始文件名>
---
```

**Frontmatter 模板（`scope: bulk`）**：
```yaml
---
date: YYYY-MM-DD
ingested_at: YYYY-MM-DD
doc_type: admission_data
scope: bulk
data_type: admission_lines    # admission_lines / scores_distribution / batch_lines
title: [资料名称]
province: [省份]                # 与 profile.md 的「高考省份」匹配，而非「学籍省份」
year: 2025                     # 数据年份，用于时效判断
subject_type: [物理类 / 历史类]
batch: [本科批 / 本科提前批]
row_count: [表格行数]
credibility: authoritative
source_path: raw/sources/YYYY/MM/<原始文件名>
# 不枚举 colleges/groups/majors——编译时按需查询表格内容
---
```

> [!WARNING]
> `scope: entity` 的记录**必须**至少填写 `colleges`、`groups`、`majors` 三者之一，否则编译无法定位目标，该资料会被静默漏掉。数据体检会专门检查这一点（体检 5.4）。
>
> `scope` 本身缺失更严重——编译连取数方式都判断不了，整条记录失效（体检 2.6）。`scope: bulk` 缺 `province`/`year` 会导致无法做省份匹配与超期提示（体检 2.8）。

---

## 五、触发目标驱动（pull）编译

升学资料写入 `raw/notes/` 后，编译**不遍历资料里的实体**，而是**读 `profile.md` 的目标列表**，只刷新已列为目标的院校专业组与专业档案（完整规则见 [compile_admission_workflow.md](compile_admission_workflow.md)）：

1. 读 `profile.md` 的「学习目标」章节，取目标院校专业组与目标专业列表
2. 对每个目标：
   - 从 `scope: entity` 记录取选科要求、包含专业、就业指标
   - 从 `scope: bulk` 记录**查询**该专业组对应的行，取投档线与最低位次
3. 刷新 `colleges/groups/` 与 `colleges/majors/` 下的档案
4. **重跑选科校验**：与 `profile.md` 的选科组合比对，判定 ✅ 满足 / ❌ 不满足 / ⚠️ 部分满足；判为 ❌ 时必须在本次回复中显式报出
5. 回填 `colleges/_index.md` 的目标索引与参考数据表

**例外：`data_type: scores_distribution`（一分一段表）不受目标列表限制**——写入后立即编译更新 `colleges/scores-distribution.md` 对应省份年份的一行，与 `profile.md` 是否已设定目标无关（规则见 [compile_admission_workflow.md](compile_admission_workflow.md) 第六节）。

**目标列表为空时（其余 `scope: bulk` 数据）**：只把记录登记到 `colleges/_index.md` 的「参考数据」表，不建任何档案，并提示用户"这份资料已存档，设定目标院校后会自动用上"。

**目标查不到数据时**：在档案的「待补数据」中记录缺口（如"缺少 2025 年投档线"），并提示用户可以上传相应资料。

---

## 六、就业数据的检索与可信度

就业与薪资数据在网络上噪音极大（培训机构营销、自媒体炒作），必须按来源分级：

| 级别 | 来源 | 处理 |
|------|------|------|
| `authoritative` | 高校就业质量年报、教育部/统计局数据 | 直接采用，标注年份 |
| `reference` | 院校官网专业介绍、正规行业报告 | 采用并标注来源 |
| `questionable` | 自媒体、论坛、培训机构、贴吧 | **不写入记录**；确需提及时在对话中明确标注为传闻 |

需要联网补充就业数据时，检索式优先锁定权威来源，而非泛搜"XX专业好不好"：

```
"[院校名] 毕业生就业质量年度报告 [年份]"
"[专业名] 就业 site:edu.cn"
```

---

## 七、检索与复用

遵循核心规则 8 的固定顺序，**优先读编译层**：

1. **`colleges/_index.md`** 的目标索引与参考数据表——"有哪些目标、各自差多少"到这一层就够了
2. **`colleges/groups/`、`colleges/majors/` 档案**——需要单个目标的选科要求、历年录取、包含专业、就业与深造时
3. **`colleges/scores-distribution.md`**——需要做分数↔位次换算时
4. **`raw/notes/` 的 `scope: bulk` 记录**——需要按行查投档线原表、一分一段表原始逐行数据时（编译层只存索引，不重复存表）
5. **`raw/sources/`**——需要看简章扫描件或原始表格文件时

---

## 八、不参与学年归档

`doc_type: admission_data` 的记录**留在活跃层，不随学年归档移入 `archive/`**。

升学族是目标驱动（pull）编译——档案里的数据不是"存下来的"，是每次重编时从 `raw/notes/` 重新查出来的；一旦被归档（归档数据默认不参与检索），下次全量重编就会丢失那些年份的投档线与位次。完整理由见 [maintain_workflow.md](maintain_workflow.md) 的「归档单位」。

---

## 九、收尾：log 与 `input/` 清理

### 6. 操作概要记入 log 文件

每次导入后记入 `output/YYYY/MM/YYYY-MM-DD-log.md`：

**记录内容**：
- **操作类型**：升学资料导入
- **处理的文件**：`raw/sources/` 中的原件路径、涉及的院校或省份
- **生成的文件**：`raw/notes/` 记录路径，含 `scope` 与（`bulk` 时）表格行数
- **编译更新**：刷新的院校专业组／专业档案，或 `scores-distribution.md`
- **更新的索引**：`colleges/_index.md` 的目标索引与参考数据表
- **核心数据**：`scope`、数据年份、刷新的目标数、**选科校验结果**（满足／不满足各几个）

**记录格式**：
```markdown
## 操作记录

### YYYY-MM-DD HH:MM:SS
- **操作类型**：升学资料导入
- **处理文件**：raw/sources/2026/07/beijing_2025_lines.pdf
- **生成文件**：raw/notes/2026/07/2026-07-15-admission-beijing-2025-lines.md（scope: bulk，812 行）
- **编译更新**：colleges/groups/pku-1000101.md、colleges/groups/ruc-1002803.md 等 9 个目标专业组（投档线与位次刷新至 2025 年）
- **更新索引**：colleges/_index.md（目标索引 9 行、参考数据表 +1）
- **核心数据**：scope=bulk，数据年份 2025，刷新 9 个目标；选科校验 8 满足 / 1 不满足（临床医学组要求 化学+生物）
```

> 选科校验判为 ❌ 时，除了记入 log，**必须在本次回复中显式报出**（核心规则 14）——目标不可达是本技能能提前捕获的、后果最严重的错误。

### 7. 移动 `input/` 中的原文件（仅当来源为 `input/` 时）

**触发条件**：仅当本次原件来自 `input/` 目录扫描时执行；GUI 直接上传不涉及。

**执行时机**：作为单份资料导入的最后一步，在第 3–6 步（解析、归档、编译、日志）**全部成功完成后**才执行。

**执行内容**：
- 原件已在第 2 步归档至 `raw/sources/YYYY/MM/`，此时移除 `input/` 中的副本
- 批量场景逐个文件独立判断；未走完流程的一律**保留**在 `input/` 不动——常见原因是缺 `scope`、缺 `credibility`、`bulk` 表转换后行数明显不足——并在回复中逐个说明原因
- 移除失败（如权限问题）不阻断其余部分，告知用户手动清理

---

## 十、使用示例

### 示例1：导入招生简章（`scope: entity`）
```text
这是北京大学2026年的招生简章，请帮我保存。
[上传图片]
```
存为 `scope: entity` 记录，填 `colleges`/`groups`/`majors`；随后按 `profile.md` 的目标列表刷新相关专业组档案并重跑选科校验。

### 示例2：导入投档线全量表（`scope: bulk`）
```text
这是我们省2025年的录取投档线，请整理一下。
[上传图片]
```
整张表存为一条 `scope: bulk` 记录并**完整保留表格**；编译只查 `profile.md` 里那几个目标专业组对应的行，不为表中其余专业组建档案。

### 示例3：导入就业质量年报
```text
这是清华的就业质量报告，帮我导入。
[上传文件]
```
存为 `scope: entity`、`data_type: employment`、`credibility: authoritative` 的记录；编译刷新相关专业档案的「就业与深造」，每条数据带来源与年份。

### 示例4：aim 对话中途上传资料
```text
（在讨论目标院校时）等下，这是我刚查到的人大投档线。
[上传图片]
```
`aim` 转 `ingest` 完成存储与编译，再回到 `aim` 继续目标对齐——用户无需切换命令。
