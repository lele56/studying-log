# LangGraph 框架学习

## 📅 学习信息
- **日期**: 2026-08-31
- **主题**: LangGraph 框架基础 - HelloWorld
- **目标**: 理解 LangGraph 是什么，知道它为什么适合编排"有状态、可分支、可循环、可暂停、可人工介入"的复杂 LLM 工作流。

## 📚 核心知识点

### 1. LangGraph 是什么？
- LangGraph 是一个用于编排复杂 LLM 工作流的框架，专为**有状态、可分支、可循环、可暂停**的流程设计。它通过图结构（节点 + 边）来定义执行逻辑，让复杂工作流更可控、可调试。

### 2. 关键概念
- **State（状态）**：整个图共享的上下文，不是每个节点独立的。节点返回的是对 State 的**部分更新**，框架会自动合并。
- **Node（节点）**：图中的执行单元，接收当前 State，返回对 State 的部分更新字典。
- **Edge（边）**：定义节点之间的执行顺序，可以是固定边或条件边（Conditional Edge）。
- **START / END**：特殊标记，表示图的入口和出口，不是真正的节点。
- **Reducer（规约器）**：字段级别的合并策略（如 `add_messages` 是追加而非覆盖），决定节点返回的值如何合并到 State 中。

### 3. 重要函数
- `StateGraph()`：创建状态图构建器，需要传入 State 类型（TypedDict 或 dict）。
- `graph.add_node()`：添加节点到图中，第一个参数是节点名，第二个是节点函数。
- `graph.add_edge()`：添加边到图中，定义从一个节点到另一个节点的执行顺序。
- `graph.compile()`：编译图构建器，返回可执行的 app 对象。
- `app.invoke()`：执行编译后的图，传入初始状态字典，返回最终状态。

## 💻 代码示例

### 示例 1：LangGraph HelloWorld
```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. 定义 State：声明图中要传递的字段及类型
class HelloState(TypedDict):
    name: str
    greeting: str

# 2. 定义节点函数：接收当前 state，返回部分更新字典
def greet(state: HelloState) -> dict:
    return {"greeting": f"Hello, {state['name']}!"}

def add_emoji(state: HelloState) -> dict:
    return {"greeting": state["greeting"] + " 😄"}

# 3. 构建图：初始化 StateGraph，添加节点与边
graph = StateGraph(HelloState)
graph.add_node("greeting", greet)
graph.add_node("add_emoji", add_emoji)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

# 4. 编译图，得到可执行的 app
app = graph.compile()

# 5. 执行：传入初始状态字典
result = app.invoke({"name": "z3"})
print(result["greeting"])  # 输出: Hello, z3! 😄
```

### 示例 2：业务逻辑编排（状态传递）
```python
from langgraph.graph import StateGraph, START, END

# 节点函数：接收 state，返回部分更新
def addition(state):
    print(f"加法节点收到的值: {state['x']}")
    return {"x": state["x"] + 1}

def subtraction(state):
    print(f"减法节点收到的值: {state['x']}")
    return {"x": state["x"] - 2}

# 使用 dict 作为状态类型，无需预定义 TypedDict
graph = StateGraph(dict)
graph.add_node("addition", addition)
graph.add_node("subtraction", subtraction)

# 定义执行顺序：START → addition → subtraction → END
graph.add_edge(START, "addition")
graph.add_edge("addition", "subtraction")
graph.add_edge("subtraction", END)

# 编译并执行
app = graph.compile()
result = app.invoke({"x": 5})
print(f"最终结果: {result['x']}")  # 5 + 1 - 2 = 4
```

### 示例 3：结合 LLM 的对话图（使用 Reducer）
```python
from typing import Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage

# 定义 State：messages 使用 add_messages 规约器
# add_messages 会让节点返回的新消息自动追加到列表，而不是覆盖
class ChatState(TypedDict):
    messages: Annotated[List, add_messages]

# 初始化大模型
llm = init_chat_model(model="qwen-plus")

# 定义节点：将当前消息列表交给模型，返回新消息
def model_node(state: ChatState):
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}  # add_messages 会自动追加

# 构建图：START → model → END
graph = StateGraph(ChatState)
graph.add_node("model", model_node)
graph.add_edge(START, "model")
graph.add_edge("model", END)

# 编译并执行
app = graph.compile()
result = app.invoke({
    "messages": [HumanMessage(content="请用一句话解释什么是 LangGraph。")]
})
print(result["messages"][-1].content)
```

## 🐛 问题与思考

### Q1: 什么样的流程值得用 LangGraph 表达，而不是普通函数顺序调用？
**答**: 当流程有共享状态、分支、循环、并行、暂停恢复或人工介入时，LangGraph 的图结构更有价值。普通线性脚本能清楚表达的任务，不必强行上图。

### Q2: State、Node、Edge 三者如果用业务流程类比，分别是什么？
**答**: State 是流程里的共享工单或上下文，Node 是处理步骤，Edge 是流转规则。这个类比能帮助理解图不是画给人看的，而是可执行的流程模型。

### Q3: compile() 的意义是什么？为什么它不是可有可无的步骤？
**答**: 它把定义好的图编译成可运行对象，并做必要准备和校验。没有 compile，前面只是描述了结构，还没有得到能执行的应用。

### Q4: 选一个你熟悉的业务流程，把它拆成最少 3 个节点和 1 个条件边。
**答**: 例如工单处理：分类节点、知识库检索节点、人工升级节点、回复生成节点；条件边根据分类或置信度决定走自动回复还是人工处理。重点是把"怎么走"说清楚。

## 📝 学习总结

### LangGraph 是低层图编排框架和运行时
- LangGraph 是低层图编排框架和运行时，核心价值是把有状态、可分支、可循环、可人工介入的 LLM 流程写得更可控。

### LangChain 和 LangGraph 是配合关系
- LangChain 更擅长提供模型、Prompt、Tools、RAG、Agent 等组件和高层封装；LangGraph 更擅长做流程编排、状态管理、持久化、可观测和人机协作。

### Graph API 入门先记四个词
- State、Nodes、Edges、Graph；再记五步法：定义状态、写节点、连边、编译、执行。