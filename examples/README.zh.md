# 示例知识库 —— 格式演示

> **虚构声明**：本示例库仅为格式演示。所有具体内容已移除——条目保留结构（frontmatter + 章节）并填入占位符。与任何真实账号或个人无关。This sample vault is a format demonstration only, not related to any real account or person.

这个文件夹是 Kei-Second-Brain 系统一套完整、可运行的示例——一个小的 Obsidian 库，展示一个人如何跑通完整流水线：**输入 → 编译 → 维护 → 输出**。每个文件都保留系统的*真实格式*（你自建知识库将使用的精确 frontmatter 和章节结构），内容为占位符。

## 示例与流水线的对应关系

| 流水线环节 | 示例中的位置 |
|------------|--------------|
| ① 输入（获取） | `0_Inbox/` — 日记、周复盘、对话沉淀、网页剪藏（每类一个格式示例） |
| ② 转写 | （隐含——逐字稿同样会落到 `0_Inbox/`） |
| ③ 编译 | `1_Wiki/` — 每类一条（概念/实体/对比/框架/资源） |
| ④ 维护 | `3_KnowledgeBaseIterationLog/` — 编译报告 + 迭代报告（格式示例） |
| ⑤ 输出 | `4_outputs/` — 由知识条目编译的文章格式 |

## 建议阅读顺序

1. 仓库根目录 `README.zh.md` — 系统是什么、如何搭建自己的库
2. `2_Schema/TheSchema.md` — 本库运行的规则
3. 本文件夹按顺序：
   - `0_Inbox/diary/` — 日记格式（原始素材，未处理）
   - `3_KnowledgeBaseIterationLog/2026-09-13-compile-report.md` — /by-a 的产出
   - `1_Wiki/` — 编译条目的格式
   - `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — /kb-iter 的发现
   - `4_outputs/output-sample.zh.md` — 输出格式

## 一句话看懂这个循环

素材进入日记（输入）→ 编译 skill 把它变成知识条目（编译）→ 迭代 skill 检查全库并建议补什么（维护）→ 文章或脚本从条目取材（输出）→ 下周的日记记录这些内容带来了什么——循环继续。

> 配置层（2_Schema、skills、目录名）仅英文；示例层中英双版（`*.md` = 英文，`*.zh.md` = 中文）。以英文版为准。
