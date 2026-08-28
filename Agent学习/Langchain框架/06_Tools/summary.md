# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-25
- **主题**: LangChain 框架基础 - Tools
- **目标**: 理解 LangChain 框架中 Tools 的使用方法

## 📚 核心知识点

### 1. Tools Calling 是什么？
- Tool Calling 是模型根据当前任务情况来调用外部工具的机制。

### 2. 关键概念
- **@tool 装饰器**：将普通 Python 函数包装成 LangChain 可识别的工具，自动提取函数名和文档字符串作为描述。
- **args_schema (Pydantic)**：定义工具参数的结构（类型、描述、校验规则），帮助模型生成正确的参数。
- **Tool Parser**：解析模型输出的 JSON，提取工具调用意图和参数。
- **bind_tools**：将工具列表绑定到模型，告诉模型“你可以使用这些工具”。


### 3. 重要函数
- `@tool`：将函数包装成模型可以调用的工具。
- `model.bind_tools([tools])`：将工具绑定到模型，开启工具调用能力。
- `JsonOutputKeyToolsParser`：解析模型输出，提取指定工具的参数。
- `tool.invoke(args)`：直接调用工具函数，传入参数并返回结果。


## 💻 代码示例

### 示例 1：使用 @tool 定义简单工具
```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int) -> int:
    """计算两个数字的和"""
    return a + b

# 手动调用
print(add.invoke({"a": 5, "b": 3}))  # 输出: 8
```

### 示例 2：使用 Pydantic 定义参数描述
```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class WeatherInput(BaseModel):
    city: str = Field(description="城市名称，如 Beijing")

@tool(args_schema=WeatherInput)
def get_weather(city: str) -> str:
    """查询指定城市的天气"""
    return f"{city} 的天气是晴天"
```

### 示例 3：绑定工具并解析调用
```python
from langchain_core.output_parsers import JsonOutputKeyToolsParser

# 1. 绑定工具
model_with_tools = model.bind_tools([get_weather])

# 2. 解析器配置
parser = JsonOutputKeyToolsParser(key_name="get_weather", first_tool_only=True)

# 3. 组合链
chain = model_with_tools | parser

# 4. 调用
result = chain.invoke("北京今天天气怎么样？")
# 返回: {'city': 'Beijing'}
```

## 🐛 问题与思考

### Q1: 一个函数是否应该暴露成 Tool，判断标准是什么？
**答**: 看它是否需要模型根据自然语言判断调用时机和参数。如果是固定内部流程，普通代码即可；如果需要模型按上下文选择并填参，才值得暴露成 Tool。

### Q2: 工具描述写得差，会导致哪些真实问题？
**答**: 模型可能不用工具、错用工具、参数填错、在不该执行时执行。模型看不到你的函数内部，只能依赖名称、描述和参数 schema 判断能力边界。

### Q3: “模型负责决策，程序负责执行”在安全上意味着什么？
**答**: 模型可以提出调用意图，但真正访问数据库、发消息、下单、删除数据必须由程序执行，并加权限、校验、确认、审计和失败处理。不能把副作用完全交给模型自由发挥。

### Q4: 有副作用的工具和只读工具，在设计上应该有什么不同？
**答**: 只读工具重点是参数和结果质量；有副作用工具还要加二次确认、权限控制、幂等、回滚、日志和告警。风险越高，自动化程度越要谨慎。

## 📝 学习总结

### Tool 是什么
- Tool 是暴露给模型的外部能力，本质上通常是被包装过的函数或接口；Tool Calling / Function Calling 则是模型输出调用意图的机制。

### 基本分工
- 模型负责“要不要调、调哪个、传什么参数”，程序负责“真正执行工具并回填结果”。

### 怎么定义 Tool
- 最简单的方式是使用 @tool 装饰器。模型主要通过 name、description、args_schema 理解工具，所以工具名、工具说明、参数定义都非常关键。

### 为什么要配合 Pydantic
- Pydantic 能让参数定义更清晰、校验更稳定、错误更容易定位，也更利于模型生成正确参数，是 Tool 从“能跑”走向“工程化”的重要一步。