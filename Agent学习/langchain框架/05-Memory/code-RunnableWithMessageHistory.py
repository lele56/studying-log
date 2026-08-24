import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from loguru import logger

# 初始化模型
llm = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 提示模板：history 占位符用于注入历史消息，input 为当前用户输入
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
parser = StrOutputParser()
chain = prompt | llm | parser

# 记忆组件：内存实现，进程内有效，重启后丢失
history = InMemoryChatMessageHistory()

# 包装链为「带历史」版本：本例固定返回同一个 history，重点先放在“自动读写历史”
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,  # 历史消息管理器
    input_messages_key="input",                      # 输入消息键名
    history_messages_key="history",                  # 历史消息键名
)
history.clear()
# 保留 session_id 配置，是为了让调用方式和 v2 / redis 版保持一致
config = RunnableConfig(configurable={"session_id": "user-001"})

# 第一轮
logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
# 第二轮
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))

"""
【输出示例】
2026-08-24 16:15:26.764 | INFO     | __main__:<module>:50 - 你好，张三！很高兴认识你。

“爱好学习”是一个非常棒的品质，它能让人不断拓宽视野、获得成长。

你平时最喜欢学习哪方面的知识呢？是科技、历史、文学，还是其他什么有趣的领域？如果有任何问题想要探讨，或者需要我帮你查资料、解答疑惑，随时都可以告诉我哦！
2026-08-24 16:15:28.708 | INFO     | __main__:<module>:52 - 你叫张三，你的爱好是学习。
"""