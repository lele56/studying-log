# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-28
- **主题**: LangChain 框架基础 - Agent
- **目标**: 理解 Agent（智能体） 到底是什么、适合解决什么问题，以及它与 Tool、Function Calling、RAG、MCP 的关系。

## 📚 核心知识点

### 1. Agent 是什么？
- Agent 是基于 LLM 的智能体，能够根据用户意图进行**自主规划、决策、工具调用**，并通过"思考 → 行动 → 观察"的多轮循环，最终完成复杂任务并交付结果。

### 2. 关键概念
- **ReAct 模式**：Agent 经典范式，按照 **思考（Reason）→ 行动（Act）→ 观察（Observe）** 循环进行。LLM 先推理出下一步动作，调用工具，再根据工具结果继续推理，直至得出最终答案。
- **Tool Calling**：Agent 调用外部工具执行任务。现代 LLM 原生支持 Function Calling，无需手动解析 JSON。
- **Agent 编排（Orchestration）**：多个 Agent 之间协调完成任务，可以是顺序执行、条件分支或并行调度。
- **A2A（Agent-to-Agent）**：多个专用 Agent 通过协调器（Coordinator）按业务流程串联协作，每个 Agent 只负责单一职责。
- **Structured Output**：通过 `TypedDict` 或 Pydantic 模型约束 Agent 最终输出为结构化数据，便于代码中直接取字段使用。

### 3. 重要函数
- `create_agent()`：LangChain 1.0 推荐的一站式创建方法，支持传入 model、tools、system_prompt、response_format 等。
- `@tool`：将普通函数包装成 LangChain Tool，函数名和 docstring 会自动作为工具名和描述传给 LLM。
- `llm.bind_tools()`：将工具列表绑定到 LLM 实例，使模型具备 Function Calling 能力，返回带 `tool_calls` 的 AIMessage。
- `agent.invoke()`：执行 Agent 实例的任务，返回包含消息历史和最终结果的字典。
- `response_format`：定义 Agent 实例的响应格式，支持 `TypedDict` 或 Pydantic，Agent 会自动将最终输出解析为指定结构。

## 💻 代码示例

### 示例 1：ReAct Agent 多轮推理与工具调用
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool

# 模拟产品数据库
PRODUCT_DATABASE = {
    "无线耳机": [
        {"id": "WH-1000XM5", "name": "索尼 WH-1000XM5", "popularity": 95, "price": 299},
        {"id": "QC45", "name": "Bose QuietComfort 45", "popularity": 88, "price": 329},
    ],
}

INVENTORY_DATABASE = {
    "WH-1000XM5": {"stock": 10, "location": "仓库-A"},
    "QC45": {"stock": 0, "location": "仓库-B"},
}

@tool
def search_products(query: str) -> str:
    """搜索产品并返回按受欢迎度排序的结果"""
    # ... 匹配逻辑 ...
    return "找到 2 个产品..."

@tool
def check_inventory(product_id: str) -> str:
    """检查特定产品的库存状态"""
    # ... 库存查询逻辑 ...
    return f"产品 {product_id}: 有库存"

model = ChatOpenAI(model="qwen-plus")

# 创建 ReAct Agent：系统提示中明确 ReAct 模式
agent = create_agent(
    model,
    tools=[search_products, check_inventory],
    system_prompt="""你是电商助手，遵循ReAct模式：
    1. 先推理用户需求
    2. 选择合适的工具执行操作
    3. 基于工具结果进行下一步推理
    4. 重复直到获得完整答案""",
)

# 调用：一次问题可能触发多轮「推理 → 选工具 → 观察 → 再推理」
result = agent.invoke({
    "messages": [
        {"role": "user", "content": "查找当前最受欢迎的无线耳机并检查是否有库存"}
    ]
})
```

### 示例 2：Agent 结构化输出
```python
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool

# 定义结构化输出
class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str

@tool
def get_weather(loc: str) -> str:
    """查询即时天气"""
    # ... 调用天气 API ...
    return '{"temp": 20.5, ...}'

model = ChatOpenAI(model="qwen-plus")

# 创建 Agent 并指定 response_format
agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="你是天气助手，需要比较多个城市温度。",
    response_format=WeatherCompareOutput,
)

# 调用后，结果中包含 structured_response 字段
result = agent.invoke({"input": "北京和上海哪个更热？"})
print(result["structured_response"])
# 输出: {'beijing_temp': 20.5, 'shanghai_temp': 28.3, 'hotter_city': 'Shanghai', ...}
```

### 示例 3：A2A 多 Agent 协作编排
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import tool

@tool("CtripBookFlight", description="预订机票")
def ctrip_book_flight(departure: str, arrival: str, date: str) -> str:
    return f"机票预订成功: {departure} -> {arrival}"

@tool("MeituanBookHotel", description="预订酒店")
def meituan_book_hotel(city: str, check_in: str, check_out: str) -> str:
    return f"酒店预订成功: {city}"

llm = ChatOpenAI(model="qwen-plus")
output_parser = StrOutputParser()

# 创建多个专用 Agent，每个只绑定一个工具（单一职责）
def create_ctrip_agent(llm):
    llm_with_tools = llm.bind_tools([ctrip_book_flight])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是专业的机票预订助手，只能调用CtripBookFlight工具。"),
        ("human", "{input}"),
    ])
    return prompt | llm_with_tools | output_parser

def create_meituan_agent(llm):
    llm_with_tools = llm.bind_tools([meituan_book_hotel])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是专业的酒店预订助手，只能调用MeituanBookHotel工具。"),
        ("human", "{input}"),
    ])
    return prompt | llm_with_tools | output_parser

# 总协调器：按业务顺序调用子 Agent
def travel_coordinator():
    ctrip_agent = create_ctrip_agent(llm)
    meituan_agent = create_meituan_agent(llm)
    
    # 1. 订机票
    print("1. 调用【携程机票Agent】>>>")
    ctrip_result = ctrip_agent.invoke({"input": "订机票"})
    
    # 2. 订酒店
    print("2. 调用【美团酒店Agent】>>>")
    meituan_result = meituan_agent.invoke({"input": "订酒店"})
    
    return f"✅ 旅行安排完成！\n{ctrip_result}\n{meituan_result}"

travel_coordinator()
```

## 🐛 问题与思考

### Q1: 一个任务是否需要 Agent，你会看哪些信号？
**答**: 看任务是否步骤不固定、需要多次决策、需要选择工具、需要根据中间结果调整路线。如果只是固定输入到固定输出，链或工作流通常更简单。

### Q2: Agent、Tool、RAG、MCP 放在一起时，各自的位置是什么？
**答**: Agent 负责决策和推进任务，Tool 提供可执行能力，RAG 提供外部知识上下文，MCP 提供标准化接入方式。它们不是互相替代，而是在不同层协作。

### Q3: 为什么 Agent 系统要设置迭代上限、超时和失败处理？
**答**: Agent 会根据中间结果继续决策，如果没有边界，可能循环调用、成本失控或执行危险动作。工程上需要有停止条件、错误兜底和日志追踪。

### Q4: 旧的 AgentExecutor 和新的 create_agent 思路，你会怎样看待它们？
**答**: 旧写法有助于读懂历史代码，新写法更贴近当前 LangChain / LangGraph 主线。学习时不必纠结“谁完全替代谁”，要看项目版本、依赖和维护成本。

## 📝 学习总结

### Agent 的定位是决策层
- 它不是多几个 API，也不是多几个 Tool，而是让系统围绕目标判断下一步做什么。Tool 是能力层，Agent 负责协调这些能力。

### 理解 Agent，可以放回 ReAct 循环里看
- 观察问题、决定动作、调用工具、拿回观察结果、继续决策。这样再去看 classic 路线里的 scratchpad / AgentExecutor，以及 1.x 路线里的 create_agent，就不会只剩 API 记忆。

### LangChain 1.x 的主线要抓住三个工程点
- response_format 负责把最终输出结构化，checkpointer 负责线程状态持久化，thread_id 负责多轮对话和会话隔离。它们共同决定 Agent 能不能从“演示能跑”走向“系统可用”。