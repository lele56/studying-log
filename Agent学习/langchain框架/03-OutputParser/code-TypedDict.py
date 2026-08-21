import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 用 TypedDict 定义「一个动物」的结构；Annotated 里的字符串是给模型看的描述，便于生成合适内容
class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

# 定义「动物列表」：一个字段 animals，类型是 Animal 的列表
class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]

# 普通对话消息
messages = [{"role": "user", "content": "任意生成三种动物，以及他们的 emoji 表情"}]

# 给模型绑定「结构化输出」：按 AnimalList 的结构返回并解析
llm_with_structured_output = model.with_structured_output(AnimalList)
resp = llm_with_structured_output.invoke(messages)

print(
    resp
)  # 得到符合 AnimalList 的 dict，如 {"animals": [{"animal": "猫", "emoji": "🐱"}, ...]}

"""
【输出示例】
{'animals': [{'animal': '狗', 'emoji': '🐶'}, {'animal': '猫', 'emoji': '🐱'}, {'animal': '鸟', 'emoji': '🐦'}]}
"""