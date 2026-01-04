#!/usr/bin/env python3
"""
DSPY 文档复制脚本
简化版本，直接复制和分类文档
"""

import os
import shutil
from pathlib import Path

def copy_dspy_docs():
    """复制 DSPY 文档到技能目录"""
    base_dir = Path(__file__).parent.parent.parent.parent

    source_dir = base_dir / "docs" / "dspy"
    target_dir = base_dir / "skills" / "output" / "dspy" / "references"

    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return False

    print("🚀 开始复制 DSPY 文档...")

    # 创建目标目录结构
    dirs_to_create = [
        "core_concepts",
        "api_reference",
        "tutorials/basics",
        "tutorials/advanced",
        "learning"
    ]

    for dir_path in dirs_to_create:
        (target_dir / dir_path).mkdir(parents=True, exist_ok=True)

    copied_count = 0

    # 1. 复制核心文档
    print("\n📚 复制核心文档...")
    core_docs = ["index.md", "cheatsheet.md"]
    for doc in core_docs:
        source_file = source_dir / doc
        if source_file.exists():
            target_file = target_dir / "core_concepts" / doc
            shutil.copy2(source_file, target_file)
            copied_count += 1
            print(f"  ✅ {doc}")

    # 2. 复制 API 文档
    print("\n📋 复制 API 文档...")
    api_dir = source_dir / "api"
    if api_dir.exists():
        target_api_dir = target_dir / "api_reference"
        for item in api_dir.rglob("*.md"):
            if item.is_file():
                rel_path = item.relative_to(api_dir)
                target_file = target_api_dir / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_file)
                copied_count += 1
        print(f"  ✅ API 文档已复制")

    # 3. 复制基础教程
    print("\n🎓 复制基础教程...")
    basic_tutorials = [
        "tutorials/build_ai_program",
        "tutorials/classification",
        "tutorials/rag",
        "tutorials/agents"
    ]

    for tutorial in basic_tutorials:
        source_tutorial_dir = source_dir / tutorial
        if source_tutorial_dir.exists():
            target_tutorial_dir = target_dir / "tutorials" / "basics" / source_tutorial_dir.name
            copy_directory(source_tutorial_dir, target_tutorial_dir)
            copied_count += len(list(source_tutorial_dir.rglob("*.md")))
            print(f"  ✅ {tutorial}")

    # 4. 复制进阶教程
    print("\n🚀 复制进阶教程...")
    advanced_tutorials = [
        "tutorials/optimization",
        "tutorials/deployment",
        "tutorials/streaming"
    ]

    for tutorial in advanced_tutorials:
        source_tutorial_dir = source_dir / tutorial
        if source_tutorial_dir.exists():
            target_tutorial_dir = target_dir / "tutorials" / "advanced" / source_tutorial_dir.name
            copy_directory(source_tutorial_dir, target_tutorial_dir)
            copied_count += len(list(source_tutorial_dir.rglob("*.md")))
            print(f"  ✅ {tutorial}")

    # 5. 创建快速参考
    print("\n🔍 创建快速参考...")
    quick_ref_content = """# DSPy 快速参考

## 核心概念
- [框架介绍](core_concepts/index.md)
- [速查表](core_concepts/cheatsheet.md)

## API 文档
- [API 参考](api_reference/) - 完整的 API 文档

## 教程
- [基础教程](tutorials/basics/) - 入门教程
- [进阶教程](tutorials/advanced/) - 高级应用

## 使用指南
1. 从 core_concepts/index.md 开始了解框架
2. 查看 cheatsheet.md 获取常用代码模式
3. 通过基础教程学习实践应用
4. 参考进阶教程了解高级特性
"""

    quick_ref_file = target_dir / "quick_reference.md"
    with open(quick_ref_file, 'w', encoding='utf-8') as f:
        f.write(quick_ref_content)
    copied_count += 1
    print(f"  ✅ quick_reference.md")

    print(f"\n🎉 完成! 复制了 {copied_count} 个文件")
    return True

def copy_directory(source_dir: Path, target_dir: Path):
    """复制目录中的 Markdown 文件"""
    target_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.rglob("*.md"):
        if item.is_file():
            rel_path = item.relative_to(source_dir)
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target_file)

if __name__ == "__main__":
    success = copy_dspy_docs()
    exit(0 if success else 1)