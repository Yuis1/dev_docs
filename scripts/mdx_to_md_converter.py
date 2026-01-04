#!/usr/bin/env python3
"""
MDX to MD Converter for LangChain Ecosystem Skill
将 .mdx 文件转换为标准 .md 格式，移除前端matter特定标记并清理格式
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple

class MDXConverter:
    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.converted_files = []
        self.errors = []

    def clean_frontmatter(self, content: str) -> str:
        """清理或标准化 YAML frontmatter"""
        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            # 找到 frontmatter 结束位置
            end_idx = -1
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    end_idx = i + 1
                    break

            if end_idx > 0:
                frontmatter = lines[1:end_idx-1]
                # 保留重要的 frontmatter 信息
                cleaned_fm = []
                for line in frontmatter:
                    if any(key in line for key in ['title:', 'description:', 'slug:']):
                        cleaned_fm.append(line)

                # 重新构建内容
                if cleaned_fm:
                    return '---\n' + '\n'.join(cleaned_fm) + '\n---\n' + '\n'.join(lines[end_idx:])
                else:
                    return '\n'.join(lines[end_idx:])

        return content

    def clean_mdx_syntax(self, content: str) -> str:
        """清理 MDX 特定语法"""
        # 移除 :::python 和 :::js 块标记，保留代码
        content = re.sub(r':::python\s*\n', '```python\n', content)
        content = re.sub(r':::js\s*\n', '```javascript\n', content)
        content = re.sub(r':::\s*\n', '```\n', content)

        # 处理 @[`function`] 语法
        content = re.sub(r'@\[`([^`]+)`\]', r'`\1`', content)

        # 处理其他 MDX 特定组件
        content = re.sub(r'<Info>\s*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'</Info>\s*\n', '', content, flags=re.MULTILINE)

        # 清理多余的空行
        content = re.sub(r'\n{3,}', '\n\n', content)

        return content.strip() + '\n'

    def convert_file(self, source_file: Path, target_file: Path) -> bool:
        """转换单个文件"""
        try:
            # 确保目标目录存在
            target_file.parent.mkdir(parents=True, exist_ok=True)

            # 读取源文件
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 清理内容
            content = self.clean_frontmatter(content)
            content = self.clean_mdx_syntax(content)

            # 写入目标文件
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)

            self.converted_files.append(str(target_file))
            return True

        except Exception as e:
            self.errors.append(f"转换文件 {source_file} 时出错: {e}")
            return False

    def convert_directory(self, source_subdir: str = "") -> Tuple[int, int]:
        """转换整个目录"""
        source_path = self.source_dir / source_subdir if source_subdir else self.source_dir
        target_path = self.target_dir / source_subdir if source_subdir else self.target_dir

        if not source_path.exists():
            print(f"源目录不存在: {source_path}")
            return 0, 0

        success_count = 0
        total_count = 0

        # 遍历所有 .mdx 文件
        for mdx_file in source_path.rglob("*.mdx"):
            if mdx_file.is_file():
                # 计算相对路径并更改扩展名
                rel_path = mdx_file.relative_to(source_path)
                target_file = target_path / rel_path.with_suffix('.md')

                total_count += 1
                if self.convert_file(mdx_file, target_file):
                    success_count += 1

        return success_count, total_count

    def copy_other_files(self, source_subdir: str = ""):
        """复制非 .mdx 文件（如图片、资源等）"""
        source_path = self.source_dir / source_subdir if source_subdir else self.source_dir
        target_path = self.target_dir / source_subdir if source_subdir else self.target_dir

        if not source_path.exists():
            return

        for file_path in source_path.rglob("*"):
            if file_path.is_file() and file_path.suffix != '.mdx':
                rel_path = file_path.relative_to(source_path)
                target_file = target_path / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, target_file)

    def generate_index(self, subdir: str) -> str:
        """为指定子目录生成索引文件"""
        index_path = self.target_dir / subdir / "README.md"

        # 收集所有 .md 文件
        md_files = []
        for md_file in (self.target_dir / subdir).rglob("*.md"):
            if md_file.name != "README.md" and md_file.is_file():
                rel_path = md_file.relative_to(self.target_dir / subdir)
                md_files.append(rel_path)

        md_files.sort()

        # 生成索引内容
        content = f"# {subdir.title()} 文档索引\n\n"
        content += f"本目录包含 {subdir} 相关的技术文档。\n\n"

        if md_files:
            content += "## 文档列表\n\n"
            for file_path in md_files:
                # 尝试从文件中提取标题
                title = self.extract_title(file_path)
                content += f"- [{title}](./{file_path})\n"

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(index_path)

    def extract_title(self, file_path: Path) -> str:
        """从文件中提取标题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 从 frontmatter 提取 title
            fm_match = re.search(r'^---\n.*?title:\s*(.+?)\n.*?---', content, re.DOTALL)
            if fm_match:
                title = fm_match.group(1).strip().strip('"\'')
                return title

            # 从第一个 # 标题提取
            h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if h1_match:
                return h1_match.group(1).strip()

            # 使用文件名
            return file_path.stem.replace('-', ' ').replace('_', ' ').title()

        except:
            return file_path.stem.replace('-', ' ').replace('_', ' ').title()

def main():
    """主函数"""
    base_dir = Path(__file__).parent.parent

    # 定义转换任务
    conversions = [
        ("docs/langchain", "skills/output/langchain_ecosystem/references/langchain"),
        ("docs/langgraph", "skills/output/langchain_ecosystem/references/langgraph"),
        ("docs/langsmith", "skills/output/langchain_ecosystem/references/langsmith")
    ]

    converter = MDXConverter("", "")

    total_converted = 0
    total_files = 0

    print("🚀 开始转换 MDX 文档...")

    for source_subdir, target_subdir in conversions:
        print(f"\n📁 转换 {source_subdir} -> {target_subdir}")

        source_dir = base_dir / source_subdir
        target_dir = base_dir / target_subdir

        if not source_dir.exists():
            print(f"⚠️  源目录不存在: {source_dir}")
            continue

        converter = MDXConverter(str(source_dir), str(target_dir))

        # 转换文件
        success, total = converter.convert_directory()
        total_converted += success
        total_files += total

        # 复制其他资源文件
        converter.copy_other_files()

        # 生成索引
        if success > 0:
            index_file = converter.generate_index("")
            print(f"✅ 生成索引: {index_file}")

        print(f"   转换成功: {success}/{total} 个文件")

        # 显示错误
        if converter.errors:
            print("   错误:")
            for error in converter.errors:
                print(f"     - {error}")

    print(f"\n🎉 转换完成!")
    print(f"   总计转换: {total_converted}/{total_files} 个文件")

    if total_converted > 0:
        print(f"\n📚 生成的文档目录:")
        for _, target_subdir in conversions:
            target_dir = base_dir / target_subdir
            if target_dir.exists():
                file_count = len(list(target_dir.rglob("*.md")))
                print(f"   - {target_subdir}: {file_count} 个 markdown 文件")

if __name__ == "__main__":
    main()