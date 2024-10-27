import speech_recognition as sr
import edge_tts
import asyncio
import requests
import json
from pygame import mixer
from colorama import init, Fore, Style  # 用于控制台彩色输出
from datetime import datetime
import time

class VoiceAssistant:
    def __init__(self):
        self.api_key = "your-moonshot-api-key-here"  # 替换为你的 Moonshot API 密钥
        self.api_url = "https://api.moonshot.cn/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.voice = "zh-CN-XiaoxiaoNeural"  # 改回小晓的声音
        init()
        self.is_speaking = False  # 追踪语音播放状态
        # 添加热门词汇字典，帮助语音识别
        self.custom_vocab = {
            # 游戏相关
            "dota": "DOTA",
            "潮汐": "潮汐",
            "赛博朋克": "赛博朋克",
            "夜之城": "夜之城",
            
            # 三国杀相关
            "三国杀": "三国杀",
            "无懈可击": "无懈可击",
            "杀": "杀",
            "闪": "闪",
            "桃": "桃",
            "决斗": "决斗",
            "南蛮入侵": "南蛮入侵",
            "万箭齐发": "万箭齐发",
            "五谷丰登": "五谷丰登",
            "借刀杀人": "借刀杀人",
            "顺手牵羊": "顺手牵羊",
            "过河拆桥": "过河拆桥",
            
            # 三国杀武将
            "刘备": "刘备",
            "关羽": "关羽",
            "张飞": "张飞",
            "诸葛亮": "诸葛亮",
            "曹操": "曹操",
            "孙权": "孙权",
            "吕布": "吕布",
            "貂蝉": "貂蝉",
            
            # 东北话
            "咋地": "咋地",
            "得嘞": "得嘞",
            "整一个": "整一个",
            "老铁": "老铁",
            "溜达": "溜达",
            "唠嗑": "唠嗑",
            "嘎哈": "嘎哈",
            "咋整": "咋整",
            "得劲": "得劲",
            "倍儿": "倍儿",
            "嘚瑟": "嘚瑟",
            "搓火": "搓火",
            "整明白": "整明白",
            "撒欢": "撒欢",
            "哈喇子": "哈喇子",
            "嘎达": "嘎达",
            "咋回事": "咋回事",
            "整活": "整活",
            "贼": "贼",
            "老样子": "老样子",
            
            # 网络用语
            "yyds": "YYDS",
            "awsl": "AWSL",
            "gg": "GG",
            "卡bug": "卡BUG",
            "氪金": "氪金",
            "肝": "肝",
            "打工人": "打工人",
            "摸鱼": "摸鱼",
            "卷": "卷",
            "内卷": "内卷",
            "躺平": "躺平",
            "破防": "破防",
            "上头": "上头"
        }
        
        # 添加退出命令列表
        self.exit_commands = [
            "退出程序", "结束进程", "关闭程序", "停止运行", 
            "再见", "拜拜", "结束对话", "关机", "停止"
        ]
        
        # 添加常用命令
        self.commands = {
            "暂停": self.pause_speech,
            "继续": self.resume_speech,
            "重复": self.repeat_last_response,
            "声音大一点": self.increase_volume,
            "声音小一点": self.decrease_volume
        }
        
        self.last_response = None  # 存储上一次的回复
        self.volume = 1.0  # 音量控制
        
    async def start(self):
        welcome_msg = "嘿，V，欢迎回到夜之城。今天想聊点什么？"
        print(f"{Fore.CYAN}Judy: {welcome_msg}{Style.RESET_ALL}")
        await self.speak_async(welcome_msg)
        
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True
        
        while True:
            try:
                with sr.Microphone() as source:
                    listen_task = asyncio.create_task(self.listen_for_speech(recognizer, source))
                    try:
                        voice = await listen_task
                        if voice:
                            print(f"{Fore.BLUE}你: {voice}{Style.RESET_ALL}")
                            
                            if any(cmd in voice for cmd in self.exit_commands):
                                goodbye_msg = "再见，V。期待下次见面。"
                                print(f"{Fore.CYAN}Judy: {goodbye_msg}{Style.RESET_ALL}")
                                await self.speak_async(goodbye_msg)
                                return
                            
                            # 检查是否是控制命令
                            command_found = False
                            for cmd, func in self.commands.items():
                                if cmd in voice:
                                    await func()
                                    command_found = True
                                    break
                            
                            if not command_found:
                                print(f"{Fore.YELLOW}[系统] Judy正在思考...{Style.RESET_ALL}")
                                await self.get_kimi_response(voice)
                                
                    except asyncio.CancelledError:
                        continue
            except Exception as e:
                print(f"{Fore.RED}[错误] 发生异常: {str(e)}{Style.RESET_ALL}")
                continue

    async def listen_for_speech(self, recognizer, source):
        try:
            audio = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: recognizer.listen(source, timeout=1, phrase_time_limit=10)
            )
            
            if self.is_speaking:
                mixer.music.stop()
                mixer.quit()
                self.is_speaking = False
                print(f"{Fore.YELLOW}[系统] 用户打断了对话{Style.RESET_ALL}")
            
            voice = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: recognizer.recognize_google(audio, language='zh-CN')
            )
            
            # 应用自定义词汇修正
            for key, value in self.custom_vocab.items():
                voice = voice.replace(key, value)
            
            return voice
            
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None

    async def get_kimi_response(self, text):
        # 获取当前时间
        current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        data = {
            "model": "moonshot-v1-32k",
            "messages": [
                {"role": "system", "content": """你是夜之城的AI助手Judy。请注意：
1. 回答要简洁明了，避免废话
2. 使用网络搜索获取实时信息
3. 保持赛博朋克风格，但不要过度修饰"""},
                {"role": "system", "content": f"当前时间是：{current_time}"},
                {"role": "user", "content": text}
            ],
            "temperature": 0.7,
            "web_search": True,  # 确保启用网络搜索
            "top_p": 0.95,      # 添加top_p参数提高回答的准确性
            "presence_penalty": 0.6,  # 添加presence_penalty使回答更多样化
            "stream": False     # 确保完整接收响应
        }
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: requests.post(self.api_url, headers=self.headers, json=data)
            )
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content']
            
            # 显示响应时使用Judy作为名字
            print(f"{Fore.CYAN}Judy: {response_text}{Style.RESET_ALL}")
            await self.speak_async(response_text)
            
        except Exception as e:
            print(f"{Fore.RED}[错误] 连接断开: {str(e)}{Style.RESET_ALL}")

    async def speak_async(self, text):
        try:
            print(f"{Fore.YELLOW}[系统] 正在生成语音...{Style.RESET_ALL}")
            processed_text = text.replace('**', '').replace('#', '').replace('*', '')
            
            # 使用异步方式生成语音文件
            communicate = edge_tts.Communicate(processed_text, self.voice)
            await communicate.save("temp.mp3")
            
            # 创建一个新的事件循环来处理音频播放
            def play_audio():
                mixer.init()
                mixer.music.load("temp.mp3")
                mixer.music.play()
                while mixer.music.get_busy() and self.is_speaking:
                    time.sleep(0.01)  # 更短的检查间隔
                mixer.quit()
                
            self.is_speaking = True
            # 在单独的线程中运行音频播放
            await asyncio.get_event_loop().run_in_executor(None, play_audio)
            self.is_speaking = False
            
        except Exception as e:
            print(f"{Fore.RED}[错误] 语音生成失败: {str(e)}{Style.RESET_ALL}")
            self.is_speaking = False

    async def pause_speech(self):
        if self.is_speaking:
            mixer.music.pause()
            
    async def resume_speech(self):
        if self.is_speaking:
            mixer.music.unpause()
            
    async def repeat_last_response(self):
        if self.last_response:
            await self.speak_async(self.last_response)
            
    async def increase_volume(self):
        self.volume = min(1.0, self.volume + 0.1)
        mixer.music.set_volume(self.volume)
        
    async def decrease_volume(self):
        self.volume = max(0.0, self.volume - 0.1)
        mixer.music.set_volume(self.volume)

if __name__ == '__main__':
    assistant = VoiceAssistant()
    try:
        asyncio.run(assistant.start())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[系统] 程序已退出{Style.RESET_ALL}")
