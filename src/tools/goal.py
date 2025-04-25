import json
import os
from string import Template

from .openai_client import AliyunDashScopeTool


class GoalManager:
    """
    工具类，用于控制每个关卡的目标判断。
    支持从 JSON 文件加载关卡数据。
    """

    def __init__(self, goal_file=None, person=None):
        """
        初始化关卡目标管理器。
        :param goal_file: JSON 文件路径，包含关卡目标的配置信息。
        """
        if goal_file and os.path.exists(goal_file):
            # 加载 JSON 文件中的关卡数据
            with open(goal_file, "r", encoding="utf-8") as f:
                goal_data = json.load(f)

            # 提取目标描述、成功关键词、最大轮数等信息
            self.goal_description = goal_data.get("content", "未知背景")
            self.goal = goal_data.get("goal", "未知目标")
            self.success_keywords = [self.goal]  # 默认将目标动作作为成功关键词
            self.max_turns = goal_data.get("max_turns", 10)
            self.emotion = goal_data.get("emotion", "neutral")
            self.action = goal_data.get("action", "null")
            self.likability = goal_data.get("likability", 0)
        else:
            raise ValueError("关卡文件不存在或未提供有效的 JSON 文件路径。")

        # 初始化对话历史和当前轮数
        self.current_turn = 0
        self.conversation_history = []
        self.openai_tool = AliyunDashScopeTool()
        self.person = person
    def add_dialogue(self, dialogue):
        """
        添加一条对话到对话历史中，并检查是否达成目标。
        :param dialogue: 当前对话内容（字符串）。
        :return: 如果达成目标返回 True，否则返回 False。
        """
        # 更新对话历史和当前轮数
        self.conversation_history.append(dialogue)
        self.current_turn += 1

        # 检查是否包含成功关键词
        if any(keyword in dialogue for keyword in self.success_keywords):
            return True

        # 检查是否超过最大轮数
        if self.current_turn >= self.max_turns:
            return False

        return None  # 继续游戏

    def reset(self):
        """
        重置关卡状态（用于重新开始或进入下一关）。
        """
        self.current_turn = 0
        self.conversation_history = []

    def get_status(self):
        """
        获取当前关卡的状态信息。
        :return: 包含目标描述、当前轮数和对话历史的字典。
        """
        return {
            "goal_description": self.goal_description,
            "goal": self.goal,
            "current_turn": self.current_turn,
            "max_turns": self.max_turns,
            "conversation_history": self.conversation_history
        }
    def update_emotion(self, new_emotion):
        """
        更新current_emotion
        """
        self.emotion = new_emotion

    def update_action(self, new_action):
        """
        更新current_action
        """
        self.action = new_action

    def load_template(self, template_path):
        """
        加载提示词模板
        :param template_path: 模板文件路径
        :return: 模板对象
        """
        try:
            with open(template_path, "r", encoding="utf-8") as f:
                return Template(f.read())
        except FileNotFoundError:
            raise FileNotFoundError(f"模板文件未找到: {template_path}")
        except Exception as e:
            raise RuntimeError(f"加载模板文件失败: {str(e)}")
    def update_likability(self, new_likability):
        """
        更新current_likability
        """
        template = self.load_template(template_path="")
        self.likability = new_likability
    def evaluate_goal(self):
        """
        评估当前关卡是否成功或失败。
        :return: 返回一个元组 (status, message)，如 ('success', '恭喜你获得了姜影的微信！')。
        """
        # 构造提示词模板
        template = self.load_template(template_path="")
        check_prompt = template.substitute(
            talk=self.conversation_history[-1]['content'] if self.conversation_history else "",
            action=self.action,
            emotion=self.emotion,
            goal=self.goal
        )

        try:
            # 调用 generate_response 方法获取模型响应
            response = self.ollama_tool.generate_response(prompt=check_prompt)

            # 解析模型的 JSON 响应
            raw_result = response.get("response", "{}").strip()
            parsed_result = json.loads(raw_result)

            # 提取 result 字段
            result = parsed_result.get("result", "").strip()

            # 根据 result 返回状态和消息
            if result == "success":
                return "success", f"恭喜你达成了目标：{self.goal}！"
            elif result == "failed":
                return "failure", f"很遗憾，未能完成目标：{self.goal}。"
            else:
                return "in_progress", "目标尚未完成，请继续努力！"
        except Exception as e:
            # 处理解析错误或其他异常
            return "error", f"评估目标时发生错误: {str(e)}"
    def evaluate_goal_openai(self):
        """
        评估当前关卡是否成功或失败。
        :return: 返回一个元组 (status, message)，如 ('success', '恭喜你获得了姜影的微信！')。
        """
        # 构造提示词模板
        template = self.load_template(template_path="")
        check_prompt = template.substitute(
            talk=self.conversation_history[-1]['content'] if self.conversation_history else "",
            action=self.action,
            emotion=self.emotion,
            goal=self.goal
        )
        messages = [{"role": "user", "content": check_prompt}]
        try:
            # 调用 generate_response 方法获取模型响应
            response = self.openai_tool.chat_simple(messages=messages)

            # 解析模型的 JSON 响应
            # raw_result = response.get("response", "{}").strip()
            parsed_result = json.loads(response)

            # 提取 result 字段
            result = parsed_result.get("result", "").strip()

            # 根据 result 返回状态和消息
            if result == "success":
                return "success", f"恭喜你达成了目标：{self.goal}！"
            elif result == "failed":
                return "failure", f"很遗憾，未能完成目标：{self.goal}。"
            else:
                return "in_progress", "目标尚未完成，请继续努力！"
        except Exception as e:
            # 处理解析错误或其他异常
            return "error", f"评估目标时发生错误: {str(e)}"
    @staticmethod
    def load_from_json(file_path):
        """
        静态方法：从 JSON 文件加载关卡数据并创建 GoalManager 实例。
        :param file_path: JSON 文件路径。
        :return: GoalManager 实例。
        """
        return GoalManager(goal_file=file_path)
