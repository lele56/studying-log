import dashscope
import os
from http import HTTPStatus
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# 准备多句文本，用于观察“语义越接近，相似度通常越高”
texts = ["我喜欢吃苹果", "苹果是我最喜欢吃的水果", "我喜欢用苹果手机"]

embeddings = []
# 这里选用多模态 embedding 接口来处理文本输入，主要是为了演示“拿到向量后如何做比较”
# 若你在真实项目里只处理文本，也完全可以换成常规文本 embedding 模型
for text in texts:
    input_data = [{"text": text}]
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        input=input_data,
    )
    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output['embeddings'][0]['embedding']
        embeddings.append(embedding)

def cosine_similarity(vec1, vec2):
    """计算两个向量的余弦相似度：点积 / (模长之积)，结果越接近 1 一般越相似"""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

print("文本相似度比较结果:")
print("=" * 60)

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"文本{i+1} vs 文本{j+1}:")
        print(f"  文本{i+1}: {texts[i]}")
        print(f"  文本{j+1}: {texts[j]}")
        print(f"  余弦相似度: {similarity:.4f}")
        print("-" * 40)


"""
【输出示例】
文本相似度比较结果:
============================================================
文本1 vs 文本2:
  文本1: 我喜欢吃苹果
  文本2: 苹果是我最喜欢吃的水果
  余弦相似度: 0.9064
----------------------------------------
文本1 vs 文本3:
  文本1: 我喜欢吃苹果
  文本3: 我喜欢用苹果手机
  余弦相似度: 0.7656
----------------------------------------
文本2 vs 文本3:
  文本2: 苹果是我最喜欢吃的水果
  文本3: 我喜欢用苹果手机
  余弦相似度: 0.7421
----------------------------------------
"""