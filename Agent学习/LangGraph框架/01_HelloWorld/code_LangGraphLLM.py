import json
import os
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, message_to_dict
from dotenv import load_dotenv

load_dotenv()

# 定义状态 State：messages 使用 add_messages 规约器，节点返回的每条新消息会自动追加到列表
class DiliState(TypedDict):
    # add_messages 是 LangGraph 提供的「规约器」（Reducer），来自 langgraph.graph.message。
    # 含义：该字段不是「覆盖」更新，而是「追加」——节点只返回新增的消息（如 [reply]），
    # 框架会把它们合并到当前消息列表末尾，适合多轮对话、多节点共同往同一列表写消息。
    # 若不用 add_messages，节点返回 {"messages": [reply]} 会直接覆盖掉之前的对话历史。
    messages: Annotated[List, add_messages]

# 初始化大模型
llm = init_chat_model(
    model = os.getenv("OPENAI_MODEL_NAME"),
    api_key = os.getenv("OPENAI_API_KEY"),
    base_url = os.getenv("OPENAI_API_BASE"),
    model_provider = "openai",
)

# 定义节点 Nodes：将当前消息列表交给模型，返回新消息字典（add_messages 会追加到 state）
def model_node(state: DiliState):
    reply = llm.invoke(state["messages"])
    return {"messages": [reply]}

# 构建图：单节点 model，START → model → END
graph = StateGraph(DiliState)
graph.add_node("model", model_node)
graph.add_edge(START, "model")
graph.add_edge("model", END)

# 编译并执行
app = graph.compile()

# 传入初始消息（HumanMessage 或字符串均可，视模型封装而定）
result = app.invoke(
    {"messages": [HumanMessage(content="请用一句话解释什么是 LangGraph。")]}
)
# 或: result = app.invoke({"messages": "请用一句话解释什么是 LangGraph。"})

print("模型回答：", result["messages"][-1].content)

# 直接格式化输出 result：default 把消息对象转成 dict，其它不可序列化用 str 兜底
print("\n--- result 格式化输出 ---")
print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
        default=lambda o: message_to_dict(o) if isinstance(o, BaseMessage) else str(o),
    )
)

# 可视化
print(app.get_graph().print_ascii())
print("=" * 50)
print(app.get_graph().draw_mermaid())
print("=" * 50)

"""
【输出示例】
模型回答： LangGraph 是一个基于图结构的框架，用于构建具有状态管理、循环逻辑和多智能体协作能力的复杂大语言模型（LLM）应用程序。

--- result 格式化输出 ---
{
  "messages": [
    {
      "type": "human",
      "data": {
        "content": "请用一句话解释什么是 LangGraph。",
        "additional_kwargs": {},
        "response_metadata": {},
        "type": "human",
        "name": null,
        "id": "80360ffd-bc20-4879-a438-998c570010b3"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "LangGraph 是一个基于图结构的框架，用于构建具有状态管理、循环逻辑和多智能体协作能力的复杂大语言模型（LLM）应用程序。",
        "additional_kwargs": {
          "refusal": null
        },
        "response_metadata": {
          "token_usage": {
            "completion_tokens": 694,
            "prompt_tokens": 17,
            "total_tokens": 711,
            "completion_tokens_details": {
              "accepted_prediction_tokens": null,
              "audio_tokens": null,
              "reasoning_tokens": 659,
              "rejected_prediction_tokens": null,
              "text_tokens": 694
            },
            "prompt_tokens_details": {
              "audio_tokens": null,
              "cached_tokens": 0,
              "text_tokens": 17
            }
          },
          "model_provider": "openai",
          "model_name": "qwen3.7-plus-2026-05-26",
          "system_fingerprint": null,
          "id": "chatcmpl-616a4865-fa74-9c7b-b5c5-1294d1f9ebc7",
          "finish_reason": "stop",
          "logprobs": null
        },
        "type": "ai",
        "name": null,
        "id": "lc_run--01a05754-320d-7c73-90a2-6628fd317abc-0",
        "tool_calls": [],
        "invalid_tool_calls": [],
        "usage_metadata": {
          "input_tokens": 17,
          "output_tokens": 694,
          "total_tokens": 711,
          "input_token_details": {
            "cache_read": 0
          },
          "output_token_details": {
            "reasoning": 659
          }
        }
      }
    }
  ]
}
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
  +-------+    
  | model |    
  +-------+    
      *        
      *        
      *        
 +---------+   
 | __end__ |   
 +---------+   
None
==================================================
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        model(model)
        __end__([<p>__end__</p>]):::last
        __start__ --> model;
        model --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

==================================================
"""