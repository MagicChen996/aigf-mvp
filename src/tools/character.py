import json
import os


class CharacterTool:
    """
    工具类，用于获取和管理人物信息。
    """

    def __init__(self, character_data=None):
        """
        初始化工具类实例。
        :param character_data: 字典类型的角色信息，或者 JSON 文件路径。
        """
        if isinstance(character_data, str) and os.path.exists(character_data):
            # 如果传入的是文件路径，则加载 JSON 文件
            with open(character_data, "r", encoding="utf-8") as f:
                self.character_info = json.load(f)
        elif isinstance(character_data, dict):
            # 如果传入的是字典，则直接使用
            self.character_info = character_data
        else:
            raise ValueError("character_data 必须是 JSON 文件路径或字典类型的数据。")


    def update_emotion(self, new_emotion):
        """
        更新人物的情绪状态。
        :param new_emotion: 新的情绪状态（例如：'开心', '悲伤', '愤怒' 等）。
        """
        self.character_info["emotion"] = new_emotion

    def update_recent_memory(self, new_memory):
        """
        更新人物的近期记忆。
        :param new_memory: 新的记忆内容。
        """
        self.character_info["recent_memory"] = new_memory

    def to_dict(self):
        """将人物信息转换为字典格式"""
        return self.character_info

    @staticmethod
    def load_from_json(file_path):
        """
        静态方法：从 JSON 文件加载人物信息。
        :param file_path: JSON 文件路径。
        :return: CharacterTool 实例。
        """
        return CharacterTool(character_data=file_path)

    def save_to_json(self, file_path):
        """
        将人物信息保存到 JSON 文件。
        :param file_path: 保存的目标文件路径。
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.character_info, f, ensure_ascii=False, indent=4)
