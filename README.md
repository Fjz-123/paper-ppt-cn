# paper-ppt-cn

**模板驱动的中文论文汇报技能：提供模板与论文资料，生成有来源依据的PPT、逐页讲稿和图片包。**

这是一套供Codex使用的技能说明与参考规范，不是独立的PPT生成程序。实际文件读取、检索、图像提取、幻灯片编辑和渲染，由宿主环境中可用的工具完成。

## 主要能力

- **模板适配**：保留封面、目录、分节、结束等结构页，以及适用的校徽、校名、公司名和页眉页脚，正文可按内容重新编排。
- **单位与主题色适配**：提供新单位时检索官方标识和主题色；无法确认适用主题色时使用后备蓝色，不把蓝色作为固定品牌。
- **多种数据源**：PDF、补充材料、论文链接/DOI、本地文件夹、可访问的Zotero条目，以及相关笔记和数据表。
- **论文精读**：重点组织背景、方法、网络/系统结构、创新点、实验与局限；涉及网络架构的核心方法须有结构图。
- **图文可追溯**：保留科研原图；有明确数值时制作可编辑表格和数据图，记录原文页码、图号及面板。
- **跨学科与可调篇幅**：支持单篇精读、多篇比较、专题综述，不固定领域、篇数、页数或汇报时长。

默认视觉偏好为微软雅黑、所有可编辑文字加粗、重点暗红、贴合内容的虚线框，以及浅主题色小块衬底。**用户本次明确指定的字体、配色和布局规则优先。**原始科研图片内部的文字与科学配色保持原样。

## 输入与输出

最少提供一份模板及可读取的数据源，可再说明单位、听众、时长、必讲论文与页数。缺失必要输入时技能会询问；资料不足时优先补齐公开原文，不凭摘要虚构方法和实验。

完整制作默认交付：

| 文件 | 内容 |
|---|---|
| `报告.pptx` | 实际可使用的演示文稿 |
| `逐页讲稿.md` | 与最终页码一致的口语正文、指图提示和建议时长 |
| `来源清单.md` | 核心/支撑资料、联网补充项与逐页证据位置 |
| `提取图片包.zip` | 实际使用的清晰图像、处理说明和明示数值摘录 |

用户只需要改稿、大纲或讲稿时，只处理所要求内容，不强制重新生成四件套。

## 安装

将本仓库的`skills/paper-ppt-cn`目录放入Codex个人技能目录。以下以默认个人目录为例；若自定义了`CODEX_HOME`，改用其`skills`子目录。已有同名技能时先备份并比较，不直接覆盖个人改动。

先克隆仓库：

```bash
git clone https://github.com/Fjz-123/paper-ppt-cn.git
```

Windows PowerShell，在克隆时所在的目录执行：

```powershell
$skillParent = Join-Path $env:USERPROFILE '.codex/skills'
$skillDestination = Join-Path $skillParent 'paper-ppt-cn'
if (Test-Path -LiteralPath $skillDestination) {
    throw '已有同名技能，请先备份并比较。'
}
New-Item -ItemType Directory -Path $skillParent -Force | Out-Null
Copy-Item -LiteralPath './paper-ppt-cn/skills/paper-ppt-cn' -Destination $skillDestination -Recurse
```

macOS / Linux，在克隆时所在的目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
if [ -e "$HOME/.codex/skills/paper-ppt-cn" ]; then
  echo '已有同名技能，请先备份并比较。'
else
  cp -R ./paper-ppt-cn/skills/paper-ppt-cn "$HOME/.codex/skills/paper-ppt-cn"
fi
```

安装后在新会话中调用`$paper-ppt-cn`。是否需要重新加载技能，取决于宿主客户端。

## 使用示例

```text
使用 $paper-ppt-cn。
模板：我附上的PPTX。
数据源：附上的论文PDF和补充材料。
汇报目的：单篇论文精读，15分钟，问答另计。
听众：有深度学习基础，但不熟悉本方向的研究生。
沿用模板单位信息，重点讲背景、方法、网络结构、创新和关键实验。
```

替换单位时可再补充：

```text
将模板品牌替换为我的单位：填写完整单位名称。
优先采用官网公开的标准Logo、名称和主题色。
```

更多场景见[使用示例](docs/examples.md)。

## 运行环境与边界

- 需要能读取文件、处理PDF/图片、编辑并渲染PPTX的Codex环境。技能会使用当前可用的Presentations工作流，本仓库不分发相关专有运行时。
- 联网补齐文献和官方品牌资料，需要相应网络访问。Zotero等外部来源还需要已连接且有权限的读取能力。
- 未安装的字体需使用可用替代并说明影响。本仓库不提供微软雅黑、Cambria Math等字体文件。
- 输出的演示文稿和论文解释仍应由报告者复核。排练时长是建议，不是未经实际朗读的精确计时。
- 本技能不会自动修改Zotero库、安装软件、上传资料或发布PPT。

## 仓库结构

```text
skills/paper-ppt-cn/
  SKILL.md
  agents/openai.yaml
  references/
    style.md
    content.md
    script.md
    sources-and-figures.md
docs/examples.md
scripts/validate.py
tests/test_validate.py
```

## 本地校验

使用Python 3.10或更高版本，无第三方Python依赖：

```bash
python scripts/validate.py
python -m unittest discover -s tests -v
```

校验范围为技能入口、相对资源链接及公开发行包卫生，不证明论文结论正确、PPT视觉质量达标或所有宿主工具均可用。GitHub Actions会运行相同检查。

## 许可与素材

技能说明、文档和本仓库新编写的辅助代码采用[MIT许可证](LICENSE)。

**用户模板、校徽/Logo、论文全文与图表、字体，以及由这些素材组成的PPT，不因使用此技能而获得MIT授权。**使用与再分发时应保留来源并遵守各自权利和许可。本公开仓库不包含个人模板、第三方图片、真实数据集、对话记录、账号凭据或已生成报告。

欢迎通过Issue或Pull Request提出改进。不要提交个人资料、凭据或未经授权的模板和论文素材。

## English overview

`paper-ppt-cn` is a Codex skill for template-based academic presentations. It reads supplied papers and related data, preserves template structure and appropriate branding, explains methods and evidence, and produces an editable PPTX, a slide-by-slide Chinese speaking script, a source list, and a reusable figure package.

Install `skills/paper-ppt-cn` in your personal Codex skills directory. A capable host with presentation and document tools is required; this repository does not bundle a standalone slide-generation engine or third-party paper assets. The skill defaults can be overridden by the current user request. Original skill text and helper code are MIT licensed; input documents and third-party assets retain their own rights.
