from typing import Any

import json
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import httpx

load_dotenv()

# 构造函数只接受「服务名」；网络绑定信息在 run() 时再指定
mcp = FastMCP(
    "WeatherServerSSE"
)  # "WeatherServerSSE" 就是你自己起的名，可改成 "MyWeather" 等

@mcp.tool()
def get_weather(city: str) -> str:
    """查询指定城市的即时天气信息。city 为城市英文名，如 Beijing、Shanghai"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn",
    }
    resp = httpx.get(url, params=params)
    data = resp.json()
    return json.dumps(data, ensure_ascii=False)


if __name__ == "__main__":
    # host、port 在 run() 时传入，不是构造函数。
    # 这里启动后，mcp.json 中的 weather 服务就可以按约定地址连到它。
    mcp.run(transport="sse", host="127.0.0.1", port=8000)