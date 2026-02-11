> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/openai-sdk)

> 使用官方 OpenAI SDK 无缝接入 API 易 服务

API 易 完全兼容 OpenAI API 格式，您可以直接使用官方 OpenAI SDK，只需简单修改配置即可无缝切换到 API 易 服务。

支持的官方 SDK
---------

API 易 支持所有官方 OpenAI SDK：

*   Python (`openai`)
*   Node.js (`openai`)
*   .NET (`OpenAI`)
*   Go (`go-openai`)
*   Java (第三方)
*   PHP (第三方)
*   Ruby (第三方)

Python SDK
----------

### 安装

### 基础配置

```
from openai import OpenAI

# 配置 API易 服务
client = OpenAI(
    api_key="YOUR_API_KEY",  # 您的 API易 密钥
    base_url="https://api.apiyi.com/v1"  # API易 端点
)

# 使用方式与官方完全相同
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)


```

### 环境变量配置

```
import os
from openai import OpenAI

# 设置环境变量
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
os.environ["OPENAI_BASE_URL"] = "https://api.apiyi.com/v1"

# 使用默认配置
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain quantum computing"}]
)


```

### 异步使用

```
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        api_key="YOUR_API_KEY",
        base_url="https://api.apiyi.com/v1"
    )
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    
    print(response.choices[0].message.content)

asyncio.run(main())


```

### 流式输出

```
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.apiyi.com/v1"
)

stream = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


```

Node.js SDK
-----------

### 安装

### 基础配置

```
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'YOUR_API_KEY',
  baseURL: 'https://api.apiyi.com/v1'
});

const response = await openai.chat.completions.create({
  model: 'gpt-3.5-turbo',
  messages: [{ role: 'user', content: 'Hello!' }]
});

console.log(response.choices[0].message.content);


```

### 环境变量配置

```
// 设置环境变量
process.env.OPENAI_API_KEY = 'YOUR_API_KEY';
process.env.OPENAI_BASE_URL = 'https://api.apiyi.com/v1';

import OpenAI from 'openai';

// 使用默认配置
const openai = new OpenAI();

const response = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: 'Explain AI to a 5-year-old' }]
});


```

### 流式输出

```
const stream = await openai.chat.completions.create({
  model: 'gpt-3.5-turbo',
  messages: [{ role: 'user', content: 'Tell me a joke' }],
  stream: true
});

for await (const chunk of stream) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}


```

### TypeScript 支持

```
import OpenAI from 'openai';
import type { ChatCompletionCreateParamsNonStreaming } from 'openai/resources/chat/completions';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
  baseURL: 'https://api.apiyi.com/v1'
});

const params: ChatCompletionCreateParamsNonStreaming = {
  model: 'gpt-3.5-turbo',
  messages: [{ role: 'user', content: 'Hello TypeScript!' }],
  temperature: 0.7
};

const response = await openai.chat.completions.create(params);


```

.NET SDK
--------

### 安装

```
dotnet add package OpenAI


```

### 基础配置

```
using OpenAI;
using OpenAI.Chat;

var client = new OpenAIClient("YOUR_API_KEY", new OpenAIClientOptions
{
    Endpoint = new Uri("https://api.apiyi.com/v1")
});

var chatClient = client.GetChatClient("gpt-3.5-turbo");

var response = await chatClient.CompleteChatAsync("Hello!");

Console.WriteLine(response.Value.Content[0].Text);


```

### 流式输出

```
await foreach (var update in chatClient.CompleteChatStreamingAsync("Tell me a story"))
{
    if (update.ContentUpdate.Count > 0)
    {
        Console.Write(update.ContentUpdate[0].Text);
    }
}


```

Go SDK
------

### 安装

```
go get github.com/sashabaranov/go-openai


```

### 基础配置

```
package main

import (
    "context"
    "fmt"
    "github.com/sashabaranov/go-openai"
)

func main() {
    config := openai.DefaultConfig("YOUR_API_KEY")
    config.BaseURL = "https://api.apiyi.com/v1"
    
    client := openai.NewClientWithConfig(config)
    
    resp, err := client.CreateChatCompletion(
        context.Background(),
        openai.ChatCompletionRequest{
            Model: openai.GPT3Dot5Turbo,
            Messages: []openai.ChatCompletionMessage{
                {
                    Role:    openai.ChatMessageRoleUser,
                    Content: "Hello!",
                },
            },
        },
    )
    
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    fmt.Println(resp.Choices[0].Message.Content)
}


```

### 流式输出

```
stream, err := client.CreateChatCompletionStream(
    context.Background(),
    openai.ChatCompletionRequest{
        Model: openai.GPT3Dot5Turbo,
        Messages: []openai.ChatCompletionMessage{
            {
                Role:    openai.ChatMessageRoleUser,
                Content: "Write a haiku",
            },
        },
        Stream: true,
    },
)

if err != nil {
    fmt.Printf("Error: %v\n", err)
    return
}
defer stream.Close()

for {
    response, err := stream.Recv()
    if errors.Is(err, io.EOF) {
        break
    }
    
    if err != nil {
        fmt.Printf("Error: %v\n", err)
        return
    }
    
    fmt.Print(response.Choices[0].Delta.Content)
}


```

Java SDK
--------

### 依赖配置

```
<dependency>
    <groupId>com.theokanning.openai-gpt3-java</groupId>
    <artifactId>service</artifactId>
    <version>0.18.2</version>
</dependency>


```

### 基础使用

```
import com.theokanning.openai.OpenAiService;
import com.theokanning.openai.completion.chat.*;

import java.time.Duration;
import java.util.List;

public class APIYiExample {
    public static void main(String[] args) {
        OpenAiService service = new OpenAiService(
            "YOUR_API_KEY", 
            Duration.ofSeconds(60),
            "https://api.apiyi.com/v1/"
        );
        
        ChatCompletionRequest request = ChatCompletionRequest.builder()
            .model("gpt-3.5-turbo")
            .messages(List.of(
                new ChatMessage(ChatMessageRole.USER, "Hello!")
            ))
            .build();
        
        ChatCompletionResult result = service.createChatCompletion(request);
        System.out.println(result.getChoices().get(0).getMessage().getContent());
    }
}


```

模型切换
----

### 使用不同模型

```
# GPT 模型
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Claude 模型
response = client.chat.completions.create(
    model="claude-3-opus-20240229",
    messages=[{"role": "user", "content": "Hello"}]
)

# Gemini 模型
response = client.chat.completions.create(
    model="gemini-pro",
    messages=[{"role": "user", "content": "Hello"}]
)


```

### 动态模型选择

```
def chat_with_model(message: str, model: str = "gpt-3.5-turbo"):
    """支持动态切换模型的聊天函数"""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

# 使用不同模型
print(chat_with_model("解释量子计算", "gpt-4"))
print(chat_with_model("解释量子计算", "claude-3-opus-20240229"))
print(chat_with_model("解释量子计算", "gemini-pro"))


```

高级功能
----

### Function Calling

```
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    tools=tools,
    tool_choice="auto"
)

if response.choices[0].message.tool_calls:
    print("AI 想要调用函数：", response.choices[0].message.tool_calls[0].function.name)


```

### 图像输入

```
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg"
                    }
                }
            ]
        }
    ]
)


```

### 嵌入向量

```
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="要嵌入的文本内容"
)

embedding = response.data[0].embedding
print(f"向量维度：{len(embedding)}")


```

错误处理
----

### 基础错误处理

```
from openai import OpenAI, OpenAIError

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except OpenAIError as e:
    print(f"API 错误：{e}")


```

### 详细错误处理

```
from openai import (
    OpenAI, 
    APIError, 
    APIConnectionError, 
    RateLimitError,
    InternalServerError
)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except RateLimitError:
    print("请求频率超限，请稍后重试")
except APIConnectionError:
    print("网络连接错误")
except InternalServerError:
    print("服务器内部错误")
except APIError as e:
    print(f"API 错误：{e}")


```

最佳实践
----

### 1. 配置管理

```
import os
from openai import OpenAI

class APIYiClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("APIYI_API_KEY"),
            base_url=os.getenv("APIYI_BASE_URL", "https://api.apiyi.com/v1")
        )
    
    def chat(self, message: str, model: str = "gpt-3.5-turbo"):
        return self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}]
        )


```

### 2. 重试机制

```
import time
import random
from openai import OpenAI, RateLimitError

def chat_with_retry(client, messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
            else:
                raise


```

### 3. 成本控制

```
def controlled_chat(message: str, max_tokens: int = 150):
    """控制输出长度以管理成本"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}],
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response


```

迁移指南
----

### 从 OpenAI 迁移

如果您已经在使用 OpenAI 官方服务，迁移到 API 易 非常简单：

1.  **更改 base_url**

```
# 原来的配置
client = OpenAI(api_key="sk-...")

# 改为 API易
client = OpenAI(
    api_key="YOUR_APIYI_KEY", 
    base_url="https://api.apiyi.com/v1"
)


```

2.  **更新环境变量**

```
# 原来
export OPENAI_API_KEY="sk-..."

# 改为
export OPENAI_API_KEY="YOUR_APIYI_KEY"
export OPENAI_BASE_URL="https://api.apiyi.com/v1"


```

3.  **代码无需修改** 所有其他代码保持不变，包括：

*   方法调用
*   参数格式
*   响应处理

### 多服务兼容

```
class MultiProviderClient:
    def __init__(self):
        self.apiyi_client = OpenAI(
            api_key="APIYI_KEY",
            base_url="https://api.apiyi.com/v1"
        )
        self.openai_client = OpenAI(api_key="OPENAI_KEY")
    
    def chat(self, message: str, provider: str = "apiyi"):
        client = self.apiyi_client if provider == "apiyi" else self.openai_client
        return client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )


```

需要更多帮助？请访问 [API 易官网](https://vip.apiyi.com/) 或查看 [官方 SDK 文档](https://platform.openai.com/docs/libraries)。