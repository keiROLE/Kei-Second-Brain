# 示例知识库 —— 小坚果搞机工作室

> **虚构声明**：本示例知识库内容全部为虚构演示，与任何真实账号或个人无关。This sample knowledge base is entirely fictional and created for demonstration.

这个文件夹是 Kei-Second-Brain 系统一套完整、可运行的示例——一个小的 Obsidian 库，展示一个人（此处为虚构的 DIY 电脑卖家兼自媒体创作者"小坚果搞机"）如何跑通完整流水线：**输入 → 编译 → 维护 → 输出**。

## 示例与流水线的对应关系

| 流水线环节 | 示例中的位置 |
|------------|--------------|
| ① 输入（获取） | `0_Inbox/` — 日记、周复盘、一条沉淀的 AI 对话、一条网页剪藏 |
| ② 转写 | （隐含——日记提到看测评视频；逐字稿同样会落到 `0_Inbox/`） |
| ③ 编译 | `1_Wiki/` — 从 `0_Inbox/` 编译出的 8 条知识条目（概念/实体/对比/框架/资源） |
| ④ 维护 | `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — 健康检查 + 链接审计 |
| ⑤ 输出 | `output-sample.zh.md` — 由知识条目编译出的文章 |

## 建议阅读顺序

1. 仓库根目录 `README.zh.md` — 系统是什么、如何搭建自己的库
2. `2_Schema/TheSchema.md` — 本库运行的规则
3. 本文件夹按顺序：
   - `0_Inbox/diary/2026-09-10.md` — 原始素材，未处理
   - `3_KnowledgeBaseIterationLog/2026-09-13-compile-report.md` — /by-a 的编译产出
   - `1_Wiki/` — 编译后的条目
   - `3_KnowledgeBaseIterationLog/2026-09-13-iteration-report.md` — /kb-iter 的发现
   - `output-sample.zh.md` — 输出文章

## 一句话看懂这个循环

客户的问题出现在日记里（输入）→ 编译 skill 把它变成知识条目（编译）→ 迭代 skill 检查全库并建议补什么（维护）→ 视频脚本或文章从条目里取材（输出）→ 下周的日记记录这些内容带来了什么——循环继续。

> 条目使用英文，因为系统的配置层是英文生态；本 README 的中文版面向中文读者解释同一套结构。
