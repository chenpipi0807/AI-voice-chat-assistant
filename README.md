# Judy AI 助手

一个基于 Moonshot AI 的赛博朋克风格语音助手，灵感来自《赛博朋克2077》。

kimi的API需要自主获取一下：https://platform.moonshot.cn/console/account

补充一下，个人使用API还是蛮便宜的，昨天奴役kimi写了十万字的小说，才花十块钱不到。


![微信截图_20241027152916](https://github.com/user-attachments/assets/9fcb8659-93de-4432-ad4f-ad2404a78933)
![微信截图_20241027152942](https://github.com/user-attachments/assets/2e7d609a-6212-4e14-93a0-96fbf325dacf)


## 功能特点

- 🎙️ 语音交互
- 🔊 实时语音合成
- ⚡ 支持打断对话
- 🌃 赛博朋克风格回复
- 🎯 自定义词汇识别
- 🎚️ 音量控制
- ⏯️ 支持暂停/继续播放

## 使用前准备

1. 获取 Moonshot API 密钥
   - 访问 [Moonshot AI](https://www.moonshot.cn/)
   - 注册并获取 API 密钥
   - 将密钥替换到 `run_judy.py` 中的 `your-moonshot-api-key-here`

2. 安装依赖


pip install -r requirements.txt

3. 运行程序

python run_judy.py

## 支持的命令

- `暂停`：暂停当前语音播放
- `继续`：继续播放语音
- `重复`：重复上一次的回答
- `声音大一点`：增加音量
- `声音小一点`：减小音量
- `退出程序`/`再见`：结束对话并退出

## 自定义词汇支持

- 游戏相关：DOTA、赛博朋克、夜之城等
- 三国杀相关：武将名称、卡牌名称等
- 东北方言：咋地、得嘞、老铁等
- 网络用语：YYDS、GG、氪金等

## 注意事项

- 请确保有可用的麦克风设备
- 需要稳定的网络连接
- 首次运行可能需要下载语音模型
- API 密钥请妥善保管，不要上传到公开仓库

## 开发环境

- Python 3.8+
- Windows/Linux/MacOS

## 依赖项

- speech_recognition: 语音识别
- edge-tts: 微软语音合成
- pygame: 音频播放
- colorama: 控制台彩色输出
- requests: HTTP 请求
- asyncio: 异步支持

## License

MIT License

