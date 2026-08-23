import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
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

# 子链 1：中文简短介绍
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

# 子链 2：英文简短介绍（与 chain1 同结构，仅提示词语言不同）
prompt2 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

# RunnableParallel：同一输入会同时喂给多个子链，结果按键汇总为 dict
parallel_chain = RunnableParallel({
    "chinese": chain1, 
    "english": chain2
    })

# 一次 invoke，返回 {"chinese": "...", "english": "..."}
result = parallel_chain.invoke({"topic": "langchain"})
logger.info(result)

# 可选：打印并行链的 ASCII 图结构，便于理解“并行节点 + 汇总输出”的数据流
parallel_chain.get_graph().print_ascii()


"""
【输出示例】
2026-08-23 18:37:48.341 | INFO     | __main__:<module>:53 - {'chinese': 'LangChain 是一个用于开发**大语言模型（LLM）驱动的应用程序**的开源框架。你可以把它理解为构建复杂 AI 应用的“胶水”和“工具箱”。\n\n它的核心作用是**打破 LLM 的信息孤岛**，使其能够与外部世界交互。其主要特性包括：\n\n1. **模块化组件**：提供大量开箱即用的模块，如 Prompt 模板、模型接口封装、记忆机制（Memory）和向量数据库集成。\n2. **链（Chains）**：允许开发者将多个组件（LLM、API、数据库等）像搭积木一样串联，编排复杂的业务工作流。\n3. **智能体（Agents）**：赋予 LLM 逻辑推理能力，使其能根据用户意图，自主决策并调用外部工具（如搜索引擎、计算器、代码解释器）来完成任务。\n4. **强大的 RAG 支持**：极大地简化了“检索增强生成”流程，是构建基于企业私有知识库问答系统的首选工具。\n\n**总结**：LangChain 降低了 LLM 应用的开发门槛，帮助开发者快速将大模型从“聊天机器人”转化为能接入业务数据、调用外部工具的**生产力系统**。它主要支持 Python 和 JavaScript/TypeScript。', 'english': 'LangChain is an open-source framework designed for building applications powered by Large Language Models (LLMs). It provides modular components—such as chains, agents, memory, and prompt templates—that enable developers to easily connect LLMs with external data sources, APIs, and tools, facilitating the creation of complex, context-aware AI applications.'}
            +--------------------------------+             
            | Parallel<chinese,english>Input |             
            +--------------------------------+             
                   ***               ***                   
                ***                     ***                
              **                           **              
+--------------------+              +--------------------+ 
| ChatPromptTemplate |              | ChatPromptTemplate | 
+--------------------+              +--------------------+ 
           *                                   *           
           *                                   *           
           *                                   *           
    +------------+                      +------------+     
    | ChatOpenAI |                      | ChatOpenAI |     
    +------------+                      +------------+     
           *                                   *           
           *                                   *           
           *                                   *           
  +-----------------+                 +-----------------+  
  | StrOutputParser |                 | StrOutputParser |  
  +-----------------+                 +-----------------+  
                   ***               ***                   
                      ***         ***                      
                         **     **                         
            +---------------------------------+            
            | Parallel<chinese,english>Output |            
            +---------------------------------+  
"""