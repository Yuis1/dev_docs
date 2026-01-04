#!/usr/bin/env python3
"""
DSPY 文档组织和处理脚本
智能筛选、分类和整理 DSPY 技术文档
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Tuple

class DSPYDocOrganizer:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.processed_files = []
        self.excluded_files = []

        # 定义文档优先级和分类
        self.doc_priorities = {
            # 核心文档 - 最高优先级
            'core': ['index.md', 'cheatsheet.md', 'faqs.md'],

            # API 文档 - 高优先级
            'api': [
                'api/index.md',
                'api/modules/',
                'api/signatures/',
                'api/optimizers/',
                'api/primitives/',
                'api/models/',
                'api/tools/'
            ],

            # 基础教程 - 高优先级
            'tutorials_basic': [
                'tutorials/build_ai_program/',
                'tutorials/core_development/',
                'tutorials/classification/',
                'tutorials/rag/',
                'tutorials/agents/'
            ],

            # 进阶教程 - 中等优先级
            'tutorials_advanced': [
                'tutorials/optimization/',
                'tutorials/deployment/',
                'tutorials/streaming/',
                'tutorials/async/',
                'tutorials/real_world_examples/'
            ],

            # 学习资源 - 中等优先级
            'learning': [
                'learn/optimization/',
                'learn/evaluation/',
                'learn/programming/'
            ],

            # 生产部署 - 中等优先级
            'production': [
                'production/'
            ],

            # 深度内容 - 低优先级
            'advanced': [
                'deep-dive/',
                'experimental/'
            ]
        }

        # 排除的文件和目录
        self.exclude_patterns = [
            'static/',          # 静态资源
            'stylesheets/',     # 样式文件
            'js/',             # JavaScript文件
            'figures/',        # 图片文件
            'community/',      # 社区内容
            'roadmap.md',      # 过时的路线图
        ]

    def should_include_file(self, file_path: Path) -> bool:
        """判断文件是否应该包含在技能中"""
        # 检查排除模式
        for pattern in self.exclude_patterns:
            if pattern in str(file_path):
                self.excluded_files.append(str(file_path))
                return False

        # 只包含 .md 文件
        if file_path.suffix != '.md':
            self.excluded_files.append(str(file_path))
            return False

        return True

    def get_document_priority(self, file_path: Path) -> Tuple[str, int]:
        """获取文档的优先级和分类"""
        rel_path = file_path.relative_to(self.source_dir)
        path_str = str(rel_path)

        for category, patterns in self.doc_priorities.items():
            for pattern in patterns:
                if pattern.endswith('/'):
                    # 目录模式
                    if path_str.startswith(pattern):
                        priority = 1 if category in ['core', 'api'] else 2 if category in ['tutorials_basic', 'learning', 'production'] else 3
                        return category, priority
                else:
                    # 文件模式
                    if path_str == pattern or path_str.startswith(pattern.replace('.md', '/')):
                        priority = 1 if category in ['core', 'api'] else 2
                        return category, priority

        # 默认分类
        return 'other', 4

    def copy_file_with_structure(self, source_file: Path, target_subdir: str) -> Path:
        """复制文件到目标目录，保持结构"""
        target_file = self.target_dir / "references" / target_subdir / source_file.name
        target_file.parent.mkdir(parents=True, exist_ok=True)

        # 简单清理 Markdown 内容
        content = self.clean_markdown_content(source_file)

        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return target_file

    def clean_markdown_content(self, file_path: Path) -> str:
        """清理 Markdown 文件内容"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 移除 YAML frontmatter 中的特定字段
        lines = content.split('\n')
        cleaned_lines = []
        skip_frontmatter = False

        for line in lines:
            if line.strip() == '---' and not skip_frontmatter:
                skip_frontmatter = True
                continue
            elif line.strip() == '---' and skip_frontmatter:
                skip_frontmatter = False
                continue
            elif skip_frontmatter:
                # 在 frontmatter 中，移除特定字段
                if not any(key in line for key in ['sidebar_position', 'hide', 'title:']):
                    continue

            cleaned_lines.append(line)

        content = '\n'.join(cleaned_lines)

        # 清理图片路径（如果有本地图片引用）
        content = content.replace('static/img/', '')
        content = content.replace('static/', '')

        return content

    def organize_core_documents(self):
        """组织核心文档"""
        print("📚 处理核心文档...")
        core_dir = self.target_dir / "references" / "core_concepts"
        core_dir.mkdir(parents=True, exist_ok=True)

        for doc_name in self.doc_priorities['core']:
            source_file = self.source_dir / doc_name
            if source_file.exists() and self.should_include_file(source_file):
                target_file = self.copy_file_with_structure(source_file, "core_concepts")
                self.processed_files.append(str(target_file))
                print(f"  ✅ {doc_name}")

    def organize_api_documents(self):
        """组织 API 文档"""
        print("📋 处理 API 文档...")
        api_dir = self.target_dir / "references" / "api_reference"
        api_dir.mkdir(parents=True, exist_ok=True)

        # 处理 API 索引
        api_index = self.source_dir / "api" / "index.md"
        if api_index.exists():
            target_file = self.copy_file_with_structure(api_index, "api_reference")
            self.processed_files.append(str(target_file))
            print(f"  ✅ api/index.md")

        # 处理各个 API 子目录
        for subdir in ['modules', 'signatures', 'optimizers', 'primitives', 'models', 'tools', 'utils']:
            source_subdir = self.source_dir / "api" / subdir
            if source_subdir.exists():
                target_subdir = api_dir / subdir
                target_subdir.mkdir(parents=True, exist_ok=True)

                for md_file in source_subdir.glob("*.md"):
                    if self.should_include_file(md_file):
                        target_file = target_subdir / md_file.name
                        content = self.clean_markdown_content(md_file)
                        with open(target_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        self.processed_files.append(str(target_file))
                        print(f"  ✅ api/{subdir}/{md_file.name}")

    def organize_tutorial_documents(self):
        """组织教程文档"""
        print("🎓 处理教程文档...")

        # 基础教程
        basic_tutorials_dir = self.target_dir / "references" / "tutorials" / "basics"
        basic_tutorials_dir.mkdir(parents=True, exist_ok=True)

        # 进阶教程
        advanced_tutorials_dir = self.target_dir / "references" / "tutorials" / "advanced"
        advanced_tutorials_dir.mkdir(parents=True, exist_ok=True)

        # 处理基础教程
        for tutorial_dir in self.doc_priorities['tutorials_basic']:
            source_dir = self.source_dir / tutorial_dir
            if source_dir.exists():
                target_dir = basic_tutorials_dir / source_dir.name
                self.copy_tutorial_directory(source_dir, target_dir)

        # 处理进阶教程
        for tutorial_dir in self.doc_priorities['tutorials_advanced']:
            source_dir = self.source_dir / tutorial_dir
            if source_dir.exists():
                target_dir = advanced_tutorials_dir / source_dir.name
                self.copy_tutorial_directory(source_dir, target_dir)

    def copy_tutorial_directory(self, source_dir: Path, target_dir: Path):
        """复制教程目录"""
        target_dir.mkdir(parents=True, exist_ok=True)

        for item in source_dir.rglob("*"):
            if item.is_file() and self.should_include_file(item):
                rel_path = item.relative_to(source_dir)
                target_file = target_dir / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)

                content = self.clean_markdown_content(item)
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.processed_files.append(str(target_file))

        print(f"  ✅ {source_dir.name}/")

    def organize_learning_resources(self):
        """组织学习资源"""
        print("📖 处理学习资源...")
        learning_dir = self.target_dir / "references" / "learning"
        learning_dir.mkdir(parents=True, exist_ok=True)

        for resource_dir in self.doc_priorities['learning']:
            source_dir = self.source_dir / resource_dir
            if source_dir.exists():
                target_dir = learning_dir / source_dir.name
                self.copy_tutorial_directory(source_dir, target_dir)

    def create_quick_reference(self):
        """创建快速参考索引"""
        print("🔍 创建快速参考索引...")

        index_content = """# DSPy 快速参考索引

## 框架概述
DSPy 是一个声明式框架，用于构建模块化 AI 软件。它允许您在结构化代码上快速迭代，而不是脆弱的提示字符串。

## 核心概念

### 1. Signatures (签名)
定义输入输出结构的接口：
- 基础签名类
- 输入/输出字段定义
- 类型注解和描述

### 2. Modules (模块)
可重用的 AI 程序组件：
- `dspy.Predict` - 基础预测模块
- `dspy.ChainOfThought` - 思维链推理
- `dspy.ReAct` - 推理-行动循环
- `dspy.MultiChainComparison` - 多链比较

### 3. Optimizers (优化器)
自动优化提示和权重：
- `BootstrapFewShot` - 少样本学习优化
- `MIPRO` - 多指令推理优化
- `COPRO` - 程序优化

### 4. Teleprompters (提示模板)
自动生成和优化提示：
- `dspy.Prediction` - 预测模板
- `dspy.BootstrapFewShot` - 引导优化

## 快速开始

### 安装和配置
```bash
pip install -U dspy
```

```python
import dspy

# 配置语言模型
lm = dspy.LM("openai/gpt-4o-mini", api_key="YOUR_API_KEY")
dspy.configure(lm=lm)
```

### 基础示例
```python
# 定义签名
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers"""
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()

# 创建模块
qa = dspy.Predict(BasicQA)

# 使用
result = qa(question="What is the capital of France?")
print(result.answer)
```

## 文档导航

### 核心概念
- [框架介绍](core_concepts/index.md) - 完整的框架概述和安装指南
- [速查表](core_concepts/cheatsheet.md) - 常用代码模式和技巧

### API 参考
- [模块 API](api_reference/modules/) - 核心模块文档
- [签名系统](api_reference/signatures/) - 输入输出定义
- [优化器](api_reference/optimizers/) - 自动优化算法
- [基础组件](api_reference/primitives/) - 底层构建块

### 教程
- [基础教程](tutorials/basics/) - 入门级实践教程
- [进阶教程](tutorials/advanced/) - 高级应用和优化
- [学习资源](learning/) - 深入学习材料

### 实际应用
- [RAG 系统](tutorials/basics/rag/) - 检索增强生成
- [分类任务](tutorials/basics/classification/) - 文本分类
- [智能代理](tutorials/basics/agents/) - Agent 系统
- [性能优化](tutorials/advanced/optimization/) - 系统优化

## 常见问题

### Q: DSPy 与其他框架的区别？
A: DSPy 专注于程序化 AI 开发，而非提示工程。它提供了算法来自动优化提示和权重。

### Q: 如何开始使用 DSPy？
A: 从基础教程开始，理解签名、模块和优化器的概念，然后逐步学习高级特性。

### Q: 什么时候需要使用优化器？
A: 当默认性能不够满意时，使用优化器自动提升程序性能。

## 最佳实践

1. **从简单开始** - 使用 `dspy.Predict` 构建基础功能
2. **逐步优化** - 添加思维链、推理等高级模块
3. **自动化优化** - 使用 BootstrapFewShot 等优化器
4. **迭代改进** - 基于结果调整签名和模块

更多详细信息请参考各个子目录中的具体文档。
"""

        quick_ref_file = self.target_dir / "references" / "quick_reference.md"
        with open(quick_ref_file, 'w', encoding='utf-8') as f:
            f.write(index_content)

        self.processed_files.append(str(quick_ref_file))
        print(f"  ✅ quick_reference.md")

    def generate_report(self):
        """生成处理报告"""
        print("\n📊 处理报告:")
        print(f"  ✅ 已处理文件: {len(self.processed_files)}")
        print(f"  ⚠️  排除文件: {len(self.excluded_files)}")

        if self.excluded_files and len(self.excluded_files) <= 10:
            print("  排除的文件:")
            for file in self.excluded_files:
                print(f"    - {file}")

    def organize_all(self):
        """执行所有文档组织任务"""
        print("🚀 开始组织 DSPY 文档...")

        # 创建目录结构
        (self.target_dir / "references").mkdir(parents=True, exist_ok=True)

        # 执行组织任务
        self.organize_core_documents()
        self.organize_api_documents()
        self.organize_tutorial_documents()
        self.organize_learning_resources()
        self.create_quick_reference()

        # 生成报告
        self.generate_report()

        print("\n🎉 DSPY 文档组织完成!")
        return len(self.processed_files) > 0

def main():
    """主函数"""
    base_dir = Path(__file__).parent.parent.parent

    source_dir = base_dir / "docs" / "dspy"
    target_dir = base_dir / "skills" / "output" / "dspy"

    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return False

    organizer = DSPYDocOrganizer(str(source_dir), str(target_dir))
    success = organizer.organize_all()

    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)