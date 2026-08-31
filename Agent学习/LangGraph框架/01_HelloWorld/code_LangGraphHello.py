from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import uuid

# 定义 State（状态）：声明图中要传递的字段及类型
class HelloState(TypedDict):
    name: str
    greeting: str


# 定义节点函数 Node：接收当前 state，返回对 state 的「部分更新」字典
def greet(helloState: HelloState) -> dict:
    name = helloState["name"]
    return {"greeting": f"Hello, {name}!"}

def add_emoji(helloState: HelloState) -> dict:
    greeting = helloState["greeting"]
    return {"greeting": greeting + "  。。。😄"}

# 构建图 Graph：初始化 StateGraph，添加节点与边
graph = StateGraph(HelloState)
graph.add_node("greeting", greet)
graph.add_node("add_emoji", add_emoji)
graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

# 编译图，得到可执行的 app
app = graph.compile()

# 运行：invoke 只接收一个核心参数——初始状态字典
result = app.invoke({"name": "z3"})
print(result)
print(result["greeting"])

# 可视化：ASCII 和 Mermaid 两种方式最适合入门阶段快速看图结构
print(app.get_graph().print_ascii())
print("=" * 50)
print(app.get_graph().draw_mermaid())
print("=" * 50)


# 可选：生成 PNG 图片（依赖 mermaid.ink 或 Pyppeteer，易受网络影响）
png_bytes = app.get_graph().draw_mermaid_png(max_retries=2, retry_delay=2.0)
output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
with open(output_path, "wb") as f:
    f.write(png_bytes)
print(f"图片已生成：{output_path}")

"""
【输出示例】
{'name': 'z3', 'greeting': 'Hello, z3!  。。。😄'}
Hello, z3!  。。。😄
+-----------+  
| __start__ |  
+-----------+  
      *        
      *        
      *        
+----------+   
| greeting |   
+----------+   
      *        
      *        
      *        
+-----------+  
| add_emoji |  
+-----------+  
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
        greeting(greeting)
        add_emoji(add_emoji)
        __end__([<p>__end__</p>]):::last
        __start__ --> greeting;
        greeting --> add_emoji;
        add_emoji --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc

==================================================
"""