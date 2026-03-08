import scrapy
import pymysql

# 数据库配置（请确认密码正确）
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "05181128",
    "database": "data_platform",
    "charset": "utf8mb4"
}

class WeatherSpider(scrapy.Spider):
    name = "weather_spider"
    # 稳定的目标链接（北京天气，可正常访问）
    start_urls = ["https://www.weather.com.cn/weather1d/101010100.shtml"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = None
        self.cursor = None
        # 初始化数据库连接
        try:
            self.conn = pymysql.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✅ 数据库连接成功！")
        except Exception as e:
            print(f"❌ 数据库连接失败：{e}")
            raise  # 连接失败直接终止爬虫

    def parse(self, response):
        # 第一步：确认parse方法执行（已缩进4个空格）
        print("✅ parse 方法被调用了！")
        
        # 第二步：直接插入测试数据，跳过XPath（排除提取问题）
        try:
            sql = "INSERT INTO weather_data (city, weather) VALUES (%s, %s)"
            self.cursor.execute(sql, ("测试城市", "测试天气"))
            self.conn.commit()
            print("✅ 测试数据插入成功！")
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ 测试数据插入失败：{e}")

    def closed(self, reason):
        # 第三步：关闭数据库连接（修复了self.comn的拼写错误）
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("✅ 爬虫结束，数据库连接已关闭")