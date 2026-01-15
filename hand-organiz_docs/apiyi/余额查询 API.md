> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/balance-query)

> 获取账户余额、已使用额度和请求次数等信息，实现主动余额告警控制

接口概述
----

余额查询接口用于获取当前账户的额度使用情况，包括总配额、已使用额度、剩余额度和请求次数等信息。 这个接口可帮助客户以简单的方式获取账号余额，以便更主动、自由地控制余额告警。

![](https://mintcdn.com/apiyillc/PXVoab-l7wSQlQVE/images/apiyi-system-accesstoken.png?fit=max&auto=format&n=PXVoab-l7wSQlQVE&q=85&s=eb4f48476a795dfa5bfd7cb053081bdc)

接口信息
----

<table><thead><tr><th>项目</th><th>说明</th></tr></thead><tbody><tr><td><strong>接口 URL</strong></td><td><code>https://api.apiyi.com/api/user/self</code></td></tr><tr><td><strong>请求方法</strong></td><td><code>GET</code></td></tr><tr><td><strong>认证方式</strong></td><td>Authorization Header</td></tr><tr><td><strong>响应格式</strong></td><td>JSON</td></tr></tbody></table>

请求说明
----

<table><thead><tr><th>Header 名称</th><th>必填</th><th>说明</th></tr></thead><tbody><tr><td><code>Authorization</code></td><td>是</td><td>API 访问令牌，格式：直接填写 token 字符串</td></tr><tr><td><code>Accept</code></td><td>否</td><td>建议设置为 <code>application/json</code></td></tr><tr><td><code>Content-Type</code></td><td>否</td><td>建议设置为 <code>application/json</code></td></tr></tbody></table>

### 请求参数

响应说明
----

### 成功响应示例

```
{
  "success": true,
  "message": null,
  "data": {
    "id": 19489,
    "username": "testnano",
    "display_name": "testnano",
    "role": 1,
    "status": 1,
    "email": "",
    "quota": 24997909,
    "used_quota": 10027091,
    "request_count": 339,
    "group": "ceshi",
    "aff_code": "ZM0H",
    "inviter_id": 0,
    "access_token": "...",
    "ModelFixedPrice": [...]
  }
}


```

### 核心响应字段说明

<table><thead><tr><th>字段名</th><th>类型</th><th>说明</th></tr></thead><tbody><tr><td><code>success</code></td><td>Boolean</td><td>请求是否成功</td></tr><tr><td><code>message</code></td><td>String</td><td>错误信息（成功时为 null）</td></tr><tr><td><code>data.username</code></td><td>String</td><td>用户名</td></tr><tr><td><code>data.display_name</code></td><td>String</td><td>显示名称</td></tr><tr><td><code>data.quota</code></td><td>Integer</td><td><strong>剩余额度</strong>（当前可用余额，单位：额度）</td></tr><tr><td><code>data.used_quota</code></td><td>Integer</td><td><strong>已使用额度</strong>（单位：额度）</td></tr><tr><td><code>data.request_count</code></td><td>Integer</td><td><strong>总请求次数</strong></td></tr><tr><td><code>data.group</code></td><td>String</td><td>用户所属组</td></tr><tr><td><code>data.ModelFixedPrice</code></td><td>Array</td><td>模型价格列表（可忽略）</td></tr></tbody></table>

### 额度换算说明

**计算公式：**

*   美金金额 = 额度 ÷ 500,000
*   剩余额度 = quota（quota 本身就是当前剩余余额）
*   剩余美金 = quota ÷ 500,000

**示例：**

*   `quota: 24997909` → $49.99 USD（当前剩余余额）
*   `used_quota: 10027091` → $20.05 USD（已使用）

错误响应
----

### HTTP 401 - 认证失败

```
{
  "success": false,
  "message": "Unauthorized"
}


```

**原因：** Authorization 令牌无效或已过期 **解决方法：** 检查并更新 API 令牌

### HTTP 403 - 权限不足

```
{
  "success": false,
  "message": "Forbidden"
}


```

**原因：** 当前令牌无权访问该接口 **解决方法：** 联系管理员确认权限配置

代码示例
----

### cURL 示例

```
curl --compressed 'https://api.apiyi.com/api/user/self' \
  -H 'Accept: application/json' \
  -H 'Authorization: YOUR_TOKEN_HERE' \
  -H 'Content-Type: application/json'


```

**快速测试（替换 YOUR_TOKEN_HERE）：**

```
export APIYI_TOKEN='YOUR_TOKEN_HERE'

curl --compressed -s 'https://api.apiyi.com/api/user/self' \
  -H 'Accept: application/json' \
  -H "Authorization: $APIYI_TOKEN" \
  -H 'Content-Type: application/json' | \
  jq '.data | {quota, used_quota, request_count}'


```

### Python 示例（基础版）

```
import requests

{/* 配置 */}
url = "https://api.apiyi.com/api/user/self"
authorization = "YOUR_TOKEN_HERE"  # 替换为你的令牌

{/* 请求头 */}
headers = {
    'Accept': 'application/json',
    'Authorization': authorization,
    'Content-Type': 'application/json'
}

{/* 发送请求 */}
response = requests.get(url, headers=headers, timeout=10)

{/* 检查响应 */}
if response.status_code == 200:
    data = response.json()
    user_data = data['data']

    {/* 提取核心信息 */}
    quota = user_data['quota']
    used_quota = user_data['used_quota']
    request_count = user_data['request_count']

    {/* 计算美金金额 */}
    {/* 注意：quota 就是当前剩余余额 */}
    remaining_usd = quota / 500000
    used_usd = used_quota / 500000

    {/* 打印结果 */}
    print(f"剩余额度：${remaining_usd:.2f} USD ({quota:,} 额度)")
    print(f"已使用：${used_usd:.2f} USD ({used_quota:,} 额度)")
    print(f"请求次数：{request_count:,} 次")
else:
    print(f"请求失败：HTTP {response.status_code}")
    print(response.text)


```

### Python 示例（完整优化版）

我们提供了完整的优化版脚本 `quota_optimized.py`，包含以下特性：

**使用方法：**

```
{/* 方式1：使用环境变量（推荐） */}
export APIYI_TOKEN='YOUR_TOKEN_HERE'
python quota_optimized.py

{/* 方式2：命令行参数 */}
python quota_optimized.py 'YOUR_TOKEN_HERE'


```

**输出示例：**

```
============================================================
📊 APIYI 账户余额信息
============================================================
用户名称：testnano (testnano)
------------------------------------------------------------
剩余额度：24,997,909 额度 ($49.99 USD)
已使用：  10,027,091 额度 ($20.05 USD)
请求次数：339 次
============================================================
💡 换算说明：500,000 额度 = $1.00 USD
============================================================


```

常见问题
----

注意事项
----