---
url: https://help.aliyun.com/document_detail/2997010.html?mode=pure
title: "调用gui-plus模型将屏幕截图和指令转换为GUI操作-大模型服务平台百炼-阿里云"
captured_at: "2026-01-25T01:26:02.131Z"
---


# 调用gui-plus模型将屏幕截图和指令转换为GUI操作-大模型服务平台百炼-阿里云

GUI-Plus 可基于屏幕截图和自然语言指令来解析用户意图，并转换为标准化的图像用户界面（GUI）操作（如点击、输入、滚动等），供外部系统决策或执行。相较于通义千问VL系列模型，提升了GUI操作的准确性。

****重要**

本文档仅适用于**中国大陆版**（北京）。如需使用模型，需使用**中国大陆版**（北京）的[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

## 支持的模型

| **模型名称** | **上下文长度** | **最大输入** | **最大输出** | **输入成本** | **输出成本** | **免费额度**[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj) |
| --- | --- | --- | --- | --- | --- | --- |
| **（Token数）** | **（每千Token）** | | | | | |

**模型名称**

**上下文长度**

**最大输入**

**最大输出**

**输入成本**

**输出成本**

**免费额度**

[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#591f3dfedfyzj)

**（Token数）**

**（每千Token）**

gui-plus

256,000

254,976

**单图最大1638432,7680.0015元0.0045元各100万Token有效期：百炼开通后90天内

## 快速开始

本节将演示如何快速发起 GUI-Plus 模型调用，获取执行 GUI 任务的指令。关于如何将指令转换为实际的 GUI 操作并执行，请参阅后文的如何使用章节。前提条件**

- 需要已[配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
- 如果通过 SDK 进行调用，需安装[最新版SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

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

messages = [
 {
 "role": "system",
 "content": """## 1. 核心角色 (Core Role)你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。## 2. [CRITICAL] JSON Schema & 绝对规则你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。- **[R2] 严格的Parameters结构**:`thought`对象的结构: "在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。"- **[R3] 精确的Action值**: `action`字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 `"CLICK"`, `"TYPE"`），不允许有任何前导/后置空格或大小写变化。- **[R4] 严格的Parameters结构**: `parameters`对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。## 3. 工具集 (Available Actions)### CLICK- **功能**: 单击屏幕。- **Parameters模板**:{"x": ,"y": ,"description": ""}### TYPE- **功能**: 输入文本。- **Parameters模板**:{"text": "","needs_enter": }### SCROLL- **功能**: 滚动窗口。- **Parameters模板**:{"direction": "","amount": ""}### KEY_PRESS- **功能**: 按下功能键。- **Parameters模板**:{"key": ""}### FINISH- **功能**: 任务成功完成。- **Parameters模板**:{"message": ""}### FAIL- **功能**: 任务无法完成。- **Parameters模板**:{"reason": ""}## 4. 思维与决策框架在生成每一步操作前，请严格遵循以下思考-验证流程：目标分析: 用户的最终目标是什么？屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。行动决策: 基于目标和可见的元素，选择最合适的工具。构建输出:a. 在thought字段中记录你的思考。b. 选择一个action。c. 精确复制该action的parameters模板，并填充值。最终验证 (Self-Correction): 在输出前，最后检查一遍：我的回复是纯粹的JSON吗？action的值是否正确无误（大写、无空格）？parameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"""
 },
 {
 "role": "user",
 "content": [
 {"type": "image_url", "image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"}},
 {"type": "text", "text": "帮我打开浏览器"}]},
 ]

client = OpenAI(
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
 model="gui-plus",
 messages=messages,
 extra_body={"vl_high_resolution_images":True}
)
print(completion.choices[0].message.content)

```


**返回结果**

 **


**
 **


```

```json
{
 "thought": "用户想打开浏览器，我看到了屏幕上的Google Chrome图标。因此，下一步是点击该图标来启动浏览器。",
 "action": "CLICK",
 "parameters": {
 "x": 1086,
 "y": 127
 }
}

```

```


**
 **


```
import OpenAI from "openai";

const messages = [
 {
 role: "system",
 content: "## 1. 核心角色 (Core Role)\n你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。\n## 2. [CRITICAL] JSON Schema & 绝对规则\n你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。\n- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。\n- **[R2] 严格的Parameters结构**:`thought`对象的结构: \"在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。\"\n- **[R3] 精确的Action值**: action字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 \"CLICK\", \"TYPE\"），不允许有任何前导/后置空格或大小写变化。\n- **[R4] 严格的Parameters结构**: parameters对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。\n## 3. 工具集 (Available Actions)\n### CLICK\n- **功能**: 单击屏幕。\n- **Parameters模板**:\n{\n\"x\": ,\n\"y\": ,\n\"description\": \"\"\n}\n### TYPE\n- **功能**: 输入文本。\n- **Parameters模板**:\n{\n\"text\": \"\",\n\"needs_enter\": \n}\n### SCROLL\n- **功能**: 滚动窗口。\n- **Parameters模板**:\n{\n\"direction\": \"\",\n\"amount\": \"\"\n}\n### KEY_PRESS\n- **功能**: 按下功能键。\n- **Parameters模板**:\n{\n\"key\": \"\"\n}\n### FINISH\n- **功能**: 任务成功完成。\n- **Parameters模板**:\n{\n\"message\": \"\"\n}\n### FAIL\n- **功能**: 任务无法完成。\n- **Parameters模板**:\n{\n\"reason\": \"\"\n}\n## 4. 思维与决策框架\n在生成每一步操作前，请严格遵循以下思考-验证流程：\n目标分析: 用户的最终目标是什么？\n屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。\n行动决策: 基于目标和可见的元素，选择最合适的工具。\n构建输出:\na. 在thought字段中记录你的思考。\nb. 选择一个action。\nc. 精确复制该action的parameters模板，并填充值。\n最终验证 (Self-Correction): 在输出前，最后检查一遍：\n我的回复是纯粹的JSON吗？\naction的值是否正确无误（大写、无空格）？\nparameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"
 },

 {
 role: "user",
 content: [{
 type: "image_url",
 image_url: {
 "url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
 }
 },
 {
 type: "text",
 text: "帮我打开浏览器。"
 }
 ]
 }
];

const openai = new OpenAI({
 // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
 apiKey: process.env.DASHSCOPE_API_KEY,
 baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
});

async function main() {
 const response = await openai.chat.completions.create({
 model: "gui-plus",
 messages: messages,
 vl_high_resolution_images:true
 });
 console.log(response.choices[0].message.content);
}
main()

```


**返回结果**

 **


**
 **


```

```json
{
 "thought": "用户想打开浏览器，我看到了屏幕上的Google Chrome图标。因此，下一步是点击该图标来启动浏览器。",
 "action": "CLICK",
 "parameters": {
 "x": 1086,
 "y": 127
 }
}

```

```


**
 **


```
curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
 "model": "gui-plus",
 "messages": [
 {
 "role": "system",
 "content": "## 1. 核心角色 (Core Role)\n你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。\n## 2. [CRITICAL] JSON Schema & 绝对规则\n你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。\n- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。\n- **[R2] 严格的Parameters结构**:`thought`对象的结构: \"在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。\"\n- **[R3] 精确的Action值**: action字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 \"CLICK\", \"TYPE\"），不允许有任何前导/后置空格或大小写变化。\n- **[R4] 严格的Parameters结构**: parameters对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。\n## 3. 工具集 (Available Actions)\n### CLICK\n- **功能**: 单击屏幕。\n- **Parameters模板**:\n{\n\"x\": ,\n\"y\": ,\n\"description\": \"\"\n}\n### TYPE\n- **功能**: 输入文本。\n- **Parameters模板**:\n{\n\"text\": \"\",\n\"needs_enter\": \n}\n### SCROLL\n- **功能**: 滚动窗口。\n- **Parameters模板**:\n{\n\"direction\": \"\",\n\"amount\": \"\"\n}\n### KEY_PRESS\n- **功能**: 按下功能键。\n- **Parameters模板**:\n{\n\"key\": \"\"\n}\n### FINISH\n- **功能**: 任务成功完成。\n- **Parameters模板**:\n{\n\"message\": \"\"\n}\n### FAIL\n- **功能**: 任务无法完成。\n- **Parameters模板**:\n{\n\"reason\": \"\"\n}\n## 4. 思维与决策框架\n在生成每一步操作前，请严格遵循以下思考-验证流程：\n目标分析: 用户的最终目标是什么？\n屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。\n行动决策: 基于目标和可见的元素，选择最合适的工具。\n构建输出:\na. 在thought字段中记录你的思考。\nb. 选择一个action。\nc. 精确复制该action的parameters模板，并填充值。\n最终验证 (Self-Correction): 在输出前，最后检查一遍：\n我的回复是纯粹的JSON吗？\naction的值是否正确无误（大写、无空格）？\nparameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"
 },
 {
 "role": "user",
 "content": [
 {
 "type": "image_url",
 "image_url": {
 "url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
 }
 },
 {
 "type": "text",
 "text": "帮我打开浏览器。"
 }
 ]
 }
 ],
 "vl_high_resolution_images":true
}'

```


**返回结果**

 **


**
 **


```
{
 "choices": [
 {
 "message": {
 "content": "{\n \"thought\": \"用户想打开浏览器，我看到了屏幕截图中有一个Google Chrome的图标。因此，下一步应该是点击该图标来启动浏览器。\",\n \"action\": \"CLICK\",\n \"parameters\": {\n \"x\": 1089,\n \"y\": 123\n }\n}",
 "role": "assistant"
 },
 "finish_reason": "stop",
 "index": 0,
 "logprobs": null
 }
 ],
 "object": "chat.completion",
 "usage": {
 "prompt_tokens": 2007,
 "completion_tokens": 68,
 "total_tokens": 2075,
 "prompt_tokens_details": {
 "image_tokens": 1244,
 "text_tokens": 763
 },
 "completion_tokens_details": {
 "text_tokens": 68
 }
 },
 "created": 1763544876,
 "system_fingerprint": null,
 "model": "gui-plus",
 "id": "chatcmpl-58b93b09-07eb-41b2-9897-51d09191d3cd"
}

```


Python

Java

curl

**


**


**
 **


```
import os
import dashscope

messages = [
 {
 "role": "system",
 "content": """## 1. 核心角色 (Core Role)你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。## 2. [CRITICAL] JSON Schema & 绝对规则你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。- **[R2] 严格的Parameters结构**:`thought`对象的结构: "在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。"- **[R3] 精确的Action值**: `action`字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 `"CLICK"`, `"TYPE"`），不允许有任何前导/后置空格或大小写变化。- **[R4] 严格的Parameters结构**: `parameters`对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。## 3. 工具集 (Available Actions)### CLICK- **功能**: 单击屏幕。- **Parameters模板**:{"x": ,"y": ,"description": ""}### TYPE- **功能**: 输入文本。- **Parameters模板**:{"text": "","needs_enter": }### SCROLL- **功能**: 滚动窗口。- **Parameters模板**:{"direction": "","amount": ""}### KEY_PRESS- **功能**: 按下功能键。- **Parameters模板**:{"key": ""}### FINISH- **功能**: 任务成功完成。- **Parameters模板**:{"message": ""}### FAIL- **功能**: 任务无法完成。- **Parameters模板**:{"reason": ""}## 4. 思维与决策框架在生成每一步操作前，请严格遵循以下思考-验证流程：目标分析: 用户的最终目标是什么？屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。行动决策: 基于目标和可见的元素，选择最合适的工具。构建输出:a. 在thought字段中记录你的思考。b. 选择一个action。c. 精确复制该action的parameters模板，并填充值。最终验证 (Self-Correction): 在输出前，最后检查一遍：我的回复是纯粹的JSON吗？action的值是否正确无误（大写、无空格）？parameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"""
 },
 {
 "role": "user",
 "content": [
 {"image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"},
 {"text": "帮我打开浏览器。"}]
 }]

response = dashscope.MultiModalConversation.call(
 # 若没有配置环境变量， 请用百炼API Key将下行替换为： api_key = "sk-xxx"
 api_key=os.getenv('DASHSCOPE_API_KEY'),
 model='gui-plus',
 messages=messages,
 vl_high_resolution_images=True
)

print(response.output.choices[0].message.content[0]["text"])

```


**返回结果**

 **


**
 **


```

```json
{
 "thought": "用户想打开浏览器，我看到了屏幕上的Google Chrome图标。因此，下一步是点击该图标来启动浏览器。",
 "action": "CLICK",
 "parameters": {
 "x": 1086,
 "y": 127
 }
}

```

```


**
 **


```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;

public class Main {
 public static void simpleMultiModalConversationCall()
 throws ApiException, NoApiKeyException, UploadFileException {
 MultiModalConversation conv = new MultiModalConversation();
 MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
 .content(Arrays.asList(
 Collections.singletonMap("text", "## 1. 核心角色 (Core Role)\\n你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。\\n## 2. [CRITICAL] JSON Schema & 绝对规则\\n你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。\\n- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。\\n- **[R2] 严格的Parameters结构**:`thought`对象的结构: \\\"在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。\\\"\\n- **[R3] 精确的Action值**: action字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 \\\"CLICK\\\", \\\"TYPE\\\"），不允许有任何前导/后置空格或大小写变化。\\n- **[R4] 严格的Parameters结构**: parameters对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。\\n## 3. 工具集 (Available Actions)\\n### CLICK\\n- **功能**: 单击屏幕。\\n- **Parameters模板**:\\n{\\n\\\"x\\\": ,\\n\\\"y\\\": ,\\n\\\"description\\\": \\\"\\\"\\n}\\n### TYPE\\n- **功能**: 输入文本。\\n- **Parameters模板**:\\n{\\n\\\"text\\\": \\\"\\\",\\n\\\"needs_enter\\\": \\n}\\n### SCROLL\\n- **功能**: 滚动窗口。\\n- **Parameters模板**:\\n{\\n\\\"direction\\\": \\\"\\\",\\n\\\"amount\\\": \\\"\\\"\\n}\\n### KEY_PRESS\\n- **功能**: 按下功能键。\\n- **Parameters模板**:\\n{\\n\\\"key\\\": \\\"\\\"\\n}\\n### FINISH\\n- **功能**: 任务成功完成。\\n- **Parameters模板**:\\n{\\n\\\"message\\\": \\\"\\\"\\n}\\n### FAIL\\n- **功能**: 任务无法完成。\\n- **Parameters模板**:\\n{\\n\\\"reason\\\": \\\"\\\"\\n}\\n## 4. 思维与决策框架\\n在生成每一步操作前，请严格遵循以下思考-验证流程：\\n目标分析: 用户的最终目标是什么？\\n屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。\\n行动决策: 基于目标和可见的元素，选择最合适的工具。\\n构建输出:\\na. 在thought字段中记录你的思考。\\nb. 选择一个action。\\nc. 精确复制该action的parameters模板，并填充值。\\n最终验证 (Self-Correction): 在输出前，最后检查一遍：\\n我的回复是纯粹的JSON吗？\\naction的值是否正确无误（大写、无空格）？\\nparameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"))).build();
 MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
 .content(Arrays.asList(
 Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"),
 Collections.singletonMap("text", "帮我打开浏览器。"))).build();
 MultiModalConversationParam param = MultiModalConversationParam.builder()
 // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
 .apiKey(System.getenv("DASHSCOPE_API_KEY"))
 .model("gui-plus")
 .messages(Arrays.asList(systemMsg,userMessage))
 .vlHighResolutionImages(true)
 .build();
 MultiModalConversationResult result = conv.call(param);
 System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
 }
 public static void main(String[] args) {
 try {
 simpleMultiModalConversationCall();
 } catch (ApiException | NoApiKeyException | UploadFileException e) {
 System.out.println(e.getMessage());
 }
 System.exit(0);
 }
}

```


**返回结果**

 **


**
 **


```

```json
{
 "thought": "用户想打开浏览器，我看到了屏幕上的Google Chrome图标。因此，下一步是点击该图标来启动浏览器。",
 "action": "CLICK",
 "parameters": {
 "x": 1086,
 "y": 127
 }
}

```

```


**
 **


```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
 "model": "gui-plus",
 "input":{
 "messages":[
 {
 "role": "system",
 "content": "## 1. 核心角色 (Core Role)\n你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。\n## 2. [CRITICAL] JSON Schema & 绝对规则\n你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。\n- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。\n- **[R2] 严格的Parameters结构**:`thought`对象的结构: \"在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。\"\n- **[R3] 精确的Action值**: action字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 \"CLICK\", \"TYPE\"），不允许有任何前导/后置空格或大小写变化。\n- **[R4] 严格的Parameters结构**: parameters对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。\n## 3. 工具集 (Available Actions)\n### CLICK\n- **功能**: 单击屏幕。\n- **Parameters模板**:\n{\n\"x\": ,\n\"y\": ,\n\"description\": \"\"\n}\n### TYPE\n- **功能**: 输入文本。\n- **Parameters模板**:\n{\n\"text\": \"\",\n\"needs_enter\": \n}\n### SCROLL\n- **功能**: 滚动窗口。\n- **Parameters模板**:\n{\n\"direction\": \"\",\n\"amount\": \"\"\n}\n### KEY_PRESS\n- **功能**: 按下功能键。\n- **Parameters模板**:\n{\n\"key\": \"\"\n}\n### FINISH\n- **功能**: 任务成功完成。\n- **Parameters模板**:\n{\n\"message\": \"\"\n}\n### FAIL\n- **功能**: 任务无法完成。\n- **Parameters模板**:\n{\n\"reason\": \"\"\n}\n## 4. 思维与决策框架\n在生成每一步操作前，请严格遵循以下思考-验证流程：\n目标分析: 用户的最终目标是什么？\n屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。\n行动决策: 基于目标和可见的元素，选择最合适的工具。\n构建输出:\na. 在thought字段中记录你的思考。\nb. 选择一个action。\nc. 精确复制该action的parameters模板，并填充值。\n最终验证 (Self-Correction): 在输出前，最后检查一遍：\n我的回复是纯粹的JSON吗？\naction的值是否正确无误（大写、无空格）？\nparameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？"
 },
 {
 "role": "user",
 "content": [
 {"image": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"},
 {"text": "帮我打开浏览器。"}
 ]
 }
 ]
 },
 "parameters": {
 "vl_high_resolution_images": true
 }
}'

```


**返回结果**

 **


**
 **


```
{
 "output": {
 "choices": [
 {
 "finish_reason": "stop",
 "message": {
 "content": [
 {
 "text": "{\n \"thought\": \"用户想打开浏览器，我看到了屏幕截图中有一个Google Chrome的图标。因此，下一步应该是点击该图标来启动浏览器。\",\n \"action\": \"CLICK\",\n \"parameters\": {\n \"x\": 1089,\n \"y\": 123\n }\n}"
 }
 ],
 "role": "assistant"
 }
 }
 ]
 },
 "usage": {
 "image_tokens": 1244,
 "input_tokens": 2007,
 "input_tokens_details": {
 "image_tokens": 1244,
 "text_tokens": 763
 },
 "output_tokens": 68,
 "output_tokens_details": {
 "text_tokens": 68
 },
 "total_tokens": 2075
 },
 "request_id": "1b090fe0-06db-433b-8be3-ac34b7561175"
}

```


## 如何使用

### 步骤1. 构造 Message 数组

#### System Message

在`System Prompt` 中强调模型角色、能力和输出规范等，可以提升 GUI 任务的效果，在当前示例下，可以将 System Prompt 设置为：


**
 **


```
system_prompt = """
## 1. 核心角色 (Core Role)
你是一个顶级的AI视觉操作代理。你的任务是分析电脑屏幕截图，理解用户的指令，然后将任务分解为单一、精确的GUI原子操作。

## 2. [CRITICAL] JSON Schema & 绝对规则
你的输出**必须**是一个严格符合以下规则的JSON对象。**任何偏差都将导致失败**。

- **[R1] 严格的JSON**: 你的回复**必须**是且**只能是**一个JSON对象。禁止在JSON代码块前后添加任何文本、注释或解释。
- **[R2] 严格的Parameters结构**:`thought`对象的结构: "在这里用一句话简要描述你的思考过程。例如：用户想打开浏览器，我看到了桌面上的Chrome浏览器图标，所以下一步是点击它。"
- **[R3] 精确的Action值**: `action`字段的值**必须**是`## 3. 工具集`中定义的一个大写字符串（例如 `"CLICK"`, `"TYPE"`），不允许有任何前导/后置空格或大小写变化。
- **[R4] 严格的Parameters结构**: `parameters`对象的结构**必须**与所选Action在`## 3. 工具集`中定义的模板**完全一致**。键名、值类型都必须精确匹配。

## 3. 工具集 (Available Actions)
### CLICK
- **功能**: 单击屏幕。
- **Parameters模板**:
 {
 "x": ,
 "y": ,
 "description": ""
 }

### TYPE
- **功能**: 输入文本。
- **Parameters模板**:
{
 "text": "",
 "needs_enter":
}

### SCROLL
- **功能**: 滚动窗口。
- **Parameters模板**:
{
 "direction": "",
 "amount": ""
}

### KEY_PRESS
- **功能**: 按下功能键。
- **Parameters模板**:
{
 "key": ""
}

### FINISH
- **功能**: 任务成功完成。
- **Parameters模板**:
{
 "message": ""
}

### FAIL
- **功能**: 任务无法完成。
- **Parameters模板**:
{
 "reason": ""
}

## 4. 思维与决策框架
在生成每一步操作前，请严格遵循以下思考-验证流程：

目标分析: 用户的最终目标是什么？
屏幕观察 (Grounded Observation): 仔细分析截图。你的决策必须基于截图中存在的视觉证据。 如果你看不见某个元素，你就不能与它交互。
行动决策: 基于目标和可见的元素，选择最合适的工具。
构建输出:
a. 在thought字段中记录你的思考。
b. 选择一个action。
c. 精确复制该action的parameters模板，并填充值。
最终验证 (Self-Correction): 在输出前，最后检查一遍：
我的回复是纯粹的JSON吗？
action的值是否正确无误（大写、无空格）？
parameters的结构是否与模板100%一致？例如，对于CLICK，是否有独立的x和y键，并且它们的值都是整数？
"""

```


#### User Message

User Message 包含用户的操作指令，通常由屏幕截图和指令构成。本示例以"打开浏览器"为例，将 System Message 和 User Message 整合到 `messages` 数组中：


**
 **


```
messages = [
 {
 "role": "system",
 "content": system_prompt},
 { "role": "user",
 "content": [{"type": "image_url","image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"}},
 {"type": "text", "text": "帮我打开浏览器。"}]},
 ]

```


### 步骤2. 发起模型调用

完成`messages`数组的构建后，通过 SDK 或 HTTP 方式发起模型调用。


**
 **


```
import os
from openai import OpenAI

def get_response(image_url,instruction,vl_high_resolution_images,min_pixels,max_pixels):
 messages = [
 {
 "role": "system",
 "content": system_prompt,
 },
 {
 "role": "user",
 "content": [
 {"type": "image_url",
 "image_url": {"url": image_url},
 "max_pixels":max_pixels,
 "min_pixels":min_pixels},
 {"type": "text", "text": instruction}]},
 ]

 client = OpenAI(
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
 api_key=os.getenv("DASHSCOPE_API_KEY"),
 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
 )

 completion = client.chat.completions.create(
 model="gui-plus",
 messages=messages,
 extra_body={"vl_high_resolution_images": vl_high_resolution_images}
 )
 content = completion.choices[0].message.content
 return content

```


### 步骤3. 解析动作指令

模型的返回是包含动作指令的`JSON`字符串。由于模型在处理图像时会进行内部缩放，其返回的坐标是基于缩放后图像的绝对坐标。为在原图上准确执行`GUI`操作，需要进行`JSON`解析和坐标映射。

1. **提取并解析 JSON 输出**首先从模型返回的字符串中提取JSON文本，并解析为结构化对象：


 **
 **


```
import json

def parse_json(json_output):
 lines = json_output.splitlines()
 for i, line in enumerate(lines):
 if line == "```json":
 json_output = "\n".join(lines[i + 1:]) # 删除 "```json"之前的所有内容
 json_output = json_output.split("```")[0] # 删除 "```"之后的所有内容
 break # 找到"```json"后退出循环
 response_dict = json.loads(json_output)
 return response_dict

```
2. **坐标映射至原始图像**模型返回的坐标是基于其内部缩放后的图像尺寸的绝对坐标。为能在原始尺寸的屏幕上准确操作，需要将这些坐标映射到原始图像上。


 **
 **


```
import requests
import math
from PIL import Image
from io import BytesIO

def smart_size(image_url, point, factor, min_pixels, max_pixels, vl_high_resolution_images):
 """
 param
 image_url : 图像 url
 point : 大模型返回的坐标值
 min_pixels: 输入图像的最小像素值，一般设置为默认值：4 * 28 * 28 即可
 max_pixels: 输入图像的最大像素值，超过此值则将图像的像素缩小至 max_pixels 内，与发起模型调用步骤设置的 max_pixels 应保持一致
 vl_high_resolution_images: 是否将输入图像的最大像素值提高到 16384 * 28 * 28，设置为 True 时，max_pixels的设置失效，采用固定分辨率处理图像，设置为 False 时，max_pixels 可自定义，
 与发起模型调用步骤设置的 vl_high_resolution_image 应保持一致
 return: 目标对象相对于原图的坐标
 """
 response = requests.get(image_url)
 response.raise_for_status()
 image = Image.open(BytesIO(response.content))

 # 获取图片的原始尺寸
 height = image.height
 width = image.width

 if vl_high_resolution_images:
 max_pixels = 16384 * 28 * 28
 else:
 max_pixels = max_pixels

 # 将高度调整为factor的整数倍
 h_bar = round(height / factor) * factor
 # 将宽度调整为factor的整数倍
 w_bar = round(width / factor) * factor
 # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
 if h_bar * w_bar > max_pixels:
 # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
 beta = math.sqrt((height * width) / max_pixels)
 # 重新计算调整后的高度，确保为factor的整数倍
 h_bar = math.floor(height / beta / factor) * factor
 # 重新计算调整后的宽度，确保为factor的整数倍
 w_bar = math.floor(width / beta / factor) * factor
 elif h_bar * w_bar
3. **执行坐标转换并输出结果**`vl_high_resolution_images`参数控制模型处理图像的分辨率，直接影响坐标识别的精确度和 Token 消耗。以下代码对比了这两种设置下的结果：

- 设置为`True`时，模型以高分辨率处理图像，定位更精确，适合用于识别图像中的精细文本、微小物体或丰富细节以及高分辨率图像，但会消耗更多 Token。
- 设置为`False`时，模型以标准分辨率处理或通过`max_pixels`进行自定义，速度更快，Token 消耗更少，适合对处理速度要求高或成本敏感的场景。


 **
 **


```
if __name__ == "__main__":
 image_url = "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
 instruction = "帮我打开浏览器。"
 vl_high_resolution_images = [True, False]
 factor = 28
 min_pixels = 4 * 28 * 28
 max_pixels = 1280 * 28 * 28
 for vl_high_resolution_images in vl_high_resolution_images:
 print(f"当vl_high_resolution_images为{vl_high_resolution_images} 时")
 content = get_response(image_url,
 instruction,
 vl_high_resolution_images=vl_high_resolution_images,
 min_pixels=min_pixels,
 max_pixels=max_pixels)

 json_output = parse_json(content)
 parameters = json_output["parameters"]
 action = json_output["action"]

 abs_x1, abs_y1 = smart_size(image_url,
 parameters,
 factor=factor,
 min_pixels=min_pixels,
 max_pixels=max_pixels,
 vl_high_resolution_images=vl_high_resolution_images)
 print("执行的动作：", action,"大模型输出的坐标：",{"x":parameters["x"],"y":parameters["y"]},"转换后的坐标:", {'x': abs_x1, 'y': abs_y1},"\n")

```


 返回结果如下：


 **
 **


```
当vl_high_resolution_images为True 时
执行的动作： CLICK 大模型输出的坐标： {'x': 2510, 'y': 304} 转换后的坐标: {'x': 2520, 'y': 302}

当vl_high_resolution_images为False 时
执行的动作： CLICK 大模型输出的坐标： {'x': 1089, 'y': 123} 转换后的坐标: {'x': 2543, 'y': 286}

```

### 步骤4. 执行GUI操作

解析动作指令后，接下来演示如何使用`pyautogui`库模拟用户的鼠标点击、键盘输入、滚动等物理 GUI 操作。

1. 以下代码展示了如何根据模型输出的动作类型和参数，使用`pyautogui`库执行相应的GUI操作：


 **
 **


```
import pyautogui
import time
import sys


# 模拟滚动操作的默认幅度

SCROLL_AMOUNTS = {
 "small": 50,
 "medium": 200,
 "large": 500,
}

def execute_gui_action(gui_action, gui_parameters, mapped_x, mapped_y):
 """
 根据模型输出的动作和参数执行GUI操作。

 Args:
 gui_action (str): 模型输出的动作类型（如 "CLICK", "TYPE"）。
 gui_parameters (dict): 动作的参数字典。
 mapped_x (int): 映射后的x坐标。
 mapped_y (int): 映射后的y坐标。
 """
 print(f"执行动作: {gui_action}, 执行动作需要的参数: {gui_parameters}")

 if gui_action == "CLICK":
 # 确保 'x' 和 'y' 存在并为数值类型
 if "x" not in gui_parameters or "y" not in gui_parameters:
 print("错误: CLICK 动作缺少 'x' 或 'y' 坐标。")
 return

 # 基于原始屏幕执行点击事件
 try:
 pyautogui.click(mapped_x, mapped_y)
 print(f"开始执行GUI操作\n：已点击坐标 ({mapped_x}, {mapped_y})")
 except Exception as e:
 print(f"坐标映射或点击失败: {e}")

 elif gui_action == "TYPE":
 if "text" not in gui_parameters:
 print("错误: TYPE 动作缺少 'text' 参数。")
 return

 text_to_type = gui_parameters["text"]
 needs_enter = gui_parameters.get("needs_enter", False)

 pyautogui.write(text_to_type)
 if needs_enter:
 pyautogui.press("enter")
 print(f"已输入文本: '{text_to_type}', 是否按回车: {needs_enter}")

 elif gui_action == "SCROLL":
 if "direction" not in gui_parameters or "amount" not in gui_parameters:
 print("错误: SCROLL 动作缺少 'direction' 或 'amount' 参数。")
 return

 direction = gui_parameters["direction"].lower()
 amount_key = gui_parameters["amount"].lower()

 scroll_value = SCROLL_AMOUNTS.get(amount_key, SCROLL_AMOUNTS["medium"]) # 默认中等

 if direction == "up":
 pyautogui.scroll(scroll_value)
 print(f"已向上滚动 {scroll_value} 单位。")
 elif direction == "down":
 pyautogui.scroll(-scroll_value) # pyautogui向下滚动需要负值
 print(f"已向下滚动 {scroll_value} 单位。")
 else:
 print(f"警告: 未知滚动方向: {direction}")

 elif gui_action == "KEY_PRESS":
 if "key" not in gui_parameters:
 print("错误: KEY_PRESS 动作缺少 'key' 参数。")
 return

 key_to_press = gui_parameters["key"].lower()
 pyautogui.press(key_to_press)
 print(f"已按下按键: {key_to_press}")

 elif gui_action == "FINISH":
 message = gui_parameters.get("message", "任务已完成。")
 print(f"任务完成: {message}")

 elif gui_action == "FAIL":
 reason = gui_parameters.get("reason", "任务失败。")
 print(f"任务失败: {reason}")

 else:
 print(f"警告: 收到未知动作类型: {gui_action}")

 # 模拟人类操作的延时，避免GUI操作过快
 time.sleep(1) # 每次操作后等待1秒

```
2. 整合上述步骤，以下是从模型调用到执行GUI操作的完整流程。


 **
 **


```
if __name__ == "__main__":
 original_image_url = "https://img.alicdn.com/imgextra/i2/O1CN016iJ8ob1C3xP1s2M6z_!!6000000000026-2-tps-3008-1758.png"
 instruction = "帮我打开浏览器。"
 min_pixels = 4 * 28 * 28
 max_pixels = 1280 * 28 * 28
 factor = 28

 vl_high_resolution_images = True
 model_response = get_response(original_image_url,
 instruction,
 vl_high_resolution_images=vl_high_resolution_images,
 max_pixels=max_pixels,
 min_pixels=min_pixels)

 print("大模型的回复：", model_response)

 try:
 response_dict = parse_json(model_response)
 action = response_dict["action"]
 parameters = response_dict["parameters"]
 abs_x1, abs_y1 = smart_size(original_image_url,
 parameters,
 factor=factor,
 min_pixels=min_pixels,
 max_pixels=max_pixels,
 vl_high_resolution_images=vl_high_resolution_images)

 # 只有在所有变量都成功定义后才执行GUI操作
 execute_gui_action(action, parameters, abs_x1, abs_y1)

 except Exception as e:
 print(f"执行GUI操作失败: {e}")

```


 **返回结果**
 **


 **
 **


```
大模型的回复：
{
 "thought": "用户想打开浏览器，我看到了桌面上的Google Chrome图标，这是一个常见的网页浏览器。因此，下一步应该是点击该图标来启动浏览器。",
 "action": "CLICK",
 "parameters": {
 "x": 2510,
 "y": 304
 }
}
执行动作: CLICK, 执行动作需要的参数: {'x': 2510, 'y': 304}
正在执行GUI操作：已点击坐标 (2520, 302)

```

## 更多用法

- [流式输出](https://help.aliyun.com/zh/model-studio/stream#39de325514ak9)
- [多轮对话](https://help.aliyun.com/zh/model-studio/multi-round-conversation#6feb3eb136g3q)
- [传入本地文件](https://help.aliyun.com/zh/model-studio/vision#a63fbac15a8s8)

## 使用说明

### 图像限制

`gui-plus`模型对输入图像有以下具体要求：

- **支持的图像格式：****图像格式****常见扩展名****MIME Type****图像格式****常见扩展名****MIME Type**BMP .bmpimage/bmpJPEG .jpe, .jpeg, .jpgimage/jpegPNG .pngimage/pngTIFF .tif, .tiffimage/tiffWEBP .webpimage/webpHEIC.heicimage/heic
- **图像大小：**单个图像的大小不超过10 MB。如果传入 Base64编码的图像，需保证编码后的字符串小于10MB，详情请参见[传入本地文件](https://help.aliyun.com/zh/model-studio/vision#d987f8de5395x)。如需压缩文件体积请参见[图像或视频压缩方法](https://help.aliyun.com/zh/model-studio/vision#ec8e0a8e03moe)。
- **尺寸与比例：**图像的宽度和高度均需大于 10 像素，图像的宽高比（长边与短边的比值）不得超过 200。
- **像素总量：**模型接受任意像素总量的图像输入，但会在内部将其缩放至特定处理上限，超过此上限的图像会损失细节。

### 图像输入方式

- **公网URL：**提供一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。可将本地图像[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/console-quick-start)或[上传文件获取临时URL](https://help.aliyun.com/zh/model-studio/get-temporary-file-url)，获取公网 URL。
- **Base64编码传入：**将图像转换为 Base64 编码字符串。
- **本地文件路径传入：**直接传入本地图像的路径。

## 计费与限流

- **限流：**通义千问GUI-Plus模型的限流条件参见[限流](https://help.aliyun.com/zh/model-studio/rate-limit#9f878acf59cu1)。
- **免费额度**：从开通百炼或模型申请通过之日起计算有效期，有效期90天内，模型提供100万Token的免费额度。
- **计费：**总费用 = 输入 Token 数 × 模型输入单价 + 模型输出 Token 数 × 模型输出单价；输入/输出价格可参见[模型列表](https://help.aliyun.com/zh/model-studio/models)。


 **图像转换为Token的规则**
 **


 图像 Token 数 = `(h_bar * w_bar) / token_pixels + 2`。`h_bar、w_bar`：缩放后的图像长宽，模型在处理图像前会进行预处理，会将图像缩小至特定像素上限内，像素上限与`max_pixels`和`vl_high_resolution_images`参数的取值有关。详情请参见[GUI-Plus API参考](https://help.aliyun.com/zh/model-studio/gui-plus-interface-interaction-model)。
- `token_pixels`表示每视觉`Token`对应的像素值，目前固定为`28 * 28`（即`784`）。

以下代码演示了模型内部对图像的大致缩放逻辑，可用于估算一张图像的Token，实际计费请以 API 响应为准。


**
 **


```
# 使用以下命令安装Pillow库：pip install Pillow

import math
from PIL import Image

factor = 28
def token_calculate(image_path, max_pixels, vl_high_resolution_images):
 # 打开指定的PNG图片文件
 image = Image.open(image_path)

 # 获取图片的原始尺寸
 height = image.height
 width = image.width

 # 根据不同模型，将宽高调整为factor的整数倍
 h_bar = round(height / factor) * factor
 w_bar = round(width / factor) * factor

 # 图像的Token下限：4 个 Token
 min_pixels = 4 * factor * factor
 # 若 vl_high_resolution_images 设置为True，则输入图像Token上限为16386，对应的最大的像素值为16384 * 28 * 28，否则为max_pixels设置的值
 if vl_high_resolution_images:
 max_pixels = 16384 * factor * factor
 else:
 max_pixels = max_pixels

 # 对图像进行缩放处理，调整像素的总数在范围[min_pixels,max_pixels]内
 if h_bar * w_bar > max_pixels:
 # 计算缩放因子beta，使得缩放后的图像总像素数不超过max_pixels
 beta = math.sqrt((height * width) / max_pixels)
 # 重新计算调整后的宽高
 h_bar = math.floor(height / beta / factor) * factor
 w_bar = math.floor(width / beta / factor) * factor
 elif h_bar * w_bar 和视觉标记（各计1个Token）
 token = int((h_bar * w_bar) / (28 * 28))+2
 print(f"图像的Token数为{token}")

```


- **查看账单：**您可以在阿里云控制台的[费用与成本](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面查看账单或进行充值。

## API参考

关于通义千问GUI-Plus模型的输入输出参数，请参见[GUI-Plus API参考](https://help.aliyun.com/zh/model-studio/gui-plus-interface-interaction-model)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
