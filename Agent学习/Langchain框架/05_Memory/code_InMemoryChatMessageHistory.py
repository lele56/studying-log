import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

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

# 创建内存版历史实例（BaseChatMessageHistory 的实现）
history = InMemoryChatMessageHistory()

# 手动添加用户消息并调用模型；模型输入为当前全部 message
history.add_user_message("我叫张三，我的爱好是学习")
ai_message = llm.invoke(history.messages)
logger.info(f"第一次回答\n{ai_message.content}")
# 手动把 AI 回复写回 history；否则下一轮只会看到用户消息，达不到“多轮记忆”的效果
history.add_message(ai_message)

# 再追加一轮：用户问「我叫什么？我的爱好是什么？」；此时 history.messages 已含上一轮
history.add_user_message("我叫什么？我的爱好是什么？")
ai_message2 = llm.invoke(history.messages)
logger.info(f"第二次回答\n{ai_message2.content}")
# 这一轮的 AI 回复也同样需要手动写回
history.add_message(ai_message2)

# 遍历当前会话全部消息；可以直观看到 history.messages 本质上就是一组 BaseMessage
for index, message in enumerate(history.messages, start=1):
    logger.info(f"第{index}条[{message.type}] {message.content}")

"""
【输出示例】
2026-08-24 16:43:56.400 | INFO     | __main__:<module>:28 - 第一次回答
你好，张三！很高兴认识你。👋

“爱好是学习”真的是一个非常棒的爱好，保持好奇心并不断吸收新知识是一件特别有意义的事情！

既然你喜欢学习，那我这个人工智能助手刚好可以成为你的好帮手。你平时最喜欢学习哪个领域的知识呢？是科学、历史、编程、语言，还是其他什么有趣的领域？如果有任何想探讨的问题，随时都可以问我哦！
2026-08-24 16:44:01.178 | INFO     | __main__:<module>:35 - 第二次回答
你叫张三，你的爱好是学习。😊 

有什么我可以帮你的吗？
2026-08-24 16:44:01.178 | INFO     | __main__:<module>:41 - 第1条[human] 我叫张三，我的爱好是学习
2026-08-24 16:44:01.178 | INFO     | __main__:<module>:41 - 第2条[ai] 你好，张三！很高兴认识你。👋

“爱好是学习”真的是一个非常棒的爱好，保持好奇心并不断吸收新知识是一件特别有意义的事情！

既然你喜欢学习，那我这个人工智能助手刚好可以成为你的好帮手。你平时最喜欢学习哪个领域的知识呢？是科学、历史、编程、语言，还是其他什么有趣的领域？如果有任何想探讨的问题，随时都可以问我哦！
2026-08-24 16:44:01.178 | INFO     | __main__:<module>:41 - 第3条[human] 我叫什么？我的爱好是什么？
2026-08-24 16:44:01.178 | INFO     | __main__:<module>:41 - 第4条[ai] 你叫张三，你的爱好是学习。😊 

有什么我可以帮你的吗？
"""