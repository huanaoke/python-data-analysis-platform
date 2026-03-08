from flask import Blueprint, jsonify, request
from app import get_db_connection
import pandas as pd

# 初始化蓝图，前缀为 /api/agent
agent_bp = Blueprint('agent_bp', __name__, url_prefix='/api/agent')

# 测试路由
@agent_bp.route('/test')
def test():
    return jsonify({"message": "Agent API test successful!"}), 200

# 你要访问的 /query 路由
@agent_bp.route('/query', methods=['GET'])
def query():
    try:
        city = request.args.get('city', '测试城市')
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "SELECT weather, crawl_time FROM weather_data WHERE city = %s ORDER BY crawl_time DESC"
        cursor.execute(sql, (city,))
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not data:
            return jsonify({"code": -1, "message": f"未查询到{city}的天气数据"}), 404

        df = pd.DataFrame(data)
        latest_weather = df.iloc[0]['weather']
        latest_time = df.iloc[0]['crawl_time']
        ai_response = f"根据数据查询，{city}最新的天气情况为{latest_weather}，数据采集时间为{latest_time}。"

        return jsonify({
            "code": 0,
            "query": city,
            "ai_response": ai_response,
            "data": data[:3]
        }), 200
    except Exception as e:
        return jsonify({"code": -1, "message": f"查询失败：{str(e)}"}), 500