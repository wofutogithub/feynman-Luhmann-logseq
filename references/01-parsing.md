# 输入解析规范

目标：任意格式电子书 → 统一 Markdown 原文（保留章节层级）。

## 格式路由

| 格式 | 解析器 | 说明 |
|---|---|---|
| PDF | MinerU（本机） | 200MB 以下优先本机 MinerU 桌面版（macOS 位于 ~/MinerU，GUI 解析后导出 md）；CLI 备选 `mineru -p input.pdf -o outdir`；超 200MB 拆分后处理或改用 pdftotext/pymupdf |
| EPUB | pandoc | `pandoc input.epub -t markdown -o output.md`；需插图时加 `--extract-media=assets` |
| DOCX | pandoc | `pandoc input.docx -t markdown -o output.md` |
| MD/TXT | 直读 | 复制到原文库，保留原结构 |

## 执行要点

- 输出目录 `01-原文/`，文件名 = 书名.md
- 保留标题层级（#/##）作为章节锚点；记录页码/章节号用于卡片来源
- EPUB 经 pandoc 转换后常带 calibre/SVG 封面噪音与 `<span>` 锚点：用 python 清洗脚本去除 SVG、图片引用、span 锚点、calibre 类名与加粗标记，产出 `clean.md` 作为精读源
- 扫描件（图片型 PDF）：MinerU OCR 后抽查关键章节文字质量，乱码处标注「待核」
- 解析完成后先通读大纲（目录树），确认章节完整再进入精读
