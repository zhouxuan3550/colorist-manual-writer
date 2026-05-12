# 调色师手册写作 Skill

![调色师手册写作 Skill 能做什么](assets/colorist-manual-writer-overview.png)

这是一个面向「调色师手册」公众号长文写作的 Codex Skill。

它保留数字生命卡兹克式的口语化、好奇心驱动和判断力，同时加入影视后期行业底色：影视幕后、剪辑、调色、摄影修图、AI 影像工具、创作工作流和公众号长文表达。

## 能做什么

- 公众号长文出稿：适合 4000-8000 字完整发布稿。
- 普通草稿：适合先写一版 1500-3000 字可改稿。
- 片段试写：适合开头、结尾、章节、某种表达方式。
- 改写润色：保留事实和原意，增强结构、节奏和活人感。
- 影视幕后拆解：从剧本、分镜、摄影、剪辑、调色、声音、VFX 等环节拆解创作链条。
- 工具与工作流解读：围绕 DaVinci Resolve、FCPX、AI 视频工具、插件、字幕、素材管理等展开。
- 选题与结构诊断：用 HKR 判断选题是否足够有趣、有知识量、有共鸣。

## 目录结构

```text
colorist-manual-writer/
├── SKILL.md
├── README.md
├── assets/
│   └── colorist-manual-writer-overview.png
├── references/
│   ├── content_methodology.md
│   ├── quality_check.md
│   └── style_examples.md
└── scripts/
    └── check_article.py
```

## 安装到 Codex

把整个目录复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R colorist-manual-writer ~/.codex/skills/colorist-manual-writer
```

然后重启 Codex，让新 skill 生效。

## 使用场景

可以这样触发：

```text
用调色师手册风格写一篇关于 AI 视频工具的公众号文章
```

```text
帮我把这段影视幕后分析改写成调色师手册公众号风格
```

```text
这个选题适合调色师手册吗，帮我拆一下结构
```

## 注意

这个 skill 不用于短社媒文案、纯标题生成、无风格要求的普通回答。它的重点是公众号长文、影视幕后、后期制作、创作工具和影像工作流。
