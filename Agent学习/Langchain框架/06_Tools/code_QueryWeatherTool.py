from langchain_core.tools import tool
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

# @tool 装饰器：函数名 get_weather 即工具名，下方 docstring 会成为模型理解工具的重要依据
@tool
def get_weather(loc: str) -> str:
    """
    查询指定城市的即时天气

    参数:
        loc: 城市名称字符串。为了提高调用成功率，建议优先传英文城市名，
             如 Beijing、Shanghai。
    
    返回:
        OpenWeather 当前天气接口返回的 JSON 字符串，包含气温、体感温度、
        湿度、风速、天气描述等信息。
    """
    # step 1. 构建请求 URL 
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2. 设置查询参数：q=城市名，appid 从环境变量读取（安全实践），units=metric 为摄氏度，lang=zh_cn 为中文描述
    params = {
        "q": loc,
        "appid": os.getenv(
            "OPENWEATHER_API_KEY"
        ),  # 从 .env 读取，勿将 Key 写死在代码中
        "units": "metric",  # 温度单位：metric=摄氏度
        "lang": "zh_cn",  # 天气描述语言：简体中文
    }

    # Step 3. 发送 GET 请求；httpx 与 requests 用法类似，timeout 避免长时间阻塞
    response = httpx.get(url, params=params, timeout=30)

    # Step 4. 解析响应为 Python 字典后，再序列化为 JSON 字符串返回，供后续链继续处理
    weather_data = response.json()
    return json.dumps(weather_data)

# 本地测试：单参数工具可直接传值；若和更通用的工具调用风格保持一致，也可传 {"loc": "..."}
# result = get_weather.invoke("shanghai")
result = get_weather.invoke("beijing")
print(result)

"""
【输出示例】
{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 804, "main": "Clouds", "description": "\u9634\uff0c\u591a\u4e91", "icon": "04d"}], "base": "stations", "main": {"temp": 22.94, "feels_like": 23.69, "temp_min": 22.94, "temp_max": 22.94, "pressure": 1007, "humidity": 92, "sea_level": 1007, "grnd_level": 1002}, "visibility": 10000, "wind": {"speed": 1.22, "deg": 207, "gust": 6.51}, "clouds": {"all": 89}, "dt": 1787651313, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1787607319, "sunset": 1787655504}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
"""