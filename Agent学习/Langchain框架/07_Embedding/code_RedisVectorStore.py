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

# 待写入的文本及（可选）元数据
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]

# 批量转成向量：这里只是为了先观察向量维度和内容；真正写入时 add_texts 内部会再次完成向量化
embeddings = embeddingsModel.embed_documents(texts)
for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i-1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前5个向量值: {vec[:10]}\n")

# 定义每条文本对应的元数据信息
# metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]

# 定义每条文本对应的元数据信息；真实 RAG 中这些 metadata 往往来自 Document.metadata，也可作为来源展示或过滤条件
metadata = [{"segment_id": str(i)} for i in range(1, len(texts) + 1)]

# Redis 连接与索引名
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:6379",
)

# 创建 Redis 向量存储实例：此时只是“连上库 + 指定索引配置”，还没真正写入文本；真正写入发生在 add_texts()
vector_store = RedisVectorStore(embeddingsModel, config=config)

# 将文本与元数据写入向量库（add_texts 内部会调 embed_documents，无需先算向量）
ids = vector_store.add_texts(texts, metadata)

# 打印前5个存储记录的ID
print(ids[0:5])

"""
【输出示例】
文本 1: 我喜欢吃苹果
向量长度: 1024
前5个向量值: [-0.040658846497535706, 0.03661542385816574, -0.07420426607131958, 0.0038889849092811346, -0.06338436901569366, -0.02869705855846405, -0.027835959568619728, 0.036840058863162994, -0.023455586284399033, -0.02789211831986904]

文本 2: 苹果是我最喜欢吃的水果
向量长度: 1024
前5个向量值: [-0.03397761657834053, 0.04141080006957054, -0.06891913712024689, 0.0057834237813949585, -0.06954938173294067, -0.04560007527470589, -0.0416332371532917, 0.04504397511482239, -0.0455259270966053, -0.017934175208210945]

文本 3: 我喜欢用苹果手机
向量长度: 1024
前5个向量值: [-0.05257301777601242, 0.006232932209968567, -0.11312419176101685, -0.023445231840014458, -0.03652263060212135, -0.043917473405599594, 0.005461459513753653, 0.028713824227452278, 0.0019592575263231993, 0.011205165646970272]

['newsgroups:01M0YBB8H1004QK1M950Z8K17V', 'newsgroups:01M0YBB8H1004QK1M950Z8K17W', 'newsgroups:01M0YBB8H1004QK1M950Z8K17X']
"""