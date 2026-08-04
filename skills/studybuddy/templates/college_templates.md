# 升学档案模板定义

本文件定义升学编译层 `<STUDYBUDDY_DATA_DIR>/colleges/` 下两类档案的模板格式。档案由编译流程按**目标驱动（pull）**模型自动创建与维护，规则见 [references/compile_admission_workflow.md](../references/compile_admission_workflow.md)。

> [!IMPORTANT]
> **档案属于编译层，不可手工编辑**。所有升学资料一律经 `ingest` 写入 `raw/notes/`，再由编译刷新档案。`colleges/` 下只有 `_index.md`、`groups/`、`majors/`、`scores-distribution.md` 四种内容，**不含日期目录**——按日期归档的记录属于源层。

---

## 一、两类档案的分工

| 档案 | 路径 | 回答什么 | 数据来源 |
|------|------|----------|----------|
| **院校专业组档案** | `colleges/groups/<college-slug>-<group-code>.md` | 能不能考上：选科要求、历年投档线与位次、招生计划、当前差距 | 招生简章、投档线表、一分一段表 |
| **专业档案** | `colleges/majors/<major-slug>.md` | 值不值得读：学什么、就业去向、深造率、哪些院校开设 | 专业介绍、就业质量年报 |

**为什么拆成两个**：就业数据挂在**专业**上，不挂在专业组上。「计算机科学与技术学什么、去哪就业」在几十个院校专业组里是同一份内容——只建专业组档案会把它复制几十次。两者靠双向引用组成图，不复制内容。

---

## 二、录取数据模型

新高考按「院校 — 院校专业组 — 具体专业」三层组织，**平行志愿的投档单位是院校专业组**。

### 1. 院校信息（University Info）
- `college_code`：院校招生代码（5 位数字，如 `10001`）
- `college_name`：院校名称（如 `北京大学`）
- `province`：院校所在地省份（用于区分本省与外省；与学生 `profile.md` 的「高考省份」是两个概念，一个是院校注册地，一个是学生实际参加高考的省份）

### 2. 院校专业组（College Major Group）
每个专业组是独立的投档主体，有专属招生代码、选科要求和投档分数线。
- `group_code`：专业组招生代码（通常为院校代码 + 2-3 位数字，如 `1000101`）
- `group_name`：专业组名称（通常按选科或大类命名，如 `物理类-计算机与电子信息组`）
- `subject_requirement`：选科限制（如 `物理+化学`、`物理（不限）`、`历史（不限）`）
- `contained_majors`：包含专业列表，每个专业含 `major_code`、`major_name`、`tuition`、`duration`

### 3. 录取与投档数据（Admission & Enrollment）
- `academic_year`：录取年份
- `batch`：录取批次（如 `本科批`、`本科提前批`）
- `admission_line`：投档分数线（该专业组录取最低分，即门槛分）
- `min_rank`：最低录取位次（**跨年对比时比分数更具参考价值**）
- `enrollment_plan` / `actual_enrollment`：计划与实际录取人数
- `major_admission_details`：组内具体专业的录取详情（`major_code`、`major_name`、`min_score`、`min_rank`）

> [!IMPORTANT]
> **考生个人信息**（姓名、学籍省份、高考省份、选科组合、教材版本等）是学生的背景档案，统一保存在 `profile.md`，**禁止在 `colleges/` 下以任何形式保存**（如 candidate-info.md）。编译与匹配时直接从 `profile.md` 读取。`scope: bulk` 参考数据（投档线、一分一段表）的 `province` 字段与「高考省份」匹配，而非「学籍省份」。

---

## 三、院校专业组档案模板

### 命名

`colleges/groups/<college-slug>-<group-code>.md`，如 `pku-1000101.md`、`ruc-1002803.md`。`college-slug` 取院校英文缩写或拼音短横线命名，同一院校必须始终映射到同一个 slug。

### Frontmatter

```yaml
---
doc_type: college_group
college_name: 北京大学
college_slug: pku
college_code: "10001"
group_code: "1000101"
group_name: 物理类-计算机与电子信息组
college_province: 北京
subject_requirement: 物理+化学        # 选科限制原文，取 latest_data_year 那一年的值，供选科校验直接读取
requirement_met: true                 # 选科校验结果，由编译比对 profile.md 得出
requirement_status: 满足              # 满足 / 不满足 / 部分满足
priority: 冲                          # 冲 / 稳 / 保，同步自 profile.md
batch: 本科批
contained_majors:                     # → colleges/majors/<slug>.md
  - 计算机科学与技术
  - 人工智能
  - 电子信息科学与技术
admission_history:                    # 按年份倒序，位次为主指标；选科要求逐年记录，因为它也可能变化
  - year: 2025
    subject_requirement: 物理+化学
    admission_line: 692
    min_rank: 486
    enrollment_plan: 32
  - year: 2024
    subject_requirement: 物理+化学
    admission_line: 688
    min_rank: 512
    enrollment_plan: 30
latest_data_year: 2025                # 最新数据年份，用于时效提示
current_gap:                          # 当前差距，每次成绩录入后刷新
  student_rank: 1240
  rank_gap: -754                      # 负数表示尚未达到
  as_of: 2026-07-12
sources:                              # 编译自哪些 raw/notes/ 记录
  - raw/notes/2026/07/2026-07-12-admission-pku-enrollment-guide.md
  - raw/notes/2026/07/2026-07-15-admission-beijing-2025-lines.md
---
```

### 正文（四段）

```markdown
# 北京大学 物理类-计算机与电子信息组（1000101）

> 优先级：冲 ｜ 选科校验：✅ 满足（要求 物理+化学，你的选科 物理+化学+生物）
> 最新数据：2025 年 ｜ 当前位次差距：1240 → 486，还差 754 位

## 一、选科与报考条件

- **选科要求**：物理+化学
- **校验结果**：✅ 满足
- 其他限制：[体检要求、单科成绩要求等，无则写「无特殊要求」]

## 二、历年录取（位次优先）

| 年份 | 选科要求 | 投档线 | 最低位次 | 计划数 | 实录数 |
|------|----------|--------|----------|--------|--------|
| 2025 | 物理+化学 | 692 | 486 | 32 | 32 |
| 2024 | 物理+化学 | 688 | 512 | 30 | 31 |

> 分数随试题难度波动，**位次跨年可比**，以位次为准判断差距。
> 招生计划变动、大小年现象、专业组重组都会让历史数据失效，不得把历史位次当作今年的确定门槛。
> **选科要求逐年记录而非只存一份**：部分专业组的选科要求会跨年调整（如从「不限」收紧为「物理+化学」），若只存当前值会丢失这一变化，选科校验也可能误判往年数据。

## 三、包含专业

| 专业 | 学费 | 学制 | 专业档案 |
|------|------|------|----------|
| 计算机科学与技术 | 5300 元/年 | 4 年 | [computer-science](../majors/computer-science.md) |
| 人工智能 | 5300 元/年 | 4 年 | [artificial-intelligence](../majors/artificial-intelligence.md) |

## 四、当前差距

- 最近一次考试（2026-07 期末）估算位次：**1240**
- 目标位次（2025 年最低位次）：**486**
- 差距：**754 位**
- 数据来源：`_index.md` 历次考试成绩 + 一分一段表 `raw/notes/2026/07/2026-07-15-admission-beijing-2025-distribution.md`

> 不做录取概率预测。位次法存在系统误差（招生计划变动、大小年、政策调整），此处只呈现位次差距这一事实。
```

---

## 四、专业档案模板

### 命名

`colleges/majors/<major-slug>.md`，如 `computer-science.md`、`clinical-medicine.md`。

### Frontmatter

```yaml
---
doc_type: major
major_name: 计算机科学与技术
major_slug: computer-science
category: 工学-计算机类               # 学科门类-专业类
common_requirement: 物理+化学          # 多数院校的选科要求（不是硬约束，仅供反向推荐）
offered_by:                            # → colleges/groups/<slug>.md
  - pku-1000101
  - tsinghua-1000301
employment_data_year: 2025             # 就业数据年份，用于时效提示
employment_credibility: authoritative  # authoritative / reference，questionable 不入档
sources:
  - raw/notes/2026/07/2026-07-20-admission-pku-employment-report.md
---
```

### 正文（四段）

```markdown
# 计算机科学与技术

> 学科门类：工学-计算机类 ｜ 多数院校选科要求：物理+化学
> 就业数据年份：2025（来源：高校就业质量年报，权威级）

## 一、学什么

[主干课程、能力培养方向、与相近专业（软件工程、人工智能、电子信息）的区别]
来源：[北京大学2026年招生简章](../../raw/notes/2026/07/2026-07-12-admission-pku-enrollment-guide.md)

## 二、就业与深造

| 指标 | 数值 | 年份 | 来源级别 |
|------|------|------|----------|
| 深造率 | [%] | 2025 | 权威 |
| 就业率 | [%] | 2025 | 权威 |
| 主要行业去向 | [行业分布] | 2025 | 权威 |
| 主要就业地区 | [地区分布] | 2025 | 权威 |

> 每条数据必须标注**来源与年份**。就业与薪资数据在网络上噪音极大，存疑来源（自媒体、论坛、培训机构）**不写入本档案**。
> 本节只呈现数据，不对专业做「好/不好」的价值判断——权衡由学生和家长自己完成。

## 三、开设该专业的目标院校专业组

| 院校专业组 | 优先级 | 选科要求 | 最新最低位次 | 档案 |
|------------|--------|----------|--------------|------|
| 北京大学-1000101 | 冲 | 物理+化学 | 486 | [pku-1000101](../groups/pku-1000101.md) |

> 只列出 `profile.md` 中已设为目标的专业组（pull 编译模型），不做全国全量收录。

## 四、待补数据

- [尚未导入的资料类型，如「缺少 2025 年就业质量年报」]，可提示用户上传或联网检索
```

---

## 五、选科校验状态

由编译比对 `profile.md` 的选科组合与专业组的 `subject_requirement` 得出，是升学域最重要的一次判定。

| 状态 | 判定 | 处理 |
|------|------|------|
| ✅ 满足 | 学生选科覆盖该组全部要求 | 正常参与差距分析 |
| ❌ 不满足 | 学生选科不满足要求 | **该目标不可达**，必须明确告知；不得静默写入 `profile.md`；数据体检列为高严重度 |
| ⚠️ 部分满足 | 该组本身不限选科，但该专业在多数院校要求更严 | 提示当前组合会缩小可选院校范围，给出仍可报的目标数 |

> **为什么这条最重要**：选科在高一下学期后基本不可逆。一旦目标专业要求物理+化学而学生选了物理+地理，再努力也够不着——这是本技能能提前捕获的、后果最严重且完全可预防的错误。

---

## 六、`colleges/_index.md` 中的索引行

每个档案在 [index_templates.md](index_templates.md) 定义的 `colleges/_index.md` 中占一行。索引回答「有哪些目标」，档案回答「每个目标具体怎么样」——检索时先读索引，命中后再打开档案。

---

## 七、一分一段表索引（`colleges/scores-distribution.md`）

### 为什么单独建一份

一分一段表（分数-位次换算表）是**当前差距**（第三节）与**目标分设定**共用的查询依据，但它本身既不属于某个院校专业组，也不属于某个专业——按目标驱动（pull）model 编译会导致同一张表被每个目标各查一次却不落地，且无法追踪"这个省份已经导入了哪几年的表"。因此它是**唯一的编译层单例文件**，直接放在 `colleges/` 下，不进 `groups/` 或 `majors/`。

> [!IMPORTANT]
> 这是升学域目标驱动（pull）模型的**唯一例外**：一分一段表按**高考省份**索引，不按 `profile.md` 的目标列表筛选——因为它是每个省份一份的单例数据，不是像投档线表那样需要从 800 个专业组里挑 30 个的组合数据，不存在同样的规模问题。触发规则见 [compile_admission_workflow.md](../references/compile_admission_workflow.md) 第六节。

### Frontmatter

```yaml
---
doc_type: scores_distribution_index
provinces:                              # 按高考省份分组，通常只有一个，异地高考/转学场景下可能有多个
  - province: 北京
    years:
      - year: 2025
        subject_type: 物理类            # 3+1+2 省份区分物理类/历史类；3+3 省份可省略
        row_count: 1024
        credibility: authoritative
        source: raw/notes/2026/07/2026-07-15-admission-beijing-2025-distribution.md
      - year: 2024
        subject_type: 物理类
        row_count: 1018
        credibility: authoritative
        source: raw/notes/2025/07/2025-07-10-admission-beijing-2024-distribution.md
latest_year:
  北京: 2025
---
```

### 正文

```markdown
# 一分一段表索引

> 编译层单例文件，`colleges/` 下唯一，不按院校/专业拆分文件。按学生的**高考省份**索引已导入的一分一段表年份；原始逐行数据保留在 `raw/notes/` 的 `scope: bulk` 记录里，本文件只做跨年索引，不重复存储。

## 一、已收录年份（按高考省份分组）

### 北京

| 年份 | 类别 | 行数 | 来源 | 可信度 |
|------|------|------|------|--------|
| 2025 | 物理类 | 1024 | [2026-07-15-admission-beijing-2025-distribution.md](../../raw/notes/2026/07/2026-07-15-admission-beijing-2025-distribution.md) | 权威 |
| 2024 | 物理类 | 1018 | [2025-07-10-admission-beijing-2024-distribution.md](../../raw/notes/2025/07/2025-07-10-admission-beijing-2024-distribution.md) | 权威 |

> 最新年份：2025

## 二、用途

- **分数 → 位次**：把最近一次考试估算分数换算成位次，供「当前差距」（第三节）使用；
- **位次 → 分数**：把目标院校专业组的 `min_rank` 换算成分数，供目标分设定使用；
- **跨年趋势**：同一位次在不同年份对应的分数差异，用于识别试题难度波动，避免直接套用去年分数线。

## 三、数据缺口

- [如「缺 2023 年及以前数据，跨年趋势暂只能看 2 年」]
```

### 编译与维护

- **触发**：`ingest` 导入 `data_type: scores_distribution` 的 `scope: bulk` 记录后立即追加/更新对应省份年份的一行，无需等待目标变更（见上方例外说明）。
- **全量重编**：重新扫描 `raw/notes/` 下全部 `data_type: scores_distribution` 记录并重建整份索引。
- **数据体检**：索引内容与 `raw/notes/` 实际存在的记录是否一致，纳入 `maintain_workflow.md` 的体检项。
