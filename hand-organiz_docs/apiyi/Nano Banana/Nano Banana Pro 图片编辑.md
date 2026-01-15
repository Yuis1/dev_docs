> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/nano-banana-image-edit)

> 使用 Gemini 2.5 Flash Image 进行图片编辑、合成和修改。支持多图片输入、文本指令编辑、自定义分辨率，10 秒快速生成。

概述
--

**Nano Banana 图片编辑**基于谷歌 Gemini 图像生成模型系列，目前有以下版本可用：

### 最新版本（推荐）

*   **Nano Banana Pro**：`gemini-3-pro-image-preview`（🔥 2025 年 11 月 20 日上线）
    *   基于 Gemini 3 Pro，推理能力更强
    *   支持 4K 高清图像编辑（1K、2K、4K）
    *   高级局部编辑：摄像机角度、焦点、色彩分级、场景照明
    *   业界最佳文本渲染能力

### 前代版本

*   **正式版**：`gemini-2.5-flash-image`（稳定版，支持 10 种宽高比）
*   **预览版**：`gemini-2.5-flash-image-preview`（⚠️ 已于 2025 年 10 月 30 日下线）

[

📚 最新文档
-------

**飞书完整使用指南** - 更新最快，支持评论互动访问飞书文档获取最新的使用教程、技巧分享和问题解答。文档持续更新，遇到问题可直接在飞书上评论交流。

](https://xinqikeji.feishu.cn/wiki/W4vEwdiCPi3VfTkrL5hcVlDxnQf)

调用方式对比
------

API 易 支持两种调用方式，您可以根据需求选择：

### 端点对比表

<table><thead><tr><th>特性</th><th>谷歌原生格式</th><th>OpenAI 兼容模式</th></tr></thead><tbody><tr><td><strong>端点 URL</strong></td><td><code>/v1beta/models/gemini-2.5-flash-image:generateContent</code></td><td><code>/v1/chat/completions</code></td></tr><tr><td><strong>图片生成尺寸</strong></td><td>支持 10 种宽高比自定义</td><td>默认 1:1</td></tr><tr><td><strong>图片编辑尺寸</strong></td><td>支持宽高比自定义</td><td>智能遵循原图比例</td></tr><tr><td><strong>调用格式</strong></td><td>谷歌官方格式</td><td>OpenAI 格式</td></tr><tr><td><strong>适用场景</strong></td><td>需要精确控制输出尺寸</td><td>快速集成，兼容现有代码</td></tr></tbody></table>

编辑能力
----

### Nano Banana Pro 专属高级编辑

*   **📐 局部精细编辑**：
    *   调整摄像机角度（Camera Angles）
    *   改变焦点和景深
    *   应用专业级色彩分级（Color Grading）
*   **🌓 场景照明控制**：
    *   日夜转换效果
    *   背景虚化（Bokeh Effect）
    *   自定义光照和阴影
*   **🎯 4K 高清处理**：
    *   最高 4K 分辨率编辑
    *   保持高清晰度细节
    *   专业级输出质量

### 通用编辑能力

*   **图片合成**：将多张图片无缝融合成一张
*   **元素添加**：在图片中添加新的对象或元素
*   **风格修改**：改变图片的艺术风格或色调
*   **背景替换**：更换图片背景场景
*   **尺寸调整**：改变图片比例或尺寸
*   **细节优化**：增强图片质量或修复缺陷
*   **文本添加 / 编辑**：Nano Banana Pro 的文本渲染能力最强

快速开始
----

### 方式一：最简单示例（单图编辑）

```
import requests
import base64

API_KEY = "sk-your-api-key"
IMAGE_PATH = "./input.png"
PROMPT = "增加一只可爱的小猫"

# 读取并编码图片
with open(IMAGE_PATH, 'rb') as f:
    img_b64 = base64.b64encode(f.read()).decode()

# 发送请求
response = requests.post(
    "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "contents": [{
            "parts": [
                {"text": PROMPT},
                {"inline_data": {"mime_type": "image/png", "data": img_b64}}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}
        }
    },
    timeout=300  # 2K 推荐 5 分钟超时
).json()

# 保存结果
img_data = response["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
with open("output.png", 'wb') as f:
    f.write(base64.b64decode(img_data))


```

### 方式二：简化版（配置式 + 多图支持）

**特点**：清晰的配置区域、支持多图输入、完善的错误处理、自动超时控制

#### 核心配置示例

```
# ============================================================================
# 配置区域 - 请在此处修改您的配置
# ============================================================================

# 1. API Key（必填）
API_KEY = "sk-your-api-key"

# 2. 输入图片（支持多张）
INPUT_IMAGES = [
    "cat.png",           # 第一张图片
    "dog.png",           # 第二张图片
    # "image3.png",      # 可以添加更多图片
]

# 3. 编辑指令
EDIT_PROMPT = "将这两张图片合成，添加温馨的家庭氛围和柔和背景"

# 4. 输出参数
ASPECT_RATIO = "16:9"  # 宽高比（1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5）
RESOLUTION = "2K"      # 分辨率：1K, 2K, 4K
OUTPUT_FILE = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

# ============================================================================
# 超时配置（根据分辨率自动调整）
# ============================================================================
TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}  # 单位：秒


```

#### 多图片输入示例

```
import requests
import base64
import time
from pathlib import Path
from datetime import datetime

API_KEY = "sk-your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 配置多张输入图片
INPUT_IMAGES = ["person1.png", "person2.png", "background.png"]
EDIT_PROMPT = "将这三张图片合成为一张专业的团队照片"
RESOLUTION = "2K"
TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}

def load_image_base64(image_path):
    """读取图片并转换为 base64"""
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # 自动检测图片格式
    if image_path.lower().endswith('.png'):
        mime_type = "image/png"
    elif image_path.lower().endswith(('.jpg', '.jpeg')):
        mime_type = "image/jpeg"
    elif image_path.lower().endswith('.webp'):
        mime_type = "image/webp"
    else:
        mime_type = "image/png"

    return base64.b64encode(image_bytes).decode("utf-8"), mime_type

# 准备所有图片
print(f"📤 正在读取 {len(INPUT_IMAGES)} 张图片...")
parts = []

for image_path in INPUT_IMAGES:
    image_base64, mime_type = load_image_base64(image_path)
    parts.append({
        "inline_data": {
            "mime_type": mime_type,
            "data": image_base64
        }
    })
    print(f"✅ {image_path} ({mime_type})")

# 添加编辑指令
parts.append({"text": EDIT_PROMPT})

# 发送请求
print(f"\n⏳ 正在处理，预计 {TIMEOUT_MAP[RESOLUTION] // 60} 分钟...")
start_time = time.time()

response = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "contents": [{"parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": "16:9",
                "imageSize": RESOLUTION
            }
        }
    },
    timeout=TIMEOUT_MAP[RESOLUTION]
)

elapsed = time.time() - start_time
print(f"⏱️  实际用时: {elapsed:.1f} 秒")

# 保存结果
result = response.json()
image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

output_file = f"edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
with open(output_file, 'wb') as f:
    f.write(base64.b64decode(image_data))

print(f"✅ 编辑成功！已保存至: {output_file}")


```

完整代码示例
------

根据您的需求，可以选择以下两种方式之一：

### 方式一：谷歌原生格式（推荐）

**支持自定义分辨率和宽高比**，使用谷歌官方 API 格式。

#### 端点

```
POST https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent


```

#### 请求格式

```
{
  "contents": [
    {
      "parts": [
        {
          "text": "编辑指令文本"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "base64编码的图片数据"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9"
    }
  }
}


```

#### 支持的宽高比

`21:9`, `16:9`, `4:3`, `3:2`, `1:1`, `9:16`, `3:4`, `2:3`, `5:4`, `4:5`

#### 分辨率配置详解

*   Gemini 3 Pro (支持 4K)
    
*   Gemini 2.5 Flash (仅 1K)
    

**模型**: `gemini-3-pro-image-preview`支持三个分辨率级别：**1K**、**2K**、**4K**

<table><thead><tr><th>宽高比</th><th>1K 分辨率</th><th>1K Tokens</th><th>2K 分辨率</th><th>2K Tokens</th><th>4K 分辨率</th><th>4K Tokens</th></tr></thead><tbody><tr><td data-numeric="true"><strong>1:1</strong></td><td data-numeric="true">1024×1024</td><td data-numeric="true">1210</td><td data-numeric="true">2048×2048</td><td data-numeric="true">1210</td><td data-numeric="true">4096×4096</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>2:3</strong></td><td data-numeric="true">848×1264</td><td data-numeric="true">1210</td><td data-numeric="true">1696×2528</td><td data-numeric="true">1210</td><td data-numeric="true">3392×5056</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>3:2</strong></td><td data-numeric="true">1264×848</td><td data-numeric="true">1210</td><td data-numeric="true">2528×1696</td><td data-numeric="true">1210</td><td data-numeric="true">5056×3392</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>3:4</strong></td><td data-numeric="true">896×1200</td><td data-numeric="true">1210</td><td data-numeric="true">1792×2400</td><td data-numeric="true">1210</td><td data-numeric="true">3584×4800</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>4:3</strong></td><td data-numeric="true">1200×896</td><td data-numeric="true">1210</td><td data-numeric="true">2400×1792</td><td data-numeric="true">1210</td><td data-numeric="true">4800×3584</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>4:5</strong></td><td data-numeric="true">928×1152</td><td data-numeric="true">1210</td><td data-numeric="true">1856×2304</td><td data-numeric="true">1210</td><td data-numeric="true">3712×4608</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>5:4</strong></td><td data-numeric="true">1152×928</td><td data-numeric="true">1210</td><td data-numeric="true">2304×1856</td><td data-numeric="true">1210</td><td data-numeric="true">4608×3712</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>9:16</strong></td><td data-numeric="true">768×1376</td><td data-numeric="true">1210</td><td data-numeric="true">1536×2752</td><td data-numeric="true">1210</td><td data-numeric="true">3072×5504</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>16:9</strong></td><td data-numeric="true">1376×768</td><td data-numeric="true">1210</td><td data-numeric="true">2752×1536</td><td data-numeric="true">1210</td><td data-numeric="true">5504×3072</td><td data-numeric="true">2000</td></tr><tr><td data-numeric="true"><strong>21:9</strong></td><td data-numeric="true">1584×672</td><td data-numeric="true">1210</td><td data-numeric="true">3168×1344</td><td data-numeric="true">1210</td><td data-numeric="true">6336×2688</td><td data-numeric="true">2000</td></tr></tbody></table>

**模型**: `gemini-2.5-flash-image`仅支持 **1K** 分辨率（约 1024px）

<table><thead><tr><th>宽高比</th><th>分辨率</th><th>Tokens</th></tr></thead><tbody><tr><td data-numeric="true"><strong>1:1</strong></td><td data-numeric="true">1024×1024</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>2:3</strong></td><td data-numeric="true">832×1248</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>3:2</strong></td><td data-numeric="true">1248×832</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>3:4</strong></td><td data-numeric="true">864×1184</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>4:3</strong></td><td data-numeric="true">1184×864</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>4:5</strong></td><td data-numeric="true">896×1152</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>5:4</strong></td><td data-numeric="true">1152×896</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>9:16</strong></td><td data-numeric="true">768×1344</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>16:9</strong></td><td data-numeric="true">1344×768</td><td data-numeric="true">1290</td></tr><tr><td data-numeric="true"><strong>21:9</strong></td><td data-numeric="true">1536×672</td><td data-numeric="true">1290</td></tr></tbody></table>

#### Bash 示例（Gemini 2.5 Flash - 仅 1K）

适用于 `gemini-2.5-flash-image`，仅支持 1K 分辨率：

```
API_KEY="sk-your-api-key"
INPUT_IMAGE="./dog.png"
PROMPT="增加一只帅气的猫咪在狗狗的旁边"
ASPECT_RATIO="16:9"
OUTPUT_FILE="edited_$(date +%Y%m%d_%H%M%S).png"

# 编码图片
IMG_BASE64=$(base64 -i "$INPUT_IMAGE")

# 发送请求并保存
curl -X POST "https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "'"$PROMPT"'"},
        {"inline_data": {"mime_type": "image/png", "data": "'"$IMG_BASE64"'"}}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {"aspectRatio": "'"$ASPECT_RATIO"'"}
    }
  }' | jq -r '.candidates[0].content.parts[0].inlineData.data' | base64 --decode > "$OUTPUT_FILE"

echo "✅ 图片已保存: $OUTPUT_FILE"


```

#### Python 完整示例（Gemini 3 Pro - 支持 4K）

```
import requests
import base64

# 配置
API_KEY = "sk-your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"
INPUT_IMAGE = "./dog.png"
PROMPT = "增加一只帅气的猫咪在狗狗的旁边"
ASPECT_RATIO = "16:9"  # 可选: "1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"
RESOLUTION = "2K"       # 可选: "1K", "2K", "4K"

# 读取并编码图片
with open(INPUT_IMAGE, 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# 发送请求
response = requests.post(
    API_URL,
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "contents": [{
            "parts": [
                {"text": PROMPT},
                {"inline_data": {"mime_type": "image/png", "data": image_base64}}
            ]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": ASPECT_RATIO,
                "imageSize": RESOLUTION  # Gemini 3 Pro 专属参数
            }
        }
    },
    timeout=120
)

# 保存结果
result = response.json()
image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

with open("edited_output.png", 'wb') as f:
    f.write(base64.b64decode(image_data))

print("✅ 图片已保存: edited_output.png")


```

#### Bash/cURL 完整示例（支持 4K）

```
#!/bin/bash

API_KEY="sk-your-api-key"
INPUT_IMAGE="./photo.jpg"
PROMPT="将这张照片转换为专业摄影作品，应用电影级色彩分级"
ASPECT_RATIO="16:9"
RESOLUTION="4K"  # "1K", "2K", "4K"
OUTPUT_FILE="edited_4k.png"

# 编码图片
IMG_BASE64=$(base64 -i "$INPUT_IMAGE")

# 发送请求并保存
curl -X POST "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "'"$PROMPT"'"},
        {"inline_data": {"mime_type": "image/jpeg", "data": "'"$IMG_BASE64"'"}}
      ]
    }],
    "generationConfig": {
      "responseModalities": ["IMAGE"],
      "imageConfig": {
        "aspectRatio": "'"$ASPECT_RATIO"'",
        "imageSize": "'"$RESOLUTION"'"
      }
    }
  }' | jq -r '.candidates[0].content.parts[0].inlineData.data' | base64 --decode > "$OUTPUT_FILE"

echo "✅ 4K 图片已保存: $OUTPUT_FILE"


```

### 方式二：OpenAI 兼容模式

**兼容现有 OpenAI 格式代码**，适合快速集成。编辑图片时会智能遵循原图比例。

#### 端点

```
POST https://api.apiyi.com/v1/chat/completions


```

#### 请求格式

```
{
  "model": "gemini-2.5-flash-image",
  "stream": false,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "编辑指令文本"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "图片URL1"
          }
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "图片URL2"
          }
        }
      ]
    }
  ]
}


```

#### Python 完整示例

```
#!/usr/bin/env python3
import requests
import json
import base64
import re
from datetime import datetime
import sys

# 配置
API_KEY = "sk-"  # 请替换为你的实际密钥
API_URL = "https://api.apiyi.com/v1/chat/completions"

def edit_images():
    """
    图片编辑主函数
    支持多图片合成和编辑
    """
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 请求数据 - 多图片合成示例
    data = {
        "model": "gemini-2.5-flash-image",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Combine 2 images and add a Corgi dog image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://github.com/dianping/cat/raw/master/cat-home/src/main/webapp/images/logo/cat_logo03.png"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://raw.githubusercontent.com/leonindy/camel/master/camel-admin/src/main/webapp/assets/images/camel_logo_blue.png"
                        }
                    }
                ]
            }
        ]
    }
    
    print("🚀 正在请求图片编辑API...")
    print(f"📝 编辑指令: {data['messages'][0]['content'][0]['text']}")
    print(f"🖼️  输入图片数量: {len([c for c in data['messages'][0]['content'] if c['type'] == 'image_url'])}")
    
    try:
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        print("✅ API请求成功，正在处理响应...")
        
        # 解析响应
        result = response.json()
        
        # 提取内容
        content = result['choices'][0]['message']['content']
        print(f"📄 收到内容长度: {len(content)} 字符")
        print(f"📄 内容预览: {content[:200]}...")
        
        # 查找Base64图片数据
        base64_data = None
        
        # 方法1: 查找标准格式 data:image/type;base64,data
        base64_match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
        
        if base64_match:
            base64_data = base64_match.group(1)
            print("✅ 找到标准格式的Base64数据")
        else:
            # 方法2: 查找纯Base64数据（长字符串）
            base64_match = re.search(r'([A-Za-z0-9+/=]{100,})', content)
            if base64_match:
                base64_data = base64_match.group(1)
                print("✅ 找到纯Base64数据")
            else:
                print("❌ 错误: 无法找到Base64图片数据")
                print("📄 完整响应内容:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return False
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"edited_image_{timestamp}.png"
        
        print("💾 正在保存编辑后的图片...")
        
        # 解码并保存图片
        try:
            image_data = base64.b64decode(base64_data)
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            print(f"🎉 图片编辑完成！")
            print(f"📁 文件保存为: {filename}")
            print(f"📊 文件大小: {len(image_data):,} 字节")
            return True
            
        except Exception as e:
            print(f"❌ 错误: 保存图片时出现问题: {e}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 错误: API请求失败: {e}")
        return False
    except KeyError as e:
        print(f"❌ 错误: 响应格式不正确，缺少字段: {e}")
        if 'response' in locals():
            print("📄 完整响应内容:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return False
    except Exception as e:
        print(f"❌ 错误: 未知错误: {e}")
        return False

def custom_edit_example():
    """
    自定义编辑示例
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 自定义编辑任务
    data = {
        "model": "gemini-2.5-flash-image",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please remove the background and make it transparent, then add a sunset background"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "your_image_url_here"  # 替换为你的图片URL
                        }
                    }
                ]
            }
        ]
    }
    
    print("🎨 执行自定义编辑任务...")
    # 调用编辑逻辑...

def main():
    """
    主函数 - 演示不同的编辑功能
    """
    print("=" * 60)
    print("Nano Banana 图片编辑器 - Python版本")
    print("=" * 60)
    print(f"🕐 开始时间: {datetime.now()}")
    
    # 检查API Key
    if API_KEY == "sk-":
        print("⚠️  请先设置正确的API密钥")
        return
    
    print("\n🔧 可用的编辑功能:")
    print("1. 多图片合成")
    print("2. 背景替换") 
    print("3. 元素添加")
    print("4. 风格转换")
    
    print("\n🚀 执行多图片合成示例...")
    success = edit_images()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 编辑任务执行成功！")
        print("✅ 图片已保存到本地")
    else:
        print("❌ 编辑任务执行失败！")
        print("💡 请检查API密钥和网络连接")
    
    print(f"🕐 结束时间: {datetime.now()}")
    print("=" * 60)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


```

编辑示例场景
------

### Nano Banana Pro 高级场景

#### 1. 4K 高清商业海报编辑

```
import requests
import base64

API_KEY = "sk-your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 读取图片
with open('product.png', 'rb') as f:
    image_base64 = base64.b64encode(f.read()).decode('utf-8')

# 4K 高清编辑 - 适合商业印刷
payload = {
    "contents": [{
        "parts": [
            {"text": "将这个产品照片转换为专业商业海报，添加高端质感和完美照明"},
            {"inline_data": {"mime_type": "image/png", "data": image_base64}}
        ]
    }],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": "3:4",
            "imageSize": "4K"  # 输出 3584×4800 像素
        }
    }
}

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
result = response.json()

# 保存 4K 图片
image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
with open("poster_4k.png", 'wb') as f:
    f.write(base64.b64decode(image_data))


```

#### 2. 局部精细编辑

```
# 调整摄像机角度和焦点
{
  "type": "text",
  "text": "Change camera angle to bird's eye view and adjust focus to the foreground"
}


```

#### 3. 场景照明控制

```
# 日夜转换和背景虚化
{
  "type": "text",
  "text": "Transform this daytime photo to nighttime with bokeh effect in the background"
}


```

#### 4. 专业色彩分级

```
# 应用电影级色彩效果
{
  "type": "text",
  "text": "Apply cinematic color grading with warm tones and enhanced contrast"
}


```

### 通用编辑场景

#### 5. 多图片合成（支持 2K/4K）

```
import requests
import base64

API_KEY = "sk-your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 读取多张图片
def read_image(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

# 多图片合成 - 团队照片合成
payload = {
    "contents": [{
        "parts": [
            {"text": "Create a professional office team photo with these people, modern office background"},
            {"inline_data": {"mime_type": "image/png", "data": read_image('person1.png')}},
            {"inline_data": {"mime_type": "image/png", "data": read_image('person2.png')}},
            {"inline_data": {"mime_type": "image/png", "data": read_image('person3.png')}},
            {"inline_data": {"mime_type": "image/png", "data": read_image('person4.png')}}
        ]
    }],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": "16:9",
            "imageSize": "2K"  # 2K 足够高清，速度更快
        }
    }
}

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
result = response.json()

# 保存结果
image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
with open("team_photo.png", 'wb') as f:
    f.write(base64.b64decode(image_data))


```

#### 6. OpenAI 格式多图合成

```
# 将两个logo合成，并添加新元素（OpenAI 兼容格式）
{
  "type": "text",
  "text": "Combine these two logos and add a cute animal"
}


```

#### 7. 背景替换

```
# 替换图片背景
{
  "type": "text",
  "text": "Remove the background and add a sunset landscape"
}


```

#### 8. 风格转换

```
# 改变图片风格
{
  "type": "text",
  "text": "Convert this photo to anime/cartoon style"
}


```

#### 9. 元素修改

```
# 添加或删除元素
{
  "type": "text",
  "text": "Add sunglasses to the person and change hair color to blue"
}


```

使用建议
----

### 选择合适的调用方式

### 迁移指南

如果您当前使用预览版模型或希望迁移到谷歌原生格式，请参考：

最佳实践
----

### 编辑指令优化

### 图片输入建议

*   **格式支持**：PNG、JPEG、GIF 等主流格式
*   **分辨率**：建议不超过 4096x4096
*   **文件大小**：单张图片建议不超过 10MB
*   **URL 要求**：确保图片 URL 可公开访问

### 编辑质量优化

1.  **高质量输入**：使用清晰、高分辨率的原图
2.  **合理指令**：避免过于复杂或矛盾的编辑要求
3.  **多次迭代**：对复杂编辑可以分多步进行
4.  **参考示例**：参考成功的编辑案例

### 分辨率选择指南

错误处理
----

### 常见错误及解决方案

定价信息
----

### Nano Banana Pro (`gemini-3-pro-image-preview`)

按次计费，所有分辨率统一价格：

<table><thead><tr><th>分辨率</th><th>API 易价格</th><th>官方价格</th><th>等于官网的</th><th>充值加赠价格</th><th>生成时间</th><th>推荐场景</th></tr></thead><tbody><tr><td data-numeric="true"><strong>1K-2K</strong></td><td data-numeric="true">$0.050 / 张</td><td data-numeric="true">$0.134 / 张</td><td data-numeric="true">30%</td><td>￥0.29 / 张</td><td data-numeric="true">20-25 秒</td><td>高清网页 / 社交媒体</td></tr><tr><td data-numeric="true"><strong>4K</strong></td><td data-numeric="true">$0.050 / 张</td><td data-numeric="true">$0.24 / 张</td><td data-numeric="true">17%</td><td>￥0.29 / 张</td><td data-numeric="true">30-40 秒</td><td>专业印刷 / 商业设计</td></tr></tbody></table>

**特性优势**：

*   🎯 支持 4K 超高清输出
*   📐 局部精细编辑能力（摄像机、焦点、色彩）
*   🌓 场景照明控制
*   📝 业界最佳文本渲染

### 前代版本 (`gemini-2.5-flash-image`)

*   **API 易价格**：$0.025 / 张（仅 1K 分辨率）
*   **官方价格**：约 $0.039 / 张
*   **等于官网的**：52%，节省 48%
*   **充值加赠价格**：约 ￥0.15 / 张
*   **生成时间**：10-15 秒
*   **推荐场景**：快速编辑、常规图像处理

### 成本对比计算器

高级功能
----

### 批量编辑

```
def batch_edit_images(image_urls, edit_instruction):
    """批量编辑多张图片"""
    results = []
    for i, url in enumerate(image_urls):
        data = {
            "model": "gemini-2.5-flash-image",
            "messages": [{
                "role": "user", 
                "content": [
                    {"type": "text", "text": edit_instruction},
                    {"type": "image_url", "image_url": {"url": url}}
                ]
            }]
        }
        # 执行编辑...
        results.append(result)
    return results


```

### 编辑历史记录

```
def save_edit_history(original_url, instruction, result_path):
    """保存编辑历史记录"""
    history = {
        "timestamp": datetime.now().isoformat(),
        "original_image": original_url,
        "edit_instruction": instruction,
        "result_path": result_path
    }
    # 保存到文件或数据库...


```

相关文档
----

*   [Nano Banana 图片生成](https://docs.apiyi.com/api-capabilities/nano-banana-image)
*   [其他图片编辑功能](https://docs.apiyi.com/api-capabilities/image-edit)
*   [图片生成对比测试](https://imagen.apiyi.com/)
*   [API 使用手册](https://docs.apiyi.com/api-manual)