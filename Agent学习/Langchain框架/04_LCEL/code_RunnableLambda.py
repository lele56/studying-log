import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from loguru import logger

from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

def debug_print(x):
    """打印中间结果，并把文本包装成 chain2 所需的 {"input": 文本} 结构。"""
    logger.info(f"中间结果:{x}")
    return {"input": x}

# 子链 1：中文介绍某主题，输出 str
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# 子链 2：将 input 翻译成英文
prompt2 = ChatPromptTemplate.from_messages(
    [("system", "你是一个翻译助手，将用户输入内容翻译成英文"), ("human", "{input}")]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# 方式一：直接把函数放在 | 之间，LCEL 会自动包装成 Runnable
full_chain = chain1 | debug_print | chain2
result1 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果111:{result1}")

# 方式二：显式使用 RunnableLambda(函数)，效果相同
debug_node = RunnableLambda(debug_print)
full_chain = chain1 | debug_node | chain2
result2 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果222:{result2}")

"""
【输出示例】
2026-08-23 18:43:42.652 | INFO     | __main__:debug_print:27 - 中间结果:LangChain 是一个用于开发由**大语言模型（LLM）驱动的应用程序**的开源框架。它的核心作用是作为“胶水”，将 LLM 与外部数据源（如文档、数据库）和工具（如 API、计算器）连接起来。

其主要特性和组件包括：
1. **模块化组件**：提供标准化的接口来管理提示词（Prompts）、模型（Models）和输出解析器。
2. **链（Chains）**：允许将多个步骤（如获取数据、提问、格式化结果）组合成复杂的工作流。
3. **智能体（Agents）**：让 LLM 能够自主推理，并根据需要动态选择和调用外部工具来完成任务。
4. **检索增强生成（RAG）**：内置强大的文档加载和向量检索功能，方便接入私有知识库，减少模型幻觉。
5. **记忆（Memory）**：赋予应用多轮对话的上下文记忆能力。

**一句话总结**：LangChain 帮助开发者快速构建不仅能聊天，还能**理解私有数据**、**记住上下文**并**执行复杂操作**的定制化 AI 应用。
2026-08-23 18:44:02.105 | INFO     | __main__:<module>:50 - 最终结果111:LangChain is an open-source framework for developing applications **powered by Large Language Models (LLMs)**. Its core role is to act as the "glue" connecting LLMs to external data sources (such as documents and databases) and tools (such as APIs and calculators).

Its main features and components include:
1. **Modular Components**: Provides standardized interfaces for managing prompts, models, and output parsers.
2. **Chains**: Allows combining multiple steps (e.g., fetching data, asking questions, and formatting results) into complex workflows.
3. **Agents**: Enables LLMs to reason autonomously and dynamically select and invoke external tools as needed to accomplish tasks.
4. **Retrieval-Augmented Generation (RAG)**: Features powerful built-in document loading and vector retrieval capabilities, making it easy to integrate private knowledge bases and reduce model hallucinations.
5. **Memory**: Empowers applications with contextual memory capabilities for multi-turn conversations.

**In one sentence**: LangChain helps developers rapidly build customized AI applications that can not only chat, but also **understand private data**, **remember context**, and **execute complex operations**.
2026-08-23 18:44:15.257 | INFO     | __main__:debug_print:27 - 中间结果:**LangChain** 是一个用于开发**大型语言模型（LLM）驱动应用程序**的开源框架。

它的核心理念是将大模型与外部工具和数据源“链接（Chain）”起来，使其能够解决复杂的实际业务问题。其主要特性包括：

1. **RAG（检索增强生成）**：轻松将大模型与私有数据源（如本地文档、数据库、向量库）结合，实现基于企业知识的精准问答。
2. **Agents（智能体）**：赋予大模型自主规划和决策的能力，使其能主动调用外部工具（如搜索引擎、计算器、API）来执行任务。
3. **Memory（记忆）**：提供上下文状态管理，支持流畅的多轮对话。
4. **统一接口**：高度模块化，方便开发者快速切换和组合不同的 LLM（如 OpenAI、Claude）及各种组件。

**简而言之**：如果把大模型比作“大脑”，LangChain 就是为它搭建的“神经系统”，赋予它连接外部数据、使用工具和落地为实际应用的能力。
2026-08-23 18:44:31.785 | INFO     | __main__:<module>:56 - 最终结果222:**LangChain** is an open-source framework used for developing **Large Language Model (LLM)-driven applications**.

Its core philosophy is to "chain" LLMs with external tools and data sources, enabling them to solve complex, real-world business problems. Its key features include:

1. **RAG (Retrieval-Augmented Generation)**: Easily integrate LLMs with private data sources (such as local documents, databases, and vector databases) to enable precise question-answering based on enterprise knowledge.
2. **Agents**: Empower LLMs with autonomous planning and decision-making capabilities, allowing them to proactively invoke external tools (e.g., search engines, calculators, APIs) to execute tasks.
3. **Memory**: Provides context state management to support seamless multi-turn conversations.
4. **Unified Interface**: Highly modular, making it convenient for developers to quickly swap and combine different LLMs (such as OpenAI and Claude) and various components.

**Simply put**: If an LLM is the "brain," LangChain is the "nervous system" built for it, empowering it with the ability to connect to external data, utilize tools, and be deployed as real-world applications.
"""