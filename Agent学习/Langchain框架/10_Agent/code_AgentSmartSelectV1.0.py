import os
import json
import httpx
from pathlib import Path
from typing_extensions import (
    TypedDict,
)  # Python < 3.12 下 Pydantic 要求用 typing_extensions.TypedDict

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# .env 在项目根目录，从任意子目录运行脚本时都从根目录加载
load_dotenv()


@tool
def get_weather(loc: str) -> str:
    """
    查询即时天气函数
    :param loc: 城市英文名，如 Beijing、Shanghai。
    :return: OpenWeather API 返回的天气信息（JSON 字符串）。
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
    return json.dumps(data, ensure_ascii=False)

# 定义结构化输出：Agent 最终回答会按此结构填充，便于代码中直接取字段
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str

model = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL_NAME"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# V1.0 一步创建 Agent：模型、工具、系统提示、输出格式一次传入
# 如果后面还要扩展短期记忆或拦截控制，通常会继续给 create_agent 传 checkpointer / middleware
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=(
        "你是天气助手。"
        "当用户询问多个城市天气时，"
        "你需要分别调用工具获取数据，并进行比较分析。"
    ),
    response_format=WeatherCompareOutput,
)

# 调用 Agent，返回结果中包含 messages 与 structured_response（若指定了 response_format）
# 这里先用 invoke 看最终结果；如需观察中间步骤，可在工程里改为 stream()
result = agent.invoke({"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"})
print(result)
print()
print(json.dumps(result["structured_response"], ensure_ascii=False, indent=2))

"""
【输出示例】
{'messages': [AIMessage(content='\n</think>\n\n', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 109, 'prompt_tokens': 418, 'total_tokens': 527, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None, 'text_tokens': 109}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0, 'text_tokens': 418}}, 'model_provider': 'openai', 'model_name': 'qwen3.7-plus-2026-05-26', 'system_fingerprint': None, 'id': 'chatcmpl-a1abee4f-1906-9514-874c-a9bd0511ed24', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a047e1-018e-7cc1-8801-5b0d500ef4c9-0', tool_calls=[{'name': 'get_weather', 'args': {'loc': 'Beijing'}, 'id': 'call_ed69d089d9004727ac2485bd', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'loc': 'Shanghai'}, 'id': 'call_10f0de926a1c400791ef316d', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'loc': 'Beijing'}, 'id': 'call_c58892cf3d99429e9c4e59a8', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'loc': 'Shanghai'}, 'id': 'call_1395346f17c54313a69ac62e', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 418, 'output_tokens': 109, 'total_tokens': 527, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 804, "main": "Clouds", "description": "阴，多云", "icon": "04d"}], "base": "stations", "main": {"temp": 19.94, "feels_like": 20.39, "temp_min": 19.94, "temp_max": 19.94, "pressure": 1011, "humidity": 92, "sea_level": 1011, "grnd_level": 1006}, "visibility": 10000, "wind": {"speed": 1.95, "deg": 183, "gust": 3.13}, "clouds": {"all": 100}, "dt": 1787911703, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1787866690, "sunset": 1787914433}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}', name='get_weather', id='10769884-adee-4e03-8848-1373a852428a', tool_call_id='call_ed69d089d9004727ac2485bd'), ToolMessage(content='{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 802, "main": "Clouds", "description": "多云", "icon": "03d"}], "base": "stations", "main": {"temp": 29.92, "feels_like": 36.92, "temp_min": 29.92, "temp_max": 29.92, "pressure": 1003, "humidity": 79, "sea_level": 1003, "grnd_level": 1003}, "visibility": 10000, "wind": {"speed": 6, "deg": 110}, "clouds": {"all": 38}, "dt": 1787911852, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1787866058, "sunset": 1787912636}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}', name='get_weather', id='fa0bd8f0-9db9-47ce-8d19-329cfeb95bb3', tool_call_id='call_10f0de926a1c400791ef316d'), ToolMessage(content='{"coord": {"lon": 116.3972, "lat": 39.9075}, "weather": [{"id": 804, "main": "Clouds", "description": "阴，多云", "icon": "04d"}], "base": "stations", "main": {"temp": 19.94, "feels_like": 20.39, "temp_min": 19.94, "temp_max": 19.94, "pressure": 1011, "humidity": 92, "sea_level": 1011, "grnd_level": 1006}, "visibility": 10000, "wind": {"speed": 1.95, "deg": 183, "gust": 3.13}, "clouds": {"all": 100}, "dt": 1787911703, "sys": {"type": 1, "id": 9609, "country": "CN", "sunrise": 1787866690, "sunset": 1787914433}, "timezone": 28800, "id": 1816670, "name": "Beijing", "cod": 200}', name='get_weather', id='3452b655-6e68-440c-a863-d14721831f6d', tool_call_id='call_c58892cf3d99429e9c4e59a8'), ToolMessage(content='{"coord": {"lon": 121.4581, "lat": 31.2222}, "weather": [{"id": 802, "main": "Clouds", "description": "多云", "icon": "03d"}], "base": "stations", "main": {"temp": 29.92, "feels_like": 36.92, "temp_min": 29.92, "temp_max": 29.92, "pressure": 1003, "humidity": 79, "sea_level": 1003, "grnd_level": 1003}, "visibility": 10000, "wind": {"speed": 6, "deg": 110}, "clouds": {"all": 38}, "dt": 1787911852, "sys": {"type": 1, "id": 9659, "country": "CN", "sunrise": 1787866058, "sunset": 1787912636}, "timezone": 28800, "id": 1796236, "name": "Shanghai", "cod": 200}', name='get_weather', id='38cf7f47-6776-4a29-8133-2937d935b395', tool_call_id='call_1395346f17c54313a69ac62e'), AIMessage(content='\n</think>\n\n', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 259, 'prompt_tokens': 1766, 'total_tokens': 2025, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 0, 'rejected_prediction_tokens': None, 'text_tokens': 259}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0, 'text_tokens': 1766}}, 'model_provider': 'openai', 'model_name': 'qwen3.7-plus-2026-05-26', 'system_fingerprint': None, 'id': 'chatcmpl-ee76dac8-7a23-9b19-b475-c7b2253b77b3', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a047e1-1039-7b62-9e75-bd2f3cdb3a50-0', tool_calls=[{'name': 'WeatherCompareOutput', 'args': {'beijing_temp': 19.94, 'shanghai_temp': 29.92, 'hotter_city': 'Shanghai', 'summary': '北京当前气温为19.94°C，天气为阴，多云；上海当前气温为29.92°C，天气为多云。上海比北京热约9.98°C，上海是更热的城市。'}, 'id': 'call_c46c18e2996a47d48f805f9f', 'type': 'tool_call'}, {'name': 'WeatherCompareOutput', 'args': {'beijing_temp': 19.94, 'shanghai_temp': 29.92, 'hotter_city': 'Shanghai', 'summary': '当前上海比北京更热，温差约10°C。北京阴天多云，体感温度20.39°C，湿度较高(92%)；上海多云，体感温度高达36.92°C，湿度79%。'}, 'id': 'call_09a2782f244c4dd88345dd8d', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 1766, 'output_tokens': 259, 'total_tokens': 2025, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 0}}), ToolMessage(content='Error: Model incorrectly returned multiple structured responses (WeatherCompareOutput, WeatherCompareOutput) when only one is expected.\n Please fix your mistakes.', name='WeatherCompareOutput', id='c13c9a8b-2c18-4e59-9b7e-f77cb45f253a', tool_call_id='call_c46c18e2996a47d48f805f9f'), ToolMessage(content='Error: Model incorrectly returned multiple structured responses (WeatherCompareOutput, WeatherCompareOutput) when only one is expected.\n Please fix your mistakes.', name='WeatherCompareOutput', id='5e0afeb8-aa6f-4491-ac7a-3a7541c2ce58', tool_call_id='call_09a2782f244c4dd88345dd8d'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 270, 'prompt_tokens': 2100, 'total_tokens': 2370, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 137, 'rejected_prediction_tokens': None, 'text_tokens': 270}, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0, 'text_tokens': 2100}}, 'model_provider': 'openai', 'model_name': 'qwen3.7-plus-2026-05-26', 'system_fingerprint': None, 'id': 'chatcmpl-6b148005-eb7c-9a58-b2b4-023a5ddda35b', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a047e1-23dd-7db1-a33f-b9a4b930dde5-0', tool_calls=[{'name': 'WeatherCompareOutput', 'args': {'beijing_temp': 19.94, 'shanghai_temp': 29.92, 'hotter_city': 'Shanghai', 'summary': '当前上海比北京更热，温差约10°C。北京阴天多云，体感温度20.39°C，湿度较高(92%)；上海多云，体感温度高达36.92°C，湿度79%。'}, 'id': 'call_2aa32e17947845ad92b14473', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 2100, 'output_tokens': 270, 'total_tokens': 2370, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 137}}), ToolMessage(content="Returning structured response: {'beijing_temp': 19.94, 'shanghai_temp': 29.92, 'hotter_city': 'Shanghai', 'summary': '当前上海比北京更热，温差约10°C。北京阴天多云，体感温度20.39°C，湿度较高(92%)；上海多云，体感温度高达36.92°C，湿度79%。'}", name='WeatherCompareOutput', id='335d5508-0ae7-4d0e-b3da-b7dd6f0de6d1', tool_call_id='call_2aa32e17947845ad92b14473')], 'structured_response': {'beijing_temp': 19.94, 'shanghai_temp': 29.92, 'hotter_city': 'Shanghai', 'summary': '当前上海比北京更热，温差约10°C。北京阴天多云，体感温度20.39°C，湿度较高(92%)；上海多云，体感温度高达36.92°C，湿度79%。'}}

{
  "beijing_temp": 19.94,
  "shanghai_temp": 29.92,
  "hotter_city": "Shanghai",
  "summary": "当前上海比北京更热，温差约10°C。北京阴天多云，体感温度20.39°C，湿度较高(92%)；上海多云，体感温度高达36.92°C，湿度79%。"
}
"""