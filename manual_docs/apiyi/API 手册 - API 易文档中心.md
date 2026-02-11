> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-manual)

> API 易 接口使用手册和参考文档，本手册提供 API 易 的完整接口文档，帮助您快速集成和使用我们的服务。

平台特色
----

### OpenAI 兼容模式

API 易采用 **OpenAI 兼容格式**，让您可以用统一的接口调用 200 + 主流大模型： **支持的模型厂商：**

*   🤖 **OpenAI**：gpt-4o、gpt-5-chat-latest、gpt-3.5-turbo 等
*   🧠 **Anthropic**：claude-sonnet-4-20250514、claude-opus-4-1-20250805 等
*   💎 **Google**：gemini-2.5-pro、gemini-2.5-flash 等
*   🚀 **xAI**：grok-4-0709、grok-3 等
*   🔍 **DeepSeek**：deepSeek-r1、deepSeek-v3 等
*   🌟 **阿里**：Qwen 系列模型
*   💬 **Moonshot**：Kimi 模型等

### 功能支持范围

**✅ 支持的功能：**

*   💬 **对话补全**：Chat Completions 接口
*   🖼️ **图像生成**：gpt-image-1、flux-kontext-pro、flux-kontext-max 等
*   🔊 **语音处理**：Whisper 转录
*   📊 **嵌入向量**：文本向量化
*   ⚡ **函数调用**：Function Calling
*   📡 **流式输出**：实时响应
*   🔧 **OpenAI 参数**：temperature、top_p、max_tokens 等
*   🆕 **Responses 端点**：OpenAI 最新功能

**❌ 不支持的功能：**

*   🔧 微调接口（Fine-tuning）
*   📁 Files 管理接口
*   🏢 组织管理接口
*   💳 计费管理接口

### 简单切换模型

**核心优势：一套代码，多种模型** 用 OpenAI 格式跑通后，只需要**更换模型名称**即可切换到其他大模型：

```
# 使用GPT-4o
response = client.chat.completions.create(
    model="gpt-4o",  # OpenAI模型
    messages=[...]
)

# 切换到Claude，其他代码完全不变！
response = client.chat.completions.create(
    model="claude-3.5-sonnet",  # 只改模型名
    messages=[...]
)

# 切换到Gemini
response = client.chat.completions.create(
    model="gemini-1.5-pro",  # 只改模型名
    messages=[...]
)


```

快速开始
----

### 获取 API Key

1.  访问 [API 易控制台](https://api.apiyi.com/token)
2.  登录您的账户
3.  在令牌管理页面点击” 新增” 创建 API Key
4.  复制生成的 API Key 用于接口调用

### 查看请求示例

在令牌管理页面，您可以快速获取各种编程语言的代码示例： **操作步骤：**

1.  进入 [令牌管理页面](https://api.apiyi.com/token)
2.  找到您要使用的 API Key 所在的行
3.  点击” 操作” 列中的🔧**小扳手图标**（工具图标）
4.  在弹出菜单中选择” **请求示例**”
5.  查看包含以下语言的完整代码示例：

![](https://mintcdn.com/apiyillc/OMY6ItCc2mC1yzgA/images/apiyi-token-simple-code.png?fit=max&auto=format&n=OMY6ItCc2mC1yzgA&q=85&s=067d8d551cd1d8aaebb833932e6632a5) **支持的编程语言：**

*   **cURL** - 命令行测试
*   **Python (SDK)** - 使用官方 OpenAI 库
*   **Python (requests)** - 使用 requests 库
*   **Node.js** - JavaScript/TypeScript
*   **Java** - Java 应用开发
*   **C#** - .NET 应用开发
*   **Go** - Go 语言开发
*   **PHP** - Web 开发
*   **Ruby** - Ruby 应用开发
*   以及更多语言…

**代码示例特点：**

*   ✅ **完整可运行**：复制粘贴即可使用
*   ✅ **参数说明**：详细的参数配置
*   ✅ **错误处理**：包含异常处理逻辑
*   ✅ **最佳实践**：遵循各语言开发规范

基础信息
----

### API 端点

*   **主要端点**：`https://api.apiyi.com/v1`
*   **备用端点**：`https://vip.apiyi.com/v1`

### 认证方式

所有 API 请求需要在 Header 中包含认证信息：

```
Authorization: Bearer YOUR_API_KEY


```

### 请求格式

*   **Content-Type**：`application/json`
*   **编码格式**：UTF-8
*   **请求方法**：POST（大部分接口）

核心接口
----

### 1. 对话补全（Chat Completions）

创建一个对话补全请求，支持多轮对话。 **请求端点**

```
POST /v1/chat/completions


```

**请求参数**

<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td>model</td><td>string</td><td>是</td><td>模型名称，如 <code>gpt-3.5-turbo</code></td></tr><tr><td>messages</td><td>array</td><td>是</td><td>对话消息数组</td></tr><tr><td>temperature</td><td>number</td><td>否</td><td>采样温度，0-2 之间，默认 1</td></tr><tr><td>max_tokens</td><td>integer</td><td>否</td><td>最大生成令牌数</td></tr><tr><td>stream</td><td>boolean</td><td>否</td><td>是否流式返回，默认 false</td></tr><tr><td>top_p</td><td>number</td><td>否</td><td>核采样参数，0-1 之间</td></tr><tr><td>n</td><td>integer</td><td>否</td><td>生成数量，默认 1</td></tr><tr><td>stop</td><td>string/array</td><td>否</td><td>停止序列</td></tr><tr><td>presence_penalty</td><td>number</td><td>否</td><td>存在惩罚，-2 到 2 之间</td></tr><tr><td>frequency_penalty</td><td>number</td><td>否</td><td>频率惩罚，-2 到 2 之间</td></tr></tbody></table>

**消息格式**

```
{
  "role": "system|user|assistant",
  "content": "消息内容"
}


```

**完整代码示例**

*   cURL
    
*   Python (SDK)
    
*   Python (requests)
    
*   Node.js
    
*   Java
    
*   C#
    
*   Go
    
*   PHP
    
*   Ruby
    

```
curl -X POST "https://api.apiyi.com/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "你是一个有用的AI助手。"},
      {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'


```

```
from openai import OpenAI

# 初始化客户端
client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.apiyi.com/v1"
)

# 发送聊天请求
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一个有用的AI助手。"},
        {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)


```

```
import requests
import json

url = "https://api.apiyi.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "你是一个有用的AI助手。"},
        {"role": "user", "content": "你好！请介绍一下自己。"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

if response.status_code == 200:
    print(result["choices"][0]["message"]["content"])
else:
    print(f"错误: {result}")


```

```
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: 'YOUR_API_KEY',
  baseURL: 'https://api.apiyi.com/v1'
});

async function chatCompletion() {
  try {
    const response = await client.chat.completions.create({
      model: 'gpt-3.5-turbo',
      messages: [
        {"role": "system", "content": "你是一个有用的AI助手。"},
        {"role": "user", "content": "你好！请介绍一下自己。"}
      ],
      temperature: 0.7,
      max_tokens: 1000
    });
    
    console.log(response.choices[0].message.content);
  } catch (error) {
    console.error('API调用错误:', error);
  }
}

chatCompletion();


```

```
import okhttp3.*;
import com.google.gson.Gson;
import java.io.IOException;
import java.util.*;

public class APIYiExample {
    private static final String API_KEY = "YOUR_API_KEY";
    private static final String BASE_URL = "https://api.apiyi.com/v1";
    
    public static void main(String[] args) throws IOException {
        OkHttpClient client = new OkHttpClient();
        Gson gson = new Gson();
        
        // 构建请求体
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("model", "gpt-3.5-turbo");
        requestBody.put("temperature", 0.7);
        requestBody.put("max_tokens", 1000);
        
        List<Map<String, String>> messages = Arrays.asList(
            Map.of("role", "system", "content", "你是一个有用的AI助手。"),
            Map.of("role", "user", "content", "你好！请介绍一下自己。")
        );
        requestBody.put("messages", messages);
        
        RequestBody body = RequestBody.create(
            gson.toJson(requestBody),
            MediaType.parse("application/json")
        );
        
        Request request = new Request.Builder()
            .url(BASE_URL + "/chat/completions")
            .addHeader("Authorization", "Bearer " + API_KEY)
            .addHeader("Content-Type", "application/json")
            .post(body)
            .build();
        
        try (Response response = client.newCall(request).execute()) {
            System.out.println(response.body().string());
        }
    }
}


```

```
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

class Program
{
    private static readonly string API_KEY = "YOUR_API_KEY";
    private static readonly string BASE_URL = "https://api.apiyi.com/v1";
    
    static async Task Main(string[] args)
    {
        using var client = new HttpClient();
        client.DefaultRequestHeaders.Add("Authorization", $"Bearer {API_KEY}");
        
        var requestBody = new
        {
            model = "gpt-3.5-turbo",
            messages = new[]
            {
                new { role = "system", content = "你是一个有用的AI助手。" },
                new { role = "user", content = "你好！请介绍一下自己。" }
            },
            temperature = 0.7,
            max_tokens = 1000
        };
        
        var json = JsonConvert.SerializeObject(requestBody);
        var content = new StringContent(json, Encoding.UTF8, "application/json");
        
        try
        {
            var response = await client.PostAsync($"{BASE_URL}/chat/completions", content);
            var result = await response.Content.ReadAsStringAsync();
            Console.WriteLine(result);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"错误: {ex.Message}");
        }
    }
}


```

```
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
)

type Message struct {
    Role    string `json:"role"`
    Content string `json:"content"`
}

type ChatRequest struct {
    Model       string    `json:"model"`
    Messages    []Message `json:"messages"`
    Temperature float64   `json:"temperature"`
    MaxTokens   int       `json:"max_tokens"`
}

func main() {
    apiKey := "YOUR_API_KEY"
    baseURL := "https://api.apiyi.com/v1"
    
    reqData := ChatRequest{
        Model: "gpt-3.5-turbo",
        Messages: []Message{
            {Role: "system", Content: "你是一个有用的AI助手。"},
            {Role: "user", Content: "你好！请介绍一下自己。"},
        },
        Temperature: 0.7,
        MaxTokens:   1000,
    }
    
    jsonData, _ := json.Marshal(reqData)
    
    req, _ := http.NewRequest("POST", baseURL+"/chat/completions", bytes.NewBuffer(jsonData))
    req.Header.Set("Authorization", "Bearer "+apiKey)
    req.Header.Set("Content-Type", "application/json")
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        fmt.Printf("请求错误: %v\n", err)
        return
    }
    defer resp.Body.Close()
    
    body, _ := ioutil.ReadAll(resp.Body)
    fmt.Println(string(body))
}


```

```
<?php
$api_key = 'YOUR_API_KEY';
$base_url = 'https://api.apiyi.com/v1';

$data = array(
    'model' => 'gpt-3.5-turbo',
    'messages' => array(
        array('role' => 'system', 'content' => '你是一个有用的AI助手。'),
        array('role' => 'user', 'content' => '你好！请介绍一下自己。')
    ),
    'temperature' => 0.7,
    'max_tokens' => 1000
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $base_url . '/chat/completions');
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Authorization: Bearer ' . $api_key,
    'Content-Type: application/json'
));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code == 200) {
    $result = json_decode($response, true);
    echo $result['choices'][0]['message']['content'];
} else {
    echo "错误: " . $response;
}
?>


```

```
require 'net/http'
require 'json'

api_key = 'YOUR_API_KEY'
base_url = 'https://api.apiyi.com/v1'

uri = URI("#{base_url}/chat/completions")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri)
request['Authorization'] = "Bearer #{api_key}"
request['Content-Type'] = 'application/json'

request.body = {
  model: 'gpt-3.5-turbo',
  messages: [
    { role: 'system', content: '你是一个有用的AI助手。' },
    { role: 'user', content: '你好！请介绍一下自己。' }
  ],
  temperature: 0.7,
  max_tokens: 1000
}.to_json

response = http.request(request)

if response.code == '200'
  result = JSON.parse(response.body)
  puts result['choices'][0]['message']['content']
else
  puts "错误: #{response.body}"
end


```

**响应示例**

```
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1699000000,
  "model": "gpt-3.5-turbo",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 10,
    "total_tokens": 30
  }
}


```

### 2. 文本补全（Completions）

为兼容旧版接口保留，建议使用 Chat Completions。 **请求端点**

**请求参数**

<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td>model</td><td>string</td><td>是</td><td>模型名称</td></tr><tr><td>prompt</td><td>string/array</td><td>是</td><td>提示文本</td></tr><tr><td>max_tokens</td><td>integer</td><td>否</td><td>最大生成长度</td></tr><tr><td>temperature</td><td>number</td><td>否</td><td>采样温度</td></tr><tr><td>top_p</td><td>number</td><td>否</td><td>核采样参数</td></tr><tr><td>n</td><td>integer</td><td>否</td><td>生成数量</td></tr><tr><td>stream</td><td>boolean</td><td>否</td><td>流式输出</td></tr><tr><td>stop</td><td>string/array</td><td>否</td><td>停止序列</td></tr></tbody></table>

### 3. 嵌入向量（Embeddings）

将文本转换为向量表示。 **请求端点**

**请求参数**

<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td>model</td><td>string</td><td>是</td><td>模型名称，如 <code>text-embedding-ada-002</code></td></tr><tr><td>input</td><td>string/array</td><td>是</td><td>输入文本</td></tr><tr><td>encoding_format</td><td>string</td><td>否</td><td>编码格式，<code>float</code> 或 <code>base64</code></td></tr></tbody></table>

**完整代码示例**

*   cURL
    
*   Python (SDK)
    
*   Python (requests)
    
*   Node.js
    

```
curl -X POST "https://api.apiyi.com/v1/embeddings" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "这是一段需要向量化的文本示例"
  }'


```

```
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.apiyi.com/v1"
)

response = client.embeddings.create(
    model="text-embedding-ada-002",
    input="这是一段需要向量化的文本示例"
)

# 获取向量
embedding = response.data[0].embedding
print(f"向量维度: {len(embedding)}")
print(f"前5个值: {embedding[:5]}")


```

```
import requests
import json

url = "https://api.apiyi.com/v1/embeddings"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}

data = {
    "model": "text-embedding-ada-002",
    "input": "这是一段需要向量化的文本示例"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

if response.status_code == 200:
    embedding = result["data"][0]["embedding"]
    print(f"向量维度: {len(embedding)}")
    print(f"向量值: {embedding[:5]}")  # 显示前5个值
else:
    print(f"错误: {result}")


```

```
const OpenAI = require('openai');

const client = new OpenAI({
  apiKey: 'YOUR_API_KEY',
  baseURL: 'https://api.apiyi.com/v1'
});

async function getEmbedding() {
  try {
    const response = await client.embeddings.create({
      model: 'text-embedding-ada-002',
      input: '这是一段需要向量化的文本示例'
    });
    
    const embedding = response.data[0].embedding;
    console.log(`向量维度: ${embedding.length}`);
    console.log(`前5个值: ${embedding.slice(0, 5)}`);
  } catch (error) {
    console.error('API调用错误:', error);
  }
}

getEmbedding();


```

### 4. 图像生成（Images）

生成、编辑或变换图像。 **生成图像**

```
POST /v1/images/generations


```

**请求参数**

<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td>model</td><td>string</td><td>是</td><td>模型名称，推荐 <code>gpt-image-1</code></td></tr><tr><td>prompt</td><td>string</td><td>是</td><td>图像描述提示词</td></tr><tr><td>n</td><td>integer</td><td>否</td><td>生成数量，默认 1</td></tr><tr><td>size</td><td>string</td><td>否</td><td>图像尺寸：<code>1024x1024</code>, <code>1792x1024</code>, <code>1024x1792</code></td></tr><tr><td>quality</td><td>string</td><td>否</td><td>质量：<code>standard</code> 或 <code>hd</code></td></tr><tr><td>style</td><td>string</td><td>否</td><td>风格：<code>vivid</code> 或 <code>natural</code></td></tr></tbody></table>

**完整代码示例**

*   cURL
    
*   Python (SDK)
    
*   Node.js
    

```
curl -X POST "https://api.apiyi.com/v1/images/generations" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-image-1",
    "prompt": "一只可爱的橙色小猫坐在阳光明媚的花园里",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd"
  }'


```

```
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.apiyi.com/v1"
)

response = client.images.generate(
    model="gpt-image-1",  # 推荐使用gpt-image-1
    prompt="一只可爱的橙色小猫坐在阳光明媚的花园里",
    n=1,
    size="1024x1024",
    quality="hd"
)

# 获取图片URL
image_url = response.data[0].url
print(f"生成的图片: {image_url}")

# 下载图片
import requests
img_response = requests.get(image_url)
with open("generated_image.png", "wb") as f:
    f.write(img_response.content)
print("图片已保存为 generated_image.png")


```

```
const OpenAI = require('openai');
const fs = require('fs');

const client = new OpenAI({
  apiKey: 'YOUR_API_KEY',
  baseURL: 'https://api.apiyi.com/v1'
});

async function generateImage() {
  try {
    const response = await client.images.generate({
      model: 'gpt-image-1',  // 推荐使用gpt-image-1
      prompt: '一只可爱的橙色小猫坐在阳光明媚的花园里',
      n: 1,
      size: '1024x1024',
      quality: 'hd'
    });
    
    const imageUrl = response.data[0].url;
    console.log('生成的图片:', imageUrl);
    
    // 下载图片
    const fetch = require('node-fetch');
    const imgResponse = await fetch(imageUrl);
    const buffer = await imgResponse.buffer();
    fs.writeFileSync('generated_image.png', buffer);
    console.log('图片已保存');
    
  } catch (error) {
    console.error('生成图片错误:', error);
  }
}

generateImage();


```

### 5. 音频转文字（Audio）

语音识别和转录。 **转录音频**

```
POST /v1/audio/transcriptions


```

**请求参数**（Form-Data）

<table><thead><tr><th>参数</th><th>类型</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td>file</td><td>file</td><td>是</td><td>音频文件</td></tr><tr><td>model</td><td>string</td><td>是</td><td>模型名称，如 <code>whisper-1</code></td></tr><tr><td>language</td><td>string</td><td>否</td><td>语言代码</td></tr><tr><td>prompt</td><td>string</td><td>否</td><td>指导提示</td></tr><tr><td>response_format</td><td>string</td><td>否</td><td>响应格式</td></tr><tr><td>temperature</td><td>number</td><td>否</td><td>采样温度</td></tr></tbody></table>

### 6. 模型列表

获取可用模型列表。 **请求端点**

**响应示例**

```
{
  "object": "list",
  "data": [
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai"
    }
  ]
}


```

流式响应
----

### 开启流式输出

在请求中设置 `stream: true`：

```
{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": true
}


```

### 流式响应格式

响应将以 Server-Sent Events (SSE) 格式返回：

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699000000,"model":"gpt-3.5-turbo","choices":[{"delta":{"content":"Hello"},"index":0}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1699000000,"model":"gpt-3.5-turbo","choices":[{"delta":{"content":" there"},"index":0}]}

data: [DONE]


```

### 处理流式响应

*   Python
    
*   JavaScript
    

```
import requests
import json

response = requests.post(
    'https://api.apiyi.com/v1/chat/completions',
    headers={
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'stream': True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = line[6:]
            if data != '[DONE]':
                chunk = json.loads(data)
                content = chunk['choices'][0]['delta'].get('content', '')
                print(content, end='')


```

```
const response = await fetch('https://api.apiyi.com/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'gpt-3.5-turbo',
    messages: [{role: 'user', content: 'Hello'}],
    stream: true
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const {done, value} = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      if (data !== '[DONE]') {
        const json = JSON.parse(data);
        const content = json.choices[0].delta.content || '';
        process.stdout.write(content);
      }
    }
  }
}


```

错误处理
----

### 错误响应格式

```
{
  "error": {
    "message": "Invalid API key provided",
    "type": "invalid_request_error",
    "param": null,
    "code": "invalid_api_key"
  }
}


```

### 常见错误码

<table><thead><tr><th>错误码</th><th>HTTP 状态码</th><th>说明</th></tr></thead><tbody><tr><td>invalid_api_key</td><td>401</td><td>API 密钥无效</td></tr><tr><td>insufficient_quota</td><td>429</td><td>额度不足</td></tr><tr><td>model_not_found</td><td>404</td><td>模型不存在</td></tr><tr><td>invalid_request_error</td><td>400</td><td>请求参数错误</td></tr><tr><td>server_error</td><td>500</td><td>服务器内部错误</td></tr><tr><td>rate_limit_exceeded</td><td>429</td><td>请求频率过高</td></tr></tbody></table>

### 错误处理示例

```
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    if hasattr(e, 'status_code'):
        if e.status_code == 401:
            print("API密钥无效")
        elif e.status_code == 429:
            print("请求过于频繁或额度不足")
        elif e.status_code == 500:
            print("服务器错误，请稍后重试")
    else:
        print(f"未知错误：{str(e)}")


```

最佳实践
----

### 1. 请求优化

*   **合理设置 max_tokens**：避免不必要的长输出
*   **使用 temperature**：控制输出的随机性
*   **批量处理**：合并多个请求减少调用次数

### 2. 错误重试

实现指数退避的重试机制：

```
import time
import random

def retry_with_backoff(func, max_retries=3):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise e
            wait_time = (2 ** i) + random.uniform(0, 1)
            time.sleep(wait_time)


```

### 3. 安全建议

*   **保护 API 密钥**：使用环境变量存储
*   **限制权限**：为不同应用创建不同的密钥
*   **监控使用**：定期检查 API 使用日志

### 4. 性能优化

*   **使用流式输出**：提升用户体验
*   **缓存响应**：对相同请求缓存结果
*   **并发控制**：合理控制并发请求数

速率限制
----

API 易 实施以下速率限制：

<table><thead><tr><th>限制类型</th><th>限制值</th><th>说明</th></tr></thead><tbody><tr><td>RPM (每分钟请求数)</td><td>3000</td><td>每个 API 密钥</td></tr><tr><td>TPM (每分钟令牌数)</td><td>1000000</td><td>每个 API 密钥</td></tr><tr><td>并发请求数</td><td>100</td><td>同时处理的请求</td></tr></tbody></table>

超出限制时会返回 429 错误，请合理控制请求频率。

需要帮助？
-----

*   查看 [完整 API 文档](https://docs.apiyi.com/api-reference/introduction)
*   访问 [API 易官网](https://api.apiyi.com/)
*   联系技术支持：[support@apiyi.com](mailto:support@apiyi.com)