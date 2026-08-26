# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-26
- **主题**: LangChain 框架基础 - RAG
- **目标**: 理解 LangChain 框架中 RAG 的使用方法

## 📚 核心知识点

### 1. RAG 是什么？
- RAG（检索增强生成）是一种架构模式：先从外部知识库检索出相关文档，再让模型基于这些文档生成答案，从而减少幻觉，提高准确性。

### 2. 关键概念
- **Document Loader**: 文档加载器，负责从各种格式（PDF、Word、CSV、JSON 等）读取内容，转换为 LangChain 的 `Document` 对象。
- **Text Splitter**: 文本分割器，将长文档按规则（字符数、重叠量）切分成小块（Chunk），避免超出模型上下文窗口。
- **Retriever**: 检索器，封装了向量库的查询逻辑，根据用户输入返回最相关的文档块列表。
- **RunnablePassthrough**: LCEL 中的透传组件，将输入原封不动地传递给下一步，确保 Prompt 能同时拿到检索结果和原始问题。

### 3. 重要函数
- `loader.load()`: 加载文档，返回 `Document` 对象列表。
- `splitter.split_documents(docs)`: 按规则将文档切分成更小的块。
- `vector_store.as_retriever()`: 将向量存储转换为检索器，供链调用。
- `retriever.invoke(query)`: 执行检索，返回相关文档块。
- `create_stuff_documents_chain(llm, prompt)`: 创建一个将文档内容注入 Prompt 并调用模型的链。


## 💻 代码示例

### 示例 1：加载多种格式文档
```python
from langchain_community.document_loaders import (
    TextLoader, CSVLoader, JSONLoader, 
    UnstructuredMarkdownLoader, PyPDFLoader, 
    UnstructuredWordDocumentLoader
)

# 加载不同格式的文件
txt_docs = TextLoader("sample.txt", encoding="utf-8").load()
csv_docs = CSVLoader("sample.csv").load()
pdf_docs = PyPDFLoader("sample.pdf").load()
docx_docs = UnstructuredWordDocumentLoader("sample.docx").load()
```

### 示例 2：递归文本分割
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 每块最多 500 字符
    chunk_overlap=50,    # 块之间重叠 50 字符，保持语义连贯
)

# 分割文档
chunks = splitter.split_documents(txt_docs)
print(f"分割后共 {len(chunks)} 个块")
```

### 示例 3：搭建完整 RAG 链
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. 定义 Prompt 模板
template = """根据以下参考资料回答问题：
{context}

问题：{question}
回答："""
prompt = ChatPromptTemplate.from_template(template)

# 2. 组装 RAG 链
# retriever 负责查资料，RunnablePassthrough 负责保留原始问题
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt 
    | llm
)

# 3. 调用
result = rag_chain.invoke("阿里巴巴的核心价值观是什么？")
```

## 🐛 问题与思考

### Q1: 一个完整 RAG 系统里，哪些步骤属于离线建库，哪些属于在线问答？
**答**: 离线建库包括文档加载、清洗、切分、Embedding、入向量库；在线问答包括问题向量化、召回、重排、上下文组装、模型生成和答案返回。两段分清，排障会简单很多。

### Q2: 文本切分为什么不是越细越好，也不是越大越好？
**答**: 太细会丢上下文，太大又会引入噪声并浪费 token。好的切分要兼顾语义完整、召回精度和上下文成本，必要时还要保留标题、层级和来源信息。

### Q3: 如果 RAG 答案出现幻觉，你会如何判断是检索问题还是生成问题？
**答**: 先看召回片段是否包含答案依据。如果没召回到，查文档、切分、Embedding 和检索参数；如果召回到了但模型乱答，查 Prompt、引用约束、上下文排序和输出要求。

### Q4: 为什么 RAG 需要保留来源和 metadata？
**答**: 来源能让答案可追溯，metadata 能支持过滤、排序、权限控制和排障。企业场景里，只答对还不够，还要知道依据来自哪里、是否有权限使用。

## 📝 学习总结

### RAG 的本质
- 不是训练模型，而是"先检索、后生成"。通过引入外部知识，让模型回答有据可依，大幅减少幻觉。

### RAG 的两阶段
- **索引阶段（离线）**：加载文档 → 切分 → 向量化 → 存入向量库。
- **检索阶段（在线）**：用户提问 → 检索相关文档 → 组装 Prompt → 模型生成答案。

### 核心组件分工
- **Loader** 负责"读"，**Splitter** 负责"切"，**Retriever** 负责"找"，**LLM** 负责"答"。各司其职，通过 LCEL 串联成完整链路。