import os
from typing import TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START

from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

class State(TypedDict):
    query: str
    answer: str


def node(state: State):
    print("开始调用 node 节点")

    model = init_chat_model(
        model = os.getenv("OPENAI_MODEL_NAME"),
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    llm_result = model.invoke([("user", state["query"])])
    print("llm invoke 结束", end="\n\n")

    return {"answer": llm_result}


def main():
    graph = (
        StateGraph(state_schema=State).add_node(node).add_edge(START, "node").compile()
    )

    inputs = {"query": "帮我生成一个200字的小学生作文，主题为我的一天"}

    # messages：从图内触发的大模型调用处流式输出；(chunk, metadata) 见官方文档
    for chunk, _metadata in graph.stream(inputs, stream_mode="messages"):
        # print(f"type of chunk:{type(chunk)}")  # 调试时可打开
        print(chunk.content, end="")
        # print(chunk, end="")


if __name__ == "__main__":
    main()

"""
【输出示例】
开始调用 node 节点
早晨，温暖的阳光把我叫醒。我快速穿好衣服，吃完妈妈做的爱心早餐，背着书包高高兴兴地去上学。

在学校里，我认真听讲，学到了好多新知识。最开心的是体育课，我和好朋友们一起比赛跑步，操场上到处都是我们的欢声笑语。

放学后，我回到家认真写完作业，还看了一会儿我最爱的童话书。晚上，妈妈给我讲了睡前故事，我甜甜地进入了梦乡。

这就是我的一天，简单又快乐，我非常喜欢！llm invoke 结束

"""