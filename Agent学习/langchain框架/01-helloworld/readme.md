# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-20
- **主题**: LangChain 框架基础 - HelloWorld 示例
- **目标**: 理解 LangChain 框架的基本调用流程

## 📚 核心知识点

### 1. LangChain 是什么？
- 基于 Python 的应用层框架
- 用于封装和调用大语言模型
- 支持多种模型提供商（OpenAI、阿里云等）

### 2. 关键概念
- **LLM 客户端**: 通过 `ChatOpenAI` 创建对话客户端
- **invoke()**: 一次性获取完整回复
- **stream()**: 流式输出，边生成边返回

### 3. 重要参数
- `temperature`: 控制回复随机程度（0-1）
- `max_tokens`: 单次回复最大长度
- `LOG_LEVEL`: 环境变量控制日志输出级别

## 💻 代码示例

```python
# 初始化客户端
llm = ChatOpenAI(
    model=model_name,
    temperature=0.7,
    max_tokens=2048,
)

# 调用方式
response = llm.invoke("你是谁")  # 一次性
for chunk in llm.stream("你是谁"):  # 流式
    print(chunk.content, end="")
```

## 🐛 问题与思考

### Q1: 第一次 LangChain 调用失败时，你会按什么顺序排查？
**答**: 先检查依赖问题，查看 langchain 是否能成功导入，再检查环境变量、Base URL、模型名称、网络和模型额度，最后检查代码对象和调用方式。

### Q2: 为什么本章要同时关注 invoke() 和 stream()？
**答**: invoke() 是一次性获取完整的回复，而 stream() 是边生成边回复，更接近实际情况。

### Q3: 多模型共存时，哪些配置最容易写乱？
**答**: 模型名称、Base URL、API 密钥等。

### Q4: 教学 Demo 和真实项目代码最大的差别是什么？
**答**: 教学 Demo 是为了展示基本流程，代码只需要跑通就行了，而真实项目还要处理配置校验、日志、异常、超时、重试、流式输出和敏感信息隐藏。

## 📝 学习总结

- HelloWorld 的本质不是“写一个很简单的例子”，而是验证整条调用链是否打通。对 LangChain 来说，这条最小链路就是：准备 API Key、模型名、Base URL → 初始化模型 → invoke() 调用 → .content 取回复。