from string import Template

from .character import CharacterTool
from .goal import GoalManager


class prompt_tool:
    def __init__(self):
        pass

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

    def load_character_info(self, character_path):
        """
        加载角色信息
        :param character_path: 角色信息 JSON 文件路径
        :return: 角色信息字典
        """
        with open(character_path, "r", encoding="utf-8") as f:
            person = CharacterTool(character_data=character_path)
            return person

    def load_goal_info(self, goal_path):
        """
        加载关卡信息
        :param goal_path: 关卡 JSON 文件路径
        :return: 关卡信息字典
        """
        with open(goal_path, "r", encoding="utf-8") as f:
            goal = GoalManager(goal_file=goal_path)
            return goal
    def generate_talk_prompt(self, template, character_info, goal_info):
        """
        填充提示词模板
        :param template: 模板对象
        :param character_info: 角色信息字典
        :param goal_info: 关卡信息字典
        :return: 填充后的提示词
        """
        try:
            filled_template = template.substitute(
                name=character_info.get("name", "未知"),
                job=character_info.get("job", "未知"),
                age=character_info.get("age", "未知"),
                height=character_info.get("height", "未知"),
                weight=character_info.get("weight", "未知"),
                hobby=character_info.get("hobby", "未知"),
                appearance=character_info.get("appearance", "未知"),
                personality=character_info.get("personality", "未知"),
                background=character_info.get("background", "未知"),
                recent_memory=character_info.get("recent_memory", "无"),
                description=character_info.get("description", "未知"),
                example_dialogue=character_info.get("example_dialogue", "无"),
                emotion=goal_info.get("emotion", "未知"),
                likability=goal_info.get("likability", "未知")
            )
            return filled_template
        except KeyError as e:
            raise KeyError(f"模板中缺少占位符: {e}")
