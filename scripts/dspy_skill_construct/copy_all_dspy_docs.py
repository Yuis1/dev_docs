#!/usr/bin/env python3
"""
DSPY 完整文档复制脚本
复制所有教程内容，包括 .ipynb 和图片文件，并按功能分类组织
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

class DSPYCompleteDocCopier:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.copied_files = []
        self.copied_dirs = []

        # 定义教程分类策略
        self.tutorial_categories = {
            # 核心 GEPA 优化器系列（第一优先级）
            'gepa': {
                'description': 'GEPA 优化器系列教程',
                'directories': [
                    'gepa_aime',
                    'gepa_papillon',
                    'gepa_ai_program',
                    'gepa_facilitysupportanalyzer',
                    'gepa_trusted_monitor'
                ],
                'priority': 1
            },

            # 优化器核心（第一优先级）
            'optimization': {
                'description': '优化器核心教程',
                'directories': [
                    'optimize_ai_program',
                    'optimizer_tracking',
                    'math'
                ],
                'priority': 1
            },

            # 基础应用教程（第二优先级）
            'core_applications': {
                'description': '基础应用教程',
                'directories': [
                    'build_ai_program',
                    'classification',
                    'rag',
                    'agents',
                    'entity_extraction',
                    'multihop_search'
                ],
                'priority': 2
            },

            # 高级功能教程（第二优先级）
            'advanced_features': {
                'description': '高级功能教程',
                'directories': [
                    'program_of_thought',
                    'tool_use',
                    'customer_service_agent',
                    'mem0_react_agent'
                ],
                'priority': 2
            },

            # 系统特性教程（第三优先级）
            'system_features': {
                'description': '系统特性教程',
                'directories': [
                    'papillon',
                    'mcp',
                    'observability',
                    'deployment'
                ],
                'priority': 3
            },

            # 实验性功能（第三优先级）
            'experimental': {
                'description': '实验性功能教程',
                'directories': [
                    'async',
                    'streaming',
                    'cache',
                    'llms_txt_generation',
                    'sample_code_generation',
                    'conversation_history',
                    'real_world_examples',
                    'yahoo_finance_react',
                    'ai_text_game',
                    'games',
                    'audio'
                ],
                'priority': 3
            }
        }

    def create_directory_structure(self):
        """创建目标目录结构"""
        print("🏗️  创建目录结构...")

        tutorials_base = self.target_dir / "references" / "tutorials"

        # 删除现有 tutorials 目录（如果存在）
        if tutorials_base.exists():
            shutil.rmtree(tutorials_base)

        # 创建新的分类目录
        for category_name, category_info in self.tutorial_categories.items():
            category_dir = tutorials_base / category_name
            category_dir.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ 创建目录: {category_name}/")

    def copy_tutorial_directory(self, source_subdir: str, target_category: str) -> int:
        """复制单个教程目录到指定分类"""
        source_path = self.source_dir / source_subdir

        if not source_path.exists():
            print(f"  ⚠️  源目录不存在: {source_subdir}")
            return 0

        target_path = self.target_dir / "references" / "tutorials" / target_category / source_subdir
        target_path.mkdir(parents=True, exist_ok=True)

        copied_count = 0

        # 复制所有文件
        for item in source_path.rglob("*"):
            if item.is_file():
                # 计算相对路径
                rel_path = item.relative_to(source_path)
                target_file = target_path / rel_path

                # 确保目标目录存在
                target_file.parent.mkdir(parents=True, exist_ok=True)

                # 复制文件
                shutil.copy2(item, target_file)
                copied_count += 1

                # 记录复制的文件类型
                if item.suffix in ['.md', '.ipynb', '.py', '.png', '.jpg', '.jpeg']:
                    self.copied_files.append({
                        'source': str(item),
                        'target': str(target_file),
                        'category': target_category,
                        'type': item.suffix
                    })

        return copied_count

    def copy_all_tutorials(self):
        """按优先级复制所有教程"""
        print("\n📚 开始复制教程内容...")

        total_copied = 0

        # 按优先级排序
        sorted_categories = sorted(
            self.tutorial_categories.items(),
            key=lambda x: x[1]['priority']
        )

        for category_name, category_info in sorted_categories:
            print(f"\n🎯 处理分类: {category_info['description']} (优先级: {category_info['priority']})")

            category_total = 0
            for subdir in category_info['directories']:
                copied = self.copy_tutorial_directory(subdir, category_name)
                category_total += copied
                if copied > 0:
                    print(f"  ✅ {subdir}/ - {copied} 个文件")

            total_copied += category_total
            print(f"  📊 {category_name} 分类总计: {category_total} 个文件")

        return total_copied

    def create_category_indexes(self):
        """为每个分类创建索引文件"""
        print("\n📝 创建分类索引...")

        tutorials_base = self.target_dir / "references" / "tutorials"

        for category_name, category_info in self.tutorial_categories.items():
            category_dir = tutorials_base / category_name

            if not category_dir.exists():
                continue

            # 收集该分类下的所有教程
            tutorials = []
            for item in category_dir.iterdir():
                if item.is_dir():
                    tutorials.append(item.name)

            if not tutorials:
                continue

            # 创建索引内容
            index_content = f"""# {category_info['description']}

本分类包含以下教程：

"""

            for tutorial in sorted(tutorials):
                tutorial_dir = category_dir / tutorial

                # 查找主要文件
                main_files = []
                for suffix in ['.md', '.ipynb']:
                    main_file = tutorial_dir / f"index{suffix}"
                    if main_file.exists():
                        main_files.append(f"index{suffix}")

                if main_files:
                    main_file_ref = main_files[0]
                    index_content += f"## [{tutorial.replace('_', ' ').title()}]({main_file_ref})\n\n"

                    # 列出该教程包含的文件
                    files = list(tutorial_dir.rglob("*"))
                    files = [f for f in files if f.is_file()]

                    if len(files) > 1:
                        index_content += "**包含文件:**\n"
                        for file in sorted(files):
                            rel_path = file.relative_to(tutorial_dir)
                            if rel_path.suffix in ['.md', '.ipynb', '.py']:
                                index_content += f"- [{rel_path.name}]({rel_path})\n"
                        index_content += "\n"

            # 写入索引文件
            index_file = category_dir / "README.md"
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_content)

            print(f"  ✅ 创建索引: {category_name}/README.md")

    def create_master_index(self):
        """创建主教程索引"""
        print("\n🗂️  创建主教程索引...")

        tutorials_base = self.target_dir / "references" / "tutorials"

        master_content = """# DSPy 教程完整索引

本目录包含 DSPy 框架的完整教程集合，按功能和学习难度分类组织。

## 学习路径建议

### 🌱 初学者路径
1. 从 **core_applications** 分类开始
2. 先学习 `build_ai_program` 和 `classification`
3. 然后尝试 `rag` 和 `agents`
4. 最后接触 `entity_extraction` 和 `multihop_search`

### 🚀 进阶开发者路径
1. 掌握基础应用后，学习 **optimization** 分类
2. 重点学习 `optimize_ai_program` 和 `math`
3. 使用 `optimizer_tracking` 监控性能
4. 深入研究 **gepa** 分类的优化器

### 👨‍💻 专家用户路径
1. 精通 GEPA 优化器后，探索 **advanced_features**
2. 学习 `program_of_thought` 和复杂推理
3. 掌握 `tool_use` 和高级代理模式
4. 最后探索 **experimental** 分类的实验性功能

## 教程分类

"""

        # 按优先级排序添加分类
        sorted_categories = sorted(
            self.tutorial_categories.items(),
            key=lambda x: x[1]['priority']
        )

        for category_name, category_info in sorted_categories:
            category_dir = tutorials_base / category_name

            if not category_dir.exists():
                continue

            priority_icon = "🔥" if category_info['priority'] == 1 else "⚡" if category_info['priority'] == 2 else "🔬"

            master_content += f"### {priority_icon} {category_info['description']}\n\n"

            # 添加教程列表
            for subdir in sorted(category_info['directories']):
                tutorial_path = category_dir / subdir
                if tutorial_path.exists():
                    master_content += f"- **[{subdir.replace('_', ' ').title()}]({category_name}/{subdir}/)**\n"

            master_content += "\n"

        # 添加文件统计
        master_content += f"""## 统计信息

- **总文件数**: {len(self.copied_files)} 个
- **分类数量**: {len(self.tutorial_categories)} 个
- **包含教程**: {len(set(f['source'].split('/')[-2] for f in self.copied_files))} 个

## 使用说明

1. **Jupyter Notebook (.ipynb)**: 可直接运行的代码示例
2. **Markdown (.md)**: 说明文档和教程指南
3. **图片文件 (.png/.jpg)**: 可视化和界面截图
4. **Python (.py)**: 独立的代码脚本

每个教程目录都有自己的 README.md 文件，包含该教程的详细说明和文件列表。
"""

        # 写入主索引
        master_file = tutorials_base / "README.md"
        with open(master_file, 'w', encoding='utf-8') as f:
            f.write(master_content)

        print(f"  ✅ 创建主索引: tutorials/README.md")

    def generate_statistics(self):
        """生成详细的复制统计报告"""
        print("\n📊 生成统计报告...")

        # 按类型统计
        type_stats = {}
        category_stats = {}

        for file_info in self.copied_files:
            file_type = file_info['type']
            category = file_info['category']

            type_stats[file_type] = type_stats.get(file_type, 0) + 1
            category_stats[category] = category_stats.get(category, 0) + 1

        print("\n📈 复制统计报告:")
        print(f"  总计复制文件: {len(self.copied_files)} 个")

        print("\n📁 按文件类型:")
        for file_type, count in sorted(type_stats.items()):
            print(f"  {file_type}: {count} 个")

        print("\n📂 按分类:")
        for category in sorted(self.tutorial_categories.keys()):
            count = category_stats.get(category, 0)
            if count > 0:
                description = self.tutorial_categories[category]['description']
                print(f"  {category}: {count} 个 ({description})")

    def copy_all_complete(self):
        """执行完整的复制流程"""
        print("🚀 开始 DSPY 完整文档复制...")

        # 1. 创建目录结构
        self.create_directory_structure()

        # 2. 复制所有教程
        total_files = self.copy_all_tutorials()

        # 3. 创建分类索引
        self.create_category_indexes()

        # 4. 创建主索引
        self.create_master_index()

        # 5. 生成统计报告
        self.generate_statistics()

        print(f"\n🎉 DSPY 完整文档复制完成!")
        print(f"📚 总计复制: {total_files} 个文件")
        print(f"📁 涵盖分类: {len(set(f['category'] for f in self.copied_files))} 个")

        return total_files > 0

def main():
    """主函数"""
    base_dir = Path(__file__).resolve().parent.parent.parent

    source_dir = base_dir / "docs" / "dspy" / "tutorials"
    target_dir = base_dir / "skills" / "output" / "dspy"

    if not source_dir.exists():
        print(f"❌ 源目录不存在: {source_dir}")
        return False

    copier = DSPYCompleteDocCopier(str(source_dir), str(target_dir))
    success = copier.copy_all_complete()

    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
