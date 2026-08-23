import os

from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger

# 创建聊天提示模板（Runnable 子类）：包含系统角色与用户问题占位符
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个{role}，请简短回答我提出的问题"),
        ("human", "请回答:{question}"),
    ]
)

# 使用 invoke 渲染提示词，返回 PromptValue，可直接交给模型（统一接口）
prompt = chat_prompt.invoke(
    {"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"}
)
logger.info(prompt)

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 模型接受上一步的 PromptValue，返回 AIMessage
result = model.invoke(prompt)
logger.info(f"********>模型原始输出:\n{result}")

# 字符串输出解析器（Runnable）：从 AIMessage 中取出文本，得到更适合业务继续处理的文本结果
parser = StrOutputParser()

# 解释器接收 AIMessage，这里得到的是文本结果
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")

print()
print("*" * 60)
print()

# 用管道符 | 构建顺序链：LCEL 是写法，组合后的 chain 才是最终得到的 RunnableSequence 对象
chain = chat_prompt | model | parser

# 链整体也是 Runnable：一次 invoke 完成「渲染 → 模型 → 解析」，入参为提示词变量
result_chain = chain.invoke(
    {"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"}
)

logger.info(f"Chain执行结果:\n{result_chain}")
logger.info(f"Chain执行结果类型: {type(result_chain)}")

print()
print(type(chain))

"""
【输出示例】
2026-08-23 17:33:25.533 | INFO     | __main__:<module>:28 - messages=[SystemMessage(content='你是一个AI助手，请简短回答我提出的问题', additional_kwargs={}, response_metadata={}), HumanMessage(content='请回答:什么是LangChain，简洁回答100字以内', additional_kwargs={}, response_metadata={})]
2026-08-23 17:33:49.262 | INFO     | __main__:<module>:40 - ********>模型原始输出:
content='LangChain是一个开源框架，用于开发基于大语言模型（LLM）的应用程序。它通过提供标准接口和丰富组件，简化了LLM与外部数据、API及工具的连接，助力开发者快速构建问答系统、智能代理等复杂AI应用。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 482, 'prompt_tokens': 38, 'total_tokens': 520, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 422, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': None}, 'model_provider': 'openai', 'model_name': 'qwen3.7-max-preview', 'system_fingerprint': None, 'id': 'chatcmpl-d58d91f2-15bf-93a2-8814-fee626652b10', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--01a02df8-071f-7eb0-9152-fadb0d5664e2-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 38, 'output_tokens': 482, 'total_tokens': 520, 'input_token_details': {}, 'output_token_details': {'reasoning':422}}
2026-08-23 17:33:49.262 | INFO     | __main__:<module>:47 - 解析后的结构化结果:
LangChain是一个开源框架，用于开发基于大语言模型（LLM）的应用程序。它通过提供标准接口和丰富组件，简化了LLM与外部数据、API及工具的连接，助力开发者快速构建问答系统、智能代理等复杂AI应用。
2026-08-23 17:33:49.262 | INFO     | __main__:<module>:48 - 结果类型: <class 'langchain_core.messages.base.TextAccessor'>

************************************************************

2026-08-23 17:33:56.377 | INFO     | __main__:<module>:62 - Chain执行结果:
LangChain是一个用于开发大语言模型（LLM）应用的开源框架。它提供模块化工具，支持将LLM与外部数据、API和各种工具链接，帮助开发者快速构建智能问答、聊天机器人等复杂的AI应用。
2026-08-23 17:33:56.377 | INFO     | __main__:<module>:63 - Chain执行结果类型: <class 'langchain_core.messages.base.TextAccessor'>

<class 'langchain_core.runnables.base.RunnableSequence'>
"""