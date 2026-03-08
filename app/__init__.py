from flask import Flask
from app.config import Config
import pymysql

def get_db_connection():
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册 data_bp（原有代码）
    from app.api.data_api import data_bp
    app.register_blueprint(data_bp)

    # 新增：注册 agent_bp
    from app.api.agent_api import agent_bp
    app.register_blueprint(agent_bp)

    @app.route('/')
    def index():
        return "后端服务启动成功！数据库连接配置已加载", 200

    return app