from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class DiliState(TypedDict):
    topic: str
    joke: str

def refine_topic(state: DiliState):
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: DiliState):
    return {"joke": f"This is a joke about {state['topic']}"}

def main():
    graph = (
        StateGraph(DiliState)
        .add_node(refine_topic)
        .add_node(generate_joke)
        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)
        .compile()
    )

    # updates：每步结束后只流出「本步对状态的更新」
    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="updates"):
        print(chunk)

    print()

    # values：每步结束后流出「当前完整 state」（未写字段可能仍为空字符串等初始形态）
    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="values"):
        print(chunk)


if __name__ == "__main__":
    main()

"""
【输出示例】
{'refine_topic': {'topic': 'ice cream and cats'}}
{'generate_joke': {'joke': 'This is a joke about ice cream and cats'}}

{'topic': 'ice cream'}
{'topic': 'ice cream and cats'}
{'topic': 'ice cream and cats', 'joke': 'This is a joke about ice cream and cats'}
"""