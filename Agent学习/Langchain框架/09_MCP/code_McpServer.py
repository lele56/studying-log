import json
import os
import httpx
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

# ---------------------- 极简版 MCP 服务类（无 FastMCP 依赖，纯手写）----------------------
# 若使用 FastMCP，则不需要下面这一整段 class，直接 mcp = FastMCP("名") + @mcp.tool() + mcp.run() 即可，见 McpServerWeatherByFastMCP.py
class MCPWeatherServer:
    """极简版教学服务类：只保留“注册工具”和“维持进程”两层概念"""

    def __init__(self, name: str, host: str, port: int):
        """保留原实例化参数，与原代码配置对齐"""
        self.name = name
        self.host = host
        self.port = port
        # 存储已注册的工具函数；本仓库里的同进程客户端会直接读取这个注册表做教学演示
        self._tools = {}

    def tool(self):
        """实现 @mcp.tool() 装饰器：把普通函数登记到工具注册表中"""

        def decorator(func):
            self._tools[func.__name__] = func  # 注册工具函数，key 为函数名
            return func

        return decorator

    def run(self, transport: str):
        """模拟 run() 入口；这里只打印监听信息并保持进程存活，不提供完整网络服务。"""
        if transport != "sse":
            logger.warning(f"不支持的传输协议 {transport}，默认使用 SSE")
        logger.info(f"启动 MCP SSE 天气服务器，监听 http://{self.host}:{self.port}/sse")
        self._keep_alive()

    def _keep_alive(self):
        """简单保持进程运行，便于从日志层面观察“服务端已启动”的状态。"""
        try:
            while True:
                pass
        except KeyboardInterrupt:
            logger.info("MCP 天气服务器已停止")


# ---------------------- 创建 MCP 实例并注册工具 ----------------------
# 对应教程：MCP 架构中的「MCP 服务器」角色，为客户端提供可暴露的能力
# 若改用 FastMCP：构造函数只接受服务名，不能写 FastMCP(..., host=..., port=...)；
# host/port 在 run() 时传，如 mcp.run(transport="sse", host="127.0.0.1", port=8000)。参见 McpServerWeatherByFastMCP.py
mcp = MCPWeatherServer("WeatherServerSSE", host="127.0.0.1", port=8000)

@mcp.tool()  # 将 get_weather 注册为 MCP 工具；教学版客户端会直接从注册表里取出它
def get_weather(city: str) -> str:
    """
    查询指定城市的即时天气信息。
    参数 city：城市英文名，如 Beijing
    返回：OpenWeather API 的 JSON 字符串
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv(
            "OPENWEATHER_API_KEY"
        ),  # 从环境变量读取 API Key，避免写死密钥
        "units": "metric",  # 使用摄氏度
        "lang": "zh_cn",  # 输出语言为简体中文
    }
    resp = httpx.get(url, params=params)
    data = resp.json()
    logger.info(f"查询 {city} 天气结果：{data}")
    return json.dumps(data, ensure_ascii=False)

if __name__ == "__main__":
    logger.info("启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse")
    mcp.run(transport="sse")


"""
【输出示例】
2026-08-28 15:30:31.562 | INFO     | __main__:<module>:75 - 启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse
2026-08-28 15:30:31.562 | INFO     | __main__:run:35 - 启动 MCP SSE 天气服务器，监听 http://127.0.0.1:8000/sse
"""