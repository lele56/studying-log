# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-24
- **主题**: LangChain 框架基础 - Memory
- **目标**: 理解 LangChain 框架中 Memory 的使用方法

## 📚 核心知识点

### 1. Memory 是什么？
- 这里的“记忆”不是更新模型参数，而是**将历史消息作为上下文重新注入给模型**，让模型在推理时能参考之前的对话内容。


### 2. 关键概念
- **BaseChatMessageHistory**: 所有历史存储类的**抽象基类**，定义了 `add_message`、`clear` 等标准接口。
- **InMemoryChatMessageHistory**: 内存存储实现，速度快但进程结束即丢失，适合本地调试。
- **RedisChatMessageHistory**: Redis 存储实现，支持持久化和多实例共享，适合生产环境。
- **RunnableWithMessageHistory**: 链的包装器，负责在调用前后自动读写历史消息，实现“自动化记忆”。
- **MessagesPlaceholder**: Prompt 模板中的占位符，告诉模型“历史消息应该插在这个位置”。

### 3. 重要函数
- `history.add_user_message(msg)`: 向历史中添加一条用户消息。
- `history.add_message(msg)`: 向历史中添加任意类型的消息（如 AI 回复）。
- `history.clear()`: 清空当前存储的所有历史消息。
- `get_session_history(session_id)`: 回调函数，根据会话 ID 返回对应的历史存储对象。

## 💻 代码示例

### 示例 1：手动管理内存历史
```python
from langchain_core.chat_history import InMemoryChatMessageHistory

history = InMemoryChatMessageHistory()
history.add_user_message("我叫张三")
ai_msg = llm.invoke(history.messages)
history.add_message(ai_msg) # 必须手动把回复加回去，否则模型记不住
```

### 示例 2：自动管理多会话历史
```python
store = {}
def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 包装链，自动根据 session_id 存取历史
with_history = RunnableWithMessageHistory(
    chain, 
    get_session_history, 
    input_messages_key="question", 
    history_messages_key="history"
)
```

## 🐛 问题与思考

### Q1: 如果用户说“模型记住了我”，你会怎样解释本章里的“记忆”到底是什么？
**答**: 这里的记忆不是模型参数更新，而是系统把历史消息重新取出来，作为上下文交给模型。模型看起来记得，是因为应用帮它带上了历史。

### Q2: RunnableWithMessageHistory 和具体存储类的边界为什么要分清？
**答**: 前者负责把历史接入调用链，决定何时读写；后者负责消息消息真正存在哪里。边界分清后，内存、Redis、数据库等存储可以替换，而调用链逻辑不用大改。

### Q3: 多用户场景里，session_id 设计不好会出现什么问题？
**答**: 可能串会话、串用户、误用历史，甚至泄露隐私。session_id 应该和用户、会话、业务租户等隔离策略一起设计，而不是随便写一个字符串。

### Q4: 为什么完整历史不能无限塞回模型？
**答**: 上下文窗口、成本、延迟和噪声都会增加。历史越多不一定越好，真实系统要做窗口截断、摘要、重要信息提取和过期清理。

## 📝 学习总结

### 记忆是什么 
- 这里讲的是短期记忆 / 对话历史，不是训练模型，也不是更新模型参数，而是把历史消息保存下来，并在下一轮调用前重新交给模型。

### 基本流程
- 读历史 → 拼入提示 → 调模型 → 写回历史。MessagesPlaceholder 负责给历史消息留位置，RunnableWithMessageHistory 负责管理读写时机，BaseChatMessageHistory 及其实现类负责具体存储。

### 存储怎么选
- InMemoryChatMessageHistory 适合单进程学习和演示，进程一停就丢；RedisChatMessageHistory 适合持久化、多实例共享和跨进程会话恢复。