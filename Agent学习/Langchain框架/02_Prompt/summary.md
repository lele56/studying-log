# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-21
- **主题**: LangChain 框架基础 - Prompt
- **目标**: 理解 LangChain 框架中 PromptTemplate 类和 ChatPromptTemplate 类的基本使用

## 📚 核心知识点

### 1. PromptTemplate 类和 ChatPromptTemplate 类是什么？
- 将原本模型json格式的消息模板包装成类，方便在代码中调用和管理。两种类代表两种不同的消息模板类型，分别用于普通字符串和对话消息。

### 2. 关键概念
- **PromptTemplate**: 用于生成普通字符串提示词，适合简单文本补全场景
- **ChatPromptTemplate**: 用于生成聊天消息列表，支持多角色（system/user/assistant）
- **MessagesPlaceholder**: 占位符，用于在模板中动态插入历史对话消息
- **消息角色**: 
  - `system`: 系统提示，设定模型行为
  - `user`: 用户输入
  - `assistant`: 模型回复

### 3. 重要函数
- `format_messages()`: 填入变量，最终生成提示消息列表
- `format()`: 填入变量，最终生成字符串
- `MessagesPlaceholder`: 用于在模板中插入历史对话消息列表
- `invoke()`: 通过 invoke 方法传入消息列表和问题

## 💻 代码示例

### 示例 1: PromptTemplate（普通字符串）
```python
from langchain_core.prompts import PromptTemplate

# 创建模板
prompt = PromptTemplate(
    template="请翻译以下文本：{text}，目标语言：{language}",
    input_variables=["text", "language"]
)

# 填入变量
formatted = prompt.format(text="Hello World", language="中文")
print(formatted)
# 输出：请翻译以下文本：Hello World，目标语言：中文
```

### 示例 2: ChatPromptTemplate（聊天消息）
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 创建聊天模板
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译助手"),
    MessagesPlaceholder("history"),  # 插入历史对话
    ("user", "{input}")
])

# 填入变量
messages = chat_prompt.format_messages(
    input="翻译：Hello",
    history=[("user", "你好"), ("assistant", "你好！有什么可以帮你的？")]
)
```

### 示例 3: 调用模型
```python
# 调用模型
response = llm.invoke(messages)
print(response.content)  # 获取回复内容
```

## 🐛 问题与思考

### Q1: 普通字符串 Prompt 和消息模板最大的工程差别是什么？
**答**: 普通字符串 Prompt 是直接在代码中写死的，消息模板则可以动态填入变量，更符合工程化需求。

### Q2: 什么时候应该用 MessagesPlaceholder，而不是把历史对话拼成一大段字符串？
**答**: 当需要根据历史对话消息列表动态生成提示词时，应该使用 MessagesPlaceholder。例如，在一个对话中，用户连续输入了多个问题，每个问题都需要根据之前的上下文来回答。

### Q3: 如果一个模板变量越来越多，你会如何判断它是不是该拆分？
**答**: 当变量属于不同职责或变化频率不同时，应该拆分。例如：系统提示词（很少变）和用户输入（经常变）应该分开管理；或者按功能模块拆分，如翻译模板、总结模板各自独立。

### Q4: 把提示词放到外部文件有什么好处和风险？
**答**: 
- **好处**: 提示词与代码分离，方便修改和维护；支持多语言/多版本管理；非技术人员也能编辑提示词。
- **风险**: 文件路径错误会导致加载失败；格式不一致可能引发解析错误；版本管理不当会造成混乱。

## 📝 学习总结

### Prompt 本质
Prompt 不是"随便写一句话"，而是对模型输入进行结构化组织。随着项目复杂度提升，输入会从纯字符串演化成多角色消息，再进一步演化成模板、占位符与外部配置文件。

### 消息与调用
聊天模型常见输入包括 str、消息对象列表、元组列表、字典列表；常见调用方式包括 invoke / ainvoke、stream / astream、batch / abatch。返回值通常是 AIMessage，正文一般通过 `.content` 读取。

### 模型与工程化
`PromptTemplate` 适合文本模板，`ChatPromptTemplate` 适合聊天模型与多角色场景，`MessagesPlaceholder` 是多轮历史拼接的关键。