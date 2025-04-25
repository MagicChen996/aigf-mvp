import os
from openai import OpenAI
import re
import requests
import readline
from settings import DASHSCOPE_API_KEY, MINIMAX_API_KEY, MINIMAX_GROUP_ID
class AliyunDashScopeTool:
    def __init__(self, api_key=DASHSCOPE_API_KEY, base_url=None, model_name="qwen-plus"):
        """
        初始化阿里云 DashScope 工具类
        :param api_key: 百炼 API Key，如果未提供则从环境变量 DASHSCOPE_API_KEY 中读取
        :param base_url: API 的基础 URL，默认为 "https://dashscope.aliyuncs.com/compatible-mode/v1"
        :param model_name: 使用的模型名称，默认为 "qwen-plus"
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未提供，请设置 DASHSCOPE_API_KEY 环境变量或传入 api_key 参数。")

        self.base_url = base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
        self.model_name = model_name

        # 初始化 OpenAI 客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )
    def refix_response(self, response):
        exchange_resp = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        exchange_resp = re.sub(r'```json\s*|\s*```', '', exchange_resp)
        exchange_resp = exchange_resp.lstrip("json ").strip()
        return exchange_resp
    def chat(self, messages, model_name=None):
        """
        调用聊天接口生成响应
        :param messages: 对话历史列表，每个元素为 {"role": "user" 或 "assistant", "content": "消息内容"}
        :param model_name: 模型名称（可选），如果不传入则使用初始化时的默认模型
        :return: 模型生成的完整响应
        """
        try:
            # 动态选择模型名称
            model = model_name or self.model_name

            # 调用 API 生成响应
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )

            # 返回完整的响应
            return completion.model_dump_json(indent=2)
        except Exception as e:
            raise RuntimeError(f"调用 DashScope API 失败: {str(e)}")

    def chat_simple(self, messages, model_name=None):
        """
        调用聊天接口并返回简化版的响应内容
        :param messages: 对话历史列表，每个元素为 {"role": "user" 或 "assistant", "content": "消息内容"}
        :param model_name: 模型名称（可选），如果不传入则使用初始化时的默认模型
        :return: 模型生成的文本内容
        """
        try:
            # 动态选择模型名称
            model = model_name or self.model_name

            # 调用 API 生成响应
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )

            # 提取生成的文本内容
            response_text = self.refix_response(completion.choices[0].message.content.strip())
            return response_text
        except Exception as e:
            raise RuntimeError(f"调用 DashScope API 失败: {str(e)}")

class MinimaxTool:
    def __init__(self, bot_name=None, bot_content=None, user_name=None):
        self.api_key = MINIMAX_API_KEY
        self.group_id = MINIMAX_GROUP_ID
        self.url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={self.group_id}"
        self.headers = {"Authorization":f"Bearer {self.api_key}", "Content-Type":"application/json"}
        self.bot_name = bot_name
        self.bot_content = bot_content
        self.user_name = user_name
    def exchange_messages(self, messages):
        new_messages = []
        for msg in messages:
            if msg["role"] == "user":
                sender_type = "USER"
                sender_name = self.user_name
            elif msg["role"] == "assistant":
                sender_type = "BOT"
                sender_name = self.bot_name
            else:
                new_messages.append(msg)
            new_msg = {
                "sender_type": sender_type,
                "sender_name": sender_name,
                "text": msg["content"]
            }
            new_messages.append(new_msg)
        return new_messages

    def chat(self, messages):
        request_body = payload = {
            "model": "MiniMax-Text-01",
            "tokens_to_generate": 8192,
            "reply_constraints": {"sender_type": "BOT", "sender_name": self.bot_name},
            "messages": self.exchange_messages(messages),
            "bot_setting": [
                {
                    "bot_name": self.bot_name,
                    "content": self.bot_content,
                }
            ],
        }
        response = requests.post(self.url, headers=self.headers, json=request_body)

        reply = response.json()["reply"]
        return reply
