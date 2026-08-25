from langchain_core.tools import tool
from loguru import logger
from pydantic import BaseModel, Field

# Pydantic 模型：定义“工具参数接口”，字段 description 会进入工具参数 schema
class FieldInfo(BaseModel):
    """定义加法运算所需的参数结构"""

    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")

# args_schema=FieldInfo：把参数模型绑定到工具，模型会更清楚看到 a、b 的类型与说明
@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    """计算两个整数之和"""
    return a + b

# 打印工具属性：带 args_schema 时，args 中会包含 Field 的 description
logger.info(f"name = {add_number.name}")
logger.info(f"args = {add_number.args}")
logger.info(f"description = {add_number.description}")
logger.info(f"return_direct = {add_number.return_direct}")

# 调用工具：传入字典，Pydantic 会做类型校验与转换
res = add_number.invoke({"a": 1, "b": 2})
logger.info(res)

"""
【输出示例】
2026-08-25 16:00:56.435 | INFO     | __main__:<module>:19 - name = add_number
2026-08-25 16:00:56.436 | INFO     | __main__:<module>:20 - args = {'a': {'description': '第1个参数', 'title': 'A', 'type': 'integer'}, 'b': {'description': '第2个参数', 'title': 'B', 'type': 'integer'}}
2026-08-25 16:00:56.436 | INFO     | __main__:<module>:21 - description = 计算两个整数之和
2026-08-25 16:00:56.437 | INFO     | __main__:<module>:22 - return_direct = False
2026-08-25 16:00:56.520 | INFO     | __main__:<module>:26 - 3
"""