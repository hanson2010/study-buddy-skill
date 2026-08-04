# 升学族编译（compile_admission_workflow）

本文件定义**升学族**的编译规则：如何把 `raw/notes/` 下的升学资料记录，按 `profile.md` 的目标列表编译成 [templates/college_templates.md](../templates/college_templates.md) 定义的两类档案。

> [!IMPORTANT]
> **学科族编译**走 [compile_subject_workflow.md](compile_subject_workflow.md)，那是一份**平级的完整流程**。分流在 SKILL.md 完成。
>
> **两条不变式**（`raw/` 只追加不修改；编译层可从源层完整重建）对两族都成立，权威定义在 SKILL.md 的「架构总览」。本文件只引用，不复述，以免两处产生分歧。
>
> **重编的编排与用户确认在 [maintain_workflow.md](maintain_workflow.md)**；本族被重放时的具体规则见下方第八节，与 `compile_subject_workflow.md` 的对应章节平级。

**存储规则见** [ingest_admission_workflow.md](ingest_admission_workflow.md)——那份负责"怎么存"，本文件负责"怎么编"。

---

## 一、为什么触发方向必须反过来

学科族是**记录驱动（push）**：写入一条错题 → 读它的 `topics` → 编译那 2-3 个档案。之所以可行，是因为一条记录只命中少数几个键。

升学族**不成立**：一份《某省 2025 年录取投档线》包含 **800+ 个院校专业组**，一份一分一段表覆盖全省考生。既无法在 frontmatter 里枚举，也没有必要——学生只关心其中 10-30 个。

所以升学族采用**目标驱动（pull）**：

```
学科族（push）：写入记录 → 按记录的 topics 编译
升学族（pull）：profile.md 的目标列表 → 从全部升学资料中提取这些目标的数据
```

**`profile.md` 的「学习目标」章节是升学编译的唯一范围界定**。不在目标列表里的院校专业组和专业，无论资料里出现多少次，都不建档案。

---

## 二、编译的输入

升学族不设 `subject`/`topics`，它的连接键是一组实体标识；**取数方式由 `scope` 决定**（字段定义见 [ingest_admission_workflow.md](ingest_admission_workflow.md) 第三节）：

| 字段 | 必填 | 说明 | 缺失后果 |
|------|------|------|----------|
| `doc_type: admission_data` | ✅ | 标识本条属于升学族，不参与学科档案编译 | 会被当作学科记录处理，因缺 `topics` 而静默漏掉 |
| `scope` | ✅ | `entity` / `bulk` | **无法判断取数方式**，整条记录失效（体检 2.6） |
| `colleges` / `groups` / `majors` | `entity` 时三者至少填一个 | 涉及的院校代码 / 专业组代码 / 专业名称 | 编译无法定位目标，资料被静默漏掉（体检 5.4） |
| `province` + `year` | `bulk` 时必填 | 与 `profile.md` 的**高考省份**匹配；`year` 用于时效判断 | 无法做省份匹配与超期提示（体检 2.8） |
| `credibility` | ✅ | `authoritative` / `reference`；`questionable` 不得入库 | 无法执行就业数据分级（体检 2.7） |
| `academic_year` / `data_type` | 建议 | 招生年度、资料细分类型 | 只影响检索便利，不影响编译能否跑通 |

> **与学科族的关键差别**：学科族的连接键决定"编译到哪里去"（push）；升学族的连接键只决定"这条记录能不能被查到"，**编译到哪里去由 `profile.md` 的目标列表决定**（pull）。

### `scope` 决定数据怎么取

| `scope` | 典型资料 | 编译取数方式 |
|---------|----------|--------------|
| `entity` | 某校招生简章、某校就业年报、某专业介绍 | frontmatter 已枚举 `colleges`/`groups`/`majors`，直接取用 |
| `bulk` | 投档线全量表、一分一段表、批次线 | frontmatter 不枚举实体，编译某目标时**到表里查对应的行** |

`scope: bulk` 的记录只登记在 `colleges/_index.md` 的「参考数据」表，不逐条展开。其 `province` 字段与 `profile.md` 的「高考省份」匹配（而非「学籍省份」）——投档线与一分一段表按考生实际参加高考的省份划定，异地高考/随迁子女场景下两者可能不同。

> **这不是引入 dataset 层**：`scope` 只是记录上的一个标记位，没有新目录、没有 manifest、没有查询配方。但"有些原始资料大到只能查询、不能枚举"这个压力在升学域真实存在（一分一段表就是典型），这是用最小代价回应它。

---

## 三、两个触发点

| 触发 | 动作 |
|------|------|
| **目标变更**（`aim` 增删改 `profile.md` 的目标院校专业组或目标专业） | 对新增目标执行编译：扫描**全部已有**升学资料，抽取该专业组/专业的数据生成档案；删除的目标，其档案移入 `colleges/.archive/` 而非直接删除 |
| **资料导入**（`ingest` 导入新的投档线/简章/就业年报） | **只重编 `profile.md` 中已列出的目标**，不为资料里其余专业组建档案 |

---

## 四、院校专业组档案的编译

1. **定位档案**：`colleges/groups/<college-slug>-<group-code>.md`；`college-slug` 复用 `colleges/_index.md` 中已有的映射，无则新建。同一院校必须始终映射到同一个 slug。
2. **选科与报考条件**：从 `scope: entity` 的招生简章记录取 `subject_requirement`。
3. **选科校验**（关键）：与 `profile.md` 的选科组合比对，写入 `requirement_met` 与 `requirement_status`（✅ 满足 / ❌ 不满足 / ⚠️ 部分满足）。判定为 ❌ 时，编译流程**必须在结果中显式报出**，不得静默写入档案了事。
4. **历年录取**：从 `scope: bulk` 的投档线表中查该 `group_code` 的行，按年份倒序填入 `admission_history`（每年一条，**同时记录该年的 `subject_requirement`**，因为选科要求也可能逐年变化）；**以位次为主指标**，分数为辅；顶层 `subject_requirement` 字段取最新一年的值。
5. **包含专业**：从招生简章取 `contained_majors`，并为其中已在目标列表中的专业建立到 `colleges/majors/` 的链接。
6. **当前差距**：读 Root `_index.md` 最近一次考试成绩 → 查一分一段表反推位次 → 与该组最新 `min_rank` 相减，写入 `current_gap`。
7. **回填索引**：更新 `colleges/_index.md` 的目标索引行。

---

## 五、专业档案的编译

1. **定位档案**：`colleges/majors/<major-slug>.md`。
2. **学什么**：从招生简章、专业介绍记录中提取主干课程与培养方向，附来源链接。
3. **就业与深造**：从就业质量年报等记录提取，**每条数据必须带来源与年份**，并按 `credibility` 过滤：
   - `authoritative`（就业质量年报、教育部/统计局）→ 直接采用
   - `reference`（院校官网、正规行业报告）→ 采用并标注来源
   - `questionable`（自媒体、论坛、培训机构）→ **不写入档案**
4. **开设院校**：只列出 `profile.md` 目标列表中的专业组，不做全国全量收录。
5. **待补数据**：记录缺失的资料类型，供 `aim`/`ingest` 提示用户补充。

---

## 六、一分一段表索引的编译（例外：省份驱动，非目标驱动）

`colleges/scores-distribution.md` 是升学域**唯一不走目标驱动（pull）模型**的编译产物，模板与理由见 [college_templates.md](../templates/college_templates.md) 第七节。

1. **触发**：`ingest` 写入 `data_type: scores_distribution` 的 `scope: bulk` 记录后**立即**编译，不等待 `profile.md` 目标变更。
2. **取数**：按记录的 `province`（对应学生的**高考省份**）与 `year` 定位分组，追加或覆盖该省份年份的一行；`row_count`、`credibility`、`source` 取自记录本身。
3. **为什么是例外**：它是每个省份一份的单例数据，不像投档线表要从 800 个专业组里挑 30 个——不存在目标驱动要解决的组合爆炸问题，eager 编译成本很低且让「当前差距」计算（第四节步骤 6）随时能查到最新表。

---

## 七、数据时效

- 每份录取数据标 `year`，档案记 `latest_data_year`；展示时若最新数据超过 1 年，**主动提示"这是 X 年数据，今年可能变化"**。
- 就业数据记 `employment_data_year`，超过 2 年提示可能失真。
- **不做录取概率预测**：位次法存在系统误差（招生计划变动、大小年、专业组重组、政策调整），给出概率数字是虚假精确，而升学决策不可逆。档案与所有下游输出只呈现位次差距这一事实。

---

## 八、本族的重放规则（供重编调用）

重编本身是 `maintain` 子命令的操作，**编排与用户确认在 [maintain_workflow.md](maintain_workflow.md)**；本节只定义"轮到升学族时怎么重放"。学科族的重放规则见 [compile_subject_workflow.md](compile_subject_workflow.md) 对应章节。

### 重放范围

| 范围 | 覆盖对象 |
|------|----------|
| **单一目标** | `profile.md` 目标列表中的一个院校专业组或一个专业，对应单个 `colleges/groups/<...>.md` 或 `colleges/majors/<...>.md` |
| **全部目标** | `colleges/groups/`、`colleges/majors/` 下全部档案 + `colleges/_index.md` 动态章节 + `colleges/scores-distribution.md` |

### 执行步骤

1. **清空档案**：删除范围内的档案文件。
2. **按目标列表重新拉取**：读 `profile.md` 的目标院校专业组与目标专业，对每个目标执行第四、五节的编译流程。
   - **顺序无关**——这是与学科族最大的差别。pull 模型每次都从全量资料里重新取数，不存在"错因史依赖时间正序"那类约束，因此不需要按 `date` 排序重放。
3. **重建一分一段表索引**：重新扫描 `raw/notes/` 下全部 `data_type: scores_distribution` 记录，重建 `colleges/scores-distribution.md`。**按省份重建，不受目标列表限制**（第六节的省份驱动例外同样适用于重编）。
4. **重跑选科校验**：对每个目标与 `profile.md` 的选科组合比对；判为 ❌ 的必须在结果中显式报出，不得静默写入档案了事。
5. **回填索引**：更新 `colleges/_index.md` 的目标索引、专业索引与参考数据表；若影响 Root `_index.md` 的目标进度，同步刷新。

### 归档数据的处理

升学资料（`doc_type: admission_data`）**从不进入 `archive/`**——学年归档明确跳过它（见 [maintain_workflow.md](maintain_workflow.md) 的「归档单位」），因此本族重编始终能扫到全部年份的投档线与一分一段表。

**为什么必须这样**：学科族重编时档案本身不删，历史错因史留在档案里；而本族是 pull——档案里的历年数据每次都要从 `raw/notes/` 重新查出来，源记录一旦被跳过，数据就直接消失。高三做差距分析时要用的，恰恰是高一高二导入的那几年投档线。

---

## 九、操作概要记入 log 文件

增量编译的记录**并入触发它的子命令的 log 条目**（通常是 `ingest` 导入升学资料，或 `aim` 变更目标），不单独成条。在该条目中增加一行：

```markdown
- **编译更新**：colleges/groups/pku-1000101.md（投档线刷新至 2025 年，位次差距 -754）
```

重编单独成条：

```markdown
### YYYY-MM-DD HH:MM:SS
- **操作类型**：重新编译（升学目标）
- **重编范围**：北京大学 1000101 专业组
- **拉取来源**：raw/notes/ 中 2 条 entity 记录 + 3 条 bulk 表
- **生成档案**：colleges/groups/pku-1000101.md
- **更新索引**：colleges/_index.md 目标索引 1 行
- **核心数据**：最新数据年份 2025，最低位次 486，当前差距 -754；选科校验 ✅ 满足
```

---

## 十、与学科族的联动

编译完成后，两层可以合成一件单独任何一层都做不到的事——**把升学目标翻译成知识点行动**：

```
目标专业组 min_rank → 目标总分（查一分一段表反推）
  → 各科目标分（profile.md）
  → 与最近考试成绩比对得出各科分差
  → 分差最大的科目 → 取其 subjects/<学科>/_index.md 的薄弱点索引
  → 与该科「高频考点」交叉 → 提分性价比排序
```

> 末端取**薄弱点索引**（只含 `error_count ≥ 1`），与 [aim_workflow.md](aim_workflow.md) 同一口径——提分性价比需要失分数据作输入，📘 已学未测的知识点没有这项数据，另行单列。

具体输出规则见 [aim_workflow.md](aim_workflow.md) 的「学习规划」一节。

---

## 十一、使用示例

### 示例：导入投档线后的目标驱动编译（隐式）

```text
这是我们省2025年的录取投档线，请整理一下。
[上传图片]
```

`ingest` 把整张表存为一条 `scope: bulk` 记录，随后编译**只处理 `profile.md` 里的 9 个目标专业组**，从表中查出各自的投档线与最低位次刷新档案——表里其余 800 个专业组不建档案。若某个目标在表中查不到（如今年未在本省招生），在档案的「待补数据」中记录并提示用户。
