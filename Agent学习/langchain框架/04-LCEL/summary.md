# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-23
- **主题**: LangChain 框架基础 - LCEL
- **目标**: 理解 LangChain 框架中 LCEL 的使用方法

## 📚 核心知识点

### 1. LCEL 是什么？
- LCEL 全称 **LangChain Expression Language**，是一种**声明式**的链式组合语言。
- 它通过 `|` 操作符将不同的 `Runnable` 组件串联起来，形成完整的处理流程。

### 2. 关键概念
- **Runnable**: LangChain 中统一的"可执行组件"抽象。Prompt、Model、Parser、Tool 等都实现了 Runnable 接口。
- **RunnableSequence**: 顺序链，将多个 Runnable 按顺序执行，前一个的输出是后一个的输入。
- **RunnableBranch**: 分支链，根据条件判断执行哪个子链。
- **RunnableParallel**: 并行链，多个子链同时运行，最后汇总结果。
- **RunnableLambda**: Lambda 函数链，将自定义函数包装成 Runnable 对象，插入到链中。

### 3. 重要函数
- `|` (管道符): 连接两个 Runnable，创建 RunnableSequence
- `.invoke()`: 同步调用链，等待完整结果返回
- `.stream()`: 流式调用，逐步返回结果（适合 LLM 输出）
- `.batch()`: 批量调用，同时处理多个输入
- `.with_retry()`: 设置重试策略，提高链路稳定性
- `.with_fallbacks()`: 设置兜底模型，主模型失败时自动切换


## 💻 代码示例

### 示例 1：基础顺序链
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("请简要介绍{topic}")
model = init_chat_model(model="qwen-turbo")
parser = StrOutputParser()

# 使用 | 连接
chain = prompt | model | parser
result = chain.invoke({"topic": "Python"})
```

### 示例 2：并行链
```python
from langchain_core.runnables import RunnableParallel

parallel_chain = RunnableParallel({
    "summary": summary_chain,
    "keywords": keyword_chain,
})
result = parallel_chain.invoke({"text": "文章内容"})
# 返回: {"summary": "...", "keywords": [...]}
```

### 示例 3：自定义 Lambda
```python
from langchain_core.runnables import RunnableLambda

def format_output(data):
    return f"摘要：{data['summary']}\n关键词：{', '.join(data['keywords'])}"

chain = parallel_chain | RunnableLambda(format_output)
```

## 🐛 问题与思考

### Q1: LCEL 帮你解决的不是“少写几行代码”，而是什么问题？
**答**: 它让输入格式化、模型调用、解析、分支、并行、和后处理都变成可组合的 Runnable。重点式流程结构清楚、可复用、可流式、可批处理，而不是管道符看起来简洁。

### Q2: 读一条 LCEL 链时，你会如何判断每一段是否设计合理？
**答**: 看每个 Runnable 的输入和输出是否清楚，是否只做一类事情，是否方便单独测试。链路问题很多不是模型错，而是前后节点的数据结构没对上。

### Q3: RunnableLambda 什么时候是好用的胶水，什么时候会变成坏味道？
**答**: 少量字段转换、清洗、路由判断适合用它；如果里面塞了大量业务逻辑、外部副作用和复杂异常处理、就应该拆成明确函数、工具或服务，而不是藏在链里。

### Q4: 遇到“先分类、再分流、部分并行、最后汇总”的任务，你会如何拆链？
**答**: 先用顺序链做分类，再用分支链选择路线，可并行的检索或分析用并行链，最后用汇总节点统一输出。先画数据流，再写 LCEL，会比直接拼管道稳。

## 📝 学习总结

### Runnable 
- Runnable 式 LangChain 中统一的“可执行组件”抽象。Prompt、Model、Parser、Tool、Chain之所以能被统一调用，是因为它们在 Runnable 这层被约束成了同一种接口风格。

### LCEL
- LCEL 是把多个 Runnable 组合成链的表达式语言。它最核心的价值，不只是 | 写起来简介，而是让流程变得声明式、可组合、可扩展。

### 常见链结构
- 常见链结构中，顺序链是基础，分支链解决路由问题，多步串行链解决前后步骤依赖问题，并行链解决多路同时处理问题，RunnableLambda 解决自定义逻辑如何插入链；重试与兜底则解决链路稳定性问题。