> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/nano-banana-image)

> 谷歌最新、最强的图像生成模型 Gemini 2.5 Flash Image，代号 Nano Banana。支持自定义分辨率、10 种宽高比，10 秒快速生成，官网 7 折优惠。

概述
--

**Nano Banana**（代号）是谷歌图像生成模型系列，目前有以下版本可用：

### 最新版本（推荐）

*   **Nano Banana Pro**：`gemini-3-pro-image-preview`（🔥 2025 年 11 月 20 日上线）
    *   基于 Gemini 3 Pro，推理能力更强
    *   支持 4K 高清图像生成（1K、2K、4K）
    *   业界最佳文本渲染能力
    *   支持高级局部编辑功能

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

<table><thead><tr><th>特性</th><th>谷歌原生格式</th><th>OpenAI 兼容模式</th></tr></thead><tbody><tr><td><strong>端点 URL</strong></td><td><code>/v1beta/models/gemini-2.5-flash-image:generateContent</code></td><td><code>/v1/chat/completions</code></td></tr><tr><td><strong>输出尺寸</strong></td><td>支持 10 种宽高比自定义</td><td>默认 1:1</td></tr><tr><td><strong>调用格式</strong></td><td>谷歌官方格式</td><td>OpenAI 格式</td></tr><tr><td><strong>兼容性</strong></td><td>谷歌原生 API</td><td>gpt-4o-image、sora_image</td></tr><tr><td><strong>适用场景</strong></td><td>需要精确控制输出尺寸</td><td>快速集成，兼容现有代码</td></tr></tbody></table>

### OpenAI 兼容模式端点说明

#### 正确端点 ✅

```
POST /v1/chat/completions


```

#### 错误端点 ❌

```
POST /v1/images/generations  # 不支持此端点


```

兼容性说明
-----

如果你之前使用过以下模型，可以直接替换模型名称：

### 升级到最新版本

*   任何旧版本 → `gemini-3-pro-image-preview`（🔥 推荐，Nano Banana Pro）
    *   支持 4K 高清出图
    *   文本渲染能力最强
    *   局部编辑功能

### 使用稳定版本

*   `gpt-4o-image` → `gemini-2.5-flash-image`
*   `sora_image` → `gemini-2.5-flash-image`
*   旧版 Nano Banana → `gemini-2.5-flash-image`

其他参数保持不变，即可无缝切换使用。

快速开始
----

### 方式一：最简单示例（基础生成）

```
import requests
import base64

API_KEY = "sk-your-api-key"
PROMPT = "一只可爱的小猫坐在花园里，油画风格，高清，细节丰富"

# 发送请求
response = requests.post(
    "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent",
    headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
    json={
        "contents": [{"parts": [{"text": PROMPT}]}],
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

### 方式二：简化版（配置式 + 完整功能）

**特点**：清晰的配置区域、完善的错误处理、智能超时控制、自动文件命名

#### 核心配置示例

```
# ============================================================================
# 配置区域 - 请在此处修改您的配置
# ============================================================================

# 1. API Key（必填）
API_KEY = "sk-your-api-key"

# 2. 图片描述
PROMPT = "一只可爱的小猫咪坐在花园里，油画风格，高清，细节丰富"

# 3. 图片参数
ASPECT_RATIO = "16:9"  # 宽高比：1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5
RESOLUTION = "2K"      # 分辨率：1K, 2K, 4K （推荐 2K）

# 4. 输出文件名（自动添加时间戳）
OUTPUT_FILE = f"NanoBananaPro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

# ============================================================================
# 超时配置（根据分辨率自动调整）
# ============================================================================
TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}  # 单位：秒


```

#### 完整生成示例

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import base64
import time
from datetime import datetime

# ============================================================================
# 配置区域
# ============================================================================
API_KEY = "sk-your-api-key"
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

PROMPT = "一只可爱的小猫坐在花园里，油画风格，高清，细节丰富"
ASPECT_RATIO = "16:9"  # 可选: 1:1, 16:9, 9:16, 4:3, 3:4, 3:2, 2:3, 21:9, 5:4, 4:5
RESOLUTION = "2K"      # 可选: 1K, 2K, 4K
OUTPUT_FILE = f"NanoBananaPro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

# 超时配置
TIMEOUT_MAP = {"1K": 180, "2K": 300, "4K": 360}

def generate_image():
    """生成图片"""

    print(f"\n{'='*60}")
    print(f"🎨 开始生成图片")
    print(f"{'='*60}")
    print(f"📝 提示词: {PROMPT}")
    print(f"📐 宽高比: {ASPECT_RATIO}")
    print(f"🔍 分辨率: {RESOLUTION}")

    # 构建请求参数
    payload = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": ASPECT_RATIO,
                "imageSize": RESOLUTION
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # 发送请求
    print(f"\n⏳ 正在生成，预计 {TIMEOUT_MAP[RESOLUTION] // 60} 分钟...")
    start_time = time.time()

    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=TIMEOUT_MAP[RESOLUTION]
        )

        elapsed = time.time() - start_time
        print(f"⏱️  实际用时: {elapsed:.1f} 秒")

        if response.status_code != 200:
            print(f"\n❌ API 错误 ({response.status_code}): {response.text}")
            return False

        # 解析响应
        data = response.json()
        image_base64 = data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

        # 保存图片
        image_bytes = base64.b64decode(image_base64)
        with open(OUTPUT_FILE, "wb") as f:
            f.write(image_bytes)

        print(f"\n✅ 生成成功！")
        print(f"📁 已保存至: {OUTPUT_FILE}")
        print(f"📦 文件大小: {len(image_bytes) / 1024:.1f} KB")
        return True

    except requests.Timeout:
        print(f"\n❌ 请求超时（超过 {TIMEOUT_MAP[RESOLUTION]} 秒）")
        print(f"💡 建议：尝试使用更低的分辨率（1K 或 2K）")
        return False
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Gemini 3 Pro Image - 文本生成图片（简化版）")
    print("="*60)

    generate_image()

    print(f"\n{'='*60}")
    print("程序结束")
    print("="*60 + "\n")


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
          "text": "图片描述提示词"
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

#### Python 完整示例

参考完整的 Python 实现：[gemini-image-generate-python.py](https://xinqikeji.feishu.cn/wiki/W4vEwdiCPi3VfTkrL5hcVlDxnQf)

```
#!/usr/bin/env python3
import requests
import base64
import os
from datetime import datetime

class GeminiImageGenerator:
    """Gemini 图片生成器（谷歌原生格式）"""

    SUPPORTED_ASPECT_RATIOS = [
        "21:9", "16:9", "4:3", "3:2", "1:1",
        "9:16", "3:4", "2:3", "5:4", "4:5"
    ]

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def generate_image(self, prompt: str, aspect_ratio: str = "1:1", output_dir: str = "."):
        """生成图片并保存"""
        print(f"🚀 开始生成图片...")
        print(f"📝 提示词: {prompt}")
        print(f"📐 纵横比: {aspect_ratio}")

        # 验证纵横比
        if aspect_ratio not in self.SUPPORTED_ASPECT_RATIOS:
            return False, f"不支持的纵横比 {aspect_ratio}"

        # 构建请求
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {"aspectRatio": aspect_ratio}
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=120)

            if response.status_code != 200:
                return False, f"API 请求失败，状态码: {response.status_code}"

            result = response.json()

            # 提取图片数据
            image_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

            # 保存图片
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(output_dir, f"gemini_{timestamp}.png")

            decoded_data = base64.b64decode(image_data)
            with open(output_file, 'wb') as f:
                f.write(decoded_data)

            print(f"✅ 图片已保存: {output_file}")
            return True, f"成功保存图片: {output_file}"

        except Exception as e:
            return False, f"错误: {str(e)}"


{/* 使用示例 */}
if __name__ == "__main__":
    API_KEY = "sk-your-api-key"
    PROMPT = "a handsome dog under the tree"
    ASPECT_RATIO = "16:9"  # 可选: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5

    generator = GeminiImageGenerator(API_KEY)
    success, message = generator.generate_image(PROMPT, ASPECT_RATIO)

    if success:
        print(f"🎉 生成成功！{message}")
    else:
        print(f"❌ 生成失败：{message}")


```

### 方式二：OpenAI 兼容模式

**兼容现有 OpenAI 格式代码**，适合快速集成。默认生成 1:1 比例图片。

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
      "content": "图片描述提示词"
    }
  ]
}


```

#### Python 完整示例

以下是完整的 Python 示例代码，支持自动保存 base64 图片到本地：

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini 图片生成 - Python版本
支持非流式输出和自动保存base64图片到本地
"""

import requests
import json
import base64
import re
import os
import datetime
from typing import Optional, Tuple

class GeminiImageGenerator:
    def __init__(self, api_key: str, api_url: str = "https://api.apiyi.com/v1/chat/completions"):
        """
        初始化Gemini图片生成器
        
        Args:
            api_key: API密钥
            api_url: API地址
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_image(self, prompt: str, model: str = "gemini-2.5-flash-image",
                      output_dir: str = ".") -> Tuple[bool, str]:
        """
        生成图片并保存到本地
        
        Args:
            prompt: 图片描述提示词
            model: 使用的模型
            output_dir: 输出目录
            
        Returns:
            Tuple[是否成功, 结果消息]
        """
        print("🚀 开始生成图片...")
        print(f"提示词: {prompt}")
        print(f"模型: {model}")
        
        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"gemini_generated_{timestamp}.png")
        
        try:
            # 准备请求数据
            payload = {
                "model": model,
                "stream": False,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            print("📡 发送API请求...")
            
            # 发送非流式请求
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=300
            )
            
            if response.status_code != 200:
                error_msg = f"API请求失败，状态码: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f", 错误详情: {error_detail}"
                except:
                    error_msg += f", 响应内容: {response.text[:500]}"
                return False, error_msg
            
            print("✅ API请求成功，正在解析响应...")
            
            # 解析非流式JSON响应
            try:
                result = response.json()
                print("✅ 成功解析JSON响应")
            except json.JSONDecodeError as e:
                return False, f"JSON解析失败: {str(e)}"
            
            # 提取消息内容
            full_content = ""
            if "choices" in result and len(result["choices"]) > 0:
                choice = result["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    full_content = choice["message"]["content"]
            
            if not full_content:
                return False, "未找到消息内容"
            
            print(f"📝 获取到消息内容，长度: {len(full_content)} 字符")
            print("🔍 正在解析图片数据...")
            
            # 提取并保存图片（支持base64和URL两种方式）
            success, message = self._extract_and_save_images(full_content, output_file)
            
            if success:
                return True, message
            else:
                return False, f"图片保存失败: {message}"
                
        except requests.exceptions.Timeout:
            return False, "请求超时（300秒）"
        except requests.exceptions.ConnectionError as e:
            return False, f"连接错误: {str(e)}"
        except Exception as e:
            return False, f"未知错误: {str(e)}"
    
    def _extract_and_save_images(self, content: str, base_output_file: str) -> Tuple[bool, str]:
        """
        高效提取并保存base64图片数据
        
        Args:
            content: 包含图片数据的内容
            base_output_file: 基础输出文件路径
            
        Returns:
            Tuple[是否成功, 结果消息]
        """
        try:
            print(f"📄 内容预览（前200字符）: {content[:200]}")
            
            # 使用精确的正则表达式一次性提取base64图片数据
            base64_pattern = r'data:image/([^;]+);base64,([A-Za-z0-9+/=]+)'
            match = re.search(base64_pattern, content)
            
            if not match:
                print('⚠️  未找到base64图片数据')
                return False, "响应中未包含base64图片数据"
            
            image_format = match.group(1)  # png, jpg, etc.
            b64_data = match.group(2)
            
            print(f'🎨 图像格式: {image_format}')
            print(f'📏 Base64数据长度: {len(b64_data)} 字符')
            
            # 解码并保存图片
            image_data = base64.b64decode(b64_data)
            
            if len(image_data) < 100:
                return False, "解码后的图片数据太小，可能无效"
            
            # 根据检测到的格式设置文件扩展名
            output_file = base_output_file.replace('.png', f'.{image_format}')
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
            
            with open(output_file, 'wb') as f:
                f.write(image_data)
            
            print(f'🖼️  图片保存成功: {output_file}')
            print(f'📊 文件大小: {len(image_data)} 字节')
            
            return True, f"图片保存成功: {output_file}"
                
        except Exception as e:
            return False, f"处理图片时发生错误: {str(e)}"

def main():
    """
    主函数
    """
    # 配置参数
    API_KEY = "sk-"  # 请替换为你的实际API密钥
    PROMPT = "a beautiful cat under the tree"
    
    print("="*60)
    print("Gemini 图片生成器 - Python版本")
    print("="*60)
    print(f"开始时间: {datetime.datetime.now()}")
    
    # 创建生成器实例
    generator = GeminiImageGenerator(API_KEY)
    
    # 生成图片
    success, message = generator.generate_image(PROMPT)
    
    print("\n" + "="*60)
    if success:
        print("🎉 执行成功！")
        print(f"✅ {message}")
    else:
        print("❌ 执行失败！")
        print(f"💥 {message}")
    
    print(f"结束时间: {datetime.datetime.now()}")
    print("="*60)

if __name__ == "__main__":
    main()


```

使用步骤
----

1.  **替换 API Key**：将代码中的 `API_KEY` 替换为你的实际 API 密钥
2.  **修改提示词**：根据需要修改 `PROMPT` 变量
3.  **运行脚本**：执行 Python 脚本，图片将自动保存到本地

使用建议
----

### 选择合适的调用方式

### 迁移指南

如果您当前使用预览版模型或希望迁移到谷歌原生格式，请参考：

价格对比
----

<table><thead><tr><th>模型</th><th>定价</th><th>优势</th></tr></thead><tbody><tr><td><strong>Nano Banana Pro</strong> (4K)</td><td>$0.050 / 张 (充值加赠约￥0.29)</td><td>🔥 支持 4K 高清，官网 17% 价格</td></tr><tr><td><strong>Nano Banana Pro</strong> (1K-2K)</td><td>$0.050 / 张 (充值加赠约￥0.29)</td><td>🔥 高清出图，官网 30% 价格</td></tr><tr><td><strong>Nano Banana</strong></td><td>$0.025 / 张 (充值加赠约￥0.15)</td><td>⭐ 快速生成，官网 52% 价格</td></tr><tr><td>gpt-image-1</td><td>更高</td><td data-numeric="true">-</td></tr><tr><td>flux-kontext-pro</td><td data-numeric="true">$0.035 / 张</td><td>持平</td></tr><tr><td>sora_image</td><td>更低</td><td>逆向模型，稳定性一般</td></tr></tbody></table>

特性对比
----

### 速度对比

*   **Nano Banana**：平均 10 秒
*   **OpenAI 系列**：15-30 秒
*   **其他模型**：因模型而异

### 兼容性

*   ✅ 完全兼容 `gpt-4o-image` 调用方式
*   ✅ 完全兼容 `sora_image` 调用方式
*   ✅ 支持对话补全端点
*   ❌ 不支持传统图像生成端点

API 错误处理指南
----------

Nano Banana Pro 对内容安全有严格控制，可能会在多个层级拒绝不合规的请求。了解错误类型和处理方法，能够帮助您更好地诊断问题并提供友好的用户体验。

### 核心错误判断指标

### 常见错误场景

### 错误处理最佳实践

常见问题
----

相关文档
----

*   [详细使用指南](https://xinqikeji.feishu.cn/wiki/W4vEwdiCPi3VfTkrL5hcVlDxnQf)
*   [图像生成对比测试](https://imagen.apiyi.com/)
*   [Nano Banana 图片编辑](https://docs.apiyi.com/api-capabilities/nano-banana-image-edit)
*   [其他图像生成模型](https://docs.apiyi.com/api-capabilities/gpt-image-1)
*   [API 使用手册](https://docs.apiyi.com/api-manual)