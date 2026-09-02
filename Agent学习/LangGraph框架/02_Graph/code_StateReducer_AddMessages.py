from typing import Annotated, List
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

# messages 使用 add_messages：节点只返回增量，自动追加
class AddMessagesState(TypedDict):
    messages: Annotated[List, add_messages]

def chat_node_1(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 1")]}


def chat_node_2(state: AddMessagesState) -> dict:
    return {"messages": [("assistant", "Hello from node 2")]}

def run_demo():
    print("2. add_messages Reducer（消息列表专用）演示:")
    builder = StateGraph(AddMessagesState)
    builder.add_node("chat1", chat_node_1)
    builder.add_node("chat2", chat_node_2)
    builder.add_edge(START, "chat1")
    builder.add_edge(START, "chat2")  # 两节点并行，各自追加消息
    builder.add_edge("chat1", END)
    builder.add_edge("chat2", END)
    graph = builder.compile()

    result = graph.invoke({"messages": [("user", "Hi there!")]})
    print(f"初始状态: {{'messages': [('user', 'Hi there!')]}}")
    print(f"执行结果: {result}\n")
    print("*" * 60)
    print(graph.get_graph().print_ascii())


if __name__ == "__main__":
    run_demo()

"""
【输出示例】
2. add_messages Reducer（消息列表专用）演示:
初始状态: {'messages': [('user', 'Hi there!')]}
执行结果: {'messages': [HumanMessage(content='Hi there!', additional_kwargs={}, response_metadata={}, id='6e882fca-a39c-4970-a5e5-165cdde1c0ca'), AIMessage(content='Hello from node 1', additional_kwargs={}, response_metadata={}, id='00ac9e4e-6f0b-4dd3-ae2b-20eca3f3c839', tool_calls=[], invalid_tool_calls=[]), AIMessage(content='Hello from node 2', additional_kwargs={}, response_metadata={}, id='84832923-26e8-4d68-bc62-e3896e088d6b', tool_calls=[], invalid_tool_calls=[])]}

************************************************************
       +-----------+         
       | __start__ |         
       +-----------+         
         *        *          
       **          **        
      *              *       
+-------+         +-------+  
| chat1 |         | chat2 |  
+-------+         +-------+  
         *        *          
          **    **           
            *  *             
        +---------+          
        | __end__ |          
        +---------+          
None
"""