#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 3 Pro Image - 图片编辑示例（支持多图）

功能：上传一张或多张图片 + 文字描述，对图片进行编辑修改
模型：gemini-3-pro-image-preview (Nano Banana Pro)
价格：约 $0.05/张
"""

import requests
import base64
import time
from pathlib import Path
from datetime import datetime

# ============================================================================
# 配置区域 - 请在此处修改您的配置
# ============================================================================

# 1. API Key（必填）- 从 https://api.apiyi.com/token 获取
API_KEY = "sk-填在这里"

# 2. API 端点（无需修改）
API_URL = "https://api.apiyi.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

# 3. 编辑配置（可根据需求修改）
CONFIG = {
    "input_images": [               # 输入图片路径（支持一张或多张）
        "cat.png",                  # 第一张图片
        # "image2.png",             # 可以添加更多图片
        # "image3.png",
    ],
    "edit_prompt": "将这张图片变成水彩画风格，保持主体不变，柔和的色调",  # 编辑指令
    "aspect_ratio": "9:16",          # 宽高比（建议与原图一致）
    "resolution": "2K",             # 分辨率：1K, 2K, 4K
    "output_file": f"NanoBananaPro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"  # 输出文件名（自动添加时间戳）
}

# 4. 超时时间（秒）
TIMEOUT = {
    "1K": 180,  # 3 分钟
    "2K": 300,  # 5 分钟
    "4K": 360,  # 6 分钟
}

# ============================================================================
# 核心编辑函数
# ============================================================================

def edit_image(input_image_paths, edit_prompt, aspect_ratio="1:1", resolution="2K"):
    """
    编辑图片的核心函数（支持多图）
    
    参数说明：
        input_image_paths: 输入图片的文件路径（可以是字符串或列表）
        edit_prompt: 编辑指令，例如 "将背景变成蓝色"
        aspect_ratio: 输出图片的宽高比
        resolution: 输出图片的分辨率
    
    返回：
        成功：返回 {"success": True, "image_data": "base64数据"}
        失败：返回 {"success": False, "error": "错误信息"}
    """
    
    # 支持单图和多图
    if isinstance(input_image_paths, str):
        input_image_paths = [input_image_paths]
    
    print(f"\n{'='*60}")
    print(f"✏️  开始编辑图片")
    print(f"{'='*60}")
    print(f"📁 输入图片: {len(input_image_paths)} 张")
    for i, img in enumerate(input_image_paths, 1):
        print(f"   {i}. {img}")
    print(f"📝 编辑指令: {edit_prompt}")
    print(f"📐 输出宽高比: {aspect_ratio}")
    print(f"🔍 输出分辨率: {resolution}")
    
    # ========================================
    # 步骤 1: 读取并编码所有输入图片
    # ========================================
    print(f"\n📤 正在读取图片...")
    
    parts = []  # 存储所有图片和文字
    
    try:
        for input_image_path in input_image_paths:
            if not Path(input_image_path).exists():
                return {
                    "success": False,
                    "error": f"图片文件不存在: {input_image_path}"
                }
            
            with open(input_image_path, "rb") as f:
                image_bytes = f.read()
            
            # 将图片转换为 base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            
            # 检测图片格式
            if input_image_path.lower().endswith('.png'):
                mime_type = "image/png"
            elif input_image_path.lower().endswith(('.jpg', '.jpeg')):
                mime_type = "image/jpeg"
            elif input_image_path.lower().endswith('.webp'):
                mime_type = "image/webp"
            else:
                mime_type = "image/png"  # 默认
            
            # 添加到 parts
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": image_base64
                }
            })
            
            print(f"✅ {input_image_path} ({len(image_bytes) / 1024:.1f} KB, {mime_type})")
        
    except Exception as e:
        return {
            "success": False,
            "error": f"读取图片失败: {e}"
        }
    
    # ========================================
    # 步骤 2: 构建请求参数
    # ========================================
    # 添加文字指令到 parts 的最后
    parts.append({"text": edit_prompt})
    
    payload = {
        # 内容部分：包含所有图片 + 编辑指令
        "contents": [
            {
                "parts": parts  # 所有图片 + 文字指令
            }
        ],
        
        # 生成配置部分
        "generationConfig": {
            "responseModalities": ["IMAGE"],  # 指定返回图片
            
            # 图片配置
            "imageConfig": {
                "aspectRatio": aspect_ratio,  # 输出宽高比
                "image_size": resolution       # 输出分辨率
            }
        }
    }
    
    # ========================================
    # 步骤 3: 设置请求头
    # ========================================
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # ========================================
    # 步骤 4: 发送 API 请求
    # ========================================
    print(f"\n🚀 正在请求 API...")
    print(f"⏱️  预计时间: {TIMEOUT[resolution] // 60} 分钟")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=TIMEOUT[resolution]
        )
        
        elapsed = time.time() - start_time
        print(f"✅ 请求完成，耗时 {elapsed:.1f} 秒")
        
        # ========================================
        # 步骤 5: 解析响应数据
        # ========================================
        if response.status_code == 200:
            data = response.json()
            
            try:
                parts = data["candidates"][0]["content"]["parts"]
                
                # 遍历 parts 查找图片数据
                for part in parts:
                    # 尝试驼峰命名（标准格式）
                    if "inlineData" in part:
                        output_image_base64 = part["inlineData"]["data"]
                        return {
                            "success": True,
                            "image_data": output_image_base64,
                            "elapsed_time": elapsed
                        }
                    # 兼容下划线命名
                    elif "inline_data" in part:
                        output_image_base64 = part["inline_data"]["data"]
                        return {
                            "success": True,
                            "image_data": output_image_base64,
                            "elapsed_time": elapsed
                        }
                
                # 如果没找到图片数据
                return {
                    "success": False,
                    "error": "响应中未找到图片数据",
                    "response": data
                }
                
            except (KeyError, IndexError) as e:
                return {
                    "success": False,
                    "error": f"响应数据格式错误: {e}",
                    "response": data
                }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}"
            }
    
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": f"请求超时（超过 {TIMEOUT[resolution]} 秒）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"请求失败: {str(e)}"
        }


def save_image(image_base64, filename):
    """保存 base64 图片到文件"""
    try:
        image_bytes = base64.b64decode(image_base64)
        with open(filename, "wb") as f:
            f.write(image_bytes)
        print(f"💾 图片已保存: {filename}")
        return True
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return False


# ============================================================================
# 示例 1: 单张图片编辑（默认）
# ============================================================================

def example_single_edit():
    """编辑图片 - 使用配置区的设置（支持单图或多图）"""
    print("\n" + "="*60)
    print("✏️  示例 1: 编辑图片")
    print("="*60)
    
    result = edit_image(
        input_image_paths=CONFIG["input_images"],
        edit_prompt=CONFIG["edit_prompt"],
        aspect_ratio=CONFIG["aspect_ratio"],
        resolution=CONFIG["resolution"]
    )
    
    if result["success"]:
        print(f"\n✅ 编辑成功！")
        save_image(result["image_data"], CONFIG["output_file"])
    else:
        print(f"\n❌ 编辑失败: {result['error']}")
        # 如果有响应数据，打印出来用于调试
        if "response" in result:
            print(f"\n🔍 调试信息（响应结构）:")
            import json
            print(json.dumps(result["response"], indent=2, ensure_ascii=False)[:500] + "...")


# ============================================================================
# 示例 2: 批量编辑（可选）
# ============================================================================

def example_batch_edit():
    """批量编辑多张图片 - 演示如何对多张图片应用不同编辑"""
    print("\n" + "="*60)
    print("📚 示例 2: 批量编辑图片")
    print("="*60)
    
    # 定义批量编辑任务
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    batch_tasks = [
        {
            "input_images": ["input.png"],
            "edit_prompt": "将这张图片转换为黑白风格，提高对比度",
            "aspect_ratio": "1:1",
            "resolution": "2K",
            "output_file": f"NanoBananaPro_edit_1_bw_{timestamp}.png"
        },
        {
            "input_images": ["input.png"],
            "edit_prompt": "添加温暖的日落光线效果，橙红色调",
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_file": f"NanoBananaPro_edit_2_sunset_{timestamp}.png"
        },
        {
            "input_images": ["input.png"],
            "edit_prompt": "将背景模糊化，突出前景主体",
            "aspect_ratio": "4:3",
            "resolution": "2K",
            "output_file": f"NanoBananaPro_edit_3_blur_{timestamp}.png"
        }
    ]
    
    print(f"\n📋 共 {len(batch_tasks)} 个编辑任务\n")
    
    success_count = 0
    for i, task in enumerate(batch_tasks, 1):
        print(f"\n--- 任务 {i}/{len(batch_tasks)} ---")
        
        result = edit_image(
            input_image_paths=task["input_images"],
            edit_prompt=task["edit_prompt"],
            aspect_ratio=task["aspect_ratio"],
            resolution=task["resolution"]
        )
        
        if result["success"]:
            save_image(result["image_data"], task["output_file"])
            success_count += 1
        else:
            print(f"❌ 失败: {result['error']}")
        
        # 添加延迟
        if i < len(batch_tasks):
            print("⏳ 等待 2 秒...")
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print(f"✅ 批量编辑完成: {success_count}/{len(batch_tasks)} 成功")
    print(f"{'='*60}")


# ============================================================================
# 主程序
# ============================================================================

def main():
    """主程序入口"""
    print("\n" + "="*60)
    print("Gemini 3 Pro Image - 图片编辑")
    print("="*60)
    
    # 检查 API Key
    if API_KEY == "your-api-key-here":
        print("\n❌ 错误: 请先在代码顶部设置您的 API Key")
        return
    
    # 检查输入图片
    missing_images = [img for img in CONFIG["input_images"] if not Path(img).exists()]
    if missing_images:
        print(f"\n❌ 错误: 以下输入图片不存在:")
        for img in missing_images:
            print(f"   - {img}")
        print(f"   请准备图片并修改 CONFIG['input_images'] 路径")
        return
    
    # 显示当前配置
    print("\n📋 当前配置:")
    print(f"   输入图片: {len(CONFIG['input_images'])} 张")
    for i, img in enumerate(CONFIG['input_images'], 1):
        print(f"      {i}. {img}")
    print(f"   编辑指令: {CONFIG['edit_prompt']}")
    print(f"   输出宽高比: {CONFIG['aspect_ratio']}")
    print(f"   输出分辨率: {CONFIG['resolution']}")
    print(f"   输出文件: {CONFIG['output_file']}")
    
    # 用户选择
    print("\n请选择运行模式:")
    print("  1. 编辑图片（支持单图或多图，默认）")
    print("  2. 批量编辑示例")
    print("  0. 退出")
    
    try:
        choice = input("\n请输入选项 [1]: ").strip() or "1"
        
        if choice == "1":
            example_single_edit()
        elif choice == "2":
            example_batch_edit()
        elif choice == "0":
            print("👋 再见!")
            return
        else:
            print("❌ 无效选项，将运行默认模式")
            example_single_edit()
        
        print("\n" + "="*60)
        print("✅ 程序运行完成")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  程序被用户中断")
    except Exception as e:
        print(f"\n\n❌ 程序出错: {e}")


if __name__ == "__main__":
    main()

