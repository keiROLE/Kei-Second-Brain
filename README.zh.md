# Kei-Second-Brain

**一个由 AI 编译的第二大脑。** 一套完整、可开源的个人知识库方法论——**AI 负责编译、维护和输出**，而不只是存储。

本仓库是一套可直接运行的系统：一份成文的架构、9 个可复用的 AI Skill、以及一个演示完整流水线的示例知识库。Clone 下来、读一遍、搭建你自己的。

> English version: [README.md](README.md)（翻译可能滞后，以英文版为准）

---

## 这是什么

Kei-Second-Brain 是把个人知识库方法论做成可复用系统的开源发行版。核心理念：

> **知识不是存的，是编译出来的。**

原始素材（日记、剪藏、AI 对话、逐字稿）流入收件箱；AI 把它编译成结构化知识条目；健康检查让知识库保持诚实；编译后的知识再反哺新内容——文章、视频脚本、帖子。

仓库包含三部分：

| 部分 | 位置 | 是什么 |
|------|------|--------|
| **系统** | `2_Schema/` | 规则：架构、frontmatter 规范、命名、链接规则、流水线手册 |
| **Skill** | `.agents/skills/` | 9 个驱动系统运转的 AI Skill（编译、迭代、复盘、规划……） |
| **示例** | `examples/` 及 `0_Inbox/` `1_Wiki/` `3_KnowledgeBaseIterationLog/` `4_outputs/` | 完整的格式演示——每类一条、仅占位符，展示流水线的每个环节。`examples/compile-demo/` 存放唯一一段真实内容：原始视频文案 → 编译后的条目 |

## 与其他方法的区别

| 方法 | 它给你什么 | 本系统在此基础上加了什么 |
|------|-----------|--------------------------|
| **PARA** | 分类骨架（项目/领域/资源/归档）——本系统**借鉴了它的标签思想**，大部分条目带 PARA 标签 | PARA 只决定"内容放哪"。Kei-Second-Brain 加了 **AI 编译层**（素材自动变成知识条目）、**维护层**（健康检查、链接审计、幻觉检测）和**输出层**（知识反哺内容）。 |
| **Zettelkasten** | 原子笔记互链成思想网络——本系统**借鉴了链接思想**（带类型标注的 `## 参见`） | ZK 靠手写卡片。这里条目由 **AI 编译产出**，并有质量红线（不编造、溯源、confidence 分级）防幻觉。 |

**一句话**：PARA 提供分类骨架，Zettelkasten 提供链接思想，Kei-Second-Brain 提供**"AI 编译流水线 + 主动维护 + 知识反哺输出"**——让知识库真正长大的三件事。

## 前置条件

只需要两个工具：

1. **Obsidian** —— 知识库运行在 Obsidian 里（免费），任意较新版本即可。
2. **支持自定义 Skill/Agent 的 AI 客户端** —— 如豆包、Claude Code，或任何能读取 markdown 指令并操作文件的 agent。`.agents/skills/` 里的 Skill 就是纯 markdown 指令文件（SKILL.md），你的 AI 客户端只需要能加载并执行它们。

不需要写代码、不需要服务器、不需要数据库。

## 架构

```
0_Inbox/                             1_Wiki/                            2_Schema/
原始素材层（只读）                     知识编译层                          配置层
diary/  weekly-review/               concepts/  entities/               TheSchema（全局规则）
chat-distill/  clippings/            comparisons/  frameworks/          AGENTS（AI 行为守则）
                                      resources/  index.md              frontmatter/naming
                                                                        pipeline（操作手册）
3_KnowledgeBaseIterationLog/         4_outputs/
迭代层                               输出层
编译报告 / 迭代报告 / 链接审计          文章、脚本、帖子
```

| 层级 | 职责 | 谁写 |
|------|------|------|
| `0_Inbox/` | 原始素材——事实来源 | 你（只追加） |
| `1_Wiki/` | 编译后的知识条目 | AI（通过 Skill） |
| `2_Schema/` | 知识库运转的规则 | 你 + AI |
| `3_KnowledgeBaseIterationLog/` | 报告：编译、健康检查、审计 | AI |
| `4_outputs/` | 由条目编译的内容 | AI（取材 wiki） |

## 流水线（一段话）

**输入**：视频逐字稿、网页剪藏、AI 对话、日记都落到 `0_Inbox/`。**编译**：`/by-1`（单篇）或 `/by-a`（批量）把它们变成 `1_Wiki/` 里的类型化条目——概念、实体、对比、框架、资源——每条都带来源、置信度和类型化链接。**维护**：`/kb-iter` 扫描缺口、断链、孤岛和幻觉，输出只读的迭代报告。**输出**：条目被取材成文章、视频脚本和帖子（如 `/blog-1`）。没有任何环节自动运行——每步都由用户主动触发。完整操作手册见 `2_Schema/pipeline.md`。

## 快速开始

### 方式 A —— 先逛示例（推荐）

```bash
git clone https://github.com/keiROLE/Kei-Second-Brain.git
# 用 Obsidian 打开本文件夹（"作为库打开文件夹"）
# 先读 examples/README.zh.md，再按建议顺序浏览
```

本仓库本身就是一套完整的示例库。`0_Inbox/`、`1_Wiki/`、`2_Schema/`、`3_KnowledgeBaseIterationLog/` 和 `4_outputs/` 以格式演示展示流水线的每个环节——每类一条、具体内容已移除、仅保留占位符。

### 方式 B —— 让 AI 帮你搭建

**你可以把本 README 交给任意 AI 助手，让它帮你搭建知识库。** AI 会：

1. 创建四个顶层目录（`0_Inbox/`、`1_Wiki/`、`2_Schema/`、`3_KnowledgeBaseIterationLog/`）及子目录。
2. 让你从本仓库复制 `2_Schema/`（规则）和 `.agents/skills/`（Skill）。
3. 带你走完第一个循环：写一篇日记 → 对这篇日记跑 `/by-1` → 看编译出的条目。

### 方式 C —— 手动从零搭建

1. 新建 Obsidian 库。
2. 从本仓库复制 `2_Schema/` 和 `.agents/skills/`。
3. 读 `2_Schema/TheSchema.md`（规则）和 `2_Schema/pipeline.md`（操作手册）。
4. 开始在 `0_Inbox/` 里写原始笔记，然后触发 `/by-a` 编译。

## 仓库地图

| 路径 | 内容 |
|------|------|
| `AGENTS.md` | AI 行为守则（仓库根目录——AI 客户端优先读取） |
| `2_Schema/TheSchema.md` | 架构、标签、8 类链接类型、质量红线、工作流 |
| `2_Schema/frontmatter.md` | frontmatter 字段规范 |
| `2_Schema/naming.md` | 命名规范 + PARA 分类口径 |
| `2_Schema/pipeline.md` | 端到端操作手册（输入 → 输出） |
| `.agents/skills/` | by-1、by-a、kb-iter、jh-1、wr-1、rec-1、chat-distill、blog-1、chiselplan |
| `examples/` | 示例库（自带中英双版本 README） |
| `examples/compile-demo/` | 真实原始素材 + 它编译成的条目 |
| `4_outputs/` | 输出层格式示例（由条目编译的文章） |

## 支持与维护边界

- 这是**个人方法论分享，不是社区项目**。
- 欢迎提 issue：提问、报问题都可以。
- **不承诺定期更新**；大版本随作者自用库演进不定期发布。
- PR 需讨论后合入，不接受未经讨论的大改。
- 示例内容为虚构演示；支持范围限于方法论本身，不含演示数据。

## 许可证

**CC BY-NC 4.0**（署名-非商业性使用 4.0 国际）。

你可以自由共享、演绎，但须署名，且仅限非商业用途。完整法律文本：<https://creativecommons.org/licenses/by-nc/4.0/legalcode>。见 [LICENSE](LICENSE)。

---

*由 Kei 构建——AI 编译的知识，献给想让笔记真正"想回来"的人。*
