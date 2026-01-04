#!/usr/bin/env python3
"""
LangChain Ecosystem 文档转换脚本
使用通用 MDX 转换器处理技术文档
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

try:
    from scripts.mdx_to_md_converter import MDXConverter
except ImportError:
    print("❌ 无法导入 MDX 转换器，请确保 scripts/mdx_to_md_converter.py 存在")
    sys.exit(1)

def main():
    """转换 LangChain 生态系统文档"""
    base_dir = Path(__file__).parent.parent

    # 确保参考文档目录存在
    (base_dir / "references" / "langchain").mkdir(parents=True, exist_ok=True)
    (base_dir / "references" / "langgraph").mkdir(parents=True, exist_ok=True)
    (base_dir / "references" / "langsmith").mkdir(parents=True, exist_ok=True)

    # 定义转换配置
    conversions = [
        {
            "source": project_root / "docs" / "langchain",
            "target": base_dir / "references" / "langchain",
            "name": "LangChain"
        },
        {
            "source": project_root / "docs" / "langgraph",
            "target": base_dir / "references" / "langgraph",
            "name": "LangGraph"
        },
        {
            "source": project_root / "docs" / "langsmith",
            "target": base_dir / "references" / "langsmith",
            "name": "LangSmith"
        }
    ]

    print("🔄 开始转换 LangChain 生态系统文档...")

    total_converted = 0
    total_files = 0

    for config in conversions:
        source_dir = config["source"]
        target_dir = config["target"]
        name = config["name"]

        print(f"\n📚 处理 {name} 文档...")

        if not source_dir.exists():
            print(f"⚠️  源目录不存在: {source_dir}")
            continue

        # 创建转换器
        converter = MDXConverter(str(source_dir), str(target_dir))

        # 转换文档
        success, count = converter.convert_directory()
        total_converted += success
        total_files += count

        # 复制资源文件
        converter.copy_other_files()

        # 生成索引
        if success > 0:
            index_file = converter.generate_index("")
            print(f"✅ 生成索引: {Path(index_file).name}")

        print(f"   转换结果: {success}/{count} 个文件")

        # 显示错误（如果有）
        if converter.errors:
            print(f"   ⚠️  发现 {len(converter.errors)} 个错误:")
            for error in converter.errors[:3]:  # 只显示前3个错误
                print(f"     - {error}")
            if len(converter.errors) > 3:
                print(f"     - ... 还有 {len(converter.errors) - 3} 个错误")

    print(f"\n🎉 文档转换完成!")
    print(f"📊 总计: {total_converted}/{total_files} 个文件成功转换")

    # 生成总体统计报告
    print(f"\n📋 转换报告:")
    for config in conversions:
        target_dir = config["target"]
        name = config["name"]
        if target_dir.exists():
            md_count = len(list(target_dir.rglob("*.md")))
            print(f"   - {name}: {md_count} 个 Markdown 文件")

    return total_converted > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)