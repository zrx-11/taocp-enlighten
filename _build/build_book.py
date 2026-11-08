#!/usr/bin/env python3
"""装配单本书：content/<slug>/ 源目录 -> 输出目录（Markdown 知识库 + manifest.json）。

用法：python3 build_book.py <content_dir> <输出根目录>

源目录要求：
  meta.py   导出 META 字典（slug/title/book/about/mermaid/path/gaps/glossary/patterns/cheatsheet/chapters/concepts）
  quiz.py   导出 QUIZZES 列表（可为空）
  cards.py  导出 CARDS 列表（可为空）
  chapters/*.md, concepts/*.md  正文
"""
import importlib.util
import json
import os
import shutil
import sys


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def write(path, text):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")


def build(content_dir, root):
    meta = load(os.path.join(content_dir, "meta.py"), "meta_" + os.path.basename(content_dir)).META
    quizzes = []
    cards = []
    qp = os.path.join(content_dir, "quiz.py")
    cp = os.path.join(content_dir, "cards.py")
    if os.path.exists(qp):
        quizzes = load(qp, "quiz_" + meta["slug"]).QUIZZES
    if os.path.exists(cp):
        cards = load(cp, "cards_" + meta["slug"]).CARDS

    outdir = os.path.join(root, meta["dir"])
    ensure_dir(outdir)

    # 正文搬运
    for sub in ("chapters", "concepts"):
        src = os.path.join(content_dir, sub)
        dst = os.path.join(outdir, sub)
        ensure_dir(dst)
        if os.path.isdir(src):
            for fn in os.listdir(src):
                if fn.endswith(".md"):
                    shutil.copyfile(os.path.join(src, fn), os.path.join(dst, fn))

    chapters = meta["chapters"]
    concepts = meta.get("concepts", [])

    # glossary.md
    lines = ["# 术语表", "", "| 术语 | 白话定义 | 首次出现 | 所属章节 |", "|---|---|---|---|"]
    for g in meta.get("glossary", []):
        t = next((c["title"] for c in chapters if c["id"] == g["chapterId"]), "")
        lines.append(f"| {g['term']} | {g['def']} | {g['chapterId']} | {t} |")
    write(os.path.join(outdir, "glossary.md"), "\n".join(lines))

    write(os.path.join(outdir, "patterns.md"), meta["patterns"])
    write(os.path.join(outdir, "cheatsheet.md"), meta["cheatsheet"])

    def ans_text(q):
        if q["type"] == "multi":
            return "、".join(chr(65 + k) for k in q["answer"])
        if q["type"] == "single":
            return chr(65 + q["answer"])
        return q["answer"]

    # quiz.md
    qlines = [f"# {meta['title']} · 测验", ""]
    for ch in chapters:
        qs = [q for q in quizzes if q["chapterId"] == ch["id"]]
        if not qs:
            continue
        qlines += [f"## {ch['title']}", ""]
        for i, q in enumerate(qs, 1):
            qlines.append(f"### Q{i}. {q['question']}")
            for j, opt in enumerate(q.get("options") or []):
                qlines.append(f"- {chr(65 + j)}. {opt}")
            qlines += [f"**答案**：{ans_text(q)}", f"**解析**：{q['explain']}", ""]
    allq = [q for q in quizzes if q.get("chapterId") == "__all__"]
    if allq:
        qlines += ["## 综合测验", ""]
        for i, q in enumerate(allq, 1):
            qlines.append(f"### 综合 Q{i}. {q['question']}")
            for j, opt in enumerate(q.get("options") or []):
                qlines.append(f"- {chr(65 + j)}. {opt}")
            qlines += [f"**答案**：{ans_text(q)}", f"**解析**：{q['explain']}", ""]
    write(os.path.join(outdir, "quiz.md"), "\n".join(qlines))

    # flashcards.md
    flines = [f"# {meta['title']} · 抽认卡", ""]
    for ch in chapters:
        cs = [c for c in cards if c["chapterId"] == ch["id"]]
        if not cs:
            continue
        flines += [f"## {ch['title']}", ""]
        for c in cs:
            flines += [f"### 卡片：{c['front']}", f"- **背面**：{c['back']}",
                       f"- **标签**：{', '.join(c.get('tags', []))}", f"- **章节**：{ch['id']}", ""]
    write(os.path.join(outdir, "flashcards.md"), "\n".join(flines))

    # SKILL.md
    idx = []
    for ch in chapters:
        d = ch.get("difficulty", 1)
        idx.append(f"- {ch['title']}（难度 {'★' * d}{'☆' * (3 - d)}，约 {ch.get('hours', 2)} 小时）→ [{ch['file']}]({ch['file']})")
    path_rows = [f"| {p['step']} | {p['title']} | {'、'.join(p['chapterIds'])} | {p['checkpoint']} |" for p in meta["path"]]
    gap_rows = [f"| {g['gap']} | {g['where']} | {g['signal']} |" for g in meta.get("gaps", [])]

    skill = f"""---
name: {meta['slug']}-点化学习总纲
---

# {meta['title']} 点化学习系统

## 这本书在讲什么

{meta['about']}

## 全书心智模型

```mermaid
{meta['mermaid']}
```

## 学习路径（推荐顺序）

| 步骤 | 主题 | 章节 | 检查点 |
|---|---|---|---|
{chr(10).join(path_rows)}

## 章节索引

{chr(10).join(idx)}

## 前置知识（零基础缺口补讲）

| 缺口 | 补讲位置 | 学完标志 |
|---|---|---|
{chr(10).join(gap_rows)}

## 术语表 / 模式库 / 速查表

- 术语：[glossary.md](glossary.md)
- 模式库：[patterns.md](patterns.md)
- 速查表：[cheatsheet.md](cheatsheet.md)
- 测验：[quiz.md](quiz.md)
- 抽认卡：[flashcards.md](flashcards.md)

## 怎么学

打开同目录的 `{meta['slug']}学习伴侣.html`，按「学习路径」推进。每章读完做自测题，答对再走下一步。
"""
    write(os.path.join(outdir, "SKILL.md"), skill)

    manifest = {
        "slug": meta["slug"],
        "title": meta["title"],
        "subtitle": meta.get("subtitle", ""),
        "book": meta["book"],
        "audience": meta.get("audience", "零基础"),
        "goal": meta.get("goal", "系统掌握"),
        "companion": f"{meta['slug']}学习伴侣.html",
        "learningPath": meta["path"],
        "chapters": [{"id": c["id"], "title": c["title"], "file": c["file"],
                      "difficulty": c.get("difficulty", 1)} for c in chapters],
        "concepts": [{"id": c["id"], "title": c["title"], "file": c["file"],
                      "chapterIds": c["chapterIds"]} for c in concepts],
        "glossary": [{"term": g["term"], "def": g["def"], "chapterId": g["chapterId"]}
                     for g in meta.get("glossary", [])],
        "patterns": {"file": "patterns.md"},
        "cheatsheet": {"file": "cheatsheet.md"},
        "quizzes": quizzes,
        "flashcards": cards,
    }
    write(os.path.join(outdir, "manifest.json"), json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"[ok] {meta['slug']}: {len(chapters)} 章 / {len(concepts)} 概念 / {len(quizzes)} 题 / {len(cards)} 卡")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
