from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger
from pydantic import BaseModel, Field

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 定义一个 Pydantic 模型，用于约束模型输出的 JSON 结构
class person(BaseModel):
    """定义一条「新闻」的结构：时间、人物、事件。用于约束模型输出的 JSON 形状。"""
    time: str = Field(..., description="新闻发生的时间")
    person: str = Field(..., description="新闻涉及的人物")
    event: str = Field(..., description="新闻事件的内容")

# 绑定 Pydantic 模型：主要驱动 get_format_instructions() 的 schema；invoke 后得到 dict
parser = JsonOutputParser(pydantic_object=person)

# 获取「格式说明」：描述 Person 各字段，便于拼进提示词让模型按此输出
format_instructions = parser.get_format_instructions()

# 在 human 消息里加入 {format_instructions}，模型会看到「请按如下格式输出 JSON …」
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，你只能输出结构化JSON数据。"),
        ("human", "请生成一个关于{topic}的新闻。{format_instructions}"),
    ]
)

# ---------- 第二种方式 ----------
# 在系统消息里直接写明：返回 json，且包含 q（问题）、a（答案）字段
# chat_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "你是一个{role}，请简短回答我提出的问题，结果返回json格式，q字段表示问题，a字段表示答案。",
#         ),
#         ("human", "请回答:{question}"),
#     ]
# )

# 填入变量，生成最终的提示消息列表
prompt = chat_prompt.format_messages(
    topic="人工智能领域的最新进展",
    format_instructions=format_instructions
)

logger.info(prompt)

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")

# 用同一解析器解析，得到符合 Person 结构的数据（dict，或可转成 Person 实例）
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")


"""
【输出示例】
2026-08-21 17:36:41.826 | INFO     | __main__:<module>:54 - [SystemMessage(content='你是一个AI助手，你只能输出结构化JSON数据。', additional_kwargs={}, response_metadata={}), HumanMessage(content='请生成一个关于人工智能领域的最新进展的新闻。STRICT OUTPUT FORMAT:\n- Return only the JSON value that conforms to the schema. Do not include any additional text, explanations, headings, or separators.\n- Do not wrap the JSON in Markdown or code fences (no ``` or ```json).\n- Do not prepend or append any text (e.g., do not write "Here is the JSON:").\n- The response must be a single top-level JSON value exactly as required by the schema (object/array/etc.), with no trailing commas or comments.\n\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]} the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema (shown in a code block for readability only — do not include any backticks or Markdown in your output):\n```\n{"description": "定义一条「新闻」的结构：时间、人物、事件。用于约束模型输出的 JSON 形状。", "properties": {"time": {"description": "新闻发生的时间", "title": "Time", "type": "string"}, "person": {"description": "新闻涉及的人物", "title": "Person", "type": "string"}, "event": {"description": "新闻事件的内容", "title": "Event", "type": "string"}}, "required": ["time", "person", "event"]}\n```', additional_kwargs={}, response_metadata={})]
2026-08-21 17:37:05.775 | INFO     | __main__:<module>:65 - 模型原始输出:
content='{\n  "time": "2024年5月14日",\n  "person": "萨姆·奥特曼",\n  "event": "OpenAI公司正式发布了新一代多模态大语言模型GPT-4o，该模型不仅能高效处理文本，还能进行极低延迟的实时语音与视觉交互，标志着人工智能在人机自然交互领域取得了重大突破。"\n}' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 977, 'prompt_tokens': 395, 'total_tokens': 1372, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 887, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'qwen3.7-max-preview', 'system_fingerprint': None, 'id': 'chatcmpl-bdd4cc22-ed1c-9e5a-ac8a-94d5d5edadc5', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--01a023ae-169f-7170-b674-30dc925a793e-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 395, 'output_tokens': 977, 'total_tokens': 1372, 'input_token_details': {}, 'output_token_details': {'reasoning': 887}}
2026-08-21 17:37:05.776 | INFO     | __main__:<module>:69 - 解析后的结构化结果:
{'time': '2024年5月14日', 'person': '萨姆·奥特曼', 'event': 'OpenAI公司正式发布了新一代多模态大语言模型GPT-4o，该模型不仅能高效处理文本，还能进行极低延迟的实时语音与视觉交互，标志着人工智能在人机自然交互领域取得了重大突破。'}
2026-08-21 17:37:05.776 | INFO     | __main__:<module>:70 - 结果类型: <class 'dict'>
"""