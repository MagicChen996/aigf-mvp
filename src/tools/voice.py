# coding=utf-8

import dashscope
from dashscope.audio.tts_v2 import *
import requests
from settings import DASHSCOPE_API_KEY, MINIMAX_API_KEY, MINIMAX_GROUP_ID
# 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
dashscope.api_key = DASHSCOPE_API_KEY

class VoiceTool:
    def __init__(self, model="cosyvoice-v1", voice="longwan"):
        self.model = model
        self.voice = voice
        self.synthesizer = SpeechSynthesizer(model=self.model, voice=self.voice)

    def synthesize(self, text):
        audio = self.synthesizer.call(text)
        return audio

class MiniMaxVoice:
    def __init__(self):
        self.api_key = MINIMAX_API_KEY
        self.group_id = MINIMAX_GROUP_ID
        self.url = f"https://api.minimax.chat/v1/t2a_v2?GroupId={self.group_id}"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        # self.bot_name = bot_name
        # self.bot_content = bot_content
        # self.user_name = user_name
    def exchange_emotion(self, emotion):
        if emotion == "":
            return "neutral"
        emotion_mapping = {
            "anger": "angry",
            "fear": "fearful",
            "sadness": "sad",
            "joy": "happy",
            "surprise": "surprised",
            "love": "neutral"
        }
        
        new_emotion = emotion_mapping.get(emotion, "")
        return new_emotion
    def get_voice(self, text, emotion):

        payload = {
            "model": "speech-02-hd",
            "text": text,
            "timber_weights": [
                {
                    "voice_id": "yangmi_new",
                    "weight": 1
                }
            ],
            "voice_setting": {
                "voice_id": "",
                "speed": 1,
                "pitch": 0,
                "vol": 1,
                "emotion": self.exchange_emotion(emotion),
                "latex_read": True
            },
            "audio_setting": {
                "sample_rate": 32000,
                "bitrate": 128000,
                "format": "mp3"
            },
            "language_boost": "auto"
        }

        response = requests.post(self.url, headers=self.headers, json=payload)
        return response.text
