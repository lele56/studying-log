import json
import os
import httpx
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

from langchain_classic.agents import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

@tool
def get_weather(loc):
    """
    查询即时天气函数

    :param loc: 必要参数，字符串类型，表示查询天气的城市名称；中国城市需用英文名，如 Beijing、Shanghai。
    :return: OpenWeather API 返回的天气信息，JSON 序列化后的字符串。
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric",
        "lang": "zh_cn",
    }
    response = httpx.get(url, params=params, timeout=30)
    data = response.json()
    print(json.dumps(data))
    return json.dumps(data)

# 初始化大模型，用于理解用户问题并决定是否调用工具、如何组合结果
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# 定义 Agent 的对话结构：system 定角色，human 为用户输入，
# placeholder 供 Executor 填入中间推理与工具调用记录
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是天气助手，请根据用户的问题，给出相应的天气信息"),
        ("human", "{input}"),
        (
            "placeholder",
            "{agent_scratchpad}",
        ),  # V0.3 必备：Agent 的「草稿本」，记录多轮推理与工具输出
    ]
)

tools = [get_weather]

# 将 LLM、工具列表、提示模板组装成「可做工具调用决策」的 Agent（尚未执行）
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

# AgentExecutor 负责循环：调用 Agent → 执行其选中的工具 →
# 把结果写回 agent_scratchpad → 再交给 Agent，直到结束
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools,
)

# 一次问题触发多工具调用（北京、上海天气）并聚合回答
result = agent_executor.invoke(
    {"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"}
)

print(result)


"""
【输出示例】
{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 804, "main": "Clouds", "description": "\u9634\uff0c\u591a\u4e91", "icon": "04d"}], "base": "stations", "main": {"temp": 19.94, "feels_like": 20.39, "temp_min": 19.94, "temp_max": 19.94, "pressure": 1011, "humidity": 92, "sea_level": 1011, "grnd_level": 1006}, "visibility": 10000, "wind": {"speed": 1.95, "deg": 183, "gust": 3.13}, "clouds": {"all": 100}, "dt": 1787911703, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1787866690, "sunset": 1787914433}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 802, "main": "Clouds", "description": "\u591a\u4e91", "icon": "03d"}], "base": "stations", "main": {"temp": 29.92, "feels_like": 36.92, "temp_min": 29.92, "temp_max": 29.92, "pressure": 1003, "humidity": 79, "sea_level": 1003, "grnd_level": 1003}, "visibility": 10000, "wind": {"speed": 6, "deg": 110}, "clouds": {"all": 38}, "dt": 1787911852, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1787866058, "sunset": 1787912636}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}
{'input': '请问今天北京和上海的天气怎么样，哪个城市更热？', 'output': '今天北京和上海的天气情况如下：\n\n*   **北京**：当前气温为 **19.94°C**，天气为阴天/多云，湿度较高（92%），体感温度约为 20.39°C。\n*   **上海**：当前气温为 **29.92°C**，天气为多云，湿度为 79%，体感温度高达 36.92°C。\n\n**哪个城市更热？**\n显然是**上海更热**。上海的实际气温比北京高出了近 10°C，而且由于湿度和气温的综合影响，上海的体感温度接近 37°C，会比北京感觉闷热得多。如果您在上海，请注意防暑降温！'}
"""