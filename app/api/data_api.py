from flask import Blueprint, jsonify
from app import get_db_connection

data_bp = Blueprint('data_bp', __name__, url_prefix='/api/data')

@data_bp.route('/test')
def test():
    return jsonify({"message": "接口测试成功！"}), 200

@data_bp.route('/weather')
def get_weather():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data ORDER BY crawl_time DESC LIMIT 10")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            "code": 0,
            "data": data,
            "message": "查询成功"
        }), 200
    except Exception as e:
        return jsonify({
            "code": -1,
            "message": f"查询失败: {str(e)}"
        }), 500
    
import pandas as pd
import numpy as np
from flask import jsonify

@data_bp.route('/weather/analysis')
def weather_analysis():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT city, weather, crawl_time FROM weather_data ORDER BY crawl_time DESC")
        data = cursor.fetchall()
        cursor.close()
        conn.close()

        if not data:
            return jsonify({"code": -1, "message": "暂无数据可分析"}), 404

        # 用 pandas 做简单统计分析
        df = pd.DataFrame(data)
        # 统计各城市出现的天气类型数量
        analysis_result = df.groupby(['city', 'weather']).size().reset_index(name='count')
        # 转换为字典列表，方便 JSON 序列化
        result_list = analysis_result.to_dict('records')

        return jsonify({
            "code": 0,
            "data": result_list,
            "message": "天气数据分析成功"
        }), 200

    except Exception as e:
        return jsonify({
            "code": -1,
            "message": f"分析失败: {str(e)}"
        }), 500