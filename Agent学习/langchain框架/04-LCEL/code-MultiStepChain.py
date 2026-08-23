import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
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

# 子链 1：用中文介绍某主题，输出为 str
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

result1 = chain1.invoke({"topic": "langchain"})
logger.info(result1)

# 子链 2：将用户输入翻译成英文，期望入参为 {"input": 文本}
prompt2 = ChatPromptTemplate.from_messages(
    [("system", "你是一个翻译助手，将用户输入内容翻译成英文"), ("human", "{input}")]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# 串行组合：chain1 输出文本，用 lambda 转为 {"input": content}，以匹配 chain2 需要的输入结构
full_chain = chain1 | (lambda content: {"input": content}) | chain2

# 一次 invoke：先执行 chain1，再把结果作为 chain2 的 input
result = full_chain.invoke({"topic": "langchain"})
logger.info(result)

"""
【输出示例】
2026-08-23 17:55:44.187 | INFO     | __main__:<module>:35 - LangChain 是一个用于开发**大语言模型（LLM）驱动应用**的开源框架。它的核心价值在于将单纯的 LLM 转化为能够结合上下文并执行实际操作的生产力工具。

其核心特性包括：

1. **模块化组件**：提供模型接口封装、提示词模板、记忆机制（Memory）和智能体（Agents）等构建块。
2. **连接外部世界（RAG）**：支持无缝对接本地文档、向量数据库和外部 API，让模型能够访问和利用专属实时数据。
3. **链式调用（Chains）**：将多个组件或操作步骤按逻辑串联，实现复杂任务的自动化编排。

简而言之，LangChain 就像是一个强大的“胶水层”和“工具箱”，大幅简化了构建复杂 AI 应用（如智能客服、私有知识库问答、自动化工作流）的开发流程。
2026-08-23 17:56:12.527 | INFO     | __main__:<module>:49 - LangChain is an open-source framework for developing applications powered by large language models (LLMs).

Its core purpose is to **connect LLMs with the outside world**. Its main features include:

1. **Modular Design**: Provides out-of-the-box components such as prompt templates, conversation memory (Memory), and intelligent agents (Agents).
2. **Connecting External Tools**: Seamlessly integrates LLMs with external data sources, APIs, and tools through the "Chains" mechanism.
3. **Support for Advanced Features**: Significantly simplifies the complexity of building **Retrieval-Augmented Generation (RAG)** and **multi-step automated tasks**.

In short, LangChain is like a "Swiss Army knife" for LLMs. It enables them to evolve from mere chatbots into intelligent application systems capable of retrieving information, invoking tools, and processing complex data. It currently primarily supports Python and JavaScript/TypeScript.
"""
