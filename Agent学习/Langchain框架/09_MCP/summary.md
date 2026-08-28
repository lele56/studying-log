# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-28
- **主题**: LangChain 框架基础 - MCP
- **目标**: 理解 MCP（Model Context Protocol，模型上下文协议） 是什么、解决什么痛点，以及它与 Tool、RAG、Agent 的定位区别。

## 📚 核心知识点

### 1. MCP 是什么？
- MCP（Model Context Protocol）是一个标准化协议，用于定义 AI 模型与外部工具、资源、提示词之间的交互规范。它的核心价值是**统一接入、跨应用复用**，让能力提供者只需写一次，就能被任何支持 MCP 的 AI 客户端调用。

### 2. 关键概念
- **Host（宿主）**：运行 AI 应用的宿主环境（如 Cursor、Claude Desktop、LangChain 应用），负责发起连接、管理会话生命周期。
- **Client（客户端）**：MCP 客户端，负责连接到 MCP Server，发现其暴露的能力（Tools/Resources/Prompts），并按协议发起调用。
- **Server（服务端）**：MCP 服务端，负责通过标准协议暴露工具、资源和提示词模板，并响应客户端的发现与调用请求。
- **Transport（传输方式）**：负责在客户端和服务端之间传递数据。常见有 `stdio`（本地进程通信）和 `SSE/HTTP`（网络通信）。

### 3. 重要函数
- `@mcp.tool()`：将普通函数包装成 MCP 工具，供 AI 模型调用执行动作。
- `@mcp.resource()`：将函数包装成 MCP 资源，提供可读取的上下文内容。
- `@mcp.prompt()`：将函数包装成 MCP 提示词模板，提供可复用的提示入口。
- `mcp.run()`：启动 MCP 服务，开始监听客户端连接。支持 `transport="stdio"` 或 `transport="sse"` 等模式。

## 💻 代码示例

### 示例 1：使用 FastMCP 创建服务端
```python
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务实例
mcp = FastMCP("Demo")

# 注册工具：供 AI 模型调用的可执行动作
@mcp.tool()
def add(a: int, b: int) -> int:
    """求两数之和"""
    return a + b

# 注册资源：提供可读取的上下文内容
@mcp.resource("greeting://default")
def get_greeting() -> str:
    return "Hello from static resource!"

# 注册提示词模板：提供可复用的提示入口
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "写一句友善的问候",
        "formal": "写一句正式的问候",
    }
    return f"为{name}{styles.get(style, styles['friendly'])}"

# 启动服务（stdio 模式：通过标准输入/输出通信）
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### 示例 2：使用 LangChain 客户端连接并获取工具
```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

# mcp.json 配置示例：
# {
#   "mcpServers": {
#     "weather": {
#       "url": "http://127.0.0.1:8000/sse",
#       "transport": "sse"
#     }
#   }
# }

async def get_mcp_tools():
    # 从配置文件加载服务连接信息
    servers = {"weather": {"url": "http://127.0.0.1:8000/sse", "transport": "sse"}}
    
    # 创建多服务客户端
    client = MultiServerMCPClient(connections=servers)
    
    # 获取所有 MCP 工具
    tools = await client.get_tools()
    print(f"已获取工具: {[t.name for t in tools]}")
    return tools

asyncio.run(get_mcp_tools())
```

### 示例 3：将 MCP 工具集成到 Agent 中执行任务
```python
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 1. 初始化 LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key="your-key", base_url="your-url")

# 2. 获取 MCP 工具（假设已通过示例 2 获取）
# tools = await client.get_tools()

# 3. 创建 Agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，需要使用提供的工具来完成用户请求。"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. 执行任务
result = agent_executor.invoke({"input": "帮我计算 10 + 20"})
print(result["output"])
```

## 🐛 问题与思考

### Q1: MCP 解决的问题，和“写一个本地工具函数”有什么不同？
**答**: 本地工具函数只服务当前代码；MCP 让工具、资源、提示词以统一协议暴露给不同 AI 应用复用。它的重点是标准化接入和跨应用复用，而不是多写一个函数。

### Q2: Host、Client、Server 三个角色如果搞混，会造成什么理解偏差？
**答**: 会分不清谁运行应用、谁负责协议通信、谁暴露能力。Host 是应用宿主，Client 负责连接 MCP Server，Server 提供 Tools/Resource/Prompt。角色清楚后，配置和排障才有方向。

### Q3: Tool、Resource、Prompt 三类能力应该怎么划分？
**答**: Tool 适合可执行动作，Resource 适合被读取的上下资料，Prompt 适合可复用提示模板。不要把所有东西都做成 Tool，否则权限和语义都会变乱。

### Q4: 什么时候用 stdio，什么时候更关注 Streamable HTTP？
**答**: 本地进程、桌面工具、开发调试常见 stdio；跨进程、服务化、远程访问更需要 HTTP 形态。传输方式服务于部署场景，不是单纯被协议名。

## 📝 学习总结

### MCP 的本质
- 不是模型、不是工具本身，而是 AI 应用与外部能力之间的标准化连接协议。

### MCP 的核心价值
- 统一发现，统一描述、统一接入，让工具、资源、提示词模板更容易跨应用复用。

### 和其他概念的区别
- Tool 解决“调用能力”，RAG 解决“检索知识”，Agent 解决“规划和决策”，MCP 解决“标准化接入”。