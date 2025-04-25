import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class GameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character = db.Column(db.String(80), nullable=False)
    level_num = db.Column(db.Integer, nullable=False)
    level_data = db.Column(db.Text, nullable=False)  # 存储每个关卡的JSON数据

    def __init__(self, userid, level_data):
        self.userid = userid
        self.level_data = json.dumps(level_data)

    def get_level_data(self):
        return json.loads(self.level_data)

    def __repr__(self):
        return f'<GameData {self.userid} {self.level_data}>'