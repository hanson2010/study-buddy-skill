# 知识点受控词表（九科预置）

本文件是本技能的**知识点受控词表**：九科高频考点的规范中文名与对应 slug。它是建档命名的权威来源。

> [!IMPORTANT]
> **本文件不写入学生数据目录**。它是随技能分发的参考数据，运行时查阅；学生的 `subjects/<学科>/_index.md` 里那份「高频考点」是给学生看的概览（见 [index_templates.md](index_templates.md) 第 4 节），两者内容一致但用途不同——**命名冲突时以本文件为准**。

---

## 一、三个用途

| 用途 | 出处 | 词表不全会怎样 |
|------|------|----------------|
| **建档命名的受控词表** | [topic_templates.md](topic_templates.md) 第一节复用查找第 2 步 | 同一知识点被起两个 slug（「导数应用」与「导数的应用」各建一份档案），错因史被劈成两半 |
| **`prerequisites` 初始骨架的派生源** | [compile_subject_workflow.md](../references/compile_subject_workflow.md) 第六节 | 前置追溯失效，"错导数应用其实是函数单调性没通"这类诊断做不出来 |
| **提分性价比的分值权重** | [aim_workflow.md](../references/aim_workflow.md) 的「学习规划」 | 高频考点与低频考点同权，补漏顺序失真 |

---

## 二、使用规则

### 1. 建档时的查找顺序

1. 先查学生的学科 `_index.md` **知识点索引**——已有同名则复用其 slug
2. 再查本文件对应学科——命中则**用本文件的规范名与 slug**
3. 都不中才允许新造，并**在回复中告知用户**："新建了一个不在词表中的知识点：XXX"

### 2. 词表不是穷举，也不该被当成穷举

本表覆盖的是**反复出现、值得独立建档**的考点。它必然有遗漏：教材版本差异、省份自主命题、新课标调整都会带来表外考点。所以第 3 步的"允许新造"是正常路径，不是异常——**只是要让用户看见**，避免同义词悄悄分叉。

反过来，**表内条目不等于必须建档**。学生没碰过的考点不建档；建档由实际的资料导入或作答触发（见建档粒度三问）。

### 3. 粒度基线

本表条目一律是**可独立出一组题、会反复出错**的单元——这正是建档粒度三问的通过线。

- 比它**大**的是 `theme`（函数与导数、电磁学、细胞代谢），进 `_index.md` 的「高频主题」，不建档
- 比它**小**的是义项／步骤／特例（虚词「之」的取独用法、洛必达法则的一次套用），并入上位条目

### 4. 维护：预置静态，真题只提建议

本表是**静态预置内容**，随技能版本更新，**运行时不被任何流程自动改写**——它随技能分发，不是学生数据，改它属于技能维护。

但预置内容会陈旧（新课标调整、省份自主命题、题型演变），所以导入**高可信度资料**时 agent 应主动比对并提出建议：

| 触发资料 | `exam_authority` | 该做什么 |
|---|---|---|
| 高考真题卷 | `gaokao_real` | 逐题比对考点；**表外考点**在回复中列出并建议补入词表；表内长期未出现的条目建议降权 |
| 省市统考／联考卷 | `provincial_mock` | 同上，但只提示不催促——命题风格未必等同高考 |
| 校内模考卷 | `school_mock` | **不据此建议改词表**——校内命题会把教师个人偏好当成高考趋势 |
| 考纲／考试说明 | — | 对照考纲条目提出增删建议，交用户确认 |

> [!WARNING]
> **建议 ≠ 自动改写，统计 ≠ 押题**。
>
> - agent 只在**回复中**列出建议，由用户决定是否反馈给技能维护者；运行时不改本文件，也不改学生 `_index.md` 的静态章节。
> - 统计"过去三年真题里这个考点考了几次"是事实陈述；推断"今年会考什么"是虚假精确。与「不做录取概率预测」同源——**不做押题**（见 SKILL.md 安全边界）。
> - 样本量不足时不下结论：少于 3 份 `gaokao_real` 时只报次数，不给"高频／低频"判定。

---

## 三、九科词表

格式：`规范中文名 · slug`，按 `theme` 分组；`theme` 与 [index_templates.md](index_templates.md) 第 4 节各科的「高频主题」一致。

---

### 语文

#### 现代文阅读
- 论述类文本论证分析 · `argumentative-text-analysis`
- 论述类文本信息筛选与推断 · `argumentative-text-inference`
- 实用类文本信息整合 · `practical-text-synthesis`
- 非连续性文本比较阅读 · `non-continuous-text-comparison`
- 小说情节结构分析 · `fiction-plot-structure`
- 小说人物形象分析 · `fiction-character-analysis`
- 小说环境描写作用 · `fiction-setting-function`
- 散文线索与结构 · `prose-structure`
- 散文语言赏析 · `prose-language-appreciation`
- 句段作用分析 · `paragraph-function-analysis`
- 标题与主旨探究 · `title-and-theme`

#### 整本书阅读

> 新课标「整本书阅读与研讨」任务群。**十三年真题、几十回练习考的是同这几个能力点**——按回目、按年份、按练习份数各建一档是典型的结构抄写错误。

- 《红楼梦》整本书阅读 · `hongloumeng-reading`
- 《乡土中国》整本书阅读 · `xiangtu-zhongguo-reading`
- 名著人物形象分析 · `classic-character-analysis`
- 名著情节梳理与结构 · `classic-plot-structure`
- 名著主题与思想意蕴 · `classic-theme-analysis`
- 学术著作概念理解与论证把握 · `academic-work-comprehension`

#### 古诗文阅读
- 文言实词理解 · `content-word-comprehension`
- 文言虚词用法 · `function-word-usage`
- 词类活用 · `part-of-speech-conversion`
- 古今异义与通假字 · `semantic-shift-and-loan-words`
- 文言特殊句式 · `special-sentence-patterns`
- 文言翻译技巧 · `classical-translation`
- 文言断句 · `classical-punctuation`
- 古代文化常识 · `classical-culture-knowledge`
- 文言文内容概括与分析 · `classical-content-analysis`
- 古诗词意象与意境 · `imagery-appreciation`
- 古诗词情感主旨 · `poetry-theme-and-emotion`
- 古诗词表达技巧 · `poetry-technique-analysis`
- 炼字炼句 · `diction-analysis`
- 名篇名句默写准确性 · `recitation-accuracy`

#### 语言文字运用
- 成语与词语辨析 · `idiom-discrimination`
- 病句辨析与修改 · `sentence-error-correction`
- 标点符号运用 · `punctuation-usage`
- 语句衔接与排序 · `sentence-cohesion`
- 补写句子 · `sentence-completion`
- 压缩语段 · `passage-condensation`
- 修辞手法辨识与效果 · `rhetorical-devices`
- 句式变换与仿写 · `sentence-transformation`
- 语言得体 · `language-appropriateness`

#### 写作
- 作文审题立意 · `essay-thesis-framing`
- 作文结构安排 · `essay-structure`
- 作文论证方法 · `essay-argumentation`
- 作文素材运用 · `essay-material-usage`
- 作文语言表达 · `essay-language-quality`
- 任务驱动型作文 · `task-driven-essay`
- 应用文写作格式 · `practical-writing-format`
- 微写作 · `micro-writing`

---

### 数学

#### 预备知识
- 集合运算与关系 · `set-operations`
- 充分必要条件 · `necessary-sufficient-conditions`
- 全称量词与存在量词 · `quantifiers`
- 不等式解法 · `inequality-solving`
- 基本不等式 · `basic-inequality`

#### 函数与导数
- 函数概念与表示 · `function-concept`
- 函数定义域与值域 · `function-domain-range`
- 函数单调性 · `function-monotonicity`
- 函数奇偶性 · `function-parity`
- 函数周期性与对称性 · `function-periodicity-symmetry`
- 二次函数 · `quadratic-function`
- 指数函数 · `exponential-function`
- 对数函数 · `logarithmic-function`
- 幂函数 · `power-function`
- 函数图像变换 · `function-graph-transformation`
- 函数零点与方程根 · `function-zeros`
- 导数概念与几何意义 · `derivative-geometric-meaning`
- 导数运算法则 · `derivative-rules`
- 导数与单调性 · `derivative-monotonicity`
- 导数与极值最值 · `derivative-applications`
- 导数与不等式证明 · `derivative-inequality-proof`
- 恒成立与存在性问题 · `always-holds-problems`

#### 三角与解三角形
- 任意角与弧度制 · `angle-and-radian`
- 三角函数定义与诱导公式 · `trig-definition-and-induction`
- 三角函数图像与性质 · `trig-graph-properties`
- 三角恒等变换 · `trig-identities`
- 辅助角公式 · `auxiliary-angle-formula`
- 正弦定理 · `law-of-sines`
- 余弦定理 · `law-of-cosines`
- 解三角形面积与最值 · `triangle-area-and-extremum`

#### 数列
- 等差数列 · `arithmetic-sequence`
- 等比数列 · `geometric-sequence`
- 数列通项公式求法 · `sequence-general-term`
- 错位相减法求和 · `sequence-sum-shifting`
- 裂项相消法求和 · `sequence-sum-telescoping`
- 分组与并项求和 · `sequence-sum-grouping`
- 递推数列 · `recursive-sequence`
- 数列与不等式 · `sequence-inequality`

#### 平面向量与复数
- 平面向量基本定理与坐标运算 · `vector-coordinates`
- 平面向量数量积 · `vector-dot-product`
- 向量的几何应用 · `vector-geometry-application`
- 复数的运算与几何意义 · `complex-numbers`

#### 立体几何
- 空间几何体表面积与体积 · `solid-surface-volume`
- 点线面位置关系 · `spatial-position-relations`
- 平行的判定与性质 · `parallelism-proof`
- 垂直的判定与性质 · `perpendicularity-proof`
- 空间向量基本定理 · `spatial-vector-basics`
- 空间向量求线面角 · `line-plane-angle`
- 空间向量求二面角 · `dihedral-angle`
- 空间距离计算 · `spatial-distance`
- 外接球与内切球 · `circumscribed-inscribed-sphere`

#### 解析几何
- 直线方程与位置关系 · `line-equation`
- 圆的方程与直线与圆 · `circle-equation`
- 椭圆定义与标准方程 · `ellipse-equation`
- 椭圆几何性质 · `ellipse-properties`
- 双曲线定义与渐近线 · `hyperbola-asymptote`
- 抛物线定义与焦点弦 · `parabola-focal-chord`
- 直线与圆锥曲线位置关系 · `line-conic-intersection`
- 圆锥曲线中的定点定值 · `conic-fixed-point-value`
- 圆锥曲线中的最值与范围 · `conic-extremum-range`

#### 概率统计
- 计数原理与排列组合 · `permutation-combination`
- 二项式定理 · `binomial-theorem`
- 古典概型 · `classical-probability`
- 条件概率与全概率公式 · `conditional-probability`
- 互斥事件与独立事件 · `mutually-exclusive-independent`
- 随机变量分布列与期望方差 · `random-variable-distribution`
- 二项分布与超几何分布 · `binomial-hypergeometric`
- 正态分布 · `normal-distribution`
- 统计图表与数字特征 · `statistical-charts`
- 成对数据与线性回归 · `linear-regression`
- 独立性检验 · `independence-test`

---

### 英语

#### 阅读理解
- 细节理解题 · `reading-detail`
- 推理判断题 · `reading-inference`
- 主旨大意题 · `reading-main-idea`
- 词义猜测题 · `reading-word-guessing`
- 作者态度与写作意图 · `reading-author-attitude`
- 篇章结构与段落大意 · `reading-text-structure`
- 七选五（信息还原） · `reading-gap-sentence`

#### 完形填空
- 完形词汇辨析 · `cloze-word-choice`
- 完形语境推理 · `cloze-context-inference`
- 完形逻辑衔接 · `cloze-logical-connection`
- 完形固定搭配 · `cloze-collocation`

#### 语法填空与语法
- 时态与语态 · `tense-and-voice`
- 非谓语动词 · `non-finite-verbs`
- 定语从句 · `attributive-clause`
- 名词性从句 · `noun-clause`
- 状语从句 · `adverbial-clause`
- 冠词与介词 · `article-preposition`
- 词性转换与构词法 · `word-formation`
- 主谓一致 · `subject-verb-agreement`
- 情态动词与虚拟语气 · `modal-subjunctive`
- 特殊句式（倒装/强调/省略） · `special-structures`

#### 写作
- 应用文格式与要点覆盖 · `applied-writing-format`
- 读后续写情节构思 · `continuation-plot`
- 读后续写语言与细节描写 · `continuation-language`
- 概要写作信息提炼 · `summary-writing`
- 高级句式运用 · `advanced-sentence-patterns`
- 语篇衔接与连贯 · `writing-cohesion`

#### 词汇
- 核心词汇拼写与词义 · `core-vocabulary`
- 短语动词与固定搭配 · `phrasal-verbs`
- 近义词辨析 · `synonym-discrimination`

---

### 物理

#### 力学
- 匀变速直线运动 · `uniform-acceleration`
- 运动图像分析 · `motion-graphs`
- 受力分析与共点力平衡 · `force-analysis`
- 牛顿运动定律 · `newtons-laws`
- 连接体与整体隔离法 · `connected-bodies`
- 平抛运动 · `projectile-motion`
- 圆周运动与向心力 · `circular-motion`
- 万有引力与天体运动 · `gravitation-celestial`
- 功和功率 · `work-and-power`
- 动能定理 · `kinetic-energy-theorem`
- 机械能守恒 · `mechanical-energy-conservation`
- 动量定理与动量守恒 · `momentum-conservation`
- 碰撞与爆炸 · `collision-explosion`
- 摩擦力与相对滑动 · `friction-relative-sliding`

#### 电磁学
- 库仑定律与电场强度 · `coulomb-electric-field`
- 电势与电势能 · `electric-potential`
- 带电粒子在电场中运动 · `charged-particle-in-field`
- 电容器 · `capacitor`
- 闭合电路欧姆定律 · `closed-circuit-ohms-law`
- 电路动态分析 · `circuit-dynamic-analysis`
- 磁感应强度与安培力 · `ampere-force`
- 洛伦兹力与带电粒子在磁场中运动 · `lorentz-force`
- 复合场中的运动 · `combined-fields`
- 法拉第电磁感应定律 · `faraday-law`
- 楞次定律与感应电流方向 · `lenz-law`
- 导体棒切割磁感线 · `rod-cutting-field-lines`
- 自感与涡流 · `self-induction`
- 交变电流与变压器 · `ac-and-transformer`

#### 热学
- 分子动理论 · `molecular-kinetic-theory`
- 理想气体状态方程 · `ideal-gas-law`
- 气体实验定律 · `gas-laws`
- 热力学第一定律 · `first-law-thermodynamics`
- 固体液体与物态变化 · `solids-liquids-phase`

#### 振动波动与光学
- 简谐运动 · `simple-harmonic-motion`
- 机械波的传播 · `mechanical-waves`
- 波的干涉与衍射 · `wave-interference-diffraction`
- 多普勒效应 · `doppler-effect`
- 光的折射与全反射 · `refraction-total-reflection`
- 光的干涉与衍射 · `light-interference`

#### 近代物理
- 光电效应 · `photoelectric-effect`
- 波粒二象性 · `wave-particle-duality`
- 原子结构与能级跃迁 · `atomic-energy-levels`
- 原子核衰变与半衰期 · `nuclear-decay`
- 核反应与质能方程 · `nuclear-reaction-mass-energy`

#### 实验与方法
- 力学实验数据处理 · `mechanics-experiment`
- 电学实验器材选择与电路设计 · `electrical-experiment-design`
- 实验误差分析 · `experimental-error-analysis`

---

### 化学

#### 化学反应原理
- 化学反应速率及影响因素 · `reaction-rate`
- 化学平衡状态判定 · `equilibrium-state`
- 化学平衡移动与勒夏特列原理 · `equilibrium-shift`
- 化学平衡常数计算 · `equilibrium-constant`
- 转化率与产率计算 · `conversion-yield`
- 反应热与盖斯定律 · `enthalpy-hess-law`
- 弱电解质电离平衡 · `ionization-equilibrium`
- 水的电离与溶液 pH · `ph-calculation`
- 盐类水解 · `salt-hydrolysis`
- 沉淀溶解平衡与 Ksp · `solubility-equilibrium`
- 原电池原理与电极反应式 · `galvanic-cell`
- 电解池与电镀 · `electrolytic-cell`
- 金属腐蚀与防护 · `metal-corrosion`

#### 物质结构与性质
- 原子结构与核外电子排布 · `atomic-structure`
- 元素周期律与周期表 · `periodic-law`
- 化学键类型与极性 · `chemical-bonds`
- 分子空间构型与杂化轨道 · `molecular-geometry-hybridization`
- 分子间作用力与氢键 · `intermolecular-forces`
- 晶体类型与性质 · `crystal-types`
- 配合物 · `coordination-compounds`

#### 元素及其化合物
- 钠及其化合物 · `sodium-compounds`
- 铝及其化合物 · `aluminum-compounds`
- 铁及其化合物 · `iron-compounds`
- 铜及其化合物 · `copper-compounds`
- 氯及其化合物 · `chlorine-compounds`
- 硫及其化合物 · `sulfur-compounds`
- 氮及其化合物 · `nitrogen-compounds`
- 碳硅及其化合物 · `carbon-silicon-compounds`
- 氧化还原反应配平 · `redox-balancing`
- 离子反应与离子方程式 · `ionic-equations`
- 离子共存判断 · `ion-coexistence`
- 化工流程分析 · `industrial-process-analysis`

#### 有机化学基础
- 有机物命名 · `organic-nomenclature`
- 同分异构体书写与判断 · `isomerism`
- 烃类性质（烷烯炔芳） · `hydrocarbon-properties`
- 卤代烃 · `haloalkanes`
- 醇酚性质 · `alcohol-phenol`
- 醛酮性质 · `aldehyde-ketone`
- 羧酸与酯 · `carboxylic-acid-ester`
- 有机反应类型判断 · `organic-reaction-types`
- 有机合成路线设计 · `organic-synthesis-route`
- 有机推断题 · `organic-structure-deduction`
- 糖类蛋白质与高分子 · `biomolecules-polymers`

#### 化学实验
- 常见气体的制备与净化 · `gas-preparation`
- 物质的分离与提纯 · `separation-purification`
- 溶液配制与滴定操作 · `titration-operation`
- 实验方案设计与评价 · `experiment-design-evaluation`
- 物质检验与鉴别 · `substance-identification`
- 阿伏加德罗常数判断 · `avogadro-constant`
- 化学计算（物质的量） · `mole-calculation`

---

### 生物

#### 分子与细胞
- 细胞中的元素与化合物 · `cell-molecules`
- 蛋白质结构与功能 · `protein-structure-function`
- 核酸的结构与功能 · `nucleic-acid-structure`
- 细胞膜与物质运输方式 · `membrane-transport`
- 细胞器结构与功能 · `organelle-function`
- 酶的特性与影响因素 · `enzyme-properties`
- ATP 与能量代谢 · `atp-energy`
- 光合作用过程 · `photosynthesis-process`
- 光合作用影响因素与曲线分析 · `photosynthesis-factors`
- 细胞呼吸过程与类型 · `cellular-respiration`
- 光合与呼吸的关系 · `photosynthesis-respiration-relation`
- 细胞周期与有丝分裂 · `mitosis`
- 减数分裂 · `meiosis`
- 细胞分化衰老与凋亡 · `cell-differentiation-apoptosis`

#### 遗传与进化
- 孟德尔分离定律 · `mendel-segregation`
- 孟德尔自由组合定律 · `mendel-independent-assortment`
- 遗传概率计算 · `genetic-probability`
- 伴性遗传 · `sex-linked-inheritance`
- 系谱图分析 · `pedigree-analysis`
- DNA 是遗传物质的实验 · `dna-genetic-material-experiments`
- DNA 分子结构与复制 · `dna-structure-replication`
- 基因的表达（转录与翻译） · `gene-expression`
- 基因突变与基因重组 · `gene-mutation-recombination`
- 染色体变异 · `chromosome-variation`
- 育种方法比较 · `breeding-methods`
- 现代生物进化理论 · `evolution-theory`
- 基因频率计算 · `allele-frequency`

#### 稳态与调节
- 内环境稳态 · `homeostasis`
- 神经调节与反射弧 · `neural-regulation`
- 兴奋的产生与传导 · `nerve-impulse-conduction`
- 突触传递 · `synaptic-transmission`
- 神经系统的分级调节 · `nervous-system-hierarchy`
- 激素调节与分级调节 · `hormone-regulation`
- 血糖与体温水盐平衡调节 · `glucose-temperature-osmotic-regulation`
- 免疫系统与免疫过程 · `immune-response`
- 免疫失调与免疫学应用 · `immune-disorders`
- 植物激素调节 · `plant-hormones`

#### 生物与环境
- 种群数量特征与增长曲线 · `population-growth`
- 群落结构与演替 · `community-succession`
- 生态系统的组成与营养结构 · `ecosystem-structure`
- 能量流动 · `energy-flow`
- 物质循环 · `matter-cycling`
- 生态系统的信息传递与稳定性 · `ecosystem-stability`
- 生态环境保护与生态足迹 · `environmental-protection`

#### 生物技术与工程
- 微生物培养与分离 · `microbial-culture`
- 发酵工程 · `fermentation-engineering`
- 基因工程操作流程 · `genetic-engineering-process`
- PCR 技术 · `pcr-technique`
- 细胞工程与克隆 · `cell-engineering`
- 胚胎工程 · `embryo-engineering`
- 生物技术的安全与伦理 · `biotech-ethics`

#### 实验与方法
- 实验变量控制与对照设置 · `experimental-variable-control`
- 生物图表与曲线分析 · `biology-graph-analysis`
- 教材经典实验 · `textbook-classic-experiments`

---

### 政治

#### 中国特色社会主义
- 社会形态更替与人类社会发展规律 · `social-development-law`
- 科学社会主义的创立与发展 · `scientific-socialism`
- 新民主主义革命与社会主义制度确立 · `socialist-system-establishment`
- 改革开放与中国特色社会主义道路 · `reform-opening-up`
- 习近平新时代中国特色社会主义思想 · `xi-thought`

#### 经济与社会
- 生产资料所有制与基本经济制度 · `ownership-system`
- 按劳分配与多种分配方式 · `distribution-system`
- 完善个人收入分配与社会保障 · `income-distribution-security`
- 市场资源配置与市场失灵 · `market-allocation`
- 宏观调控与经济政策 · `macro-regulation`
- 新发展理念与高质量发展 · `high-quality-development`
- 建设现代化经济体系 · `modern-economic-system`
- 就业与劳动者权益 · `employment-labor-rights`

#### 政治与法治
- 中国共产党的领导与执政 · `party-leadership`
- 人民代表大会制度 · `people-congress-system`
- 中国共产党领导的多党合作和政治协商制度 · `multiparty-cooperation`
- 民族区域自治与基层群众自治 · `autonomy-systems`
- 人民民主专政与公民权利义务 · `citizen-rights-duties`
- 政府职能与依法行政 · `government-functions`
- 全面依法治国与法治体系 · `rule-of-law`
- 科学立法严格执法公正司法全民守法 · `legislation-enforcement-judicature`

#### 哲学与文化
- 哲学基本问题与唯物主义唯心主义 · `philosophy-basic-question`
- 物质与意识的辩证关系 · `matter-consciousness`
- 规律的客观性与主观能动性 · `objective-laws-subjectivity`
- 实践与认识的辩证关系 · `practice-and-cognition`
- 真理的客观性与具体性 · `truth-nature`
- 联系的观点 · `dialectics-connection`
- 发展的观点 · `dialectics-development`
- 矛盾的观点（对立统一） · `dialectics-contradiction`
- 辩证否定观与创新意识 · `dialectical-negation`
- 社会存在与社会意识 · `social-existence-consciousness`
- 社会基本矛盾与改革 · `social-basic-contradiction`
- 人民群众是历史创造者 · `mass-view-of-history`
- 人生价值与价值观导向 · `value-orientation`
- 文化的内涵与功能 · `culture-function`
- 文化多样性与文化交流 · `cultural-diversity`
- 中华优秀传统文化与文化自信 · `traditional-culture-confidence`
- 文化创新与文化发展 · `cultural-innovation`

#### 当代国际政治与经济
- 国家利益与国际关系 · `national-interest-relations`
- 主权国家与国际组织 · `sovereign-states-organizations`
- 联合国与全球治理 · `un-global-governance`
- 世界多极化与经济全球化 · `multipolarity-globalization`
- 中国的外交政策与人类命运共同体 · `chinas-diplomacy`
- 国际经济合作与世界贸易组织 · `international-economic-cooperation`

#### 法律与生活
- 民事权利与民事责任 · `civil-rights-liability`
- 合同订立与履行 · `contract-law`
- 家庭婚姻与继承 · `marriage-inheritance`
- 就业与劳动合同 · `labor-contract`
- 侵权责任 · `tort-liability`
- 诉讼程序与证据规则 · `litigation-procedure`

#### 逻辑与思维
- 概念的内涵与外延 · `concept-intension-extension`
- 判断的类型与运用 · `judgment-types`
- 演绎推理 · `deductive-reasoning`
- 归纳与类比推理 · `inductive-analogical-reasoning`
- 辩证思维与创新思维 · `dialectical-creative-thinking`

#### 答题规范
- 主观题原理调用与材料结合 · `subjective-principle-application`
- 措施类与意义类设问作答 · `measure-significance-question`
- 选择题干扰项排除 · `mcq-distractor-elimination`

---

### 历史

#### 中国古代史
- 早期国家与华夏认同 · `early-states-huaxia`
- 春秋战国变革与百家争鸣 · `spring-autumn-warring-states`
- 秦汉大一统与中央集权确立 · `qin-han-centralization`
- 三国两晋南北朝民族交融 · `wei-jin-ethnic-integration`
- 隋唐制度创新与繁荣 · `sui-tang-institutions`
- 宋元经济发展与社会变化 · `song-yuan-economy-society`
- 明清君主专制强化 · `ming-qing-autocracy`
- 中央集权与地方治理演变 · `central-local-governance`
- 选官制度演变 · `civil-service-selection`
- 赋税制度演变 · `taxation-system-evolution`
- 儒家思想的演变 · `confucianism-evolution`
- 古代经济重心南移 · `economic-center-southward`
- 古代科技与文化成就 · `ancient-science-culture`

#### 中国近代史
- 鸦片战争与不平等条约体系 · `opium-wars-treaties`
- 太平天国与洋务运动 · `taiping-self-strengthening`
- 甲午战争与瓜分狂潮 · `sino-japanese-war-1894`
- 戊戌变法与义和团运动 · `reform-1898-boxer`
- 辛亥革命与中华民国建立 · `xinhai-revolution`
- 新文化运动与五四运动 · `new-culture-may-fourth`
- 中国共产党成立与国民革命 · `ccp-founding-national-revolution`
- 土地革命与红军长征 · `agrarian-revolution-long-march`
- 抗日战争 · `war-of-resistance`
- 解放战争 · `war-of-liberation`
- 近代民族资本主义发展 · `modern-national-capitalism`

#### 中国现代史
- 新中国成立与政权巩固 · `prc-founding`
- 三大改造与社会主义制度建立 · `socialist-transformation`
- 社会主义建设的探索与曲折 · `socialist-construction-exploration`
- 改革开放的进程 · `reform-opening-process`
- 中国特色社会主义的发展成就 · `contemporary-china-achievements`
- 新中国外交成就 · `prc-diplomacy`

#### 世界古代与近代史
- 古代文明的产生与早期帝国 · `ancient-civilizations`
- 中古时期的欧洲与亚洲 · `medieval-europe-asia`
- 新航路开辟与早期殖民扩张 · `age-of-exploration`
- 文艺复兴与宗教改革 · `renaissance-reformation`
- 启蒙运动 · `enlightenment`
- 英国资产阶级革命与君主立宪 · `english-revolution`
- 美国独立战争与联邦制 · `american-revolution`
- 法国大革命与拿破仑帝国 · `french-revolution`
- 第一次工业革命 · `first-industrial-revolution`
- 第二次工业革命与垄断资本主义 · `second-industrial-revolution`
- 马克思主义诞生与巴黎公社 · `marxism-paris-commune`
- 亚非拉民族解放运动 · `national-liberation-movements`

#### 世界现代史
- 第一次世界大战与凡尔赛—华盛顿体系 · `wwi-versailles-system`
- 十月革命与苏联社会主义建设 · `october-revolution-ussr`
- 1929 年经济危机与罗斯福新政 · `great-depression-new-deal`
- 法西斯主义与第二次世界大战 · `wwii-fascism`
- 冷战与两极格局 · `cold-war-bipolar`
- 战后资本主义的新变化 · `postwar-capitalism`
- 世界殖民体系瓦解与新兴国家 · `decolonization`
- 世界多极化与经济全球化趋势 · `multipolarization-globalization`

#### 史学素养与答题规范
- 史料类型与史料价值判断 · `historical-source-evaluation`
- 时空定位与阶段特征 · `chronological-spatial-positioning`
- 材料信息提取与概括 · `material-information-extraction`
- 原因背景类设问作答 · `cause-background-questions`
- 影响评价类设问作答 · `impact-evaluation-questions`
- 比较异同类设问作答 · `comparison-questions`
- 唯物史观的运用 · `historical-materialism-application`

---

### 地理

#### 地球运动与地图
- 经纬网与地图判读 · `map-reading`
- 等高线地形图判读 · `contour-map-reading`
- 地球自转及其地理意义 · `earth-rotation`
- 地球公转与昼夜长短变化 · `daylight-variation`
- 正午太阳高度计算 · `solar-altitude`
- 地方时与时区计算 · `time-zone-calculation`

#### 大气
- 大气受热过程 · `atmospheric-heating`
- 热力环流与风 · `thermal-circulation`
- 气压带与风带 · `pressure-wind-belts`
- 常见天气系统（锋面气旋） · `weather-systems`
- 气候类型判读 · `climate-type-identification`
- 气候成因分析 · `climate-formation`
- 全球气候变化 · `global-climate-change`

#### 水文
- 水循环环节与意义 · `water-cycle`
- 河流水文与水系特征 · `river-characteristics`
- 洋流分布与影响 · `ocean-currents`
- 湖泊湿地与地下水 · `lakes-wetlands-groundwater`
- 海—气相互作用与厄尔尼诺 · `sea-air-interaction`

#### 地貌与地质
- 内力作用与板块运动 · `endogenic-plate-tectonics`
- 岩石圈物质循环 · `rock-cycle`
- 流水地貌 · `fluvial-landforms`
- 风沙地貌 · `aeolian-landforms`
- 喀斯特与冰川海岸地貌 · `karst-glacial-coastal-landforms`
- 地质构造与地貌 · `geological-structures`

#### 土壤与植被
- 土壤形成因素与剖面 · `soil-formation`
- 植被类型与环境的关系 · `vegetation-environment`
- 自然地理环境的整体性 · `physical-environment-integrity`
- 自然带与地域分异规律 · `zonal-differentiation`

#### 人文地理
- 人口分布与人口容量 · `population-distribution-capacity`
- 人口迁移的影响因素 · `population-migration`
- 人口结构与人口问题 · `population-structure`
- 城镇空间结构与功能区 · `urban-spatial-structure`
- 城镇化及其问题 · `urbanization`
- 地域文化与城乡景观 · `regional-culture-landscape`
- 农业区位因素 · `agricultural-location`
- 农业地域类型 · `agricultural-types`
- 工业区位因素 · `industrial-location`
- 工业地域与产业集聚 · `industrial-agglomeration`
- 交通运输布局及其影响 · `transportation-layout`
- 服务业区位 · `service-industry-location`

#### 区域发展与国家安全
- 区域差异与区域联系 · `regional-differences-links`
- 流域综合开发治理 · `river-basin-development`
- 生态脆弱区与荒漠化水土流失 · `ecologically-fragile-areas`
- 资源枯竭型城市转型 · `resource-exhausted-cities`
- 产业转移与区域协作 · `industrial-transfer`
- 资源跨区域调配 · `resource-allocation-projects`
- 粮食与耕地安全 · `food-land-security`
- 能源安全与环境安全 · `energy-environmental-security`
- 自然灾害类型与防治 · `natural-disasters`

#### 地理信息技术与答题规范
- 遥感、GPS 与 GIS 的应用 · `geographic-information-technology`
- 统计图表判读 · `statistical-chart-reading`
- 成因类设问作答 · `cause-type-questions`
- 影响评价类设问作答 · `impact-type-questions`
- 措施对策类设问作答 · `measure-type-questions`
- 区位分析类设问作答 · `location-analysis-questions`
