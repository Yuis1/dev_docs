#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gemini 图片生成工具 - Python版本
使用 Google Gemini 2.5 Flash Image 模型生成图片，支持自定义纵横比

支持的纵横比：
- 横向: 21:9, 16:9, 4:3, 3:2
- 正方形: 1:1
- 纵向: 9:16, 3:4, 2:3
- 其他: 5:4, 4:5
"""

import requests
import base64
import os
import datetime
from typing import Optional, Tuple

class GeminiImageGenerator:
    """Gemini 图片生成器"""

    # 支持的纵横比
    SUPPORTED_ASPECT_RATIOS = [
        "21:9", "16:9", "4:3", "3:2", "1:1",
        "9:16", "3:4", "2:3", "5:4", "4:5"
    ]

    def __init__(self, api_key: str, api_url: str = "https://api.apiyi.com/v1beta/models/gemini-2.5-flash-image:generateContent"):
        """
        初始化图片生成器

        参数:
            api_key: API密钥
            api_url: API地址（默认使用 Google 原生 Gemini API）
        """
        self.api_key = api_key
        self.api_url = api_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def generate_image(self, prompt: str, aspect_ratio: Optional[str] = "1:1",
                      output_dir: str = ".") -> Tuple[bool, str]:
        """
        生成图片并保存到本地

        参数:
            prompt: 图片描述（提示词）
            aspect_ratio: 纵横比，如 "16:9", "1:1" 等（默认 1:1）
            output_dir: 保存目录（默认当前目录）

        返回:
            (是否成功, 结果消息)
        """
        print(f"🚀 开始生成图片...")
        print(f"📝 提示词: {prompt}")
        print(f"📐 纵横比: {aspect_ratio}")

        # 验证纵横比
        if aspect_ratio and aspect_ratio not in self.SUPPORTED_ASPECT_RATIOS:
            return False, f"不支持的纵横比 {aspect_ratio}。支持: {', '.join(self.SUPPORTED_ASPECT_RATIOS)}"

        # 生成文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"gemini_{timestamp}.png")

        try:
            # 构建请求数据
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }

            # 添加纵横比配置
            if aspect_ratio:
                payload["generationConfig"] = {
                    "responseModalities": ["IMAGE"],
                    "imageConfig": {
                        "aspectRatio": aspect_ratio
                    }
                }

            print("📡 发送请求到 Gemini API...")

            # 发送请求
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120
            )

            if response.status_code != 200:
                return False, f"API 请求失败，状态码: {response.status_code}"

            # 解析响应
            result = response.json()

            # 提取图片数据
            if "candidates" not in result or len(result["candidates"]) == 0:
                return False, "未找到图片数据"

            candidate = result["candidates"][0]
            if "content" not in candidate or "parts" not in candidate["content"]:
                return False, "响应格式错误"

            parts = candidate["content"]["parts"]
            image_data = None

            for part in parts:
                if "inlineData" in part and "data" in part["inlineData"]:
                    image_data = part["inlineData"]["data"]
                    break

            if not image_data:
                return False, "未找到图片数据"

            # 解码并保存图片
            print("💾 正在保存图片...")
            decoded_data = base64.b64decode(image_data)

            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)

            with open(output_file, 'wb') as f:
                f.write(decoded_data)

            file_size = len(decoded_data) / 1024  # KB
            print(f"✅ 图片已保存: {output_file}")
            print(f"📊 文件大小: {file_size:.2f} KB")

            return True, f"成功保存图片: {output_file}"

        except requests.exceptions.Timeout:
            return False, "请求超时（120秒）"
        except requests.exceptions.ConnectionError:
            return False, "网络连接错误"
        except Exception as e:
            return False, f"错误: {str(e)}"


def main():
    """主函数 - 使用示例"""

    # ========== 配置区 ==========
    # 1. 设置你的 API 密钥
    API_KEY = "sk-"

    # 2. 输入图片描述（提示词）
    PROMPT = "a handsome dog under the tree"

    # 3. 选择纵横比（可选）
    # 支持: 21:9, 16:9, 4:3, 3:2, 1:1, 9:16, 3:4, 2:3, 5:4, 4:5
    ASPECT_RATIO = "16:9"  # 宽屏
    # ASPECT_RATIO = "1:1"   # 正方形
    # ASPECT_RATIO = "9:16"  # 竖屏

    # 4. 设置保存目录（可选）
    OUTPUT_DIR = "."  # 当前目录
    # ============================

    print("="*60)
    print("Gemini 图片生成工具")
    print("="*60)
    print(f"⏰ 开始时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    # 创建生成器并生成图片
    generator = GeminiImageGenerator(API_KEY)
    success, message = generator.generate_image(
        prompt=PROMPT,
        aspect_ratio=ASPECT_RATIO,
        output_dir=OUTPUT_DIR
    )

    # 显示结果
    print("\n" + "="*60)
    if success:
        print("🎉 生成成功！")
        print(f"✅ {message}")
    else:
        print("❌ 生成失败")
        print(f"💥 {message}")
        print("\n建议检查:")
        print("  1. API 密钥是否正确")
        print("  2. 网络连接是否正常")
        print("  3. 提示词是否合理")

    print(f"⏰ 结束时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == "__main__":
    main()
