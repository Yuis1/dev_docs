本文介绍 DashScope Python SDK 调用[Qwen-Omni 实时模型](https://help.aliyun.com/zh/model-studio/realtime)时的关键接口与请求参数。

## **前期准备**

您的 SDK 版本需要不低于1.23.9。请先阅读[实时多模态交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process)。

## **快速开始**

请访问[GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)下载示例代码。我们提供了三种调用方式的示例代码：

1.  [音频对话示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：麦克风采集实时音频输入，开启[VAD 模式](https://help.aliyun.com/zh/model-studio/realtime#68d826b358q1r)（自动检测语音起止），支持语音打断。
    
    > `enable_turn_detection`参数需设为 True。
    
    > 推荐您使用耳机播放音频，避免回声触发语音打断。
    
2.  [音视频对话示例](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：麦克风和摄像头采集实时音视频输入，开启[VAD 模式](https://help.aliyun.com/zh/model-studio/realtime#68d826b358q1r)（自动检测语音起止），支持语音打断。
    
    > `enable_turn_detection`参数需设为 True。
    
    > 推荐您使用耳机播放音频，避免回声触发语音打断。
    
3.  [本地调用](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni/python)：本地音频和图片作为输入，开启[Manual 模式](https://help.aliyun.com/zh/model-studio/realtime#3dbb650fb3ird)（手动控制发送节奏）。
    
    > `enable_turn_detection`参数需设为 False。
    

## **请求参数**

下述请求参数可以通过OmniRealtimeConversation的构造方法（__init__）进行设置。

| **参数** | **类型** | **说明** |
| --- | --- | --- |
| model | str | Qwen-Omni系列模型名称。参见[模型列表](https://help.aliyun.com/zh/model-studio/models#6deec483126rk)。 |
| callback | `[OmniRealtimeCallback](https://help.aliyun.com/zh/model-studio/qwen-asr-realtime-python-sdk#9d08669109iwx)` | 用于处理服务端事件的回调对象实例。 |

下述请求参数可以通过update_session接口配置。

| **参数** | **类型** | **说明** |
| --- | --- | --- |
| output_modalities | list[MultiModality] | 模型输出模态设置，支持设置[MultiModality.TEXT]（仅输出文本）或[MultiModality.TEXT, MultiModality.AUDIO]（输出音频和文本）。 |
| voice | str | 模型生成音频的音色，支持的音色参见[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f9c68d860a3rs)。 默认音色： - `Qwen3-Omni-Flash-Realtime`: `"Cherry"` - `Qwen-Omni-Turbo-Realtime`: `"Chelsie"` |
| input_audio_format | AudioFormat | 用户输入音频的格式，当前仅支持设置为PCM_16000HZ_MONO_16BIT。 |
| output_audio_format | AudioFormat | 模型输出音频的格式： - Qwen3-Omni-Flash-Realtime：仅支持设置为`pcm24` - Qwen-Omni-Turbo-Realtime：仅支持设置为 `pcm16` |
| smooth_output | bool | 仅Qwen3-Omni-Flash-Realtime系列版本支持设置。 - True：获得口语化的回复 - False：获得更书面化、正式的回复 > 但可能会因为存在难以朗读的内容而导致效果不好。 - None：模型自动选择口语化或书面化的回复风格 |
| instructions | str | 系统消息，用于设定模型的目标或角色。 例如：你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。 |
| enable_input_audio_transcription | bool | 是否开启输入音频的语音识别。 |
| input_audio_transcription_model | str | 用于输入音频转录的语音识别模型，当前仅支持设置为gummy-realtime-v1。 |
| turn_detection_type | str | 服务端VAD类型，目前固定为server_vad。 |
| turn_detection_threshold | float | VAD检测阈值。建议在嘈杂的环境中增加， 在安静的环境中降低。 - 取值越接近-1，噪音被判定为语音的概率越大。 - 取值越接近1，噪音被判定为语音的概率越小。 默认为 0.5，参数范围：[-1.0, 1.0]。 |
| turn_detection_silence_duration_ms | int | 检测语音停止的静音持续时间，超过此值后会触发模型响应。默认值为800，参数范围[200, 6000]。 |
| temperature | float | 采样温度，控制模型生成内容的多样性。 temperature越高，生成的内容更多样，反之，生成的内容更确定。 取值范围： [0, 2) 由于temperature与top_p均可以控制生成内容的多样性，因此建议您只设置其中一个值。 - `qwen3-omni-flash-realtime`系列：0.9 - `qwen-omni-turbo-realtime`系列：1.0 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| top_p | float | 核采样的概率阈值，控制模型生成内容的多样性。 top_p越高，生成的内容更多样。反之，生成的内容更确定。 取值范围：（0,1.0] 由于temperature与top_p均可以控制生成内容的多样性，因此建议您只设置其中一个值。 top_p默认值： - `qwen3-omni-flash-realtime`系列：1.0 - `qwen-omni-turbo-realtime`系列：0.01 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| top_k | integer | 生成过程中采样候选集的大小。例如，取值为50时，仅将单次生成中得分最高的50个Token组成随机采样的候选集。取值越大，生成的随机性越高；取值越小，生成的确定性越高。取值为None或当top_k大于100时，表示不启用top_k策略，此时仅有top_p策略生效。 取值需要大于或等于0。 top_k默认值： - `qwen3-omni-flash-realtime`系列：50 - `qwen-omni-turbo-realtime`系列：20 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| max_tokens | integer | 本次请求返回的最大 Token 数。 > `max_tokens` 的设置不会影响大模型的生成过程，如果模型生成的 Token 数超过`max_tokens`，本次请求会返回截断后的内容。 默认值和最大值都是模型的最大输出长度。关于各模型的最大输出长度，请参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。 max_tokens参数适用于需要限制字数（如生成摘要、关键词）、控制成本或减少响应时间的场景。 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| repetition_penalty | float | 模型生成时连续序列中的重复度。提高repetition_penalty时可以降低模型生成的重复度，1.0表示不做惩罚。没有严格的取值范围，只要大于0即可。 默认值1.05。 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| presence_penalty | float | 控制模型生成内容的重复度。 默认值为0.0，取值范围：[-2.0, 2.0]。正数会减少重复度，负数会增加重复度。 适用场景： 较高的presence_penalty适用于要求多样性、趣味性或创造性的场景，如创意写作或头脑风暴。 较低的presence_penalty适用于要求一致性或专业术语的场景，如技术文档或其他正式文档。 > `qwen-omni-turbo` 系列模型**不支持修改**。 |
| seed | integer | 设置seed参数会使模型生成过程更具有确定性，通常用于使模型每次运行的结果一致。 在每次模型调用时传入相同的seed值（由您指定），并保持其他参数不变，模型将尽可能返回相同的结果。 取值范围：0到231−1，默认值-1。 > `qwen-omni-turbo` 系列模型**不支持修改**。 |

## **关键接口**

### **OmniRealtimeConversation类**

OmniRealtimeConversation通过`from dashscope.audio.qwen_omni import OmniRealtimeConversation`方法引入。

| 方法签名 | 服务端响应事件（通过回调下发） | 说明  |
| --- | --- | --- |
| ``` def connect(self,) -> None ``` | [服务端事件](https://help.aliyun.com/zh/model-studio/server-events#39689ed6e90ag) > 会话已创建 [session.updated](https://help.aliyun.com/zh/model-studio/server-events#424ef2e774q9p) > 会话配置已更新 | 和服务端创建连接。 |
| ``` def update_session(self, output_modalities: list[MultiModality], voice: str, input_audio_format: AudioFormat = AudioFormat. PCM_16000HZ_MONO_16BIT, output_audio_format: AudioFormat = AudioFormat. PCM_24000HZ_MONO_16BIT, enable_input_audio_transcription: bool = True, input_audio_transcription_model: str = None, enable_turn_detection: bool = True, turn_detection_type: str = 'server_vad', prefix_padding_ms: int = 300, turn_detection_threshold: float = 0.2, turn_detection_silence_duration_ms: int = 800, turn_detection_param: dict = None, smooth_output: bool = True, **kwargs) -> None ``` | [session.updated](https://help.aliyun.com/zh/model-studio/server-events#424ef2e774q9p) > 会话配置已更新 | 更新本次会话交互的默认配置。参数配置请参考《请求参数》章节。 在您建立链接，服务端会及时返回用于此会话的默认输出输入配置。如果您需要更新默认会话配置，我们也推荐您总是在建立链接后即刻调用此接口。 服务端在收到session.update事件后，会进行参数校验，如果参数不合法则返回错误，否则更新服务端侧的会话配置。 |
| ``` def append_audio(self, audio_b64: str) -> None ``` | 无   | 将base64编码后的音频数据片段追加到云端输入音频缓冲区。 音频缓冲区是你可以写入并稍后提交的临时存储。 - 打开"turn_detection"，音频缓冲区用于检测语音，服务端决定何时提交。 - 关闭"turn_detection"，客户端可以选择每个事件中放置多少音频量，最多放置 15 MiB。 例如，从客户端流式处理较小的数据块可以让 VAD 响应更迅速。 |
| ``` def append_video(self, video_b64: str) -> None ``` | 无   | 将base64编码后的图片数据添加到云端视频缓冲区。图片数据可以是本地的图片，或从视频流实时采集的图片数据。 目前对图片输入有以下限制： - 图片格式需要为JPG或JPEG，建议传入的图片分辨率为480P或720P， 最大1080P； - 单张图片大小不大于500KB（Base64编码前）； - 图片数据需要经过Base64编码； - 建议您以 1张/秒 的频率向服务端发送图片； |
| ``` def clear_appended_audio(self, ) -> None ``` | [input_audio_buffer.cleared](https://help.aliyun.com/zh/model-studio/server-events#0b916fbd51sqr) > 清空服务端收到的音频 | 删除当前云端缓冲区的音频。 |
| ``` def commit(self, ) -> None ``` | [input_audio_buffer.committed](https://help.aliyun.com/zh/model-studio/server-events#bd9bfdc258afy) > 服务端收到提交的音频 | 提交之前通过append添加到云端缓冲区的音视频，如果输入的音频缓冲区为空将产生错误。 - 打开"turn_detection"，客户端不需要发送此事件，服务端会自动提交音频缓冲区。 - 关闭"turn_detection"，客户端必须提交音频缓冲区才能创建用户消息项。 **注意**⚠️： 1. 如果 input_audio_transcription为会话配置了音频转录，系统会转录音频。 2. 提交输入音频缓冲区不会从模型创建响应。 |
| ``` def create_response(self, instructions: str = None, output_modalities: list[MultiModality] = None) -> None ``` | [服务端事件](https://help.aliyun.com/zh/model-studio/server-events#38033afc582r1) > 服务端开始生成响应 [response.output_item.added](https://help.aliyun.com/zh/model-studio/server-events#dae2260d40qtu) > 响应时有新的输出内容 [服务端事件](https://help.aliyun.com/zh/model-studio/server-events#bb4547ed5b5ht) > 对话项被创建 [response.content_part.added](https://help.aliyun.com/zh/model-studio/server-events#de7fa0b877j25) > 新的输出内容添加到assistant message 项 [response.audio_transcript.delta](https://help.aliyun.com/zh/model-studio/server-events#35396453cfood) > 增量生成的转录文字 [response.audio.delta](https://help.aliyun.com/zh/model-studio/server-events#a25cc50a15car) > 模型增量生成的音频 [response.audio_transcript.done](https://help.aliyun.com/zh/model-studio/server-events#f4d1698567bsm) > 完成文本转录 [response.audio.done](https://help.aliyun.com/zh/model-studio/server-events#9e8eb59c67qnt) > 完成音频生成 [response.content_part.done](https://help.aliyun.com/zh/model-studio/server-events#011ad54242wft) > Assistant message 的文本或音频内容流式输出完成 [response.output_item.done](https://help.aliyun.com/zh/model-studio/server-events#f580421f45w3h) > Assistant message 的整个输出项流式传输完成 [response.done](https://help.aliyun.com/zh/model-studio/server-events#f2333c777d9s4) > 响应完成 | 指示服务端创建模型响应。 打开"turn_detection"模式下配置会话时，服务端会自动创建模型响应。 |
| ``` def cancel_response(self, ) -> None ``` | 无   | 取消正在进行的响应。如果没有任何响应可供取消，服务端将以一个错误进行响应。 |
| ``` def close(self, ) -> None ``` | 无   | 终止任务，并关闭连接。 |
| ``` def get_session_id(self) -> str ``` | 无   | 获取当前任务的session_id。 |
| ``` def get_last_response_id(self) -> str ``` | 无   | 获取最近一次response的response_id。 |
| ``` def get_last_first_text_delay(self) ``` | 无   | 获取最近一次response的首包文本延迟。 |
| ``` def get_last_first_audio_delay(self) ``` | 无   | 获取最近一次response的首包音频延迟。 |

### **回调接口（OmniRealtimeCallback）**

服务端会通过回调的方式，将服务端响应事件和数据返回给客户端。您需要实现回调方法，处理服务端返回的信息或者数据。

通过`from dashscope.audio.qwen_omni import OmniRealtimeCallback`引入。

| 方法  | 参数  | 返回值 | 描述  |
| --- | --- | --- | --- |
| ``` def on_open(self) -> None ``` | 无   | 无   | 当和服务端建立连接完成后，该方法立刻被回调。 |
| ``` def on_event(self, message: str) -> None ``` | message：服务端响应事件。 | 无   | 包括对接口调用的回复响应和模型生成的文本和音频。具体可以参考：[服务端事件](https://help.aliyun.com/zh/model-studio/server-events) |
| ``` def on_close(self, close_status_code, close_msg) -> None ``` | close_status_code：关闭websocket的状态码。 close_msg：关闭websocket的关闭信息。 | 无   | 当服务已经关闭连接后进行回调。 |

## **常见问题**

#### Q：输入的音频和图片要如何对齐？

Qwen-Omni实时模型的输入将音频作为时间轴，图片会按照发送的时间，插入到音频中。您可以在音频时间轴的任意时刻添加图片。

在实时交互场景下，您可以在任意时刻打开或关闭视频输入。

#### **Q：输入图片和音频的推荐频率？**

在实时交互场景，推荐按照1 fps或2 fps的帧率发送图片，按照100ms一包的音频发送音频。

#### **Q：turn_detection开关两种模式的区别？**

目前turn_detection打开后只支持server_vad模式：

-   打开"turn_detection"：
    
    -   输入状态：云端的VAD（语音事件监测）会根据输入音频判断输入的一句话结束，并且立刻自动调用Qwen-Omni的推理下发回复文本和语音。
        
    -   回复状态：在此状态下，音视频可以继续输入，不需要在模型回复阶段中断。回复结束后会回到输入状态等待语音。
        
    -   打断：如果在模型回复期间，如果检测到用户开始说话则会触发打断，服务会立刻停止这一次的回复并且转换到输入状态。
        
-   关闭"turn_detection"：
    
    -   用户需要自己判断一轮音视频输入的结束，并且手动通过commit和create_response触发Qwen-Omni的推理，获得回复。
        
    -   在模型回复状态，需要停止音视频的输入。在模型回复结束后才可以继续输入下一轮音视频。
        
    -   需要通过cancel_response接口打断模型回复。
        

注意，在打开"turn_detection"时，依旧可以通过commit和create_response主动触发回复，通过cancel_response主动打断。

#### **Q：input_audio_transcription为何要选择其他模型？**

Qwen-Omni实时是端到端的多模态大模型，文本输出是对输入的回答，因此不会直接产生输入音频的转录。需要接入其他ASR模型转录。目前只支持gummy-realtime-v1。关于gummy可以通过[实时语音识别/翻译（Gummy）](https://help.aliyun.com/zh/model-studio/gummy-speech-recognition-translation)了解。