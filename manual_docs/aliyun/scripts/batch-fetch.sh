#!/bin/bash
# 批量爬取阿里云文档

BASE_URL="https://help.aliyun.com/document_detail"
OUTPUT_DIR="/home/yuis/dev/dev_docs/hand-organiz_docs/aliyun"

# 文档 ID 列表
IDS=(
  2842554 2880903 2841718 2866125 2866129 2870973
  2862209 2862210 2862577 2864784 2867560 2862208
  2990719 2968153 2975991 2845871 2877996 2860683
  2997010 2845960 2980468 2867839 2880812
)

SKILL_SCRIPT="/home/yuis/.claude/skills/baoyu-url-to-markdown/scripts/main.ts"

echo "开始批量爬取 ${#IDS[@]} 个文档..."
echo ""

i=0
for id in "${IDS[@]}"; do
  url="${BASE_URL}/${id}.html?mode=pure"
  echo "[$((i+1))/${#IDS[@]}] 正在爬取 ID: $id"
  ((i++))

  npx -y bun "$SKILL_SCRIPT" "$url"
  echo ""
done

echo "爬取完成！"
echo "请检查：$OUTPUT_DIR"
