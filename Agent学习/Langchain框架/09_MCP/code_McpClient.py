import json
from loguru import logger

# 「连接」方式：通过导入获取服务端的 mcp 对象，直接读取其工具注册表，并非真实网络连接
from code_McpServer import mcp

class MCPWeatherClient:
    """教学版客户端：直接访问服务端注册表，用来观察最小调用链路。"""

    def __init__(self, mcp_instance):
        self.mcp_instance = mcp_instance
        # 获取服务端已注册的所有工具（字典：工具名 -> 可调用函数）
        # 真实 MCP 客户端不会直接碰 _tools，而是先握手/发现能力，再通过协议发起调用
        self.available_tools = mcp_instance._tools

    def check_tool_availability(self, tool_name: str) -> bool:
        """检查指定是否在服务端已注册，避免调用不存在的工具"""
        is_available = tool_name in self.available_tools
        if is_available:
            logger.info(f"工具 {tool_name} 已注册")
        else:
            logger.error(f"工具 {tool_name} 未注册")
        return is_available

    def call_get_weather(self, city: str) -> str:
        """调用服务端的 get_weather 工具，查询指定城市天气"""
        tool_name = "get_weather"
        if not self.check_tool_availability(tool_name):
            return None 

        try:
            # 直接调用服务端已注册的工具函数。
            # 真实项目里，这一步通常由 MCP 客户端经由 stdio 或 HTTP 传输层去完成。
            weather_result = self.available_tools[tool_name](city)
            logger.info(
                f"成功获取 {city} 天气数据，返回结果长度：{len(weather_result)}"
            )
            return weather_result
        except Exception as exc:
            logger.error(f"调用 {tool_name} 工具失败：{str(exc)}")
            return None

def run_client_demo():
    """客户端演示：初始化客户端，依次查询多城市天气并格式化输出"""
    logger.info("初始化 MCP 天气客户端...")
    client = MCPWeatherClient(mcp)

    # 调用天气查询工具（支持 Beijing、Shanghai、Guangzhou 等英文城市名）
    target_cities = ["Beijing", "Shanghai"]
    for city in target_cities:
        logger.info(f"\n========== 查询 {city} 天气 ==========")
        weather_data = client.call_get_weather(city)
        if weather_data:
            # 格式化输出结果（可选，方便阅读）
            formatted_data = json.dumps(
                json.loads(weather_data), indent=4, ensure_ascii=False
            )
            print(f"格式化天气结果：\n{formatted_data}")
        print("-" * 50)


if __name__ == "__main__":
    logger.info("启动 MCP 天气客户端...")
    run_client_demo()


"""
【输出示例】
2026-08-28 16:24:15.550 | INFO     | __main__:<module>:63 - 启动 MCP 天气客户端...
2026-08-28 16:24:15.551 | INFO     | __main__:run_client_demo:45 - 初始化 MCP 天气客户端...
2026-08-28 16:24:15.551 | INFO     | __main__:run_client_demo:51 - 
========== 查询 Beijing 天气 ==========
2026-08-28 16:24:15.551 | INFO     | __main__:check_tool_availability:20 - 工具 get_weather 已注册
2026-08-28 16:24:17.891 | INFO     | code_McpServer:get_weather:71 - 查询 Beijing 天气结果：{'coord': {'lon': 116.3972, 'lat': 39.9075}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': '阴，多云', 'icon': '04d'}], 'base': 'stations', 'main': {'temp': 19.94, 'feels_like': 20.39, 'temp_min': 19.94, 'temp_max': 19.94, 'pressure': 1011, 'humidity': 92, 'sea_level': 1011, 'grnd_level': 1006}, 'visibility': 10000, 'wind': {'speed': 1.79, 'deg': 168, 'gust': 2.3}, 'rain': {'1h': 0.1}, 'clouds': {'all': 100}, 'dt': 1787905208, 'sys': {'type': 1, 'id': 9609, 'country': 'CN', 'sunrise': 1787866690, 'sunset': 1787914433}, 'timezone': 28800, 'id': 1816670, 'name': 'Beijing', 'cod': 200}
2026-08-28 16:24:17.891 | INFO     | __main__:call_get_weather:35 - 成功获取 Beijing 天气数据，返回结果长度：596
格式化天气结果：
{
    "coord": {
        "lon": 116.3972,
        "lat": 39.9075
    },
    "weather": [
        {
            "id": 804,
            "main": "Clouds",
            "description": "阴，多云",
            "icon": "04d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 19.94,
        "feels_like": 20.39,
        "temp_min": 19.94,
        "temp_max": 19.94,
        "pressure": 1011,
        "humidity": 92,
        "sea_level": 1011,
        "grnd_level": 1006
    },
    "visibility": 10000,
    "wind": {
        "speed": 1.79,
        "deg": 168,
        "gust": 2.3
    },
    "rain": {
        "1h": 0.1
    },
    "clouds": {
        "all": 100
    },
    "dt": 1787905208,
    "sys": {
        "type": 1,
        "id": 9609,
        "country": "CN",
        "sunrise": 1787866690,
        "sunset": 1787914433
    },
    "timezone": 28800,
    "id": 1816670,
    "name": "Beijing",
    "cod": 200
}
--------------------------------------------------
2026-08-28 16:24:17.891 | INFO     | __main__:run_client_demo:51 - 
========== 查询 Shanghai 天气 ==========
2026-08-28 16:24:17.891 | INFO     | __main__:check_tool_availability:20 - 工具 get_weather 已注册
2026-08-28 16:24:18.662 | INFO     | code_McpServer:get_weather:71 - 查询 Shanghai 天气结果：{'coord': {'lon': 121.4581, 'lat': 31.2222}, 'weather': [{'id': 802, 'main': 'Clouds', 'description': '多云', 'icon': '03d'}], 'base': 'stations', 'main': {'temp': 30.92, 'feels_like': 37.38, 'temp_min': 30.92, 'temp_max': 30.92, 'pressure': 1003, 'humidity': 70, 'sea_level': 1003, 'grnd_level': 1003}, 'visibility': 10000, 'wind': {'speed': 8, 'deg': 100}, 'clouds': {'all': 50}, 'dt': 1787905015, 'sys': {'type': 1, 'id': 9659, 'country': 'CN', 'sunrise': 1787866058, 'sunset': 1787912636}, 'timezone': 28800, 'id': 1796236, 'name': 'Shanghai', 'cod': 200}
2026-08-28 16:24:18.662 | INFO     | __main__:call_get_weather:35 - 成功获取 Shanghai 天气数据，返回结果长度：557
格式化天气结果：
{
    "coord": {
        "lon": 121.4581,
        "lat": 31.2222
    },
    "weather": [
        {
            "id": 802,
            "main": "Clouds",
            "description": "多云",
            "icon": "03d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 30.92,
        "feels_like": 37.38,
        "temp_min": 30.92,
        "temp_max": 30.92,
        "pressure": 1003,
        "humidity": 70,
        "sea_level": 1003,
        "grnd_level": 1003
    },
    "visibility": 10000,
    "wind": {
        "speed": 8,
        "deg": 100
    },
    "clouds": {
        "all": 50
    },
    "dt": 1787905015,
    "sys": {
        "type": 1,
        "id": 9659,
        "country": "CN",
        "sunrise": 1787866058,
        "sunset": 1787912636
    },
    "timezone": 28800,
    "id": 1796236,
    "name": "Shanghai",
    "cod": 200
}
--------------------------------------------------
"""