from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from loguru import logger

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 构造对话模板
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请简短回答我提出的问题"),
        ("human", "请回答:{question}"),
    ]
)
# 填入变量
prompt = chat_prompt.format_messages(role="AI开发工程师", question="什么是LangChain，简洁回答100字以内")
logger.info(prompt)

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 调用模型：传入 prompt，得到的是 AIMessage 等对象（原始输出）
result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result}")

# 创建字符串解析器：只做「从 result 里取 content 转成 str」
# 单条 AIMessage 时确实等价于 result.content；用解析器的好处：可链式组合（prompt | model | parser）、
# 流式时统一处理 chunk、多条消息时按约定取最后一条等，且与 JsonOutputParser 等接口一致便于替换。
parser = StrOutputParser()

# 解析：parser.invoke(result) 会返回一个 str 类型的结果（即 result.content）
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info("\n")
logger.info(
    f"结果类型: {type(response)}"
) # 输出示例: <class 'langchain_core.messages.base.TextAccessor'>

"""
【输出示例】
2026-08-21 17:15:55.142 | INFO     | __main__:<module>:21 - [SystemMessage(content='你是一个AI开发工程师，请简短回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:什么是LangChain，简洁回答100字以内', additional_kwargs={}, response_metadata={})]
2026-08-21 17:16:21.983 | INFO     | __main__:<module>:31 - 模型原始输出:
content='LangChain是一个开源框架，专为构建大语言模型（LLM）应用而设计。它提供标准化接口，将LLM与外部数据、API、记忆机制和代理等组件无缝连接，帮助开发者快速搭建如文档问答、智能助手等复杂AI应用。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 441, 'prompt_tokens': 38, 'total_tokens': 479, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 379, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'qwen3.7-max-preview', 'system_fingerprint': None, 'id': 'chatcmpl-e198d88b-0270-9602-8f24-52bf90af06a5', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--01a0239b-508d-75f1-89f7-0d9d574b3b3b-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 38, 'output_tokens': 441, 'total_tokens': 479, 'input_token_details': {}, 'output_token_details': {'reasoning': 379}}
2026-08-21 17:16:21.984 | INFO     | __main__:<module>:36 - 解析后的结构化结果:
LangChain是一个开源框架，专为构建大语言模型（LLM）应用而设计。它提供标准化接口，将LLM与外部数据、API、记忆机制和代理等组件无缝连接，帮助开发者快速搭建如文档问答、智能助手等复杂AI应用。
2026-08-21 17:16:21.984 | INFO     | __main__:<module>:37 - 
2026-08-21 17:16:21.984 | INFO     | __main__:<module>:38 - 结果类型: <class 'langchain_core.messages.base.TextAccessor'>
"""