from langchain.chat_models import init_chat_model
import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import CharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from dotenv import load_dotenv

load_dotenv()

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 初始化模型
llm = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 提示词模板：{context} 由检索器填充，{question} 由用户输入填充；最终会生成一段字符串 Prompt 再交给聊天模型
prompt_template = """
    请使用以下提供的文本内容来回答问题。仅使用提供的文本信息，
    如果文本中没有相关信息，请回答"抱歉，提供的文本中没有这个信息"。

    文本内容：
    {context}

    问题：{question}

    回答：
    "
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"],
)

# 嵌入模型：用于文档与查询的向量化
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3", 
    dashscope_api_key=api_key
)

# 加载 docx
loader = Docx2txtLoader("document_sample/alibaba-more.docx")
documents = loader.load()

# 分割（此处用 CharacterTextSplitter 便于快速跑通；真实项目里更常见的通用首选是 RecursiveCharacterTextSplitter）
text_splitter = CharacterTextSplitter(
    chunk_size=1000, chunk_overlap=0, length_function=len
)
texts = text_splitter.split_documents(documents)

print(f"文档个数:{len(texts)}")

# 向量化并写入 Redis，建立索引（必须用分割后的 texts，否则整篇文档作为一块）
vector_store = Redis.from_documents(
    documents=texts,
    embedding=embeddings,
    redis_url="redis://localhost:6379",
    index_name="my_index3",
)

# 检索器：按相似度取前 k 条作为 context
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# LCEL 链：输入 question → context 由 retriever 查得，question 直通 → 拼 prompt → 调 llm
rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# 提问并打印答案（有 RAG：从知识库检索）；未接输出解析器时，聊天模型返回的是 AIMessage，正文通常通过 .content 读取
question = "00000和A0001分别是什么意思"
result = rag_chain.invoke(question)
print("\n=== 有外挂知识库 ===")
print("问题:", question)
print("回答:", result.content)

# 对比演示：同一问题但「无外挂知识库」（context 为空，不查向量库，模拟未挂载文档）
no_rag_chain = (
    {
        "context": lambda _: "（未提供相关文档，模拟无外挂知识库）",
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
)
result_no_rag = no_rag_chain.invoke(question)
print("\n=== 无外挂知识库（模拟：不检索，仅靠模型自身知识）===")
print("问题:", question)
print("回答:", result_no_rag.content)

# === 有外挂知识库（RAG：从 alibaba-more.docx 检索）===
# 问题: 00000和A0001分别是什么意思
# 回答: 00000 的意思是“一切 ok”，表示正确执行后的返回；
# A0001 的意思是“用户端错误”，属于一级宏观错误码。

# === 无外挂知识库（模拟：不检索，仅靠模型自身知识）===
# 问题: 00000和A0001分别是什么意思
# 回答: 抱歉，提供的文本中没有这个信息