# LangGraph 框架学习

## 📅 学习信息
- **日期**: 2026-09-01
- **主题**: LangGraph 框架基础 - Graph
- **目标**: 理解 Graph API 里的 Graph（图） 到底是什么，知道 StateGraph、START、END、compile()、invoke() 分别负责什么。

## 📚 核心知识点

### 1. State Schema（状态模式） 是什么？
- State Schema 是图的**数据结构契约**，定义了图中允许流转的所有字段及其类型。它配合 `input_schema` 和 `output_schema` 一起，约束图的对外接口和内部实现。

### 2. 关键概念
- **Input/Output Schema（输入/输出约束）**：约束图**对外的接口**。调用方只需传 `input_schema` 定义的字段，图最终也只返回 `output_schema` 定义的字段，**隐藏内部实现细节**。
- **Reducer（规约器）**：字段级别的合并策略，决定节点返回的更新值如何与当前 State 合并（覆盖、追加、累加等）。
- **Superstep（超级步）**：图执行中的**"一个回合"**，所有可运行的节点**并行执行**，最后框架统一收集结果并按 Reducer 合并成新 State。
- **Partial Update（部分更新）**：节点返回的对 State 的部分更新字典，框架会自动合并。

### 3. 重要函数
- `StateGraph(input_schema=..., output_schema=...)`：创建状态图构建器，约束图的输入输出。
- `Annotated[Type, reducer]`：类型提示工具，为 State 字段**附加元数据（Reducer）**，决定该字段的合并策略。
- `add_messages`：LangGraph 内置的 Reducer，使消息字段按追加而非覆盖方式合并，适合对话场景。
- `operator.add`：Python 标准库操作符，作为 Reducer 时实现列表拼接或数值累加。

## 💻 代码示例

### 示例 1：State Schema 定义（基础 + 输入输出约束）
```python
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

# 仅包含「输入」字段的 Schema
class InputState(TypedDict):
    question: str

# 仅包含「输出」字段的 Schema
class OutputState(TypedDict):
    answer: str

# 图内部使用的完整 State Schema（输入 + 输出）
class OverallState(InputState, OutputState):
    pass

def answer_node(state: InputState):
    """处理节点：根据 question 生成 answer"""
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    return {"answer": answer, "question": state["question"]}

# 指定 input_schema / output_schema，约束图的对外接口
builder = StateGraph(
    OverallState,
    input_schema=InputState,
    output_schema=OutputState,
)
builder.add_node("answer_node", answer_node)
builder.add_edge(START, "answer_node")
builder.add_edge("answer_node", END)
graph = builder.compile()

# invoke 只传 InputState 的字段；返回结果仅包含 OutputState 的字段
result = graph.invoke({"question": "你好"})
print(result)  # 输出: {'answer': '你好'}
```

### 示例 2：Reducer 机制演示（默认覆盖 vs add_messages vs operator.add）
```python
from typing import Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class MyState(TypedDict):
    # 默认覆盖：节点返回新值会直接替换旧值
    name: str
    
    # add_messages：追加消息，适合对话历史
    messages: Annotated[List, add_messages]

def update_node(state: MyState) -> dict:
    return {
        "name": "新名字",  # 覆盖旧值
        "messages": [("assistant", "你好！")],  # 追加到列表
    }

graph = StateGraph(MyState)
graph.add_node("update", update_node)
graph.add_edge(START, "update")
graph.add_edge("update", END)
app = graph.compile()

result = app.invoke({
    "name": "旧名字",
    "messages": [("user", "Hello")]
})
print(result)
# name 被覆盖: "新名字"
# messages 被追加: [("user", "Hello"), ("assistant", "你好！")]
```

### 示例 3：自定义 Reducer（乘法累加场景）
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

def MyOperatorMul(current: float, update: float) -> float:
    """自定义乘法 Reducer：处理首次合并的边界情况"""
    if current == 0.0:
        return 1.0 * update  # 从 1.0 开始乘
    return current * update

class MultiplyState(TypedDict):
    factor: Annotated[float, MyOperatorMul]

def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}

builder = StateGraph(MultiplyState)
builder.add_node("multiplier", multiplier)
builder.add_edge(START, "multiplier")
builder.add_edge("multiplier", END)
graph = builder.compile()

# 初始 factor=5.0 与节点返回 2.0 经 Reducer 合并为 5.0 * 2.0 = 10.0
result = graph.invoke({"factor": 5.0})
print(result)  # 输出: {'factor': 10.0}
```

### 示例 4：完整图构建流程（入口 → 处理 → 出口）
```python
from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    process_data: str

def input_node(state: GraphState) -> dict:
    """入口节点：写入初始数据"""
    return {"process_data": "input_value"}

def process_node(state: GraphState) -> dict:
    """处理节点：更新数据"""
    return {"process_data": "process_value"}

def output_node(state: GraphState) -> dict:
    """出口节点：读取当前数据"""
    return {"process_data": state.get("process_data")}

# 1. 初始化 StateGraph
graph = StateGraph(GraphState)

# 2. 添加节点
graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

# 3. 连边：start → input → process → output → end
graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)

# 4. 编译
app = graph.compile()

# 5. 执行
result = app.invoke({"process_data": "初始值"})
print(result)  # 输出: {'process_data': 'process_value'}
```

## 🐛 问题与思考

### Q1: 为什么 State 不是随手放变量的字典？
**答**: State 是整张图的数据契约，决定节点能读写什么、并行结果怎么合并、后续如何恢复和调试。字段随便加会让图越来越难维护。

### Q2: 设计 State 字段时，你会如何区分输入、过程状态和输出？
**答**: 输入字段承接外部请求，过程字段保存中间分类、检索结果、工具返回，输出字段对外暴露最终结果。三者混在一起会让接口和内部实现互相绑死。

### Q3: Reducer 选错会产生什么隐蔽 bug？
**答**: 该追加的被覆盖，丢失历史；该覆盖的被追加，会状态膨胀；并行结果如果没有按业务语义合并，最终状态可能顺序不稳、重复或冲突。Reducer 是业务规则，不只是语法。

### Q4: 什么时候字段应该留在内部 State，而不是放进 input_schema 或 output_schema？
**答**: 只服务内部节点流转、调试或中间计算的字段留在内部 State；外部调用必须提供的才进 input，外部确实需要消费的才进 output。接口越克制，图越容易演进。

### Q5：为什么理解 Superstep 有助于设计 Reducer？
**答**：因为多个节点可能在同一轮或相邻轮写入同一个字段，最终状态不是靠某各节点手动拼出来的，而是由运行时统一合并。Reducer 设计错了，并行分支越多，状态越容易出现覆盖、重复或顺序不稳定。

## 📝 学习总结

### State 是 LangGraph 的中心数据结构
- State 是 LangGraph 的中心数据结构，不是普通"函数参数传来传去"的替代品，而是整张图的共享状态快照和单一事实来源。

### State = Schema + Reducer
- LSchema 定义字段结构，Reducer 定义字段更新怎么和旧状态合并；把两者放在一起看，才是完整的 State 设计。

### Reducer 选择要跟业务语义对齐
- 默认覆盖适合最新值，add_messages 适合消息历史，operator.add 适合拼接/累加，自定义 Reducer 适合更复杂的合并规则。