from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ---------- ChatPromptTemplate 创建 ----------
messages = [
    ("system", "你是一个{role}，请回答我提出的问题"),
    ("human", "请回答：{question}")
]

# 两种方法创建 ChatPromptTemplate 对象
chat_prompt1 = ChatPromptTemplate.from_messages(messages)
chat_prompt2 = ChatPromptTemplate(messages)

# format_messages 填入变量，最终生成提示消息列表
chatPromptTemplate = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}。"),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}。"),
        ("human", "{user_input}"),
    ]
)

prompt = chatPromptTemplate.format_messages(
    name="Bob", thing="AI", user_input="7 + 5等于多少"
)

# ---------- MessagesPlaceholder 使用 ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题"),
    MessagesPlaceholder("memory"), # 使用 MessagePlaceHolder 占位符，后续可以通过 invoke 方法传入消息列表
    ("human", "{question}")
])

# 通过 invoke 方法传入消息列表和问题
prompt_value = prompt.invoke({
    "memory": [
        HumanMessage(content="我的名字叫亮仔，是一名程序员"),
        AIMessage(content="好的，亮仔你好")
    ],
    "question": "请问我的名字叫什么？"
})