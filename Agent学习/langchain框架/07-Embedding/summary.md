# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-26
- **主题**: LangChain 框架基础 - Embedding
- **目标**: 理解 LangChain 框架中 向量数据库和 Embedding 的使用方法

## 📚 核心知识点

### 1. 向量数据库是什么？
- 向量数据库是一种存储和检索高维向量的数据库，一个向量可以表示一个文本或者一个文档。

### 2. Embedding 是什么？
- Embedding 是一种将文本转换为固定长度向量的技术，用于表示文本的语义信息。

### 3. 关键概念
- **DashScopeEmbeddings**: 阿里通义千问的 Embedding 模型实现，将文本转换为固定长度的向量。
- **Vector Store (向量数据库)**: 专门存储和检索高维向量的数据库，支持语义相似度搜索。
- **Cosine Similarity (余弦相似度)**: 衡量两个向量之间相似度的常用方法，值越接近 1 表示越相似。
- **Metadata (元数据)**: 伴随向量存储的额外信息（如原文、ID、标签），用于检索后的展示和过滤。

### 4. 重要函数
- `embeddings.embed_query(text)`: 将单条文本（如用户查询）转换为向量。
- `embeddings.embed_documents(texts)`: 批量将多条文本转换为向量列表。
- `vector_store.from_texts(texts, embedding)`: 从文本列表创建向量存储。
- `vector_store.similarity_search(query, k)`: 根据查询向量搜索最相似的 k 个文档。


## 💻 代码示例

### 示例 1：调用 DashScope 原生 API 获取向量
```python
import dashscope
from http import HTTPStatus

# 调用百炼文本嵌入接口
resp = dashscope.TextEmbedding.call(
    model="text-embedding-v4",
    input="衣服的质量杠杠的",
)

if resp.status_code == HTTPStatus.OK:
    print(resp)  # 观察完整响应结构
```

### 示例 2：计算文本间的余弦相似度
```python
import numpy as np

def cosine_similarity(vec1, vec2):
    """计算两个向量的余弦相似度：点积 / (模长之积)，结果越接近 1 一般越相似"""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# 观察结果：语义越接近，相似度越高
# "我喜欢吃苹果" vs "苹果是我最喜欢吃的水果" → 0.9064
# "我喜欢吃苹果" vs "我喜欢用苹果手机" → 0.7656
```

### 示例 3：写入 Redis 向量数据库
```python
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings

embeddingsModel = DashScopeEmbeddings(model="text-embedding-v3")

# 配置 Redis 连接
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:6379",
)

# 创建向量存储实例
vector_store = RedisVectorStore(embeddingsModel, config=config)

# 写入文本和元数据（内部自动向量化）
texts = ["我喜欢吃苹果", "苹果是我最喜欢吃的水果", "我喜欢用苹果手机"]
metadata = [{"segment_id": str(i)} for i in range(1, len(texts) + 1)]
ids = vector_store.add_texts(texts, metadata)
```

### 示例 4：从 Redis 检索相似文档
```python
# 相似度检索：返回文档内容和距离分数
query = "我喜欢用什么手机"
results = vector_store.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, 1):
    similarity = 1 - score  # 距离转相似度
    print(f"结果 {i}: {doc.page_content}, 相似度: {similarity:.4f}")
```

## 🐛 问题与思考

### Q1: 为什么 Embedding 适合做语义检索，而普通关键词匹配不够？
**答**: Embedding 把文本映射到语义空间，能捕捉同义表达和相近含义；关键词匹配更依赖字面重合。比如“退款规则”和“怎么退钱”字面不同，但语义接近。

### Q2: 向量写入数据库时，除了向量本身，还应该保存哪些信息？
**答**: 至少要保存原文片段、来源、文档 ID、段落位置、业务标签、更新时间等 metadata。否则检索回来只有一串向量，无法展示、追溯或过滤。

### Q3: 相似度高是否一定代表答案可用？为什么？
**答**: 不一定。向量相似只能说明语义接近，可能仍然答非所问、缺少关键条件或不是最新资料。真实 RAG 还要结合阈值、过滤、Rerank 和答案生成约束。

### Q4: 如果查询结果总是不相关，你会先排查哪些环节？
**答**: 查文档是否写入、Embedding 模型是否一致、向量维度是否匹配、查询文本是否合理、metadata 是否过滤过严、相似度计算和 Top K 是否设置得当。

## 📝 学习总结

### 向量与 Embedding
- Embedding 模型会把文本转换成固定长度向量，让“语义相近”可以转换成“向量相似”。

### 向量数据库
-  它解决的不是普通字段查询，而是“按语义找最接近内容”的问题；这也是 RAG 能成立的基础。
