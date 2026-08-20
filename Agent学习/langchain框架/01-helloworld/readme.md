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

## 🐛 遇到的问题

1. **环境变量配置**: 需要在 `.env` 文件中配置 API 密钥
2. **日志级别设置**: 通过 `os.getenv()` 读取，有默认值兜底

## 📝 学习总结

### 今天学到了
- LangChain 的基本调用流程
- invoke 和 stream 两种调用方式的区别
- 日志系统的配置方法