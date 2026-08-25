import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

from langchain_core.output_parsers import JsonOutputKeyToolsParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from loguru import logger

from code_QueryWeatherTool import get_weather

# 初始化模型
llm = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 将工具绑定到模型：请求时会把 get_weather 的名称、描述、参数 schema 发给模型，模型随后可能返回 tool_calls
llm_with_tools = llm.bind_tools([get_weather])

# 解析器：从模型输出中提取“命中的天气工具参数”，得到可直接传给 get_weather 的入参
parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)

# 天气查询链：用户问题 → 模型（可能返回 tool_calls）→ 解析出参数 → 执行 get_weather → 得到天气 JSON 字符串
get_weather_chain = llm_with_tools | parser | get_weather

# 输出链：把天气 JSON 塞进提示词，由模型转成更适合用户阅读的自然语言描述
output_prompt = PromptTemplate.from_template(
    """你将收到一段 JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。
    以下是天气 JSON 数据：
    请将其转换为中文天气描述，例如：
    "北京现在天气：多云，气温 28℃，体感有点闷热（约 32℃），湿度 75%，微风（东南风 2 米/秒），
    能见度很好，大约 10 公里。建议穿短袖短裤。适合做户外运动。"
    """
)
output_parser = StrOutputParser()
output_chain = output_prompt | llm | output_parser

# 完整链：先拿到天气 JSON，再包装成 {"weather_json": x} 送入输出链，得到最终中文描述
full_chain = get_weather_chain | (lambda x: {"weather_json": x}) | output_chain

result = full_chain.invoke("请问北京今天的天气如何？")
logger.info(result)

"""
【输出示例】
{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 500, "main": "Rain", "description": "\u5c0f\u96e8", "icon": "10d"}], "base": "stations", "main": {"temp": 22.94, "feels_like": 23.69, "temp_min": 22.94, "temp_max": 22.94, "pressure": 1007, "humidity": 92, "sea_level": 1007, "grnd_level": 1002}, "visibility": 10000, "wind": {"speed": 1.22, "deg": 207, "gust": 6.51}, "rain": {"1h": 0.14}, "clouds": {"all": 89}, "dt": 1787651934, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1787607319, "sunset": 1787655504}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}
2026-08-25 18:07:45.385 | INFO     | __main__:<module>:50 - 北京现在天气：小雨，气温 23℃，体感约 24℃，湿度较高（92%），微风（西南风 1.2 米/秒，偶有阵风）。能见度很好，大约 10 公里。出门记得带伞，建议穿件薄外套，不太适合进行户外活动。
"""