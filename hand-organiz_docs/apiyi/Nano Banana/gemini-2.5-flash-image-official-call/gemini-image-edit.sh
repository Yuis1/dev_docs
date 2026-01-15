#!/bin/bash

# ============================================================
# Gemini 图片编辑工具 - Bash 版本
# 上传本地图片 + 文字描述，生成新图片
# ============================================================

# ========== 配置区 ==========
API_KEY="sk-"
INPUT_IMAGE="./dog.png"
PROMPT="生成图片：增加一只帅气的猫咪在狗狗的旁边，不改变原有的图片的结构"

# 纵横比（可选）
# 支持: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
ASPECT_RATIO="16:9"

OUTPUT_FILE="gemini_edited_$(date +%Y%m%d_%H%M%S).png"
API_URL="https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent"
# ============================

# 检查依赖
if ! command -v jq &> /dev/null; then
    echo "错误: 需要安装 jq"
    echo "安装: brew install jq (macOS) 或 apt install jq (Linux)"
    exit 1
fi

# 检查图片文件
if [ ! -f "$INPUT_IMAGE" ]; then
    echo "错误: 图片不存在: ${INPUT_IMAGE}"
    exit 1
fi

echo "开始编辑图片..."
echo "输入: ${INPUT_IMAGE}"
echo "描述: ${PROMPT}"
echo "比例: ${ASPECT_RATIO}"

# 编码图片（兼容 macOS 和 Linux）
if [[ "$(uname)" == "Darwin" ]]; then
  IMG_BASE64=$(base64 -i "$INPUT_IMAGE")
else
  IMG_BASE64=$(base64 -w0 "$INPUT_IMAGE")
fi

# 检测 MIME 类型
FILE_EXT=$(echo "${INPUT_IMAGE##*.}" | tr '[:upper:]' '[:lower:]')
case "$FILE_EXT" in
    jpg|jpeg) MIME_TYPE="image/jpeg" ;;
    png)      MIME_TYPE="image/png" ;;
    webp)     MIME_TYPE="image/webp" ;;
    *)        MIME_TYPE="image/jpeg" ;;
esac

echo "类型: ${MIME_TYPE}"
echo "正在发送请求..."

# 构建 JSON 请求（使用临时文件避免参数长度限制）
TEMP_JSON=$(mktemp)
TEMP_REQUEST=$(mktemp)

cat > "$TEMP_JSON" << EOF
{
  "prompt": $(echo -n "$PROMPT" | jq -R -s .),
  "ratio": "$ASPECT_RATIO",
  "mime": "$MIME_TYPE",
  "data": $(echo -n "$IMG_BASE64" | jq -R -s .)
}
EOF

jq '{
  contents: [{
    parts: [
      {text: .prompt},
      {inline_data: {mime_type: .mime, data: .data}}
    ]
  }],
  generationConfig: {
    responseModalities: ["IMAGE"],
    imageConfig: {aspectRatio: .ratio}
  }
}' "$TEMP_JSON" > "$TEMP_REQUEST"

# 发送请求
RESPONSE=$(curl -s -X POST "${API_URL}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d @"$TEMP_REQUEST")

rm -f "$TEMP_JSON" "$TEMP_REQUEST"

# 检查错误
if echo "${RESPONSE}" | jq -e '.error' &> /dev/null; then
    echo "编辑失败:"
    echo "${RESPONSE}" | jq -r '.error.message // .error'
    exit 1
fi

# 提取并保存图片
IMAGE_DATA=$(echo "${RESPONSE}" | jq -r '.candidates[0].content.parts[0].inlineData.data' 2>/dev/null)

if [ -z "$IMAGE_DATA" ] || [ "$IMAGE_DATA" = "null" ]; then
    echo "未找到图片数据"
    echo "${RESPONSE}" | jq '.'
    exit 1
fi

echo "${IMAGE_DATA}" | base64 --decode > "${OUTPUT_FILE}"

if [ -f "${OUTPUT_FILE}" ]; then
    echo "成功! 保存至: ${OUTPUT_FILE}"
    echo "文件大小: $(du -h "${OUTPUT_FILE}" | cut -f1)"
else
    echo "保存失败"
    exit 1
fi
