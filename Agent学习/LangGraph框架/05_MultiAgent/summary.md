# LangGraph 框架学习

## 📅 学习信息
- **日期**: 2026-09-03
- **主题**: LangGraph 框架基础 - MultiAgent
- **目标**: 理解 多智能体（Multi-Agent） 到底在解决什么问题，知道它和“一个强一点的单智能体”之间的边界。

## 📚 核心知识点

### 1. Supervisor 架构模式
- 中央集中式调度：Supervisor 作为"主管"统一接收用户请求，根据任务类型分派给专精 Agent，最后汇总结果。适合流程清晰、需要统一控制的场景。

### 2. Handoff（交接）架构模式
- 去中心化交接：每个 Agent 自带 Handoff 工具，当发现自己无法处理任务时，主动将控制权转移给更合适的 Agent。适合角色边界清晰、需要灵活流转的场景。

### 3. Agent 作为节点注册
- `create_agent` 返回的 `CompiledStateGraph` 可直接通过 `.add_node(agent)` 注册到父图中，无需手动包装。调用时自动完成状态匹配和消息传递。

### 4. Command.PARENT 跨图通信
- 子图（Agent）内部返回 `Command(graph=Command.PARENT, goto=...)` 时，指令会在**父图级别**执行，实现"子图跳出自身，指挥父图调度下一个节点"的效果。

### 5. 关键概念
- **Supervisor（监督者）**：多 Agent 架构中的中央调度器，负责接收用户请求、决策路由、协调各 Agent 执行顺序，并汇总最终结果。
- **Handoff（交接）**：Agent 之间传递控制权的行为。当前 Agent 通过 Handoff 工具将自己无法处理的任务移交给另一个 Agent，由接手者继续处理。
- **Handoff Tool**：一种特殊的 Tool，本质是返回 `Command(goto=..., graph=Command.PARENT)` 的函数。LLM 调用该工具时，触发 Agent 间的控制权转移。
- **Command.PARENT**：LangGraph 的常量，用于指定 Command 的执行层级。设为 `PARENT` 时，指令在父图中生效，而非当前子图内部。
- **CompiledStateGraph**：`create_agent` 返回的对象类型，本质是编译后的 LangGraph 图。说明 Agent 底层就是图，可直接 `.invoke()` 或作为节点注册到其他图中。
- **create_supervisor 返回值**：返回的是**图构建器**（类似 `StateGraph`），必须调用 `.compile()` 才能变成可执行对象。

### 6. 重要函数
- `create_supervisor(agents, model, prompt).compile()`：创建 Supervisor 多 Agent 图。`agents` 是子 Agent 列表，`model` 是主管 LLM，`prompt` 定义调度规则。**必须调用 `.compile()`**。
- `create_agent(model, tools, name)`：创建 LangGraph Agent。返回 `CompiledStateGraph` 对象，可直接 `.invoke()`，也可作为节点注册到父图中。
- `Command(goto=..., graph=Command.PARENT)`：创建跨图指令。`goto` 指定目标节点（可配合 `Send` 并行分发），`graph=Command.PARENT` 确保指令在父图层级执行。
- `Send(agent_name, agent_input)`：创建并行分发任务。`agent_name` 是目标节点名，`agent_input` 是传给该节点的专属状态数据。常与 `Command(goto=[Send(...)])` 配合使用。

## 💻 代码示例

### 示例 1：Agent 基础（create_agent + 工具调用）
> 来源：`code_LangGraphAgent.py`
```python
import os
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def get_weather(city: str) -> str:
    """获取指定城市的天气信息。"""
    return f"今天{city}是晴天，仅做测试，固定写死"

llm = init_chat_model(
    model=os.getenv("OPENAI_MODEL_NAME"),
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

# 创建 Agent，绑定工具
agent = create_agent(model=llm, tools=[get_weather])

# Agent 底层本质是 CompiledStateGraph（编译后的图）
print("agent 底层本质是个什么对象:", type(agent))

response = agent.invoke({"messages": [HumanMessage(content="今天深圳天气怎么样？")]})
response["messages"][-1].pretty_print()
```

### 示例 2：Supervisor 架构（中央调度模式）
> 来源：`code_SupervisorV1.0.py`
```python
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def init_llm_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

# 工具（必须有 docstring）
def book_flight(from_airport: str, to_airport: str) -> str:
    """预订航班工具。根据出发机场和到达机场预订一张机票。"""
    return f"✅ 成功预订了从 {from_airport} 到 {to_airport} 的航班"

def book_hotel(hotel_name: str) -> str:
    """预订酒店工具。根据酒店名称完成酒店预订。"""
    return f"✅ 成功预订了 {hotel_name} 的住宿"

# 子 Agent
flight_assistant = create_agent(
    model=init_llm_model(), tools=[book_flight], name="flight_assistant"
)
hotel_assistant = create_agent(
    model=init_llm_model(), tools=[book_hotel], name="hotel_assistant"
)

# Supervisor（必须 .compile()）
supervisor = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=init_llm_model(),
    prompt=(
        "你是旅行预订系统的调度主管，负责协调航班和酒店预订。\n"
        "1. 先调用 flight_assistant 预订航班\n"
        "2. 再调用 hotel_assistant 预订酒店\n"
        "3. 汇总结果后结束\n"
    ),
).compile()

result = supervisor.invoke({
    "messages": [("user", "帮我订从北京到上海的航班，并预订如家酒店")]
})
```

### 示例 3：Handoff 交接模式（去中心化控制权转移）
> 来源：`code_SupervisorHandoff.py`
```python
import os
from typing import Annotated
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START
from langgraph.graph.message import MessagesState
from langgraph.prebuilt.tool_node import InjectedState
from langgraph.types import Command, Send
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def init_llm_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

model = init_llm_model()

# Handoff 工具工厂
def create_task_description_handoff_tool(*, agent_name: str, description: str = None):
    @tool(f"transfer_to_{agent_name}", description=description or f"移交给 {agent_name}")
    def handoff_tool(
        task_description: Annotated[str, "描述下一个 Agent 应该做什么"],
        state: Annotated[MessagesState, InjectedState],
    ) -> Command:
        agent_input = {
            **state,
            "messages": [{"role": "user", "content": task_description}],
        }
        return Command(
            goto=[Send(agent_name, agent_input)],
            graph=Command.PARENT  # 关键：在父图级别执行
        )
    return handoff_tool

# 业务工具
@tool("book_flight")
def book_flight(from_airport: str, to_airport: str) -> str:
    """预订航班"""
    return f"成功预订了从 {from_airport} 到 {to_airport} 的航班"

@tool("book_hotel")
def book_hotel(hotel_name: str) -> str:
    """预订酒店"""
    return f"成功预订了 {hotel_name} 的住宿"

# Handoff 工具
transfer_to_flight = create_task_description_handoff_tool(agent_name="flight_assistant")
transfer_to_hotel = create_task_description_handoff_tool(agent_name="hotel_assistant")

# 子 Agent（各自包含对方的 Handoff 工具）
flight_assistant = create_agent(
    model=model, tools=[book_flight, transfer_to_hotel], name="flight_assistant"
)
hotel_assistant = create_agent(
    model=model, tools=[book_hotel, transfer_to_flight], name="hotel_assistant"
)

# 构建多 Agent 图
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)

result = multi_agent_graph.invoke({
    "messages": [HumanMessage(content="帮我预订从北京到上海的航班，并预订如家酒店")]
})
```

## 🐛 问题与思考

### Q1: 单 Agent 什么时候应该升级成多 Agent？
**答**: 当任务明显有不同专业角色、工具权限需要隔离、上下文太长、主提示词越来越乱，或需要不同执行策略时，再考虑多 Agent。只是为了“看起来智能”而拆分，通常会增加调试成本。

### Q2: Supervisor 和 Handoff 的差别，可以用什么业务场景解释？
**答**: Supervisor 像总调度，统一分派任务并汇总；Handoff 像把客户转给更合适的专员，由接手者继续处理。前者适合集中控制，后者适合角色间自然交接。

### Q3: MCP、A2A、多智能体三者最容易混在哪里？
**答**: 多智能体是应用内部角色协作，MCP 是外部能力接入协议，A2A 是不同智能体系统之间的协作协议。它们都和“连接”有关，但连接对象和层级不同。

### Q4: 多 Agent 系统里，共享上下文应该越多越好吗？
**答**: 不一定。共享太少会重复沟通，共享太多会泄露信息、增加噪声和成本。要按角色职责决定哪些上下文共享，哪些只保留在本 Agent 内部。

## 📝 学习总结

### 多智能体
- 多智能体 不等于“多调几个模型”，而是让多个专精角色围绕一个任务进行分工与协作。

### A2A 和 MCP 不一样
- MCP 更偏模型 / Agent 与工具、资源的接入；A2A 更偏 Agent 与 Agent 的互操作和协作。

### LangGraph 多智能体不等于 A2A
- LangGraph 更适合做应用内多 Agent 编排，A2A 更适合跨系统代理协作协议。

### Supervisor 和 Handoff 是两种特别值得先掌握的模式
- 前者强调中央调度，后者强调控制权转移。

### Skills
- Skills 更像能力工程化和上下文工程的补充层：它不一定等于多智能体，但能帮助单 Agent 和多 Agent 系统都变得更可复用、更可维护，也能降低把所有能力都堆进一个总 Prompt 里的混乱度。