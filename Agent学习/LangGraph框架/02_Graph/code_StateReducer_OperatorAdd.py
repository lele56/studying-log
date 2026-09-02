import operator
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


"""
operator.add 是一个很常见的内置合并策略，但它对不同数据类型的语义不一样：

对 列表 来说，是列表拼接，效果类似 current + update。
对 字符串 来说，是字符串连接。
对 数值 来说，是数值相加。
"""

class ListAddState(TypedDict):
    data: Annotated[List[int], operator.add]

def producer_1(state: ListAddState) -> dict:
    return {"data": [1, 2]}


def producer_2(state: ListAddState) -> dict:
    return {"data": [3, 4]}

def run_demo():
    print("3.1 列表追加 Reducer 演示:")
    builder = StateGraph(ListAddState)
    builder.add_node("producer1", producer_1)
    builder.add_node("producer2", producer_2)
    builder.add_edge(START, "producer1")
    builder.add_edge("producer1", "producer2")
    builder.add_edge("producer2", END)
    graph = builder.compile()
    result = graph.invoke({"data": [0]})
    print(f"初始状态: {{'data': [0]}}")
    print(f"执行结果: {result}\n")


if __name__ == "__main__":
    run_demo()

"""
【输出示例】
3.1 列表追加 Reducer 演示:
初始状态: {'data': [0]}
执行结果: {'data': [0, 1, 2, 3, 4]}

"""