import operator
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

"""
如果字段默认值是 `0.0` 时，乘法规约很容易在第一次合并就变成 `0.0`，后面再乘什么都还是 `0.0`。
"""

class MultiplyState(TypedDict):
    # factor 默认值是 0.0
    factor: Annotated[float, operator.mul]

def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}

def run_demo():
    print("operator.mul Reducer（数值相乘）演示:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    result = graph.invoke({"factor": 5.0})
    print(f"初始状态: {{'factor': 5.0}}")
    print(f"执行结果: {result}")
    print(
        "说明: 因 float 默认 0.0 先参与规约，0.0 * 5.0 = 0.0，后续乘 2.0 仍为 0.0；乘法场景请用自定义 Reducer。\n"
    )

if __name__ == "__main__":
    run_demo()


"""
【输出示例】
operator.mul Reducer（数值相乘）演示:
初始状态: {'factor': 5.0}
执行结果: {'factor': 0.0}
说明: 因 float 默认 0.0 先参与规约，0.0 * 5.0 = 0.0，后续乘 2.0 仍为 0.0；乘法场景请用自定义 Reducer。
"""