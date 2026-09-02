# LangGraph 框架学习

## 📅 学习信息
- **日期**: 2026-09-01
- **主题**: LangGraph 框架基础 - Node 和 Edge
- **目标**: 理解 Node（节点） 的定义、职责与常见写法，知道节点为什么是 LangGraph 的最小执行单元。
掌握 Edge（边） 的核心类型：普通边、条件边、入口点、条件入口点，建立“图为什么能按规则流转”的直觉。

## 📚 核心知识点

### 1. Node 的进阶配置
- Node 不仅是最小执行单元，还支持 **partial 绑定额外参数**、**RetryPolicy 自动重试**、**缓存（cache=True）** 等进阶能力。通过 `functools.partial` 可以提前固定 LLM、API Key 等依赖，让节点函数只接收 `state` 参数。

### 2. Edge 的动态流转
- Edge 决定流程走向，分为 **普通边**（固定路径）、**条件边**（路由函数动态决定下一跳）、**入口点**（指定图起点）、**条件入口点**（根据初始状态决定从哪个节点开始）。结合 `Send` 和 `Command` 对象，可以实现 **动态并行分发** 和 **决策跳转**。

### 3. 关键概念
- **Node（节点）**：LangGraph 的最小执行单元，本质是被图调度的 Python 函数。支持 `partial` 绑定参数、`RetryPolicy` 重试策略、`cache=True` 缓存结果等进阶配置。
- **Edge（边）**：控制节点间的流转路径。普通边是固定连线，条件边根据状态动态路由，入口点决定图从哪里开始。
- **Send**：在条件边中返回 `List[Send]`，实现 **一对多并行分发**（Map-Reduce 模式）。每个 `Send` 对象包含目标节点名称和专属状态更新。
- **Command**：节点返回 `Command(goto="目标节点", update={...})`，实现 **更新 State 的同时动态跳转**。适合决策节点委派任务给子 Agent。
- **Runtime Context**：通过 `config["configurable"]` 注入 LLM、API 客户端等运行时依赖，**与业务 State 解耦**，保证 State 可序列化、可恢复。

### 4. 重要函数
- `graph.add_node(name, func, retry=..., cache=...)`：注册节点，支持绑定重试策略和缓存。节点函数通常接收 `state` 返回 `dict`。
- `graph.add_edge(source, target)`：添加普通边，定义固定的节点流转路径。
- `graph.add_conditional_edges(source, route_func, path_map)`：添加条件边，`route_func` 返回字符串或 `List[Send]`，`path_map` 映射返回值到目标节点。
- `graph.add_entry_point(target)`：指定图的入口节点，等价于 `START → target`。
- `Send(target, state_update)`：创建动态并行任务。`target` 是目标节点名，`state_update` 是传给该节点的专属数据。
- `Command(goto=..., update=...)`：在节点中返回，`goto` 指定下一跳节点，`update` 指定 State 更新内容。

## 💻 代码示例

### 示例 1：Node 进阶定义（partial 绑定参数 + RetryPolicy 重试策略）
> 来源：`code_DefNode.py`
```python
from functools import partial
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from requests import RequestException, Timeout

class GraphState(TypedDict):
    process_data: str

def input_node(state: GraphState) -> dict:
    return {"process_data": "input_value"}

# 节点可带额外参数，用 partial 绑定后传给 add_node
def process_node(state: GraphState, param1: int, param2: str) -> dict:
    print(state, param1, param2)
    return {"process_data": "process_value"}

# 重试策略：仅对 RequestException、Timeout 重试，最多 3 次
retry_policy = RetryPolicy(
    max_attempts=3,
    initial_interval=1,
    jitter=True,
    backoff_factor=2,
    retry_on=[RequestException, Timeout],
)

stateGraph = StateGraph(GraphState)
stateGraph.add_node("input", input_node)
process_with_params = partial(process_node, param1=100, param2="test")
stateGraph.add_node("process", process_with_params, retry_policy=retry_policy)
stateGraph.add_edge(START, "input")
stateGraph.add_edge("input", "process")
stateGraph.add_edge("process", END)

graph = stateGraph.compile()
result = graph.invoke({"process_data": "初始值"})
print(f"最后的结果是:{result}")
```

### 示例 2：条件边（根据状态值路由到不同节点）
> 来源：`code_Edge_Conditional.py`
```python
from typing import Optional
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel

class MyState(BaseModel):
    x: int
    result: Optional[str] = None

def check_x(state: MyState) -> MyState:
    """检查节点：不做修改，直接传递"""
    return state

def is_even(state: MyState) -> bool:
    """条件函数：判断 x 是否为偶数"""
    return state.x % 2 == 0

def handle_even(state: MyState) -> MyState:
    return MyState(x=state.x, result="even")

def handle_odd(state: MyState) -> MyState:
    return MyState(x=state.x, result="odd")

builder = StateGraph(MyState)
builder.add_node("check_x", check_x)
builder.add_node("handle_even", handle_even)
builder.add_node("handle_odd", handle_odd)

# 添加条件边，根据 is_even 返回值决定流向
builder.add_conditional_edges(
    "check_x",
    is_even,
    {True: "handle_even", False: "handle_odd"}
)
builder.add_edge(START, "check_x")
builder.add_edge("handle_even", END)
builder.add_edge("handle_odd", END)

graph = builder.compile()
# 输入偶数 4，会流向 handle_even
result = graph.invoke(MyState(x=4))
print(result)  # 输出: x=4, result='even'
```

### 示例 3：Send 对象（Map-Reduce 并行分发）
> 来源：`code_SendDemo.py`
```python
from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class DiliState(TypedDict):
    subjects: List[str]
    jokes: Annotated[List[str], lambda x, y: x + y]

def generate_subjects(state: DiliState) -> dict:
    """生成主题列表"""
    return {"subjects": ["猫", "狗", "程序员"]}

def make_joke(state: DiliState) -> dict:
    """为单个主题生成笑话"""
    subject = state.get("subject", "未知")
    jokes_map = {
        "猫": "为什么猫不喜欢在线购物？因为它们更喜欢实体店！",
        "狗": "为什么狗不喜欢计算机？因为它们害怕被鼠标咬！",
        "程序员": "为什么程序员喜欢洗衣服？因为他们在寻找bugs！",
    }
    joke = jokes_map.get(subject, f"关于{subject}的笑话")
    return {"jokes": [joke]}

def map_subjects_to_jokes(state: DiliState) -> List[Send]:
    """为每个主题创建 Send 对象，指向 make_joke 节点"""
    return [Send("make_joke", {"subject": s}) for s in state["subjects"]]

builder = StateGraph(DiliState)
builder.add_node("generate_subjects", generate_subjects)
builder.add_node("make_joke", make_joke)
builder.add_edge(START, "generate_subjects")
builder.add_conditional_edges("generate_subjects", map_subjects_to_jokes)
builder.add_edge("make_joke", END)

graph = builder.compile()
result = graph.invoke({"subjects": [], "jokes": []})
print(result["jokes"])
# 输出: ['为什么猫不喜欢...', '为什么狗不喜欢...', '为什么程序员喜欢...']
```

### 示例 4：Command 对象（决策 Agent 动态跳转）
> 来源：`code_CommandDemo.py`
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    current_agent: str
    task_completed: bool

def decision_agent(state: AgentState) -> Command:
    """决策节点：根据消息内容路由到不同 Agent"""
    if state["task_completed"]:
        return Command(
            update={"messages": [("system", "任务完成")]},
            goto=END,
        )
    last_msg = state["messages"][-1][1] if state["messages"] else ""
    if "数学" in last_msg:
        return Command(
            update={"current_agent": "math_agent"},
            goto="math_agent",
        )
    elif "翻译" in last_msg:
        return Command(
            update={"current_agent": "translation_agent"},
            goto="translation_agent",
        )
    return Command(update={"task_completed": True}, goto=END)

def math_agent(state: AgentState) -> Command:
    return Command(
        update={"messages": [("assistant", "2 + 2 = 4")], "task_completed": True},
        goto="decision_agent",
    )

def translation_agent(state: AgentState) -> Command:
    return Command(
        update={"messages": [("assistant", "Hello -> 你好")], "task_completed": True},
        goto="decision_agent",
    )

builder = StateGraph(AgentState)
builder.add_node("decision_agent", decision_agent)
builder.add_node("math_agent", math_agent)
builder.add_node("translation_agent", translation_agent)
builder.add_edge(START, "decision_agent")
builder.add_edge("math_agent", "decision_agent")
builder.add_edge("translation_agent", "decision_agent")
builder.add_edge("decision_agent", END)

graph = builder.compile()
result = graph.invoke({
    "messages": [("user", "我需要计算数学题")],
    "current_agent": "user",
    "task_completed": False,
})
print(result)
```

### 示例 5：Runtime Context（配置与状态分离）
> 来源：`code_RuntimeContextDemo.py`
```python
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RunnableConfig

class ChatState(TypedDict):
    messages: list

def chat_node(state: ChatState, config: RunnableConfig) -> dict:
    """从 Runtime Context 获取 LLM，而非塞进 State"""
    llm = config["configurable"].get("llm")
    if llm:
        reply = llm.invoke(state["messages"][-1].content)
        return {"messages": [("assistant", reply.content)]}
    return {"messages": [("assistant", "未配置 LLM")]}

builder = StateGraph(ChatState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)
graph = builder.compile()

# 调用时通过 config 注入依赖
config = {"configurable": {"llm": my_llm_instance}}
result = graph.invoke({"messages": [("user", "你好")]}, config=config)
```

## 🐛 问题与思考

### Q1: 一个真实工作流里，怎么判断某段逻辑该放 Node 还是 Edge？
**答**: 做业务处理、调用模型、检索、转换数据，放 Node；决定下一步去哪，放 Edge 或控制对象。把处理和流转混在一起，图会很快失去可读性。

### Q2: 条件边和 Command 都能影响下一跳，它们的区别在哪里？
**答**: 条件边把路由逻辑放在图结构外侧，更适合清晰分支；Command 让节点返回状态更新的同时指定下一跳，更适合节点处理结果本身就决定控制流的场景。选择时看路由逻辑属于图，还是属于节点结果。

### Q3: Send 适合解决什么问题？什么时候不该用？
**答**: 它适合运行时动态拆出多路子任务，比如对多个文档、多个查询并行处理。如果任务数量固定、顺序明确，用普通边或并行结构可能更清楚。

### Q4: Runtime Context 为什么不应该塞进 State？
**答**: Runtime 放配置、依赖和执行环境，比如客户端、用户上下文、模型参数；State 放业务流转数据。混在一起会导致状态不可序列化、难恢复，也让业务数据和运行环境耦合。

### Q5：为什么循环图需要设计退出条件和步数保护？
**答**：Agent / ReAct / 自我修正流程天然可能反复执行，如果没有清晰退出条件，图会一直调度下去。recursion_limit 是最后一道保护，但真正可靠的设计还要在 State 中记录重试次数、评分结果或工具调用状态，让条件边能稳定走向 END。

## 📝 学习总结

### Node 是什么
- Node 是 LangGraph 的最小执行单元，可以理解为被图调度的 Python 函数；除了最常见的 state -> dict 形式，还可以结合缓存、重试策略、config、runtime 使用。

### Edge 是什么
- Edge 决定流程怎么流转。普通边适合固定路径，条件边适合状态驱动分支，入口点和条件入口点则决定图从哪里开始。

### Send、Command、Runtime
- Send、Command、Runtime 是三种常用进阶能力：Send 适合动态并行分发，Command 适合决策节点，Runtime 适合把配置和状态拆开。