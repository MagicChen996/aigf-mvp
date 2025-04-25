from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys
from src.api.game import game_bp
from src.api.user import user_bp

sys.path.insert(0, os.path.abspath(
os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__, template_folder='src/ui', static_folder='src/ui')

app.register_blueprint(user_bp)
app.register_blueprint(game_bp)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'  # SQLite 示例
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭不必要的修改跟踪以提高性能

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('home.html')
@app.route('/game_page')
def game_page():
    return render_template('game_page.html')
if __name__ == '__main__':
    app.run(debug=True)