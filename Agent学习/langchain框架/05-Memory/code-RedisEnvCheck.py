import os

try:
    import redis
except ModuleNotFoundError:
    print("❌ 未找到 redis 包，请先执行：pip install -r requirements.txt")
    raise SystemExit(1)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

print("✅ redis 包导入成功！")
print(f"✅ redis 包版本：{redis.__version__}")
print(f"正在连接 Redis：{REDIS_URL}")

client = None
try:
    client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
    print(f"✅ Redis 连接成功，PING -> {client.ping()}")
except (redis.ConnectionError, redis.TimeoutError, redis.ResponseError) as e:
    print("❌ Redis 连接失败")
    print(f"   REDIS_URL = {REDIS_URL}")
    print(f"   错误信息 = {e}")
    print("   如果你使用的是 Redis Stack 的 Docker 端口映射，可尝试：")
    print("   export REDIS_URL=redis://localhost:26379")
    raise SystemExit(1)
except Exception as e:
    print(f"❌ Redis 环境校验异常：{e}")
    raise SystemExit(1)
finally:
    if client is not None:
        client.close()