import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

from langchain.chat_models import init_chat_model
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

import redis
from loguru import logger

try:
    from langchain_redis import RedisChatMessageHistory

    USE_LANGCHAIN_REDIS = True
except ModuleNotFoundError:
    from langchain_community.chat_message_histories import RedisChatMessageHistory

    USE_LANGCHAIN_REDIS = False

# 支持环境变量 REDIS_URL；未设置时默认 localhost:6379（标准 Redis），教程 Docker 可能用 26379
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
FORCE_SAVE = os.getenv("REDIS_FORCE_SAVE", "0") == "1"

def _check_redis():
    """启动时检查 Redis 是否可达，不可达时给出明确提示后退出。"""
    try:
        r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
        r.ping()
        r.close()
    except (redis.ConnectionError, redis.ResponseError) as e:
        logger.error(
            "Redis 连接失败（{}）。请先启动 Redis，例如：\n"
            "  docker run -d -p 6379:6379 redis\n"
            "若使用其他端口，可设置环境变量：REDIS_URL=redis://localhost:端口",
            REDIS_URL,
        )
        raise SystemExit(1) from e

_check_redis()

# 原生 Redis 客户端，decode_responses=True 使返回值为 str 而非 bytes
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
logger.info(
    "Redis 历史实现：{} | REDIS_URL={}",
    "langchain-redis" if USE_LANGCHAIN_REDIS else "langchain-community（兼容回退）",
    REDIS_URL,
)

# 初始化模型
llm = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 初始化提示模板
prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder("history"), ("human", "{question}")]
)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """为每个 session_id 创建/返回对应的 Redis 历史实例，实现持久化存储"""
    if USE_LANGCHAIN_REDIS:
        return RedisChatMessageHistory(
            session_id=session_id,
            redis_url=REDIS_URL,
        )
    return RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
    )

# 初始化 RunnableWithMessageHistory
chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)
config = RunnableConfig(configurable={"session_id": "user-001"})

print("开始对话（输入 'quit' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ["quit", "exit", "q"]:
        break
    response = chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response.content}")
    # 可选：把 Redis 当前内存快照刷到磁盘，方便演示“Redis 重启后仍能恢复”。
    # 这不是多轮记忆生效的必要条件，真实项目也不建议在每轮对话后都手动 SAVE。
    if FORCE_SAVE:
        redis_client.save()

"""
【输出示例】
开始对话（输入 'quit' 退出）

输入问题：你好，我叫彭于晏
2026-08-24 17:17:16.414 | INFO     | __main__:<module>:97 - AI回答:你好，彭于晏！失敬失敬！请问是那个拥有八块腹肌、会弹吉他、还会骑行的彭于晏吗？😎

很高兴认识你！今天有什么我可以帮你的吗？不管是聊天解闷、写文章、出谋划策还是查资料，随时吩咐！

输入问题：我叫什么
2026-08-24 17:17:26.912 | INFO     | __main__:<module>:97 - AI回答:你叫彭于晏呀！刚才不是才自我介绍过嘛，难道是想让我再夸你一次？😎

输入问题：redis-cli -h 127.0.0.1 -p 6379 PING
2026-08-24 17:18:00.293 | INFO     | __main__:<module>:97 - AI回答:如果 Redis 服务正常运行，这个命令在终端里的输出结果会是：

```text
PONG
```

**命令简单解析：**
* `redis-cli`：启动 Redis 的命令行客户端工具。
* `-h 127.0.0.1`：指定连接的主机 IP 为本地（127.0.0.1 等同于 localhost）。
* `-p 6379`：指定连接的端口为 Redis 的默认端口 6379。
* `PING`：向 Redis 服务器发送一个心跳测试指令，用来检查服务是否存活。

---

**如果你执行后没有看到 `PONG`，可能是遇到了以下情况：**

1. **返回 `Connection refused` (连接被拒绝)**
   * **原因**：Redis 服务没有启动，或者监听的 IP/端口不对。
   * **解决**：检查 Redis 服务是否已启动（如 `systemctl status redis` 或 `ps -ef | grep redis`）。

2. **返回 `NOAUTH Authentication required` (需要认证)**
   * **原因**：你的 Redis 配置了密码（`requirepass`）。
   * **解决**：在命令中加上 `-a` 参数指定密码，例如：
     `redis-cli -h 127.0.0.1 -p 6379 -a 你的密码 PING`

3. **进入交互模式而不是直接返回 PONG**
   * **原因**：如果你只输入了 `redis-cli -h 127.0.0.1 -p 6379` 而没有带 `PING`，就会进入 `127.0.0.1:6379>` 的交互界面，这时你需要手动输入 `PING` 并回车。

彭大明星，你是在本地调试 Redis 遇到什么报错了吗？如果有问题随时发给我看看！😎
"""