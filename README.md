# doubao-book-zettelkasten · 书籍精读 × 卢曼卡片盒笔记工作流

> 电子书 → 费曼式精读 → HTML 精读报告 → Zettelkasten 卡片盒 → Logseq 知识库 → AI 检索

一个把"读完一本书"变成"沉淀一套可检索的知识资产"的 **AI Agent 编排技能（Skill）**。本仓库即技能本体，安装到支持 Skill 的 Agent 环境（如 Doubao Work）后，AI 可自动执行以下完整流水线：

```
电子书(PDF/EPUB/MD/Word/TXT)
   │  ① 格式解析（MinerU / pandoc）
   ▼
Markdown 原文（保留章节层级）
   │  ② 费曼精读（预览定位→三层笔记→大白话讲解→自测联结）
   ▼
精读笔记 + HTML 精读报告（可独立打开的交付物）
   │  ③ ④ 卡片盒生成（金句/概念/方法/疑问 四类原子卡片）
   ▼
Logseq 原生笔记（pages/*.md，双链互联）
   │  ⑤ ⑥ 入库 + 检索支持（直接读库 / 本地 RAG）
   ▼
以后向 AI 提问 → AI 从 Logseq 图库调取资料回答
```

---

## 目录结构

```
doubao-book-zettelkasten/
├── SKILL.md                    # 技能主文件（触发词 + 六阶段编排 + 质量门）
├── README.md                   # 本文档：环境、依赖、安装、用法
├── LICENSE                     # MIT
├── references/                 # 各阶段完整规范（Agent 执行时按需读取）
│   ├── 01-parsing.md           #   输入解析：PDF/EPUB/DOCX/MD/TXT 路由
│   ├── 02-feynman.md           #   费曼精读四步协议
│   ├── 03-report.md            #   HTML 精读报告八必备章节
│   ├── 04-cards.md             #   卡片盒规范（类型/字段/命名/原子化）
│   ├── 05-logseq.md            #   Logseq 落库与降级导入
│   └── 06-retrieval.md         #   检索支持（档位 A/B）
├── scripts/
│   └── make_card.py            #   cards.json → 批量生成 Logseq 卡片
└── assets/
    └── templates/              # 书页/概念页/金句卡/方法卡 模板
        ├── book-page.md
        ├── concept-page.md
        ├── quote-card.md
        └── method-card.md
```

---

## 环境要求

| 项 | 要求 | 说明 |
|---|---|---|
| 操作系统 | macOS / Linux（Windows 需另行验证） | 已在 macOS 与本项目沙箱 Linux 双环境实测 |
| Agent 环境 | 支持 Skill 机制的 AI Agent（Doubao Work / 类 Codex Agent） | 技能本体是 SKILL.md + 附属文件，无编译过程 |
| Python | 3.8+ | 仅用于 `scripts/make_card.py`（标准库，无第三方依赖） |
| Git | 2.x | 可选；仅发布/回滚时用 |

---

## 依赖工具与插件

按六阶段流水线所需，分三类列出。**核心必装**为灰色高亮项，其余为对应场景的增强项。

### ① 格式解析层

| 工具/软件 | 用途 | 必装 | 安装/说明 |
|---|---|---|---|
| **MinerU** | PDF → Markdown（含 OCR、版面还原），200MB 以下优先本机版 | ✅ PDF 场景 | macOS 桌面版 `~/MinerU`；CLI：`pip install mineru`，`mineru -p input.pdf -o outdir`；超 200MB 拆分或改用 pdftotext/pymupdf |
| **pandoc** | EPUB / DOCX → Markdown 通用转换 | ✅ EPUB/DOCX 场景 | macOS：`brew install pandoc`；Linux：`apt install pandoc`。EPUB 需插图加 `--extract-media=assets` |
| pdftotext / pymupdf | 无 MinerU 时的 PDF 文本兜底 | 可选 | `poppler-utils` / `pip install pymupdf` |
| 维基文库等公共领域源 | 无本地文件时获取合法全文 | 可选 | 实测用《孙子兵法》跑通 |

### ② 精读与报告层

| 工具/插件 | 用途 | 必装 | 说明 |
|---|---|---|---|
| **AI Agent 内置精读能力** | 费曼四步精读（预览/三层笔记/讲解/自测） | ✅ | 由 SKILL.md + references/02 驱动，无需额外软件 |
| `html` 技能（Agent 侧） | HTML 精读报告产出规范 + shot.py 自检 | ✅ 报告场景 | 单文件自包含、响应式、交付前截图自检 |
| `doubao-visualization` 技能 | 报告内章节地图/概念关系的 HTML/SVG 可视化 | ✅ 报告场景 | 静态默认、数据可复核 |
| `doubao-learn-to-remember` 技能 | 费曼方法论增强（可选） | 可选 | 记忆方法参考 |

### ③ 卡片与知识库层

| 工具/软件 | 用途 | 必装 | 说明 |
|---|---|---|---|
| **Logseq** | 本地知识库/双链笔记软件，卡片盒落库目标 | ✅ 入库场景 | 官网下载桌面版；图库即一个文件夹，`pages/` 放 `.md` |
| **make_card.py** | cards.json → 批量生成 Logseq 卡片（本仓库自带） | ✅ | `python3 make_card.py cards.json 输出目录`，标准库零依赖 |
| Logseq 本体索引 | 重启后自动索引新 `pages/*.md` | ✅ | 无需插件；属性/双链为 Logseq 原生语法 |

### 可选增强

| 工具 | 用途 |
|---|---|
| 本地 RAG（如 LLM + 向量库） | 卡片超 500 张时的语义检索（档位 B），默认档位 A 直接读图库文件 |
| 百度网盘插件 | 电子书库云端存取（非流水线必需） |
| 飞书文档 | 精读报告二次沉淀为在线文档（非必需） |

---

## 安装方法

### 1. 复制技能到 Agent 的 Skills 目录

将本仓库（或 `SKILL.md` + `references/` + `scripts/` + `assets/`）放入 Agent 环境的用户技能目录，例如：

```bash
# Doubao Work（macOS）
cp -R doubao-book-zettelkasten \
  "$HOME/Library/Application Support/DoubaoWork/Default/.doubaowork/agent_mode/workspace/.user_skills/"

# 类 Codex Agent（Linux 沙箱）
cp -R doubao-book-zettelkasten \
  "$HOME/.doubao/agent_mode/workspace/.user_skills/"
```

技能生效后，Agent 在对应技能目录发现 `SKILL.md` 即完成注册（部分环境需重启会话）。

### 2. 准备解析工具

```bash
# macOS
brew install pandoc
# MinerU 按官方文档安装（PDF 扫描件场景）

# 查看/设置 Logseq 图库路径（默认本机图库，如 /Users/<你的用户名>/Documents/mylibrary）
export LOGSEQ_GRAPH="/Users/<你的用户名>/Documents/mylibrary"
```

### 3.（可选）校验技能结构

```bash
python3 <skills 目录>/skill-creator-for-work/scripts/quick_validate.py <技能目录>
# 输出 "Skill is valid!" 即通过
```

---

## 使用方法

对 AI 说以下任一触发语并**提供电子书文件**（或公开可访问的合法全文链接）：

- 「精读这本书」 / 「解读这本书」
- 「把这本书存入 Logseq」
- 「读书卡片入库」 / 「书籍知识库」
- 「用费曼学习法精读 X」

AI 将按 SKILL.md 六阶段自动执行，最终交付：

```
01-原文/              解析后的 Markdown 原文（可回溯）
02-精读/精读笔记.md    费曼四步精读产物
<书名>精读报告.html    可独立打开的 HTML 报告（书籍信息/一页纸结论/Q&A/章节地图/
                      费曼讲解/金句/自测题/来源）
03-卡片/*.md          卡片盒（金句/概念/方法/疑问）
交付/logseq-import/    Logseq 导入目录（图库不可达时的降级输出，含导入说明）
```

Logseq 图库可达时（配置了 `LOGSEQ_GRAPH` 或本机默认图库路径存在），卡片**直接写入图库 `pages/`**（书页+概念页+卡片页一并落库，重启 Logseq 即索引）；不可达时输出 `交付/logseq-import/pages/`，用户手动并入图库即可。

---

## 卡片规范速览

四种卡片类型（一卡一想法，必带来源）：

| 类型 | 文件命名 | 内容 |
|---|---|---|
| 金句卡 quote | `金句-《书名》-序号.md` | 原文引用 + 一句话理解 + 出处 |
| 概念卡 concept | `概念-《书名》-概念名.md` | 费曼解释 + 原文锚点 + 相关概念双链 |
| 方法卡 method | `方法-《书名》-序号.md` | 步骤 + 适用条件 + 示例来源 |
| 疑问卡 question | `疑问-《书名》-序号.md` | 未解问题 + 我的思考 + 相关卡片 |

Logseq 原生属性语法（`property::` 后必须有空格）：

```markdown
# 概念-《书名》-概念名
- card-type:: concept
- book:: [[《书名》]]
- source:: 第X章 p.Y
- tags:: #思维模型 #作者
- 费曼解释……
- related:: [[概念-《书名》-另一概念]]
```

**闪卡页面格式（Logseq Card 规范）**：正文标题用 h3 级，标题后加空格写 `#card` 作为闪卡标识；标题下的答案内容统一缩进下一级（`- ` bullet，Logseq 树形浏览），多行内容直接换行、每行一个块（可被块引用）；关联概念用二级缩进子块。

```markdown
# 疑问-《书名》-01
- card-type:: question
- book:: [[《书名》]]
- source:: 第X章 p.Y
- tags:: #tag1 #tag2

### 代码可干预 vs 不可篡改信仰：治理边界在哪？ #card
- 问题：……
- 书中线索：……
- 我的思考：……
- 关联：
  - [[概念-《书名》-相关概念]]
```

生成方式：从精读笔记提取 `cards.json` → `python3 scripts/make_card.py cards.json 03-卡片`（脚本自动处理命名、属性与闪卡格式，避免手写漂移；`content` 中两个空格开头的行输出为二级子块）。

---

## 实测验证

| 测试书 | 环境 | 结果 |
|---|---|---|
| 《数字世界生存指南》（EPUB） | macOS | 190k 字符原文 → HTML 报告（shot.py 0 blocker/0 error/0 warning）→ 58 张卡片（33 概念/18 金句/5 方法/2 疑问），断链清零 |
| 《孙子兵法》（维基文库全文） | Linux 沙箱 | 13 篇+答话 → HTML 报告（自检通过）→ 23 张卡片（7 概念/10 金句/4 方法/2 疑问），24 双链 0 断链，property 语法 0 违规 |

> 注：《博弈思考法.pdf》实测时因沙箱附件通道不可达改用公共领域文本验证，流水线与书内容无关，流程通用。

---

## 质量门（技能内置）

- 引用必须锚定来源（章节/页码），无来源的金句不生成卡片
- 卡片原子化：一条卡片只承载一个想法
- 卡片页闪卡格式：正文标题用 `### 标题 #card`（h3 + 空格 + #card），答案统一缩进下一级，多行直接换行（每行一个块）
- Logseq 语法校验：`property::` 后必须有空格；`[[双链]]` 与 `#标签` 拼写正确
- 原文不可达时不得编造书内容；如实告知并标注「待核」
- HTML 报告交付前用 `html` 技能 shot.py 自检（0 blocker / 0 error / 0 warning）

---

## 常见问题（FAQ）

**Q：没有 MinerU 能跑吗？** 能。EPUB/DOCX 用 pandoc，纯文本 MD/TXT 直读；扫描版 PDF 无 OCR 时标注「待核」或改用 pdftotext 兜底。

**Q：卡片如何导入 Logseq？** 图库不可达时，把 `交付/logseq-import/pages/` 下的全部 `.md` 并入本机 Logseq 图库的 `pages/`，重启 Logseq 自动索引；书页 `《书名》.md` 内含全部卡片索引与检索建议。

**Q：以后如何检索？** 档位 A（默认）：AI 直接读图库 `pages/` 文件回答，支持 `book:: [[《书名》]]`、`card-type:: quote`、`#标签` 过滤；卡片超 500 张或要求语义检索时升级档位 B（本地 RAG）。

**Q：发布到 GitHub 有哪些隐私注意？** 公开仓库内容所有人可见。发布前必须审查并清除个人与本机私密信息：真实 macOS/Windows 用户名、绝对路径（如 `/Users/xxx/`、`C:\Users\xxx\`）、个人邮箱、设备型号与序列号、账号令牌等，一律改用占位符（如 `<你的用户名>`）或通用描述；含真实路径的本机配置只保留在本地，不随仓库发布。任何发布动作需本人确认后再执行。

**Q：能处理 PDF 以外的格式吗？** 支持 EPUB / DOCX / MD / TXT；EPUB 转 markdown 后保留章节层级作来源锚点。

---

## License

MIT License — 自由使用、修改与再分发，保留署名即可。

---

## 致谢与关联

- 方法论：费曼学习法（Feynman Technique）、卢曼卡片盒笔记法（Niklas Luhmann's Zettelkasten）、Logseq
- 解析工具：MinerU（opendatalab）、pandoc
- 配套技能：`html`、`doubao-visualization`、`doubao-learn-to-remember`、`skill-creator-for-work`
