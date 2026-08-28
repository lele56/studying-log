import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from loguru import logger

# 初始化模型
llm = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 按 session_id 保存多份历史，便于多用户/多会议；生产可改为 Redis 等
store = {}

def get_session_history(session_id: str):
    """
    根据 session_id 获取对应的历史消息对象。
    如果不存在则创建一个新的 InMemoryChatMessageHistory。
    """
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 定义 Prompt 模板
#     - system: 给模型设定角色
#     - MessagesPlaceholder: 历史消息将注入这里
#     - human: 当前用户输入
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个友好的中文助理，会根据上下文回答问题。"),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

# 构建基本链：Prompt -> Model -> Parser
memory_chain = prompt | llm | StrOutputParser()

# 包装为带历史链：get_session_history 决定「当前 session 用哪份 history」
with_history = RunnableWithMessageHistory(
    memory_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 创建不同 session_id
cfg_user_001 = {"configurable": {"session_id": "user-001"}}
cfg_user_002 = {"configurable": {"session_id": "user-002"}}

print("用户A（user-001）：我叫张三。")
print("AI：", with_history.invoke({"question": "我叫张三。"}, cfg_user_001))

print("\n用户B（user-002）：我叫李四。")
print("AI：", with_history.invoke({"question": "我叫李四。"}, cfg_user_002))

print("\n用户A（user-001）：我叫什么？")
print("AI：", with_history.invoke({"question": "我叫什么？"}, cfg_user_001))

print("\n用户B（user-002）：我叫什么？")
print("AI：", with_history.invoke({"question": "我叫什么？"}, cfg_user_002))

# ---------- 查看当前存储了哪些历史数据 ----------
# store 的 key 为 session_id，value 为该会话的 InMemoryChatMessageHistory
# 每个 history 的 .messages 为 List[BaseMessage]，即该会话至今的全部消息（HumanMessage、AIMessage 等）
print("\n--- 当前 store 中的历史数据 ---")
for sid, history in store.items():
    print(f"[session_id={sid}] 共 {len(history.messages)} 条消息:")
    for i, msg in enumerate(history.messages):
        # msg 有 .type（如 human/ai）、.content（文本内容）
        content = str(msg.content)
        content_preview = (content[:50] + "…") if len(content) > 50 else content
        print(f"  {i+1}. [{msg.type}] {content_preview}")
print("--- 以上 ---\n")

"""
【输出示例】
用户A（user-001）：我叫张三。
AI： 你好，张三！很高兴认识你。请问今天有什么我可以帮你的吗？

用户B（user-002）：我叫李四。
AI： 你好，李四！很高兴认识你。请问今天有什么我可以帮你的吗？

用户A（user-001）：我叫什么？
AI： 你叫张三呀！请问还有什么我可以帮你的吗？

用户B（user-002）：我叫什么？
AI： 你叫李四。

--- 当前 store 中的历史数据 ---
[session_id=user-001] 共 4 条消息:
  1. [human] 我叫张三。
  2. [ai] 你好，张三！很高兴认识你。请问今天有什么我可以帮你的吗？
  3. [human] 我叫什么？
  4. [ai] 你叫张三呀！请问还有什么我可以帮你的吗？
[session_id=user-002] 共 4 条消息:
  1. [human] 我叫李四。
  2. [ai] 你好，李四！很高兴认识你。请问今天有什么我可以帮你的吗？
  3. [human] 我叫什么？
  4. [ai] 你叫李四。
--- 以上 ---
"""