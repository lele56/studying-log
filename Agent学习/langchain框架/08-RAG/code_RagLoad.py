# txt 文档加载器
from langchain_community.document_loaders import TextLoader

file_path = "document_sample/sample.txt"
encoding = "utf-8"

# load() 为 BaseLoader 统一接口，返回 List[Document]
docs = TextLoader(file_path, encoding=encoding).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'document_sample/sample.txt'}, page_content='LangChain 是一个用于构建基于大语言模型（LLM）应用的开发框架，旨在帮助开发者更高效地集成、管理和增强大语言模型的能力，构建端到端的应用程序。它提供了一套模块化工具和接口，支持从简单的文本生成到复杂的多步骤推理任务。')]"""

# pdf 文档加载器
from langchain_community.document_loaders import PyPDFLoader

docs = PyPDFLoader(
    file_path = "document_sample/sample.pdf",
    extraction_mode="plain",  # plain 纯文本；layout 按版面
).load()

print(docs)
"""
【输出示例】
[Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'assets/sample.pdf', 'total_pages': 36, 'page': 0, 'page_label': '1'}, page_content='中国科学院国家天文台 \n2023 年部门预算'), Document(metadata={'producer': 'Microsoft® Word 2019', 'creator': 'Microsoft® Word 2019', 'creationdate': '2023-07-24T17:46:07+08:00', 'title': '中国科学院国家天文台2023年度部门预算', 'author': 'MC SYSTEM', 'moddate': '2023-07-24T17:46:07+08:00', 'source': 'document_sample/sample.pdf', 'total_pages': 36, 'page': 1, 'page_label': '2'}, page_content='目……
"""

# word 文档加载器
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

docs = UnstructuredWordDocumentLoader(
    file_path="document_sample/alibaba-more.docx",
    mode="single",  # single 整篇一个 Document；elements 按元素切分
).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'document_sample/alibaba-more.docx'}, page_content='Java开发手册（黄山版）\n\nJava开发手册（黄山版）\n\n前言 \n\n《Java 开发手册》是阿里巴巴技术团队的集体智慧结晶和经验总结，经历了多次大规模一线实战的检验及不断完善，公开到业界后，众多社区开发者踊跃参与打磨完善，系统化地整理成册，当前的最新版本是黄山版。现代软件行业的高速发展对开发者的综合素质要求越来越高，因为不仅是编程知识点，其它维度的知识点也会影响到软件的最终交付质量。比如：五花八门的错误码会人为地增加排查问题的难度；数据库的表结构和索引设计缺陷带来的系统架构缺陷或性能风险；工程结构混乱导致后
"""

# markdown 文档加载器
from langchain_community.document_loaders import UnstructuredMarkdownLoader

docs = UnstructuredMarkdownLoader(
    file_path="document_sample/sample.md",
    mode="elements",  # single 整篇；elements 按元素切分
).load()

print(docs)
"""
【输出示例】
[Document(metadata={'source': 'document_sample/sample.md', 'category_depth': 0, 'languages': ['ron'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-03-10T10:36:41', 'category': 'Title', 'element_id': 'e6a3b421f39f298fffbc3cf1b3b95817'}, page_content='投机解码（Speculative Decoding）介绍'), Document(metadata={'source': 'assets/sample.md', 'category_depth': 1, 'languages': ['kor'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-03-10T10:36:41', 'parent_id': 'e6a3b421f39f298fffbc3cf1b3b95817', 'category': 'Title', 'element_id': '3a77bcc407e48690734a4701557ffdb6'}, page_content='引言'), Document(metadata={'source': 'assets/sample.md', 'languages': ['nor', 'vie', 'zho'], 'file_directory': 'assets', 'filename': 'sample.md', 'filetype': 'text/markdown', 'last_modified': '2026-03-10T10:36:41', 'parent_id': '3a77bcc407e48690734a4701557ffdb6', 'category': 'UncategorizedText', 'element_id': '5a9685df7e44c7f338356ef37bc09149'}, page_content='投机解码（Speculative Decoding）是……
"""

# json 文档加载器
from langchain_community.document_loaders import JSONLoader

docs = JSONLoader(
    file_path="document_sample/sample.json",
    jq_schema=".",  # 提取所有字段
    text_content=False,  # 是否按字符串处理内容
).load()

print(docs)

"""
【输出示例】
[Document(metadata={'source': '\\studying-log\\Agent学习\\Langchain框架\\08-RAG\\document_sample\\sample.json', 'seq_num': 1}, page_content='{"status": "success", "data": {"page": 2, "per_page": 3, "total_pages": 5, "total_items": 14, "items": [{"id": 101, "title": "Understanding JSONLoader", "content": "This article explains how to parse API responses...", "author": {"id": "user_1", "name": "Alice"}, "created_at": "2023-10-05T08:12:33Z"}, {"id": 102, "title": "Advanced jq Schema Patterns", "content": "Learn to handle nested structures with...", "author": {"id": "user_2", "name": "Bob"}, "created_at": "2023-10-05T09:15:21Z"}, {"id": 103, "title": "LangChain Metadata Handling", "content": "Best practices for preserving metadata...", "author": {"id": "user_3", "name": "Charlie"}, "created_at": "2023-10-05T10:03:47Z"}]}}')]"""

# csv 文档加载器
from langchain_community.document_loaders.csv_loader import CSVLoader

# 方式一：不指定列 → 整行（所有列）拼成一条字符串作为 page_content，metadata 通常只有 source 等
docs_all = CSVLoader(file_path="document_sample/sample.csv").load()
print("=== 方式一：整行作为 page_content ===")
print(
    "page_content 示例:",
    (
        docs_all[0].page_content[:80] + "..."
        if len(docs_all[0].page_content) > 80
        else docs_all[0].page_content
    ),
)
print("metadata 示例:", docs_all[0].metadata, "\n")

# 方式二：指定 content_columns 与 metadata_columns → 正文只取 content 列，title/author 进 metadata，便于检索时按作者/标题过滤
docs_split = CSVLoader(
    file_path="document_sample/sample.csv",
    metadata_columns=["title", "author"],
    content_columns=["content"],
).load()
print("=== 方式二：content 列作为正文，title/author 进 metadata ===")
print("page_content 示例:", docs_split[0].page_content)
print("metadata 示例:", docs_split[0].metadata)


"""
【输出示例】
=== 方式一：整行作为 page_content ===
page_content 示例: id: 1
title: Introduction to Python
content: Python is a popular programming lan...
metadata 示例: {'source': 'document_sample/sample.csv', 'row': 0} 

=== 方式二：content 列作为正文，title/author 进 metadata ===
page_content 示例: content: Python is a popular programming language.
metadata 示例: {'source': 'document_sample/sample.csv', 'row': 0, 'title': 'Introduction to Python', 'author': 'John Doe'}
"""