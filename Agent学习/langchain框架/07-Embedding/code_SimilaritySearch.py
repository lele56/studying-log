from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

# 初始化嵌入模型
embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3", 
    dashscope_api_key=os.getenv("OPENAI_API_KEY")
)

# 连接已有索引（与 RedisVectorStore.py 中 index_name、redis_url 一致）
vector_store = RedisVectorStore(
    embeddingsModel, 
    config=RedisConfig(
        index_name="newsgroups",
        redis_url="redis://localhost:6379",
    )
)

# 查询文本 → 向量化 → 在库中做相似度检索；这里取前 3 条结果
query = "我喜欢用什么手机"
results = vector_store.similarity_search_with_score(query, k=3)

print("=== 查询结果 ===")
for i, (doc, score) in enumerate(results, 1):
    # 这里把“距离”近似换算成“相似度”只是为了展示更直观；工程里请以具体返回定义为准
    similarity = 1 - score
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")

"""
【输出示例】
=== 查询结果 ===
结果 1:
内容: 我喜欢用苹果手机
元数据: {'segment_id': '3'}
相似度: 0.8594
结果 2:
内容: 我喜欢吃苹果
元数据: {'segment_id': '1'}
相似度: 0.6611
结果 3:
内容: 苹果是我最喜欢吃的水果
元数据: {'segment_id': '2'}
相似度: 0.6228
"""
