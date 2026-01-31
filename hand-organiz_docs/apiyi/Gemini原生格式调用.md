> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/gemini-native-format)

> 通过 API 易 直接使用 Gemini 官方原生格式进行 API 调用。

API 易 除了支持 OpenAI 兼容格式外，也提供了直接使用 **Gemini 官方原生格式**进行 API 调用的能力。这意味着您可以无缝迁移现有的 Gemini 代码，或直接使用 Gemini 官方 SDK 的原生请求体与 API 易 交互。

优势
--

*   **无缝兼容**：直接使用 Gemini 官方请求和响应结构，无需任何转换。
*   **功能完整**：支持 Gemini 的所有原生特性，包括多模态输入（文本、图片、视频）、Function Calling、代码执行等。
*   **推理能力**：完整支持 Gemini 2.5 系列的思维链推理功能。
*   **便捷迁移**：对于已有 Gemini 项目的用户，可以快速切换到 API 易，享受更灵活的服务。

配置与使用
-----

要使用 Gemini 原生格式，您需要将 API 请求发送到特定的 `/v1beta/` 端点。

### 环境准备

首先，确保您已安装 `google-genai` 库：

### 基础配置

配置 API 易 服务端点：

```
from google import genai

{/* 配置 API易 服务 */}
client = genai.Client(
    api_key="YOUR_API_KEY",  # 您的 API易 密钥
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 使用 Gemini 模型生成内容 */}
response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents='您的提示词'
)
print(response.text)


```

基础文本生成
------

### 非流式响应

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 发送请求 */}
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents="讲一个关于人工智能的科幻故事。"
)

{/* 输出结果 */}
print(response.text)


```

### 流式响应

对于长文本生成，推荐使用流式响应以获得更好的用户体验：

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 流式生成 */}
response = client.models.generate_content_stream(
    model='gemini-2.5-flash',
    contents="请写一篇关于量子计算的详细文章。"
)

{/* 实时输出 */}
for chunk in response:
    print(chunk.text, end='', flush=True)


```

Gemini 2.5 系列推理功能
-----------------

Gemini 2.5 系列模型支持强大的思维链推理能力，可以显示模型的思考过程。

### 推理模型类型

*   **gemini-2.5-flash**：混合推理型，可通过 `thinking_budget` 参数调整推理深度（范围：0-16384 tokens）
*   **gemini-2.5-pro**：纯推理型，自动启用思维链推理，无法关闭

### 控制推理预算

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 使用推理预算配置 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="如何设计一个高效的分布式缓存系统？请详细分析各个技术方案。",
    config={
        "thinking_budget": 8192,  # 推理预算：0-16384
        "temperature": 1.0        # 温度范围：0-2
    }
)

print(response.text)


```

### 显示思考过程

如果您想看到模型的思考过程（thinking tokens），可以设置 `include_thoughts=True`：

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 启用思考过程显示 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="分析以下代码的时间复杂度：def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
    config={
        "thinking_budget": 8192,
        "include_thoughts": True  # 显示思考过程
    }
)

{/* 遍历所有部分，包括思考过程 */}
for part in response.candidates[0].content.parts:
    if hasattr(part, 'thought') and part.thought:
        print(f"💭 思考过程: {part.text}")
    else:
        print(f"📝 最终答案: {part.text}")


```

多模态处理
-----

Gemini 模型支持处理图片、音频、视频等多种媒体类型。

### 图片处理

```
from google import genai
from PIL import Image

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 加载本地图片 */}
img = Image.open('path/to/your/image.jpg')

{/* 多模态请求 */}
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        "请详细描述这张图片的内容，包括主要元素、颜色、构图等。",
        img
    ]
)

print(response.text)


```

### 视频处理

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 上传视频文件 */}
video_file = client.files.upload(path='path/to/video.mp4')

{/* 分析视频内容 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        "请总结这个视频的主要内容和关键信息。",
        video_file
    ]
)

print(response.text)


```

### 音频处理

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 上传音频文件 */}
audio_file = client.files.upload(path='path/to/audio.mp3')

{/* 转录和分析音频 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        "请转录这段音频的内容，并总结主要话题。",
        audio_file
    ]
)

print(response.text)


```

### 媒体分辨率优化

为了节省 tokens 费用，您可以调整媒体文件的分辨率：

```
from google import genai
from PIL import Image

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 使用较低分辨率处理图片，节省费用 */}
img = Image.open('large_image.jpg')

response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        "这张图片的主题是什么？",
        img
    ],
    config={
        "response_modalities": ["TEXT"],
        "media_resolution": "MEDIA_RESOLUTION_LOW"  # LOW | MEDIUM | HIGH
    }
)

print(response.text)


```

代码执行功能
------

Gemini 模型支持自动执行 Python 代码，非常适合数据分析场景。

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 数据分析示例，启用代码执行工具 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""
假设我有以下销售数据：
- 产品A：100件，单价50元
- 产品B：200件，单价30元
- 产品C：150件，单价40元

请计算：
1. 总销售额
2. 平均单价
3. 绘制销售额分布的柱状图
""",
    config={'tools': [{'code_execution': {}}]}
)

{/* 查看执行的代码和结果 */}
for part in response.candidates[0].content.parts:
    if hasattr(part, 'executable_code'):
        print(f"执行的代码:\n{part.executable_code.code}")
    if hasattr(part, 'code_execution_result'):
        print(f"执行结果:\n{part.code_execution_result.output}")
    if hasattr(part, 'text'):
        print(f"分析说明:\n{part.text}")


```

Function Calling（工具调用）
----------------------

Gemini 原生格式完整支持 Function Calling，让模型可以调用外部工具。

### 定义工具

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 定义天气查询工具 */}
tools = [
    {
        "function_declarations": [
            {
                "name": "get_current_weather",
                "description": "获取指定城市的当前天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "温度单位"
                        }
                    },
                    "required": ["location"]
                }
            }
        ]
    }
]


```

### 自动工具调用

```
from google import genai

{/* 设置工具调用模式 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="北京现在的天气怎么样？温度是多少摄氏度？",
    config={
        'tools': tools,
        'tool_config': {'function_calling_config': {'mode': 'AUTO'}}
    }
)

{/* 检查是否需要调用工具 */}
function_call = response.candidates[0].content.parts[0].function_call

if function_call:
    print(f"调用工具: {function_call.name}")
    print(f"参数: {dict(function_call.args)}")

    {/* 实际调用您的天气 API */}
    def get_current_weather(location, unit="celsius"):
        # 这里应该调用真实的天气 API
        return {
            "location": location,
            "temperature": 22,
            "unit": unit,
            "condition": "晴朗"
        }

    {/* 获取工具执行结果 */}
    weather_data = get_current_weather(**dict(function_call.args))

    {/* 将结果返回给模型 */}
    from google.genai import types

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Content(
                parts=[
                    types.Part(
                        function_response=types.FunctionResponse(
                            name=function_call.name,
                            response=weather_data
                        )
                    )
                ]
            )
        ]
    )

    print(f"最终回答: {response.text}")


```

上下文缓存
-----

API 易 自动为 Gemini 原生格式启用隐式上下文缓存，可以显著降低重复对话的费用。

### 缓存机制

*   **自动启用**：无需手动配置，系统自动缓存上下文
*   **缓存费用**：缓存的 tokens 按正常价格的 25% 计费
*   **有效期**：缓存会在一定时间后自动过期

### 检测缓存命中

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 发送请求 */}
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="你好，请介绍一下量子计算。"
)

{/* 检查缓存命中 */}
usage = response.usage_metadata
if hasattr(usage, 'cached_content_token_count'):
    print(f"缓存命中 tokens: {usage.cached_content_token_count}")
    print(f"输入 tokens: {usage.prompt_token_count}")
    print(f"输出 tokens: {usage.candidates_token_count}")


```

Tokens 用量追踪
-----------

每次 API 调用都会返回详细的 tokens 用量信息。

### 获取用量统计

```
from google import genai

client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="解释一下机器学习的基本原理。"
)

{/* 获取用量元数据 */}
usage = response.usage_metadata

print(f"提示词 tokens: {usage.prompt_token_count}")
print(f"输出 tokens: {usage.candidates_token_count}")
print(f"总计 tokens: {usage.total_token_count}")

{/* 如果有缓存命中 */}
if hasattr(usage, 'cached_content_token_count'):
    print(f"缓存 tokens: {usage.cached_content_token_count}")

{/* 如果有推理 tokens（Gemini 2.5 系列）*/}
if hasattr(usage, 'thoughts_token_count'):
    print(f"推理 tokens: {usage.thoughts_token_count}")


```

### Tokens 字段说明

<table><thead><tr><th>字段</th><th>说明</th><th>计费</th></tr></thead><tbody><tr><td><code>prompt_token_count</code></td><td>输入提示词的 tokens 数量</td><td>按输入价格计费</td></tr><tr><td><code>candidates_token_count</code></td><td>输出内容的 tokens 数量</td><td>按输出价格计费</td></tr><tr><td><code>cached_content_token_count</code></td><td>缓存命中的 tokens 数量</td><td>按输入价格的 25% 计费</td></tr><tr><td><code>thoughts_token_count</code></td><td>推理过程的 tokens 数量</td><td>按输出价格计费</td></tr><tr><td><code>total_token_count</code></td><td>总计 tokens 数量</td><td data-numeric="true">-</td></tr></tbody></table>

注意事项
----

与 OpenAI 兼容格式的对比
----------------

<table><thead><tr><th>特性</th><th>Gemini 原生格式</th><th>OpenAI 兼容格式</th></tr></thead><tbody><tr><td><strong>端点</strong></td><td><code>https://api.apiyi.com</code></td><td><code>https://api.apiyi.com/v1/chat/completions</code></td></tr><tr><td><strong>SDK</strong></td><td><code>google-genai</code></td><td><code>openai</code></td></tr><tr><td><strong>推理控制</strong></td><td><code>thinking_budget</code> (0-16384)</td><td><code>reasoning_effort</code> (low/medium/high)</td></tr><tr><td><strong>思考过程</strong></td><td><code>include_thoughts=True</code></td><td>不支持</td></tr><tr><td><strong>代码执行</strong></td><td><code>tools=[{'code_execution': {}}]</code></td><td>不支持</td></tr><tr><td><strong>媒体上传</strong></td><td><code>client.files.upload()</code></td><td>Base64 编码</td></tr><tr><td><strong>缓存检测</strong></td><td><code>cached_content_token_count</code></td><td>无详细字段</td></tr></tbody></table>

完整示例
----

以下是一个综合示例，展示了多种功能的组合使用：

```
from google import genai
from PIL import Image

{/* 配置 */}
client = genai.Client(
    api_key="YOUR_API_KEY",
    http_options={"base_url": "https://api.apiyi.com"}
)

{/* 定义工具 */}
tools = [{
    "function_declarations": [{
        "name": "search_database",
        "description": "搜索产品数据库",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"}
            },
            "required": ["query"]
        }
    }]
}]

{/* 多模态 + 工具调用 + 流式输出 */}
img = Image.open('product.jpg')

response = client.models.generate_content_stream(
    model='gemini-2.5-flash',
    contents=[
        "这张图片中的产品是什么？请搜索数据库查找类似产品，并推荐给我。",
        img
    ],
    config={
        'tools': tools,
        'tool_config': {'function_calling_config': {'mode': 'AUTO'}},
        'thinking_budget': 4096,
        'temperature': 0.7,
        'include_thoughts': False
    }
)

{/* 处理流式响应 */}
for chunk in response:
    if chunk.text:
        print(chunk.text, end='', flush=True)

    {/* 检查工具调用 */}
    if chunk.candidates and chunk.candidates[0].content.parts:
        for part in chunk.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                print(f"\n[调用工具: {part.function_call.name}]")

{/* 查看最终用量（需要等待流式响应完全结束）*/}
if hasattr(response, 'usage_metadata'):
    print(f"\n\nTokens 用量: {response.usage_metadata.total_token_count}")


```
## 注意
VEO 系列模型，目前还不支持通过原生SDK调用。