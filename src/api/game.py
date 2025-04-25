import json

from flask import Blueprint, request, jsonify, Response
from ..models.GameData import *
from ..tools.goal import GoalManager
from ..tools.openai_client import AliyunDashScopeTool, MinimaxTool
from ..tools.prompt import prompt_tool
from ..tools.reflection import ReflectionTool
from ..tools.voice import VoiceTool, MiniMaxVoice
from settings import TEMPLATE_PATH
import torch
game_bp = Blueprint('game', __name__)
promptTools = prompt_tool()
goal = GoalManager(goal_file=TEMPLATE_PATH + "/goals/uki_2.json")
reflection_tool = ReflectionTool(model_name="nateraw/bert-base-uncased-emotion", device="cpu", torch_dtype="float32")
ai_tool = AliyunDashScopeTool()
@game_bp.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    user_id = data['user_id']
    character = data['character']
    level_num = data['level_num']
    if_restart = data['if_restart']
    if_continue = data['if_continue']
    username = data['username']
    relationship = data['relationship']
    character = promptTools.load_character_info(TEMPLATE_PATH + "/characters/uki_model.json").to_dict()
    goal = promptTools.load_goal_info(TEMPLATE_PATH + "/goals/uki_2.json")
    prompt = promptTools.load_template(TEMPLATE_PATH + "/prompt/talk.txt").substitute(
        name=character['name'],
        job=character['job'],
        age=character['age'],
        height=character['height'],
        weight=character['weight'],
        hobby=character['hobby'],
        appearance=character['appearance'],
        personality=character['personality'],
        background=character['background'],
        recent_memory=character['recent_memory'],
        description=character['description'],
        example_dialogue=character['example_dialogue'],
        emotion=goal.emotion,
        likability=goal.likability,
        username=username,
        relationship=relationship,
    )
    messages = json.dumps([{"role": "user", "content": prompt}])
    # if if_restart:
    #     game_data = GameData.query.filter_by(userid=user_id, level_num=level_num, character=character).first()
    #     if game_data:
    #         game_data.delete()
    #
    # if not if_continue:  # 如果不是继续游戏
    #     level_file_name = f"{character}_{level_num}.json"
    #     with open(level_file_name) as json_file:
    #         level_data = json.load(json_file)
    #     game_data = GameData(userid=user_id, character=character, level_num=level_num, level_data=level_data)  # 加载新的关卡数据并初始化
    # else:
    #     game_data = GameData.query.filter_by(userid=user_id, level_num=level_num, character=character).first()
    #
    # game_data.save()  # 保存到数据库
    response = {'status': 'success', 'messages': messages, 'username': username, 'bot_name': character['name'], 'bot_content': character['description']}
    return jsonify(response)

@game_bp.route('/send_text_message', methods=['POST'])
def send_text_message():
    data = request.json
    message = data['message']

    messages = json.loads(data['messages'])
    messages.append({"role": "user", "content": message})
    # 调用 OpenAI API
    # replay = ai_tool.chat(messages=messages)
    # content = ai_tool.refix_response(json.loads(replay)['choices'][0]['message']['content'].strip())
    # content = json.loads(content)['utterance']

    # 调用minimax API
    username = data.get('username', '')
    bot_name = data.get('bot_name', '')
    bot_content = data.get('bot_content', '')
    minimax = MinimaxTool(user_name=username, bot_name=bot_name, bot_content=bot_content)
    replay = minimax.chat(messages=messages)
    try:
        content = json.loads(replay)['utterance']
    except ValueError:
        content = replay  # 或者根据需要处理异常情况
    messages.append({"role": "assistant", "content": content})
    # 在此处处理发送文本消息的逻辑
    response = {'status': 'success', 'content': content, 'messages': json.dumps(messages)}
    return jsonify(response)

@game_bp.route('/send_voice_message', methods=['POST'])
def send_voice_message():
    data = request.files.get('voice')
    # 在此处处理发送语音消息的逻辑
    response = {'status': 'success'}
    return jsonify(response)

@game_bp.route('/check_goal_status', methods=['GET'])
def check_goal_status():
    # 在此处处理检查通关状态的逻辑
    status = True  # 假设的状态值
    response = {'clear_status': status}
    return jsonify(response)

@game_bp.route('/get_emotion', methods=['POST'])
def get_emotion():
    data = request.json
    content = data['content']
    emotion_data = reflection_tool.classify_text_emotion(text=content)
    response = {'status': 'success', 'data': emotion_data}
    # 返回音频数据作为HTTP响应
    return jsonify(response)

@game_bp.route('/get_voice', methods=['POST'])
def get_voice():
    data = request.json
    content = data['content']
    emotion = data.get('emotion', None)
    # cosyvoice 语音部分
    # tool = VoiceTool()
    # audio_data = tool.synthesize(content)

    # minimax 语音部分
    tool = MiniMaxVoice()
    audio_data_hex = json.loads(tool.get_voice(text=content, emotion=emotion))['data']['audio']
    # 将十六进制字符串转换为字节
    audio_data = bytes.fromhex(audio_data_hex)
    
    # 返回音频数据作为HTTP响应
    return Response(audio_data, mimetype='audio/mpeg')