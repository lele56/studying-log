import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv(encoding="utf-8")

def get_weather(city: str) -> str:
    """获取指定城市的天气信息。

    Args:
        city: 城市名称
    Returns:
        返回该城市的天气描述（本案例为写死返回值，仅作演示）
    """
    return f"今天{city}是晴天，仅做测试，固定写死"

def main():
    llm = init_chat_model(
        model=os.getenv("OPENAI_MODEL_NAME"),
        model_provider="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    agent = create_agent(
        model=llm,
        tools=[get_weather],
    )
    print("agent 底层本质是个什么对象: " + str(type(agent)))

    human_message = HumanMessage(content="今天深圳天气怎么样？")
    response = agent.invoke({"messages": [human_message]})

    print()
    print("模型回答：", response["messages"][-1].content)
    print()
    response["messages"][-1].pretty_print()

    # 流式示例（可选）：
    # stream_mode：messages 流式 token；updates 每步工具；values 整状态快照；custom 配合 get_stream_writer
    # for chunk in agent.stream(
    #     {"messages": [{"role": "user", "content": "请问北京今天天气如何？"}]},
    #     stream_mode="values",
    # ):
    #     chunk["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()

"""
【输出示例】
agent 底层本质是个什么对象: <class 'langgraph.graph.state.CompiledStateGraph'>

模型回答： 今天深圳是晴天。

*(注：由于这是测试环境，上述天气信息为固定演示数据，并非实时天气。如需准确的实时天气，建议查看当地气象台的最新预报哦！)*

================================== Ai Message ==================================

今天深圳是晴天。

*(注：由于这是测试环境，上述天气信息为固定演示数据，并非实时天气。如需准确的实时天气，建议查看当地气象台的最新预报哦！)*
"""