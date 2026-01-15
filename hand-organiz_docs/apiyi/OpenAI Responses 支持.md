> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/openai-responses)

> 新一代智能体 API - 结合对话补全的简洁性与强大的工具调用能力

API 易 全面支持 OpenAI 最新的 Responses API，这是 2025 年 3 月推出的新一代智能体构建接口。Responses API 结合了 Chat Completions 的简洁性与 Assistants API 的工具使用和状态管理能力，为开发者提供更灵活、更强大的 AI 应用构建体验。

🚀 核心特性
-------

📋 支持的模型
--------

### 推理模型（推荐）

*   **O3 系列**：`o3`, `o3-pro`, `o4-mini`
*   **特色**：推理令牌跨请求保持，提供更智能的上下文理解

### 对话模型

*   **GPT-4.1 系列**：`gpt-4.1`, `gpt-4.1-mini`
*   **特色**：强大的工具调用和多模态能力

🔧 基础用法
-------

### 简单对话

### 实际响应示例

基于您的测试结果，以下是完整的响应格式：

```
{
  "id": "resp_6884fcab4930819dbbc02f15cbe63f6c0a92c38ff214d10a",
  "object": "response",
  "created_at": 1753545899,
  "status": "completed",
  "background": false,
  "error": null,
  "incomplete_details": null,
  "instructions": "You are a helpful assistant.",
  "max_output_tokens": null,
  "max_tool_calls": null,
  "model": "gpt-4.1-2025-04-14",
  "output": [
    {
      "id": "msg_6884fcab8f18819dbcdf349f01b424f80a92c38ff214d10a",
      "type": "message",
      "status": "completed",
      "content": [
        {
          "type": "output_text",
          "annotations": [],
          "logprobs": [],
          "text": "Hello! How can I assist you today?"
        }
      ],
      "role": "assistant"
    }
  ],
  "parallel_tool_calls": true,
  "previous_response_id": null,
  "prompt_cache_key": null,
  "reasoning": {
    "effort": null,
    "summary": null
  },
  "safety_identifier": null,
  "service_tier": "default",
  "store": true,
  "temperature": 1.0,
  "text": {
    "format": {
      "type": "text"
    }
  },
  "tool_choice": "auto",
  "tools": [],
  "top_logprobs": 0,
  "top_p": 1.0,
  "truncation": "disabled",
  "usage": {
    "input_tokens": 19,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 10,
    "output_tokens_details": {
      "reasoning_tokens": 0
    },
    "total_tokens": 29
  },
  "user": null,
  "metadata": {}
}


```

📊 请求参数详解
---------

### 必需参数

<table><thead><tr><th>参数</th><th>类型</th><th>说明</th></tr></thead><tbody><tr><td><code>model</code></td><td>string</td><td>模型名称，如 <code>gpt-4.1</code>, <code>o3</code></td></tr><tr><td><code>input</code></td><td>string</td><td>用户输入内容</td></tr></tbody></table>

### 可选参数

<table><thead><tr><th>参数</th><th>类型</th><th>默认值</th><th>说明</th></tr></thead><tbody><tr><td><code>instructions</code></td><td>string</td><td>null</td><td>系统指令，定义助手行为</td></tr><tr><td><code>previous_response_id</code></td><td>string</td><td>null</td><td>上一个响应的 ID，用于维护上下文</td></tr><tr><td><code>temperature</code></td><td>float</td><td>1.0</td><td>控制输出随机性 (0-2)</td></tr><tr><td><code>max_output_tokens</code></td><td>int</td><td>null</td><td>最大输出令牌数</td></tr><tr><td><code>tools</code></td><td>array</td><td>[]</td><td>可用工具列表</td></tr><tr><td><code>tool_choice</code></td><td>string</td><td>”auto”</td><td>工具选择策略</td></tr><tr><td><code>parallel_tool_calls</code></td><td>boolean</td><td>true</td><td>是否允许并行工具调用</td></tr><tr><td><code>store</code></td><td>boolean</td><td>true</td><td>是否存储对话用于训练</td></tr><tr><td><code>metadata</code></td><td>object</td><td></td><td>自定义元数据</td></tr></tbody></table>

🛠️ 内置工具支持
----------

### 1. 函数调用

```
response = client.responses.create(
    model="gpt-4.1",
    input="What's the weather like in Beijing?",
    instructions="You are a helpful weather assistant.",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]
)


```

### 2. 代码解释器

```
response = client.responses.create(
    model="gpt-4.1", 
    input="Create a chart showing sales data: Jan:100, Feb:150, Mar:120",
    instructions="You are a data analyst. Use code interpreter to create visualizations.",
    tools=[{"type": "code_interpreter"}]
)


```

### 3. 文件搜索

```
response = client.responses.create(
    model="gpt-4.1",
    input="Search for information about quarterly reports",
    instructions="You are a document analyst.",
    tools=[{"type": "file_search"}]
)


```

🔄 状态管理
-------

### 维护对话上下文

```
# 第一轮对话
response1 = client.responses.create(
    model="gpt-4.1",
    input="My name is Alice. Please remember this.",
    instructions="You are a helpful assistant with good memory."
)

# 第二轮对话 - 使用 previous_response_id 维护上下文
response2 = client.responses.create(
    model="gpt-4.1", 
    input="What's my name?",
    instructions="You are a helpful assistant with good memory.",
    previous_response_id=response1.id
)

print(response2.output[0].content[0].text)  # 应该回答 "Alice"


```

### 多轮工具调用

```
def multi_turn_conversation():
    response_id = None
    
    for user_input in ["What's 2+2?", "Now multiply that by 3", "And divide by 2"]:
        response = client.responses.create(
            model="o3",
            input=user_input,
            instructions="You are a math tutor. Show your reasoning.",
            previous_response_id=response_id,
            tools=[{"type": "code_interpreter"}]
        )
        
        print(f"User: {user_input}")
        print(f"Assistant: {response.output[0].content[0].text}")
        
        response_id = response.id  # 保持上下文


```

📈 推理模型特性
---------

### O3/O4-mini 推理保持

推理模型在 Responses API 中具有特殊优势：

```
# 使用 O3 进行复杂推理
response = client.responses.create(
    model="o3",
    input="Solve this step by step: If a train travels 120km in 2 hours, then speeds up 20% for the next hour, how far did it travel in total?",
    instructions="Think through this problem step by step, showing all reasoning."
)

# 查看推理过程
reasoning_tokens = response.usage.output_tokens_details.reasoning_tokens
print(f"Reasoning tokens used: {reasoning_tokens}")

# 继续对话，推理上下文会保持
follow_up = client.responses.create(
    model="o3",
    input="Now what if the train slowed down 10% in the fourth hour?",
    previous_response_id=response.id
)


```

🆚 与 Chat Completions 对比
------------------------

<table><thead><tr><th>特性</th><th>Chat Completions</th><th>Responses API</th></tr></thead><tbody><tr><td><strong>基础对话</strong></td><td>✅ 支持</td><td>✅ 支持</td></tr><tr><td><strong>流式响应</strong></td><td>✅ 支持</td><td>✅ 支持</td></tr><tr><td><strong>函数调用</strong></td><td>✅ 支持</td><td>✅ 增强支持</td></tr><tr><td><strong>内置工具</strong></td><td>❌ 不支持</td><td>✅ 丰富工具</td></tr><tr><td><strong>状态管理</strong></td><td>❌ 无状态</td><td>✅ 有状态</td></tr><tr><td><strong>推理保持</strong></td><td>❌ 不支持</td><td>✅ O3/O4 支持</td></tr><tr><td><strong>文件搜索</strong></td><td>❌ 不支持</td><td>✅ 支持</td></tr><tr><td><strong>代码解释器</strong></td><td>❌ 不支持</td><td>✅ 支持</td></tr></tbody></table>

### 迁移示例

从 Chat Completions 迁移到 Responses API：

🔧 高级功能
-------

### 并行工具调用

```
response = client.responses.create(
    model="gpt-4.1",
    input="Get weather for Beijing and Shanghai, then calculate travel time between them",
    instructions="You are a travel assistant.",
    parallel_tool_calls=True,
    tools=[
        {"type": "function", "function": {"name": "get_weather", ...}},
        {"type": "function", "function": {"name": "calculate_distance", ...}}
    ]
)


```

### 输出格式控制

```
response = client.responses.create(
    model="gpt-4.1",
    input="Summarize this data in JSON format",
    instructions="Always respond in valid JSON.",
    text={
        "format": {
            "type": "json_object"
        }
    }
)


```

### 推理努力控制（O3 系列）

```
response = client.responses.create(
    model="o3",
    input="Solve this complex physics problem",
    instructions="Think carefully and show detailed reasoning.",
    reasoning={
        "effort": "high"  # low, medium, high
    }
)


```

📊 响应字段详解
---------

### 核心字段

<table><thead><tr><th>字段</th><th>类型</th><th>说明</th></tr></thead><tbody><tr><td><code>id</code></td><td>string</td><td>响应唯一标识符</td></tr><tr><td><code>object</code></td><td>string</td><td>固定为 “response”</td></tr><tr><td><code>created_at</code></td><td>integer</td><td>创建时间戳</td></tr><tr><td><code>status</code></td><td>string</td><td>状态：completed/failed/in_progress</td></tr><tr><td><code>model</code></td><td>string</td><td>实际使用的模型版本</td></tr><tr><td><code>output</code></td><td>array</td><td>输出消息数组</td></tr><tr><td><code>usage</code></td><td>object</td><td>Token 使用统计</td></tr></tbody></table>

### 输出消息格式

```
{
  "id": "msg_xxx",
  "type": "message",
  "status": "completed",
  "content": [
    {
      "type": "output_text",
      "text": "响应内容",
      "annotations": [],
      "logprobs": []
    }
  ],
  "role": "assistant"
}


```

### 使用统计

```
{
  "usage": {
    "input_tokens": 19,
    "input_tokens_details": {
      "cached_tokens": 0
    },
    "output_tokens": 10,
    "output_tokens_details": {
      "reasoning_tokens": 0  // 仅推理模型
    },
    "total_tokens": 29
  }
}


```

🚨 错误处理
-------

### 标准错误格式

```
{
  "error": {
    "type": "invalid_request_error",
    "code": "model_not_supported",
    "message": "The model 'gpt-3.5-turbo' is not supported for the responses endpoint.",
    "param": "model"
  }
}


```

### 常见错误

<table><thead><tr><th>错误码</th><th>说明</th><th>解决方案</th></tr></thead><tbody><tr><td><code>model_not_supported</code></td><td>模型不支持 Responses API</td><td>使用支持的新模型</td></tr><tr><td><code>invalid_previous_response_id</code></td><td>无效的上一个响应 ID</td><td>检查响应 ID 是否正确</td></tr><tr><td><code>tool_not_available</code></td><td>工具不可用</td><td>检查工具配置</td></tr><tr><td><code>max_tokens_exceeded</code></td><td>超出令牌限制</td><td>减少输入或设置 max_output_tokens</td></tr></tbody></table>

💡 最佳实践
-------

### 1. 状态管理策略

```
class ConversationManager:
    def __init__(self, model="gpt-4.1", instructions="You are a helpful assistant."):
        self.model = model
        self.instructions = instructions
        self.last_response_id = None
    
    def send_message(self, input_text, tools=None):
        response = client.responses.create(
            model=self.model,
            input=input_text,
            instructions=self.instructions,
            previous_response_id=self.last_response_id,
            tools=tools or []
        )
        
        self.last_response_id = response.id
        return response.output[0].content[0].text
    
    def reset_conversation(self):
        self.last_response_id = None

# 使用示例
conv = ConversationManager()
print(conv.send_message("Hello, I'm Alice"))
print(conv.send_message("What's my name?"))  # 会记住是 Alice


```

### 2. 工具调用优化

```
def smart_tool_calling(user_input):
    # 根据输入智能选择工具
    available_tools = []
    
    if "weather" in user_input.lower():
        available_tools.append(weather_tool)
    if "calculate" in user_input.lower():
        available_tools.append(calculator_tool)
    if "search" in user_input.lower():
        available_tools.append(search_tool)
    
    response = client.responses.create(
        model="gpt-4.1",
        input=user_input,
        instructions="Use the appropriate tools to help the user.",
        tools=available_tools,
        tool_choice="auto"
    )
    
    return response


```

### 3. 推理模型优化

```
def optimized_reasoning(complex_problem):
    response = client.responses.create(
        model="o3",
        input=complex_problem,
        instructions="Think step by step and show your reasoning process.",
        reasoning={
            "effort": "high"  # 对复杂问题使用高推理努力
        },
        temperature=0.1  # 降低随机性以获得一致结果
    )
    
    # 分析推理使用情况
    reasoning_tokens = response.usage.output_tokens_details.reasoning_tokens
    total_cost = calculate_cost(response.usage)
    
    return {
        "answer": response.output[0].content[0].text,
        "reasoning_tokens": reasoning_tokens,
        "cost": total_cost
    }


```

🔮 未来发展
-------

### 即将推出的功能

1.  **完整的 Assistants API 功能集成**（2026 年上半年）
2.  **更多内置工具**：Web 搜索、计算机使用等
3.  **模型上下文协议 (MCP) 支持**
4.  **增强的多模态能力**

### 迁移时间线

*   **现在**：可以开始使用 Responses API
*   **2026 年上半年**：功能对等 Assistants API
*   **2026 年**：Assistants API 弃用公告
*   **2027 年**：完全迁移到 Responses API

需要更多帮助？请访问 [API 易官网](https://api.apiyi.com/) 或查看 [OpenAI Responses API 官方文档](https://platform.openai.com/docs/api-reference/responses)。