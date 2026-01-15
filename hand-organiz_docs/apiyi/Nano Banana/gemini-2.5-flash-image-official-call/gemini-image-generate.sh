#!/bin/bash

# ============================================================
# Gemini 图片生成工具 - Bash/Curl 版本
# 使用 Google Gemini 2.5 Flash Image 模型生成图片
# ============================================================

# ========== 配置区 ==========
# 1. 设置你的 API 密钥
API_KEY="sk-"

# 2. 输入图片描述（提示词）
PROMPT="AI-generated image of a nano banana dish in a Gemini-themed restaurant"

# 3. 选择纵横比（可选）
# 支持: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
ASPECT_RATIO="9:16"  # 竖屏
# ASPECT_RATIO="1:1"   # 正方形
# ASPECT_RATIO="9:16"  # 竖屏

# 4. 设置输出文件名
OUTPUT_FILE="gemini_generated_$(date +%Y%m%d_%H%M%S).png"

# 5. API 端点
API_URL="https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent"
# ============================

# 检查依赖
if ! command -v jq &> /dev/null; then
    echo "❌ 错误: 需要安装 jq 工具"
    echo ""
    echo "安装方法:"
    echo "  macOS:   brew install jq"
    echo "  Ubuntu:  sudo apt-get install jq"
    echo "  CentOS:  sudo yum install jq"
    echo ""
    exit 1
fi

echo "============================================================"
echo "Gemini 图片生成工具"
echo "============================================================"
echo "⏰ 开始时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "============================================================"
echo "🚀 开始生成图片..."
echo "📝 提示词: ${PROMPT}"
echo "📐 纵横比: ${ASPECT_RATIO}"
echo "📡 发送请求到 Gemini API..."

# 构建 JSON 请求
REQUEST_JSON=$(jq -n \
  --arg prompt "$PROMPT" \
  --arg ratio "$ASPECT_RATIO" \
  '{
    contents: [{
      parts: [{text: $prompt}]
    }],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig: {
        aspectRatio: $ratio
      }
    }
  }')

# 发送请求
RESPONSE=$(curl -s -X POST "${API_URL}" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${REQUEST_JSON}")

# 检查错误
if echo "${RESPONSE}" | jq -e '.error' &> /dev/null; then
    echo "❌ 生成失败"
    echo "💥 错误信息:"
    echo "${RESPONSE}" | jq -r '.error.message // .error'
    echo ""
    echo "建议检查:"
    echo "  1. API 密钥是否正确"
    echo "  2. 网络连接是否正常"
    echo "  3. 提示词是否合理"
    exit 1
fi

# 提取图片数据
echo "💾 正在保存图片..."
IMAGE_DATA=$(echo "${RESPONSE}" | jq -r '.candidates[0].content.parts[0].inlineData.data' 2>/dev/null)

if [ -z "$IMAGE_DATA" ] || [ "$IMAGE_DATA" = "null" ]; then
    echo "❌ 未找到图片数据"
    echo "📋 响应内容:"
    echo "${RESPONSE}" | jq '.' 2>/dev/null || echo "${RESPONSE}"
    exit 1
fi

# 解码并保存图片
echo "${IMAGE_DATA}" | base64 --decode > "${OUTPUT_FILE}"

# 检查结果
if [ -f "${OUTPUT_FILE}" ]; then
    FILE_SIZE=$(du -h "${OUTPUT_FILE}" | cut -f1)
    echo "✅ 图片已保存: ${OUTPUT_FILE}"
    echo "📊 文件大小: ${FILE_SIZE}"
    echo ""
    echo "============================================================"
    echo "🎉 生成成功！"
    echo "⏰ 结束时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "============================================================"
else
    echo "❌ 图片保存失败"
    exit 1
fi
