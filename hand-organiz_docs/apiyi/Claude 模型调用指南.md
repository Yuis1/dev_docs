> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/claude)

> API 易第一时间上架 Claude 全系列模型，支持 OpenAI 兼容格式和 Anthropic 原生格式调用，可在 Claude Code 中直接使用。

API 易 是 Claude 模型的官方合作伙伴，通过 **AWS Bedrock** 和 **Anthropic 官网直连**双通道接入，确保第一时间上架 Anthropic 官方最新模型，如 Claude Opus 4.5、Sonnet 4.5 等。

核心优势
----

可用模型
----

API 易 支持 Claude 全系列模型，包括最新发布的 Opus 4.5：

<table><thead><tr><th>模型系列</th><th>模型名称</th><th>推荐场景</th><th>价格（输入 / 输出）</th></tr></thead><tbody><tr><td><strong>Opus 4.5</strong></td><td><code>claude-opus-4-5-20251101</code></td><td>复杂编程、深度推理</td><td data-numeric="true">$5 / $25</td></tr><tr><td><strong>Sonnet 4.5</strong></td><td><code>claude-sonnet-4-5-20250929</code></td><td>通用智能、代码生成</td><td data-numeric="true">$3 / $15</td></tr><tr><td><strong>Haiku 4.5</strong></td><td><code>claude-haiku-4-5-20251001</code></td><td>快速响应、高并发</td><td data-numeric="true">$1 / $5</td></tr><tr><td><strong>Opus 4.1</strong></td><td><code>claude-opus-4-1-250806</code></td><td>高级任务（旧版）</td><td data-numeric="true">$15 / $75</td></tr></tbody></table>

OpenAI 兼容格式调用
-------------

API 易 支持标准的 OpenAI SDK 调用 Claude 模型，只需修改 `base_url` 和 `model` 参数即可。

### Python 示例

```
from openai import OpenAI

client = OpenAI(
    api_key="your-apiyi-key",
    base_url="https://api.apiyi.com/v1"
)

response = client.chat.completions.create(
    model="claude-opus-4-5-20251101",
    messages=[
        {
            "role": "user",
            "content": "用 Python 实现一个快速排序算法，并解释时间复杂度。"
        }
    ],
    # 可选：设置推理深度（Opus 4.5 专属）
    extra_body={
        "anthropic_effort": "medium"  # low/medium/high
    }
)

print(response.choices[0].message.content)


```

### Node.js 示例

```
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'your-apiyi-key',
  baseURL: 'https://api.apiyi.com/v1'
});

const response = await client.chat.completions.create({
  model: 'claude-sonnet-4-5-20250929',
  messages: [
    {
      role: 'user',
      content: '分析这段代码的性能瓶颈...'
    }
  ]
});

console.log(response.choices[0].message.content);


```

### cURL 示例

```
curl https://api.apiyi.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-apiyi-key" \
  -d '{
    "model": "claude-haiku-4-5-20251001",
    "messages": [
      {
        "role": "user",
        "content": "你好，介绍一下你自己。"
      }
    ]
  }'


```

Anthropic 原生格式调用
----------------

API 易 完整支持 Anthropic 官方 SDK 的原生 `/messages` 端点，无需任何转换。

### Python 原生 SDK

```
import anthropic

client = anthropic.Anthropic(
    api_key="your-apiyi-key",
    base_url="https://api.apiyi.com"
)

message = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=8192,
    messages=[
        {
            "role": "user",
            "content": "设计一个高可用的微服务架构，并解释核心设计理念。"
        }
    ],
    # Opus 4.5 专属：设置推理深度
    extra_headers={
        "anthropic-effort": "high"  # low/medium/high
    }
)

print(message.content[0].text)


```

### 流式响应

```
import anthropic

client = anthropic.Anthropic(
    api_key="your-apiyi-key",
    base_url="https://api.apiyi.com"
)

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[
        {"role": "user", "content": "写一篇关于 AI 发展趋势的文章..."}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)


```

### 视觉理解（多模态）

Claude 支持图像输入，适合 UI 分析、图表解读等场景：

```
import anthropic
import base64

client = anthropic.Anthropic(
    api_key="your-apiyi-key",
    base_url="https://api.apiyi.com"
)

# 读取图片并编码为 base64
with open("screenshot.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

message = client.messages.create(
    model="claude-opus-4-5-20251101",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "这是一个网页截图，请用 React + Tailwind CSS 实现相同的 UI。"
                }
            ]
        }
    ]
)

print(message.content[0].text)


```

Claude Code 桌面应用配置
------------------

Claude Code 是 Anthropic 官方推出的 AI 编程助手桌面应用，API 易 完美支持在 Claude Code 中使用。

### 配置步骤

1.  **打开 Claude Code 设置**
    *   点击右上角齿轮图标 ⚙️
    *   选择「Settings」
2.  **配置 API 密钥**
    *   在「API Key」字段输入您的 API 易 密钥
    *   密钥格式：`sk-xxxxxxxxxxxxxxxx`
3.  **配置 Base URL**
    *   在「Custom API Endpoint」字段输入：
4.  **选择模型**
    *   在「Model」下拉框选择：
        *   `claude-opus-4-5-20251101`（最强编程能力）
        *   `claude-sonnet-4-5-20250929`（平衡性能与成本）
        *   `claude-haiku-4-5-20251001`（快速响应）
5.  **开始使用**
    *   点击「Save」保存配置
    *   在编辑器中选中代码，右键唤起 Claude Code
    *   享受顶级 AI 编程助手！

### 配置示例（JSON）

如果需要手动编辑配置文件，参考以下格式：

```
{
  "model": "claude-opus-4-5-20251101",
  "apiKey": "sk-xxxxxxxxxxxxxxxx",
  "baseURL": "https://api.apiyi.com/v1",
  "maxTokens": 8192,
  "temperature": 0.7
}


```

推理深度控制（Opus 4.5 专属）
-------------------

Claude Opus 4.5 引入了全新的 `effort` 参数，可调节推理深度：

<table><thead><tr><th>模式</th><th>说明</th><th>适用场景</th><th>Token 消耗</th></tr></thead><tbody><tr><td><strong>low</strong></td><td>快速响应，推理深度较浅</td><td>简单问答、快速原型</td><td>低</td></tr><tr><td><strong>medium</strong></td><td>平衡质量与速度（默认）</td><td>大多数编程任务</td><td>中等（比 high 节省 76%）</td></tr><tr><td><strong>high</strong></td><td>深度推理，质量最高</td><td>复杂架构设计、难题分析</td><td>高</td></tr></tbody></table>

### OpenAI 格式设置 effort

```
response = client.chat.completions.create(
    model="claude-opus-4-5-20251101",
    messages=[{"role": "user", "content": "设计一个分布式缓存系统..."}],
    extra_body={
        "anthropic_effort": "high"  # low/medium/high
    }
)


```

### Anthropic 原生格式设置 effort

```
message = client.messages.create(
    model="claude-opus-4-5-20251101",
    messages=[{"role": "user", "content": "优化这段 SQL 查询..."}],
    extra_headers={
        "anthropic-effort": "medium"
    }
)


```

最佳实践
----

### 1. 模型选择建议

*   **复杂编程任务**：使用 `claude-opus-4-5-20251101` + `high` 或 `medium` 模式
*   **日常代码生成**：使用 `claude-sonnet-4-5-20250929`，性价比最高
*   **快速问答 / 高并发**：使用 `claude-haiku-4-5-20251001`，速度快成本低
*   **多模态任务**：优先选择 Opus 或 Sonnet，视觉理解能力更强

### 2. 成本优化技巧

*   **优先使用 medium 模式**：Opus 4.5 的 medium 模式输出质量接近 Sonnet，但 token 消耗仅 24%
*   **充值加赠活动**：通过 API 易 充值享受最高 20% 加赠，实际成本低至 8 折
*   **合理使用缓存**：对于重复的 Prompt 或上下文，启用 prompt caching 节省成本
*   **按需降级**：简单任务使用 Haiku 或 Sonnet，复杂任务再用 Opus

### 3. 提示词优化

Claude 模型对清晰、结构化的提示词响应更好：

```
# 推荐：清晰的任务描述
prompt = """
任务：重构以下 Python 代码
要求：
1. 提升性能（时间复杂度从 O(n²) 降至 O(n log n)）
2. 增加错误处理和类型提示
3. 添加单元测试

代码：
[粘贴代码]
"""

# 不推荐：模糊的指令
prompt = "帮我改一下这段代码"


```

### 4. 长上下文使用

Claude Opus 4.5 支持 20 万 token 上下文，适合代码库级别分析：

```
# 示例：分析整个代码库
files_content = ""
for file in ["main.py", "utils.py", "models.py"]:
    with open(file) as f:
        files_content += f"\n\n# {file}\n{f.read()}"

response = client.chat.completions.create(
    model="claude-opus-4-5-20251101",
    messages=[{
        "role": "user",
        "content": f"分析以下代码库的架构设计，并提出优化建议：\n{files_content}"
    }]
)


```

技术规格对比
------

<table><thead><tr><th>参数</th><th>Opus 4.5</th><th>Sonnet 4.5</th><th>Haiku 4.5</th></tr></thead><tbody><tr><td><strong>上下文长度</strong></td><td>200,000 tokens</td><td>200,000 tokens</td><td>200,000 tokens</td></tr><tr><td><strong>最大输出</strong></td><td>64,000 tokens</td><td>8,192 tokens</td><td>8,192 tokens</td></tr><tr><td><strong>知识截止</strong></td><td>2025 年 3 月</td><td>2024 年 10 月</td><td>2024 年 10 月</td></tr><tr><td><strong>多模态</strong></td><td>✅ 图像输入</td><td>✅ 图像输入</td><td>✅ 图像输入</td></tr><tr><td><strong>推理控制</strong></td><td>✅ effort 参数</td><td>❌</td><td>❌</td></tr><tr><td><strong>SWE-bench</strong></td><td data-numeric="true">80.9%</td><td data-numeric="true">77.2%</td><td data-numeric="true">73.3%</td></tr></tbody></table>

常见问题
----

### 如何在 Claude Code 中使用 API 易？

只需在 Claude Code 设置中配置：

*   **Base URL**: `https://api.apiyi.com/v1`
*   **API Key**: 您的 API 易 密钥
*   **Model**: `claude-opus-4-5-20251101` 或其他 Claude 模型

### OpenAI 格式和 Anthropic 原生格式有什么区别？

*   **OpenAI 格式**：使用 `/v1/chat/completions` 端点，兼容 OpenAI SDK
*   **Anthropic 格式**：使用 `/v1/messages` 端点，支持 Anthropic 官方 SDK 全部特性
*   **推荐**：如果使用 Claude Code 或 OpenAI SDK，选择 OpenAI 格式；如果需要 Anthropic 特有功能（如 tool use），选择原生格式

### effort 参数如何影响性能和成本？

*   **high 模式**：推理深度最大，输出质量最高，但 token 消耗最多（约 3-4 倍于 medium）
*   **medium 模式**：平衡质量与成本，输出质量接近 Sonnet，token 消耗仅为 high 的 24%
*   **low 模式**：快速响应，适合简单任务，token 消耗最少

### API 易 的双通道是什么？

API 易 通过 **AWS Bedrock** 和 **Anthropic 官网直连**两条线路接入 Claude 模型：

*   **AWS Bedrock**：稳定性高，延迟低，适合企业级应用
*   **官网直连**：第一时间获取新模型，功能完整
*   **自动切换**：系统智能选择最优线路，保障服务可用性

### 如何获取 API 易 密钥？

访问 API 易 官网（`apiyi.com`）注册账号，充值后即可在控制台获取 API 密钥。新用户注册即送额度，充值享受最高 20% 加赠。

相关资源
----

*   [Claude Opus 4.5 发布公告](https://docs.apiyi.com/news/claude-opus-4-5-launch)
*   [OpenAI SDK 使用指南](https://docs.apiyi.com/api-capabilities/openai-sdk)
*   [多模态视觉理解](https://docs.apiyi.com/api-capabilities/vision-understanding)
*   [Anthropic 官方文档](https://docs.anthropic.com/)