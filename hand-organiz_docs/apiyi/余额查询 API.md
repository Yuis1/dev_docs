# APIYI 账户余额查询 API

本文档描述了如何通过 APIYI 平台查询当前账户的余额、已用额度及相关用户信息。

## 1. 接口概述

该接口用于获取当前认证用户的账户详情，核心数据包括：
*   **剩余额度 (quota)**：当前账户剩余可用的点数。
*   **已用额度 (used_quota)**：账户历史累计消耗的点数。
*   **基本信息**：用户名、显示名称等。

## 2. 接口详情

| 项目 | 说明 |
| :--- | :--- |
| **接口 URL** | `https://api.apiyi.com/api/user/self` |
| **请求方法** | `GET` |
| **认证方式** | Header 认证 (Token) |
| **响应格式** | JSON |

## 3. 请求说明

### 3.1 请求头 (Headers)

| Header 名称 | 必填 | 示例值 | 说明 |
| :--- | :--- | :--- | :--- |
| `Authorization` | **是** | `sk-xxxxxx` | API 访问令牌 (Access Token)。**直接填写 Token 字符串**，无需 `Bearer` 前缀。 |
| `Accept` | 否 | `application/json` | 建议设置 |
| `Content-Type` | 否 | `application/json` | 建议设置 |

### 3.2 请求参数

无查询参数或请求体。

## 4. 响应说明

接口返回标准的 JSON 对象，包含状态码与数据载荷。

### 4.1 成功响应示例

```json
{
  "success": true,
  "message": null,
  "data": {
    "id": 12345,
    "username": "demo_user",
    "display_name": "Demo User",
    "role": 1,
    "status": 1,
    "email": "demo@example.com",
    "quota": 25000000,        // 剩余额度
    "used_quota": 5000000,    // 已用额度
    "request_count": 100,
    "group": "default",
    "access_token": "",       // 敏感信息通常为空或脱敏
    "ModelFixedPrice": { ... } // 模型价格表
  }
}
```

### 4.2 核心字段解析

| 字段路径 | 类型 | 含义 | 备注 |
| :--- | :--- | :--- | :--- |
| `success` | Boolean | 请求状态 | `true` 表示成功 |
| `data.display_name` | String | 显示名称 | 优先展示，若无则使用 `username` |
| `data.quota` | Number | **剩余额度** | 当前账户剩余可用的点数 (余额) |
| `data.used_quota` | Number | **已用额度** | 历史累计消耗的点数 |

## 5. 额度与金额换算

APIYI 使用“额度点数 (Credits)”作为计费单位，与美元 (USD) 的换算关系如下：

**换算公式：**
$$ 
\text{金额 (USD)} = \frac{\text{额度 (Credits)}}{500,000} 
$$ 

**示例：**
*   若 `quota` = 25,000,000
    *   余额 = $25,000,000 / 500,000 = \$50.00$
*   若 `used_quota` = 500,000
    *   已用 = $500,000 / 500,000 = \$1.00$

## 6. 代码示例 (TypeScript / Next.js)

```typescript
// 这里的 env.APIYI_ACCESS_TOKEN 为你的 Token 环境变量
async function fetchAccountBalance() {
  const token = process.env.APIYI_ACCESS_TOKEN;
  
  if (!token) {
    console.warn("API Token not configured");
    return null;
  }

  try {
    const response = await fetch("https://api.apiyi.com/api/user/self", {
      method: "GET",
      headers: {
        "Accept": "application/json",
        "Authorization": token, // 直接传入 Token
        "Content-Type": "application/json",
      },
      cache: "no-store", // 确保获取最新数据
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const json = await response.json();
    
    if (!json.success || !json.data) {
      throw new Error(json.message || "Invalid response format");
    }

    const { quota, used_quota, display_name } = json.data;

    // 换算为美元
    const remainingUsd = typeof quota === 'number' ? quota / 500000 : 0;
    const usedUsd = typeof used_quota === 'number' ? used_quota / 500000 : 0;

    return {
      name: display_name,
      balance: remainingUsd,
      used: usedUsd
    };

  } catch (error) {
    console.error("Failed to fetch balance:", error);
    return null;
  }
}
```

## 7. 常见问题

*   **HTTP 401 Unauthorized**: Token 无效或过期。请检查 `.env` 配置。
*   **余额显示为 0**: 请确认是否使用了正确的除数 (500,000) 以及是否正确处理了 `0` 值（避免被视为 `null`）。
*   **Header 格式**: 该接口通常不需要 `Bearer` 前缀，直接发送 Token 字符串即可。如果失败，可尝试添加 `Bearer ` 前缀测试。
