#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 文档清理脚本
- 清理多余空行（保留最多2个连续空行）
- 清理行尾空格
- 确保标题前后有合适的空行
- 优化代码块和列表格式
"""

import re
from pathlib import Path

TARGET_DIR = Path("/home/yuis/dev/dev_docs/hand-organiz_docs/aliyun")

def clean_markdown(content):
    """清理 Markdown 内容"""

    # 1. 移除行尾空格
    lines = [line.rstrip() for line in content.split('\n')]

    # 2. 处理连续空行：最多保留1个
    cleaned_lines = []
    empty_count = 0

    for i, line in enumerate(lines):
        if line == '':
            empty_count += 1
            # 最多保留1个连续空行
            if empty_count <= 1:
                cleaned_lines.append(line)
        else:
            empty_count = 0
            cleaned_lines.append(line)

    # 3. 重新组合内容
    content = '\n'.join(cleaned_lines)

    # 4. 确保一级标题前有空行（除非在文件开头）
    content = re.sub(r'([^\n])\n\n# ', r'\1\n\n\n# ', content)

    # 5. 标题（#）后不要有空行，内容前保留一个空行
    # 只处理不在代码块中的情况
    lines = content.split('\n')
    result = []
    in_code_block = False
    code_block_indent = 0

    for i, line in enumerate(lines):
        # 检测代码块
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # 处理标题行
        if re.match(r'^#{1,6}\s', line):
            # 标题本身
            result.append(line)
            # 如果下一行不是空行且不是标题，添加空行
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if next_line.strip() != '' and not re.match(r'^#{1,6}\s', next_line):
                    if next_line.strip() != '':
                        result.append('')
        else:
            result.append(line)

    content = '\n'.join(result)

    # 6. 清理文档开头和结尾的多余空行
    content = content.strip() + '\n'

    # 7. 确保代码块前后有空行
    lines = content.split('\n')
    result = []
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            # 代码块开始前确保有空行
            if i > 0 and lines[i - 1].strip() != '':
                result.append('')
            result.append(line)
        else:
            result.append(line)

    content = '\n'.join(result)

    # 8. 清理列表中的多余空格（- 或 * 后面只需要一个空格）
    content = re.sub(r'^(\s*[-*+])\s{2,}', r'\1 ', content, flags=re.MULTILINE)

    # 9. 清理表格格式问题（确保 | 对齐）
    # 这个可选，因为可能破坏特定格式

    # 10. 移除 HTML 实体编码的空白字符
    content = content.replace('&nbsp;', ' ')

    return content

def process_file(file_path):
    """处理单个文件"""
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # 清理内容
        cleaned_content = clean_markdown(original_content)

        # 如果有变化，写回文件
        if cleaned_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            return True
        return False
    except Exception as e:
        print(f"✗ 错误: {file_path.name} - {e}")
        return False

def main():
    """主函数"""
    print("开始清理 Markdown 文档...\n")

    # 查找所有 .md 文件
    md_files = list(TARGET_DIR.rglob("*.md"))
    # 排除 scripts 目录
    md_files = [f for f in md_files if 'scripts' not in f.parts]

    total = len(md_files)
    modified = 0

    for file_path in sorted(md_files):
        relative_path = file_path.relative_to(TARGET_DIR)
        if process_file(file_path):
            modified += 1
            print(f"✓ 已清理: {relative_path}")
        else:
            print(f"  跳过: {relative_path} (无需清理)")

    print(f"\n清理完成！")
    print(f"总文件数: {total}")
    print(f"已修改: {modified}")
    print(f"无需修改: {total - modified}")

if __name__ == "__main__":
    main()
