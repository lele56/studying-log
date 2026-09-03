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


# ===============================
# 1. 初始化大语言模型
# ===============================
def init_llm_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        temperature=0.1,
        max_tokens=1024,
    )

model = init_llm_model()


# ===============================
# 2. 通用 Handoff 工具工厂
# ===============================
def create_task_description_handoff_tool(
    *, agent_name: str, description: str | None = None
):
    name = f"transfer_to_{agent_name}"
    description = description or f"移交给 {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        task_description: Annotated[
            str, "描述下一个 Agent 应该做什么，包括所有必要信息"
        ],
        state: Annotated[MessagesState, InjectedState],
    ) -> Command:
        task_description_message = {
            "role": "user",
            "content": task_description,
        }
        agent_input = {
            **state,
            "messages": [task_description_message],
        }

        return Command(
            goto=[Send(agent_name, agent_input)],
            graph=Command.PARENT
        )
    return handoff_tool

# ===============================
# 3. 业务工具（必须有 docstring）
# ===============================
@tool("book_flight")
def book_flight(from_airport: str, to_airport: str) -> str:
    """预订航班，根据出发地和目的地完成机票预订"""
    print(f"✅ 成功预订了从 {from_airport} 到 {to_airport} 的航班")
    return f"成功预订了从 {from_airport} 到 {to_airport} 的航班。"


@tool("book_hotel")
def book_hotel(hotel_name: str) -> str:
    """预订酒店，根据酒店名称完成预订"""
    print(f"✅ 成功预订了 {hotel_name} 的住宿")
    return f"成功预订了 {hotel_name} 的住宿。"


# ===============================
# 4. Handoff 工具
# ===============================
transfer_to_flight_assistant = create_task_description_handoff_tool(
    agent_name="flight_assistant",
    description="将任务移交给航班预订助手",
)

transfer_to_hotel_assistant = create_task_description_handoff_tool(
    agent_name="hotel_assistant",
    description="将任务移交给酒店预订助手",
)

# ===============================
# 5. 定义 Agent（create_agent 新接口）
# 这里不额外写长 prompt，而是更多依赖：
# 1. 工具 schema / 名称 / docstring
# 2. Handoff 工具本身描述的交接语义
# 3. MessagesState 中持续携带的历史消息
# ===============================
flight_assistant = create_agent(
    model=model,
    tools=[book_flight, transfer_to_hotel_assistant],  # 包含移交工具
    name="flight_assistant",
)

hotel_assistant = create_agent(
    model=model,
    tools=[book_hotel, transfer_to_flight_assistant],  # 包含移交工具
    name="hotel_assistant",
)

# ===============================
# 6. 构建多 Agent Graph
# ===============================
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)

# ===============================
# 7. 运行
# ===============================
if __name__ == "__main__":
    result = multi_agent_graph.invoke(
        {
            "messages": [
                HumanMessage(content="帮我预订从北京到上海的航班，并预订如家酒店")
            ]
        }
    )

    print("\n====== 最终对话结果 ======")
    for msg in result["messages"]:
        if msg.type in ("human", "ai"):
            print(msg.content)


"""
【输出示例】
✅ 成功预订了从 北京 到 上海 的航班
✅ 成功预订了 如家酒店 的住宿

====== 最终对话结果 ======
帮我预订从北京到上海的航班，并预订如家酒店
请帮用户预订如家酒店，目的地是上海。
好的，我来帮您预订如家酒店。


已成功为您预订了**如家酒店**的住宿！🎉

请问您还需要其他帮助吗？比如需要预订前往上海的航班，我可以帮您转接到航班预订助手。
"""