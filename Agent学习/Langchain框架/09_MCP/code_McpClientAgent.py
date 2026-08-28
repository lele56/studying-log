import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

# 加载 .env 文件（确保 .env 文件和脚本在同一目录）
load_dotenv()

from loguru import logger

# 默认 mcp.json 路径（与本文件同目录）
_MCP_JSON_PATH = Path(__file__).resolve().parent / "mcp.json"

def load_servers(file_path: str | Path | None = None) -> dict:
    """
    加载 MCP 服务器配置。
    :param file_path: 配置文件路径，默认使用同目录下的 mcp.json
    :return: 完整配置字典，如 {"mcpServers": {"weather": {...}, "fetch": {...}}}

    这里读取的是“客户端如何连接服务”的约定配置，而不是协议本体。
    """
    path = Path(file_path) if file_path else _MCP_JSON_PATH
    if not path.exists():
        logger.warning(f"未找到 mcp 配置文件: {path}")
        return {"mcpServers": {}}
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    logger.info(
        f"已加载 mcp 配置: {path}，共 {len(config.get('mcpServers', {}))} 个服务"
    )
    return config

async def run_chat_loop(config_path: str | Path | None = None) -> None:
    """
    启动并运行一个基于 MCP 工具的聊天 Agent 循环。
    该函数会：1）加载 MCP 服务器配置；2）初始化 MCP 客户端并获取工具；
    3）创建基于 LLM 和 Agent；4）启动命令行聊天循环；5）退出时清理资源。
    """
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
    except ImportError as e:
        logger.error(
            "请先安装 langchain-mcp-adapters: pip install langchain-mcp-adapters（部分环境需 Python 3.12 及以下）"
        )
        raise e

    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    config = load_servers(config_path)
    servers = config.get("mcpServers", {})

    if not servers:
        logger.warning("mcp.json 中未配置任何服务，无法获取 MCP 工具")
        return

    # 初始化 MCP 客户端：connections 就是 mcp.json 中的 mcpServers 字典
    # 每个条目描述一台 MCP 服务该如何连接，例如 stdio 子进程或 HTTP/SSE 地址
    client = MultiServerMCPClient(connections=servers)

    # 按官方默认用法，MultiServerMCPClient 是无状态的；获取工具时使用异步接口即可
    tools = await client.get_tools()
    if not tools:
        logger.warning(
            "未从 MCP 服务获取到任何工具，请确认服务已启动且 mcp.json 配置正确"
        )
        return

    logger.info(f"已获取 {len(tools)} 个 MCP 工具: {[t.name for t in tools]}")

    # 语言模型
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE_URL"),
    )

    # 对话提示：系统提示要求使用工具完成用户请求，agent_scratchpad 供 Executor 填入中间步骤
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个有用的助手，需要使用提供的工具来完成用户请求。"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="解析用户请求失败，请重新输入清晰的指令",
    )

    logger.info("\n MCP Agent 已启动，请先输入一个提问给(LLM+MCP)，输入 'quit' 退出")

    while True:
        try:
            user_input = input("\n您: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                logger.info("已退出")
                break
            result = agent_executor.invoke({"input": user_input})
            output = result.get("output", result)
            print(f"\nAgent: {output}")
        except KeyboardInterrupt:
            logger.info("已退出")
            break

def main() -> None:
    asyncio.run(run_chat_loop())

if __name__ == "__main__":
    main()

"""
【输出示例】
2026-08-28 17:16:23.943 | INFO     | __main__:load_servers:30 - 已加载 mcp配置: E:\project\studying-log\Agent学习\Langchain框架\09_MCP\mcp.json，共 1 个服务
2026-08-28 17:16:23.998 | INFO     | __main__:run_chat_loop:72 - 已获取 1个 MCP 工具: ['add']
2026-08-28 17:16:33.030 | INFO     | __main__:run_chat_loop:98 - 
 MCP Agent 已启动，请先输入一个提问给(LLM+MCP)，输入 'quit' 退出

您: quit
2026-08-28 17:16:40.932 | INFO     | __main__:run_chat_loop:106 - 已退出
"""