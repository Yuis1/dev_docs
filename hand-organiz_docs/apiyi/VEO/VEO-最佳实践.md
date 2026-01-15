> 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [docs.apiyi.com](https://docs.apiyi.com/api-capabilities/veo/best-practices#%E4%B8%BB%E4%BD%93%E6%8F%8F%E8%BF%B0)

> 优化 VEO API 使用效果的建议和技巧

提示词编写指南
-------

编写高质量的提示词是获得优秀视频的关键。以下是各个要素的详细说明：

### 提示词结构

*   主体描述
    
*   动作行为
    
*   环境场景
    
*   镜头运动
    
*   画质风格
    

明确描述视频的主要对象或角色**好的示例：**

*   “一只橘色的小猫”
*   “穿着红色连衣裙的年轻女孩”
*   “银色的跑车”

**避免：**

*   “某个东西”
*   “一些动物”

具体描述主体的动作和行为**好的示例：**

*   “慢慢走动”
*   “快速奔跑”
*   “优雅地跳舞”

**避免：**

*   “在移动”
*   “做某事”

详细描述背景和环境**好的示例：**

*   “阳光明媚的花园”
*   “雨夜的城市街道”
*   “日落时分的海滩”

**避免：**

*   “某个地方”
*   “外面”

描述摄像机的运动方式**好的示例：**

*   “镜头跟随”
*   “俯拍视角”
*   “360 度环绕”

**可选元素**

指定期望的视觉风格**好的示例：**

*   “4K 高清，电影级”
*   “动画风格”
*   “复古胶片质感”

**可选元素**

### 优秀提示词示例

提示词增强功能
-------

### 何时使用提示词增强

参考图片使用
------

### 图片要求

<table><thead><tr><th>要求</th><th>说明</th></tr></thead><tbody><tr><td>格式</td><td>JPG、PNG、WebP</td></tr><tr><td>大小</td><td>单张不超过 10MB</td></tr><tr><td>数量</td><td>最多 5 张</td></tr><tr><td>分辨率</td><td>建议 1024x1024 以上</td></tr><tr><td>内容</td><td>清晰、相关的参考素材</td></tr></tbody></table>

### 使用技巧

轮询策略
----

### 推荐的轮询实现

```
import time
import math

def exponential_backoff_polling(client, task_id, initial_interval=5, max_interval=60):
    """
    指数退避轮询策略
    """
    interval = initial_interval
    attempt = 0
    
    while True:
        try:
            status_data = client.get_status(task_id)
            status = status_data.get('status')
            
            if status == 'completed':
                return status_data['result']
            elif status == 'failed':
                raise Exception(f"生成失败: {status_data.get('error')}")
            
            # 指数退避
            time.sleep(interval)
            attempt += 1
            interval = min(initial_interval * math.pow(1.5, attempt), max_interval)
            
        except Exception as e:
            print(f"轮询出错: {e}")
            time.sleep(interval)


```

### 轮询参数建议

错误处理
----

### 重试策略

```
def retry_with_backoff(func, max_retries=3, backoff_factor=2):
    """
    带退避的重试机制
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = backoff_factor ** attempt
            print(f"失败，{wait_time}秒后重试...")
            time.sleep(wait_time)


```

### 常见错误处理

*   网络错误
    
*   API 错误
    
*   任务失败
    

```
try:
    result = client.submit_task(prompt)
except requests.exceptions.ConnectionError:
    print("网络连接失败，请检查网络")
except requests.exceptions.Timeout:
    print("请求超时，请稍后重试")


```

```
try:
    result = client.submit_task(prompt)
except Exception as e:
    if "QUOTA_EXCEEDED" in str(e):
        print("配额已用完")
    elif "INVALID_PROMPT" in str(e):
        print("提示词无效")


```

```
status = client.get_status(task_id)
if status['status'] == 'failed':
    error_info = status.get('error', {})
    print(f"任务失败: {error_info.get('message')}")
    # 可以尝试重新提交


```

性能优化
----

### 批量处理

当需要生成多个视频时，建议使用批量处理：

```
async def batch_process_videos(prompts, max_concurrent=5):
    """
    批量处理视频生成
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_one(prompt):
        async with semaphore:
            return await client.submit_and_wait(prompt)
    
    tasks = [process_one(prompt) for prompt in prompts]
    return await asyncio.gather(*tasks)


```

### 资源管理

成本优化
----

### 模型选择策略

```
def choose_model(requirements):
    """
    根据需求智能选择模型
    """
    if requirements.get('need_fast'):
        return 'veo3-fast'
    elif requirements.get('high_quality'):
        return 'veo3-pro'
    elif requirements.get('precise_control'):
        return 'veo3-pro-frames'
    else:
        return 'veo3'  # 默认选择标准版


```

### 测试建议

监控和日志
-----

### 建议的日志记录

```
import logging
from datetime import datetime

class VEOLogger:
    def __init__(self):
        self.logger = logging.getLogger('veo_api')
        
    def log_task_submission(self, task_id, prompt, model):
        self.logger.info(f"Task submitted: {task_id}")
        self.logger.debug(f"Prompt: {prompt[:50]}...")
        self.logger.debug(f"Model: {model}")
        
    def log_task_completion(self, task_id, duration, video_url):
        self.logger.info(f"Task completed: {task_id}")
        self.logger.info(f"Duration: {duration}s")
        self.logger.debug(f"Video URL: {video_url}")


```

### 监控指标

*   任务成功率
*   平均生成时间
*   API 响应时间
*   错误率统计
*   费用追踪