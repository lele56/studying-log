# LangGraph 框架学习

## 📅 学习信息
- **日期**: 2026-09-03
- **主题**: LangGraph 框架基础 - Senior
- **目标**: 理解 LangGraph 的五类高级能力：流式处理（Streaming）、状态持久化（Persistence）、人机协作与中断恢复（Interrupt / HITL）、时间回溯（Time-Travel）、子图（Subgraphs）。

## 📚 核心知识点

### 1. 多模式流式输出（Stream Modes）
- `graph.stream()` 支持多种输出模式：`values`（完整 State）、`updates`（节点级增量）、`messages`（LLM Token 流）、`custom`（节点自定义推送）。可组合使用，实现"边跑边看"的实时反馈。

### 2. Checkpointer 持久化机制
- 通过 `checkpointer` 参数注入 `InMemorySaver` 或 `SqliteSaver`，图会在每次节点执行后自动保存快照（Checkpoint）。配合 `thread_id` 可实现跨调用的上下文记忆和断点恢复。

### 3. Checkpoint 分叉（Fork）机制
- `graph.update_state(history_config, values)` 不会修改原历史，而是基于历史快照**创建新分支**。返回的新 `config` 指向分叉后的最新状态，适合调试、复盘和"如果当时这样做会怎样"的探索。

### 4. 子图状态传递规则
- 子图在主图中是一个"黑盒节点"。调用时，主图按**字段名自动匹配**传入子图；子图执行完后，返回的 State 会再次按 Reducer 合并回主图。注意：若父子图都使用 `add` 策略，可能导致重复追加。

### 5. 关键概念
- **Stream Mode（流模式）**：控制 `graph.stream()` 输出的内容类型。常见模式：`values`（完整 State）、`updates`（节点增量）、`messages`（LLM Token）、`custom`（自定义数据）。
- **Stream Writer**：通过 `get_stream_writer()` 获取，允许节点在执行过程中**实时向外部推送自定义数据**（如进度提示、中间状态），不阻塞 State 更新。
- **Checkpoint / Saver**：Saver 是 Checkpointer 的具体实现（如 `InMemorySaver`、`SqliteSaver`），负责在节点执行后**保存图的执行快照**，支持断点恢复和时间旅行。
- **Thread ID**：通过 `config["configurable"]["thread_id"]` 指定，用于**隔离不同会话的状态**。同一 `thread_id` 的多次调用会共享持久化历史。
- **State Fork（状态分叉）**：通过 `update_state` 修改历史快照时，LangGraph **不会覆盖原历史**，而是基于该点创建一个新分支，保证原历史可追溯。
- **Shared State（共享状态）**：父子图通过**同名字段**共享数据。主图传入时自动过滤子图不需要的字段，子图返回时按 Reducer 合并回主图。

### 6. 重要函数
- `graph.stream(inputs, stream_mode=...)`：流式执行图。`stream_mode` 可为字符串或列表（如 `["values", "custom"]`），决定输出哪些类型的数据块。
- `get_stream_writer()`：在节点内部获取流写入器，调用 `writer(data)` 可实时推送自定义数据到外部。
- `InMemorySaver / SqliteSaver`：Checkpointer 的两种实现。前者适合开发测试（重启丢失），后者适合生产环境（持久化到 SQLite 文件）。
- `graph.get_state_history(config)`：获取指定线程的所有历史 Checkpoint，按时间倒序排列，用于时间旅行和回放调试。
- `graph.update_state(config, values)`：修改指定 Checkpoint 的状态。**自动创建新分支（Fork）**，返回新 `config`，不污染原历史。
- `builder.add_node("sub", compiled_subgraph)`：将编译后的子图作为节点注册到父图。调用时自动完成状态匹配和合并。

## 💻 代码示例

### 示例 1：自定义流式输出
> 来源：`code_StreamCustomDataSimple.py`
```python
from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    query: str
    answer: str

def node(state: State):
    writer = get_stream_writer()
    writer({"custom_key": "欢迎来到线上Agent班级学习，O(∩_∩)O"})
    return {"answer": "some data"}

graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .add_edge("node", END)
    .compile()
)

# 同时输出 values（完整 State）和 custom（自定义数据）
for chunk in graph.stream({"query": "example"}, stream_mode=["values", "custom"]):
    print(chunk)
```

### 示例 2：LLM Token 流式输出
> 来源：`code_StreamLLMTokens.py`
```python
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
    model = init_chat_model(
        model=os.getenv("OPENAI_MODEL_NAME"),
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    llm_result = model.invoke([("user", state["query"])])
    return {"answer": llm_result}

graph = StateGraph(state_schema=State).add_node(node).add_edge(START, "node").compile()

# stream_mode="messages"：从 LLM 调用处流式输出 Token
for chunk, _metadata in graph.stream(
    {"query": "帮我生成一个200字的小学生作文"},
    stream_mode="messages"
):
    print(chunk.content, end="")
```

### 示例 3：持久化（InMemorySaver 实现跨调用记忆）
> 来源：`code_AgentPersistence.py`
```python
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

llm = init_chat_model(
    model=os.getenv("OPENAI_MODEL_NAME"),
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# 注入内存 Checkpointer
checkpointer = InMemorySaver()
agent = create_agent(model=llm, checkpointer=checkpointer)

# 同一 thread_id 的多次调用共享历史
config = {"configurable": {"thread_id": "user-001"}}

# 第一次调用：告诉 Agent 我叫张三
msg1 = agent.invoke(
    {"messages": [("user", "你好，我叫张三，喜欢足球")]},
    config,
)
msg1["messages"][-1].pretty_print()

# 第二次调用：Agent 记得我叫张三
msg2 = agent.invoke(
    {"messages": [("user", "我叫什么？我喜欢做什么？")]},
    config,
)
msg2["messages"][-1].pretty_print()
```

### 示例 4：时间旅行（查看历史 → 修改状态 → 创建新分支继续执行）
> 来源：`code_TimeTravel.py`
```python
from typing import TypedDict
from typing_extensions import NotRequired
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    messages: list
    user_id: NotRequired[str]

def node1(state: State) -> dict:
    return {"messages": [("assistant", "节点1回复")]}

def node2(state: State) -> dict:
    return {"messages": [("assistant", "节点2回复")]}

checkpointer = InMemorySaver()
builder = StateGraph(State)
builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node2", END)
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "thread-1"}}
result = graph.invoke({"messages": [("user", "你好")]}, config)

# 1. 查看历史 Checkpoint
history = list(graph.get_state_history(config))
print(f"共 {len(history)} 个快照")

# 2. 拿到 node1 执行完的快照
checkpoint = history[-2]  # 倒数第二个（node1 之后）

# 3. 修改状态（自动创建新分支）
new_config = graph.update_state(
    checkpoint.config,
    {"messages": [("user", "你好"), ("assistant", "手动修改的回复")]}
)

# 4. 从新分支继续跑
result = graph.invoke(None, new_config)
print(result)
```

### 示例 5：子图基础（子图作为节点，状态传递与合并）
> 来源：`code_SubGraphHello.py`
```python
from operator import add
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

class DiliState(TypedDict):
    # 使用 operator.add 合并策略：新列表与旧列表拼接
    messages: Annotated[list[str], add]

def sub_node(state: DiliState) -> DiliState:
    return {"messages": ["response from subgraph"]}

# --- 子图 ---
subgraph_builder = StateGraph(DiliState)
subgraph_builder.add_node("sub_node", sub_node)
subgraph_builder.add_edge(START, "sub_node")
subgraph_builder.add_edge("sub_node", END)
subgraph = subgraph_builder.compile()

# --- 父图：子图作为节点 ---
builder = StateGraph(DiliState)
builder.add_node("subgraph_node", subgraph)  # 编译后的子图直接当节点
builder.add_edge(START, "subgraph_node")
builder.add_edge("subgraph_node", END)
graph = builder.compile()

# 注意：add 策略会导致"子图合并一次 + 父图再合并一次"
result = graph.invoke({"messages": ["main-graph"]})
print(result)
# 输出: {'messages': ['main-graph', 'main-graph', 'response from subgraph']}
```

## 🐛 问题与思考

### Q1: Streaming、Persistence、Interrupt、Time-Travel、Subgraph 这几个能力分别解决哪类真实痛点？
**答**: Streaming 解决过程不可见，Persistence 解决上下文连续和故障恢复，Interrupt 解决关键动作前的人机审核，Time-Travel 解决回放调试，Subgraph 解决复杂流程拆分和复用。先从痛点理解，再看 API。

### Q2: 为什么 updates 和 values 适合观察不同层面的信息？
**答**: updates 看每一步变了什么，适合调试节点行为；values 看某个时刻完整状态，适合理解全局。排障时经常两者结合使用。

### Q3: Checkpointer 和 Store 的边界为什么要分清？
**答**: Checkpointer 保存线程执行状态，用于恢复和回放；Store 保存跨线程或业务级数据，用于长期复用。把业务数据全当 checkpoint，或者把执行状态全丢进 Store，都会让系统难维护。

### Q4: 如果线上任务跑偏，Time-Travel 能帮你做什么，不能帮你做什么？
**答**: 它能帮你回到某个 checkpoint 看当时状态、复盘路径、从中间点重跑；但它不能自动判断业务对错，也不能替代日志、评测和权限控制。

### Q5：为什么 interrupt 前面的代码要尽量保持幂等？
**答**：恢复执行时，含有 interrupt 的节点会从函数开头重新执行。如果暂停前已经发邮件、扣款、写订单，恢复时可能重复触发副作用。更稳的做法是暂停前只准备审核数据，真实动作放到恢复后的独立节点。

## 📝 学习总结

### Streaming
- Streaming 让你不必等图完全执行结束再拿结果，而是能边跑边观察状态、消息、进度与调试信息。

### Persistence 
- Persistence 是 LangGraph 很核心的生产能力。Checkpointer 管线程内状态，Store 更适合跨线程长期信息。

### Interrupt / HITL
- Interrupt / HITL 让图可以在关键节点暂停，把待审核数据交给人，随后通过 Command(resume=...) 恢复执行。

### Time-Travel
- Time-Travel 建立在持久化之上，可以从历史 checkpoint 恢复或修改后重跑，适合调试、复盘和分支探索。

### Subgraphs 
- Subgraphs 让复杂工作流可以模块化拆分和复用，是从“小图”走向“大系统”的关键一步。