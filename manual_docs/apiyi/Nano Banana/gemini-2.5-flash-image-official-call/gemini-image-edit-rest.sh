#!/bin/bash
# Gemini 图片编辑 - REST 风格一行命令

APIYI_KEY="sk-"
INPUT_IMAGE="./dog.png"
PROMPT="生成图片：增加一只帅气的猫咪在狗狗的旁边，不改变原有的图片的结构"
ASPECT_RATIO="16:9"

# 检测图片类型
[[ "$INPUT_IMAGE" =~ \.(jpe?g|JPE?G)$ ]] && MIME="image/jpeg" || MIME="image/png"

# 编码图片
IMG_BASE64=$(base64 -i "$INPUT_IMAGE" 2>/dev/null || base64 -w0 "$INPUT_IMAGE")

# REST 风格请求
curl -s -X POST "https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "Authorization: Bearer $APIYI_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [
        {\"text\": \"$PROMPT\"},
        {\"inline_data\": {
          \"mime_type\": \"$MIME\",
          \"data\": \"$IMG_BASE64\"
        }}
      ]
    }],
    \"generationConfig\": {
      \"responseModalities\": [\"IMAGE\"],
      \"imageConfig\": {
        \"aspectRatio\": \"$ASPECT_RATIO\"
      }
    }
  }" \
  | grep -o '"data": "[^"]*"' \
  | head -1 \
  | cut -d'"' -f4 \
  | base64 --decode > "gemini_edited_$(date +%Y%m%d_%H%M%S).png"

echo "✓ 图片编辑完成！"
