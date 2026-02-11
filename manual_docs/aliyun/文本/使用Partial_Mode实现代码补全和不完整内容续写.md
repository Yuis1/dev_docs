---
url: https://help.aliyun.com/document_detail/2862210.html?mode=pure
title: "使用Partial Mode实现代码补全和不完整内容续写-大模型服务平台百炼-阿里云"
captured_at: "2026-01-25T01:24:21.587Z"
---


# 使用Partial Mode实现代码补全和不完整内容续写-大模型服务平台百炼-阿里云

在代码补全、文本续写等场景中，需要模型从已有的文本片段（前缀）开始继续生成。Partial Mode 可提供精确控制能力，确保模型输出的内容紧密衔接提供的前缀，提升生成结果的准确性与可控性。

## 使用方式

需在`messages` 数组中将最后一条消息的 `role` 设置为 `assistant`，并在其 `content` 中提供前缀，在此消息中设置参数 `"partial": true`。`messages`格式如下：


**
 **


```
[
 {
 "role": "user",
 "content": "请补全这个斐波那契函数，勿添加其它内容"
 },
 {
 "role": "assistant",
 "content": "def calculate_fibonacci(n):\n if n


模型会以前缀内容为起点开始生成。

## 支持的模型

- **通义千问Max 系列**qwen3-max、qwen3-max-2025-09-23、qwen3-max-preview（非思考模式）、qwen-max、qwen-max-latest、qwen-max-2024-09-19及之后的快照模型
- **通义千问Plus 系列（非思考模式）**qwen-plus、qwen-plus-latest、qwen-plus-2024-09-19及之后的快照模型
- **通义千问Flash 系列（非思考模式）**qwen-flash、qwen-flash-2025-07-28及之后的快照模型
- **通义千问Coder 系列**qwen3-coder-plus、qwen3-coder-flash、qwen3-coder-480b-a35b-instruct、qwen3-coder-30b-a3b-instruct、qwen-coder-plus、qwen-coder-plus-latest、qwen-coder-plus-2024-11-06、qwen-coder-turbo、qwen-coder-turbo-latest、qwen-coder-turbo-2024-09-19、qwen2.5-coder-32b-instruct、qwen2.5-coder-14b-instruct、qwen2.5-coder-7b-instruct、qwen2.5-coder-3b-instruct、qwen2.5-coder-1.5b-instruct、qwen2.5-coder-0.5b-instruct
- **通义千问VL 系列****qwen3-vl-plus 系列（非思考模式）**qwen3-vl-plus、qwen3-vl-plus-2025-09-23及之后的快照模型
- **qwen3-vl-flash 系列（非思考模式）**qwen3-vl-flash、qwen3-vl-flash-2025-10-15及之后的快照模型
- **qwen-vl-max 系列**qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2024-08-09及之后的快照模型
- **qwen-vl-plus 系列**qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-2024-08-09及之后的快照模型

**通义千问Turbo 系列（非思考模式）**

qwen-turbo、qwen-turbo-latest、qwen-turbo-2024-09-19及之后的快照模型

**通义千问开源系列**

Qwen3 开源模型（非思考模式）、qwen2.5-72b-instruct、qwen2.5-32b-instruct、qwen2.5-14b-instruct、qwen2.5-7b-instruct、qwen2.5-3b-instruct、qwen2.5-1.5b-instruct、qwen2.5-0.5b-instruct、Qwen3-VL开源模型（非思考模式）

**通义千问Math 系列**

qwen-math-plus、qwen-math-plus-latest、qwen-math-plus-0919、qwen-math-turbo、qwen-math-turbo-latest、qwen-math-turbo-0919、qwen2.5-math-72b-instruct、qwen2.5-math-7b-instruct、qwen2.5-math-1.5b-instruct

****重要**

思考模式模型暂不支持前缀续写功能。

## 快速开始

### 前提条件

已[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并 [配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过 OpenAI SDK 或 DashScope SDK 进行调用，需要[安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk#210ee28162bs7)。如果您是子业务空间的成员，请确保超级管理员已为该业务空间进行 [模型授权操作](https://help.aliyun.com/zh/model-studio/model-authentication-instructions)。

****说明**

暂不支持 DashScope Java SDK。

### 示例代码

代码补全是 Partial Mode 的核心应用场景。以下示例演示如何使用 `qwen3-coder-plus` 模型补全一个 Python 函数。

OpenAI兼容

DashScope

**


**


Python

Node.js

curl

**


**


**
 **


```
import os
from openai import OpenAI


# 1. 初始化客户端

client = OpenAI(
 # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
 # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


# 2. 定义需要补全的代码前缀

prefix = """def calculate_fibonacci(n):
 if n


### 返回结果


**
 **


```
def calculate_fibonacci(n):
 if n


**
 **


```
import OpenAI from "openai";

const openai = new OpenAI({
 // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 apiKey: process.env.DASHSCOPE_API_KEY,
 // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

// 定义需要补全的代码前缀
const prefix = `def calculate_fibonacci(n):
 if n


**
 **


```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
 "model": "qwen3-coder-plus",
 "messages": [
 {
 "role": "user",
 "content": "请补全这个斐波那契函数，勿添加其它内容"
 },
 {
 "role": "assistant",
 "content": "def calculate_fibonacci(n):\n if n


### 返回结果


**
 **


```
{
 "choices": [
 {
 "message": {
 "content": " return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
 "role": "assistant"
 },
 "finish_reason": "stop",
 "index": 0,
 "logprobs": null
 }
 ],
 "object": "chat.completion",
 "usage": {
 "prompt_tokens": 48,
 "completion_tokens": 19,
 "total_tokens": 67,
 "prompt_tokens_details": {
 "cache_type": "implicit",
 "cached_tokens": 0
 }
 },
 "created": 1756800231,
 "system_fingerprint": null,
 "model": "qwen3-coder-plus",
 "id": "chatcmpl-d103b1cf-4bda-942f-92d6-d7ecabfeeccb"
}

```


Python

curl

**


**


**
 **


```
import os
import dashscope


# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
 {
 "role": "user",
 "content": "请补全这个斐波那契函数，勿添加其它内容"
 },
 {
 "role": "assistant",
 "content": "def calculate_fibonacci(n):\n if n


### 返回结果


**
 **


```
def calculate_fibonacci(n):
 if n


**
 **


```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===

curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
 "model": "qwen3-coder-plus",
 "input":{
 "messages":[
 {
 "role": "user",
 "content": "请补全这个斐波那契函数，勿添加其它内容"
 },
 {
 "role": "assistant",
 "content": "def calculate_fibonacci(n):\n if n


### 返回结果


**
 **


```
{
 "output": {
 "choices": [
 {
 "message": {
 "content": " return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
 "role": "assistant"
 },
 "finish_reason": "stop"
 }
 ]
 },
 "usage": {
 "total_tokens": 67,
 "output_tokens": 19,
 "input_tokens": 48,
 "prompt_tokens_details": {
 "cached_tokens": 0
 }
 },
 "request_id": "c61c62e5-cf97-90bc-a4ee-50e5e117b93f"
}

```


## 使用示例

### 传入图片或视频

通义千问VL模型支持在输入图像、视频数据时进行前缀续写，可应用于产品介绍、社交媒体内容创作、新闻稿生成、创意文案等场景。

OpenAI兼容

DashScope

**


**


Python

Node.js

curl

**


**


**
 **


```
import os
from openai import OpenAI

client = OpenAI(
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
 # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
 model="qwen3-vl-plus",
 messages=[
 {
 "role": "user",
 "content": [
 {
 "type": "image_url",
 "image_url": {
 "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
 },
 },
 {"type": "text", "text": "我要发社交媒体，请帮我想一下文案。"},
 ],
 },
 {
 "role": "assistant",
 "content": "今天发现了一家宝藏咖啡馆",
 "partial": True,
 },
 ],
)
print(completion.choices[0].message.content)

```


### 返回结果


**
 **


```
，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光

希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。

```


**
 **


```
import OpenAI from "openai";

const openai = new OpenAI({
 // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 apiKey: process.env.DASHSCOPE_API_KEY,
 // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
 const response = await openai.chat.completions.create({
 model: "qwen3-vl-plus",
 messages: [
 {
 role: "user",
 content: [
 {
 type: "image_url",
 image_url: {
 "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
 }
 },
 {
 type: "text",
 text: "我要发社交媒体，请帮我想一下文案。"
 }
 ]
 },
 {
 role: "assistant",
 content: "今天发现了一家宝藏咖啡馆",
 "partial": true
 }
 ]
 });
 console.log(response.choices[0].message.content);
}

main();

```


**
 **


```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# === 执行时请删除该注释 ===
curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
 "model": "qwen3-vl-plus",
 "messages": [
 {
 "role": "user",
 "content": [
 {
 "type": "image_url",
 "image_url": {
 "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
 }
 },
 {
 "type": "text",
 "text": "我要发社交媒体，请帮我想一下文案。"
 }
 ]
 },
 {
 "role": "assistant",
 "content": "今天发现了一家宝藏咖啡馆",
 "partial": true
 }
 ]
}'

```


### 返回结果


**
 **


```
{
 "choices": [
 {
 "message": {
 "content": "，这款提拉米苏简直是味蕾的享受！每一口都是咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光\n\n希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。",
 "role": "assistant"
 },
 "finish_reason": "stop",
 "index": 0,
 "logprobs": null
 }
 ],
 "object": "chat.completion",
 "usage": {
 "prompt_tokens": 282,
 "completion_tokens": 56,
 "total_tokens": 338,
 "prompt_tokens_details": {
 "cached_tokens": 0
 }
 },
 "created": 1756802933,
 "system_fingerprint": null,
 "model": "qwen3-vl-plus",
 "id": "chatcmpl-5780cbb7-ebae-9c63-b098-f8cc49e321f0"
}

```


Python

curl

**


**


**
 **


```
import os
import dashscope


# 使用新加坡地域服务，请启用下一行；如使用北京地域，则注释掉此行
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

messages = [
 {
 "role": "user",
 "content": [
 {
 "image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
 },
 {"text": "我要发社交媒体，请帮我想一下文案。"},
 ],
 },
 {"role": "assistant", "content": "今天发现了一家宝藏咖啡馆", "partial": True},
]

response = dashscope.MultiModalConversation.call(
 #若没有配置环境变量， 请用百炼API Key将下行替换为： api_key ="sk-xxx"
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 model="qwen3-vl-plus",
 messages=messages
)

print(response.output.choices[0].message.content[0]["text"])

```


### 返回结果


**
 **


```
，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光

希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。

```


**
 **


```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# === 执行时请删除该注释 ===
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
 "model": "qwen3-vl-plus",
 "input":{
 "messages":[
 {"role": "user",
 "content": [
 {"image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"},
 {"text": "我要发社交媒体，请帮我想一下文案。"}]
 },
 {"role": "assistant",
 "content": "今天发现了一家宝藏咖啡馆",
 "partial": true
 }
 ]
 }
}'

```


### 返回结果


**
 **


```
{
 "output": {
 "choices": [
 {
 "message": {
 "content": [
 {
 "text": "，这款提拉米苏简直是味蕾的享受！每一口都能感受到咖啡与奶油的完美融合，幸福感爆棚～ #美食分享 #提拉米苏 #咖啡时光\n\n希望你喜欢这个文案！如果有任何修改需求，请随时告诉我。"
 }
 ],
 "role": "assistant"
 },
 "finish_reason": "stop"
 }
 ]
 },
 "usage": {
 "total_tokens": 339,
 "input_tokens_details": {
 "image_tokens": 258,
 "text_tokens": 24
 },
 "output_tokens": 57,
 "input_tokens": 282,
 "output_tokens_details": {
 "text_tokens": 57
 },
 "image_tokens": 258
 },
 "request_id": "c741328c-23dc-9286-bfa7-626a4092ca09"
}

```


### 基于不完整输出进行续写

如果大模型返回不完整的内容，可使用 Partial Mode 对不完整的内容续写，使其语义完整。大模型可能返回不完整内容的情况：

- `max_tokens`参数设置过小，使模型返回被截断的内容。
- 非流式输出触发超时，已生成的内容不完整。

> 超时不再报错，而是将已生成内容返回，详情参见[如何处理模型超时的情况](https://help.aliyun.com/zh/model-studio/text-generation#11241147efwpm)。

OpenAI兼容

DashScope

**


**


Python

Node.js

**


**


**
 **


```
import os
from openai import OpenAI


# 初始化客户端
client = OpenAI(
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
 # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def chat_completion(messages,max_tokens=None):
 response = client.chat.completions.create(
 model="qwen-plus",
 messages=messages,
 max_tokens=max_tokens
 )
 print(f"###停止生成原因：{response.choices[0].finish_reason}")

 return response.choices[0].message.content


# 使用示例
messages = [{"role": "user", "content": "请写一个短篇科幻故事"}]


# 第一轮调用，设置max_tokens为40
first_content = chat_completion(messages, max_tokens=40)
print(first_content)
# 将第一轮的响应加入到assistant message，并设置partial=True
messages.append({"role": "assistant", "content": first_content, "partial": True})


# 第二轮调用
second_content = chat_completion(messages)
print("###完整内容：")
print(first_content+second_content)

```


### 返回结果

停止生成原因为`length`表示触发了`max_tokens`的限制；停止生成原因为`stop`表示大模型生成自然结束，或触发了`stop`参数。


**
 **


```
###停止生成原因：length
**《记忆的尽头》**

在遥远的未来，地球早已不再适合人类居住。大气层被污染，海洋干涸，城市变成了废墟。人类被迫迁移到一颗名为“
###停止生成原因：stop
###完整内容：
**《记忆的尽头》**

在遥远的未来，地球早已不再适合人类居住。大气层被污染，海洋干涸，城市变成了废墟。人类被迫迁移到一颗名为“伊甸星”的宜居星球，那里有蔚蓝的天空、清新的空气和无尽的资源。

然而，伊甸星并非真正的天堂。它没有人类的历史，没有过去，也没有记忆。

......

**“如果我们忘记了自己是谁，我们还算是人类吗？”**

——完——

```


**
 **


```
import OpenAI from "openai";

const openai = new OpenAI({
 // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
 // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 apiKey: process.env.DASHSCOPE_API_KEY,
 // 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
 baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function chatCompletion(messages, maxTokens = null) {
 const completion = await openai.chat.completions.create({
 model: "qwen-plus",
 messages: messages,
 max_tokens: maxTokens
 });

 console.log(`###停止生成原因：${completion.choices[0].finish_reason}`);
 return completion.choices[0].message.content;
}

// 使用示例
async function main() {
 let messages = [{"role": "user", "content": "请写一个短篇科幻故事"}];

 try {
 // 第一轮调用，设置max_tokens为40
 const firstContent = await chatCompletion(messages, 40);
 console.log(firstContent);

 // 将第一轮的响应加入到assistant message，并设置partial=true
 messages.push({"role": "assistant", "content": firstContent, "partial": true});

 // 第二轮调用
 const secondContent = await chatCompletion(messages);
 console.log("###完整内容：");
 console.log(firstContent + secondContent);

 } catch (error) {
 console.error('执行出错:', error);
 }
}

// 运行示例
main();

```


Python

**


**


### 示例代码


**
 **


```
import os
import dashscope


# 若使用新加坡地域的模型，请释放下列注释
# dashscope.base_http_api_url = "https://dashscope-intl.aliyuncs.com/api/v1"

def chat_completion(messages, max_tokens=None):
 response = dashscope.Generation.call(
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
 # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 model='qwen-plus',
 messages=messages,
 max_tokens=max_tokens,
 result_format='message',
 )

 print(f"###停止生成原因：{response.output.choices[0].finish_reason}")
 return response.output.choices[0].message.content


# 使用示例
messages = [{"role": "user", "content": "请写一个短篇科幻故事"}]


# 第一轮调用，设置max_tokens为40
first_content = chat_completion(messages, max_tokens=40)
print(first_content)


# 将第一轮的响应加入到assistant message，并设置partial=True
messages.append({"role": "assistant", "content": first_content, "partial": True})


# 第二轮调用
second_content = chat_completion(messages)
print("###完整内容：")
print(first_content + second_content)

```


### 返回结果


**
 **


```
###停止生成原因：length
标题：**《时间折纸》**

---

公元2179年，人类终于掌握了时间旅行的技术。但这项技术并不是通过庞大的机器或复杂的能量场实现的，而是一
###停止生成原因：stop
###完整内容：
标题：**《时间折纸》**

---

公元2179年，人类终于掌握了时间旅行的技术。但这项技术并不是通过庞大的机器或复杂的能量场实现的，而是一张纸。

一张能折叠时间的纸。

它被称为“时间折纸”，由一种来自外星文明的未知物质制成。科学家们无法解释它的原理，只知道，只要在纸上画出某个场景，再进行特定的折叠方式，就能打开一扇通往过去或未来的门。

......

“你不是时间的钥匙，只是提醒我们，未来，始终掌握在我们手中。”

然后，我把它撕成了碎片。

---

**（完）**

```


## 计费说明

根据请求的输入 Token 和输出 Token 计费。前缀部分作为输入 Token。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
