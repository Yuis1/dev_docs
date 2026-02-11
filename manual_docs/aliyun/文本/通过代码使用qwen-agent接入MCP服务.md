---
url: https://help.aliyun.com/document_detail/2968153.html?mode=pure
title: "通过代码使用qwen-agent接入MCP服务-大模型服务平台百炼-阿里云"
captured_at: "2026-01-25T01:25:16.031Z"
---


# 通过代码使用qwen-agent接入MCP服务-大模型服务平台百炼-阿里云

模型上下文协议（Model Context Protocol, MCP）可帮助大模型使用外部工具与数据，相比 Function Calling，MCP 更灵活且易于使用。本文介绍通过阿里云百炼模型服务接入 MCP 的方法。

## 效果展示


 MCP 路线规划 Demo


我爸妈今天下午到萧山机场，请你规划一条从萧山机场到阿里巴巴云谷园区的公共交通路线（地铁和巴士都可），并且部署为公网链接，这样我就可以转发给我爸妈了

 **以上组件仅供您参考，已对工具名称与入参进行简化，且并未真实发送请求。

## 前提条件

您需要已获取API Key并配置API Key到环境变量。本文以 qwen-plus-latest 模型为例，子业务空间的 API Key 请确保主账号已为该业务空间进行模型授权。

## 通过代码调用 MCP 工具

Qwen-Agent 是通义实验室推出的 Agent 开发框架，充分利用了通义千问模型的指令遵循、工具使用、规划与记忆能力。Qwen Chat 当前使用 Qwen-Agent 框架作为后端引擎。

### 1. 安装依赖

运行以下命令安装qwen-agent依赖。Python 版本建议不低于 3.10。建议使用独立的虚拟环境安装，避免与现有项目的依赖冲突（如 Pydantic 版本）。


 pip install -U "qwen-agent[gui,mcp]"


### 2. 添加 MCP 服务并运行代码

以高德地图与网页部署 MCP 服务器为例。参见开通云部署 MCP 服务，开通 Amap Maps 与 EdgeOne Pages MCP 服务，分别单击页面上方的外部调用**，获取 SSE Endpoint。**Amap Maps 可完成路径规划、天气查询等功能；EdgeOne Pages 可将 HTML 内容部署为可公网访问的链接。


 import os
from qwen_agent.agents import Assistant


# LLM 配置

llm_cfg = {
 "model": "qwen-plus-latest",
 "model_server": "https://dashscope.aliyuncs.com/compatible-mode/v1",
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
 "api_key": os.getenv("DASHSCOPE_API_KEY"),
}


# 系统消息

system = "你是会天气查询、地图查询、网页部署的助手"


# 工具列表

tools = [
 {
 "mcpServers": {
 "amap-maps": {
 "type": "sse",
 "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
 "headers": {
 "Authorization": os.getenv("DASHSCOPE_API_KEY")
 }
 },
 "edgeone-pages-mcp": {
 "type": "sse",
 "url": "https://dashscope.aliyuncs.com/api/v1/mcps/EdgeOne/sse",
 "headers": {
 "Authorization": os.getenv("DASHSCOPE_API_KEY")
 }
 },
 }
 }
]


# 创建助手实例

bot = Assistant(
 llm=llm_cfg,
 name="助手",
 description="高德地图、天气查询、公网链接部署",
 system_message=system,
 function_list=tools,
)

messages = []

while True:
 query = input("\nuser question: ")
 if not query.strip():
 print("user question cannot be empty！")
 continue
 messages.append({"role": "user", "content": query})
 bot_response = ""
 is_tool_call = False
 tool_call_info = {}
 for response_chunk in bot.run(messages):
 new_response = response_chunk[-1]
 if "function_call" in new_response:
 is_tool_call = True
 tool_call_info = new_response["function_call"]
 elif "function_call" not in new_response and is_tool_call:
 is_tool_call = False
 print("\n" + "=" * 20)
 print("工具调用信息：", tool_call_info)
 print("工具调用结果：", new_response)
 print("=" * 20)
 elif new_response.get("role") == "assistant" and "content" in new_response:
 incremental_content = new_response["content"][len(bot_response):]
 print(incremental_content, end="", flush=True)
 bot_response += incremental_content
 # response_chunk 是消息列表，追加到历史消息中用于多轮对话
 messages.extend(response_chunk)

 提问示例：


 我爸妈今天下午到萧山机场，请你规划一条从萧山机场到阿里巴巴云谷园区的公共交通路线（地铁和巴士都可），并且部署为公网链接，这样我就可以转发给我爸妈了

 Qwen Agent 调用 MCP 工具后进行回复：


 已为您规划好从萧山机场到阿里巴巴云谷园区的公共交通路线，并生成了专属网页链接，方便您转发给父母。

您可以通过以下链接查看详细的出行指南：
**[点击查看出行指南](https://mcp.edgeone.site/share/xxx_xxx)**

该指南包含：
- **最快路线**（约109分钟）：地铁19号线 → 公交343路
- **备选路线**（换乘少）：地铁19号线 → 公交349路
- 详细的步行指引和换乘说明
- 实用的出行小贴士（如使用支付宝扫码乘车等）

祝您父母旅途顺利！

 Qwen-Agent 提供了可视化界面进行交互：


 import os
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI


# LLM 配置

llm_cfg = {
 "model": "qwen-plus-latest",
 "model_server": "https://dashscope.aliyuncs.com/compatible-mode/v1",
 # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
 "api_key": os.getenv("DASHSCOPE_API_KEY"),
}


# 系统消息

system = "你是会天气查询、地图查询、网页部署的助手"


# 工具列表

tools = [
 {
 "mcpServers": {
 "amap-maps": {
 "type": "sse",
 "url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
 "headers": {
 "Authorization": os.getenv("DASHSCOPE_API_KEY")
 }
 },
 "edgeone-pages-mcp": {
 "type": "sse",
 "url": "https://dashscope.aliyuncs.com/api/v1/mcps/EdgeOne/sse",
 "headers": {
 "Authorization": os.getenv("DASHSCOPE_API_KEY")
 }
 },
 }
 }
]


# 创建助手实例

bot = Assistant(
 llm=llm_cfg,
 name="助手",
 description="高德地图、天气查询、公网链接部署",
 system_message=system,
 function_list=tools,
)
WebUI(bot).run()

 界面显示Running on local URL: http://127.0.0.1:7860后访问该链接。

## 通过可视化界面调用 MCP 工具

阿里云百炼的智能体应用与工作流应用：**请参见[在智能体或工作流中配置 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#8319d03864jym)。

**第三方大模型客户端：**支持多种主流大模型客户端，例如 [Cherry Studio](https://www.cherry-ai.com/)。
