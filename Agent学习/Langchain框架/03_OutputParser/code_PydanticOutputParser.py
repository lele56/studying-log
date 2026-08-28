import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from loguru import logger
from pydantic import BaseModel, Field, field_validator

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

class Product(BaseModel):
    """产品信息：名称、类别、简介。简介长度需 ≥ 10，由下方 validator 校验。"""

    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        """Pydantic 校验器：description 长度必须 ≥ 10，否则抛 ValueError。"""
        if len(value) < 10:
            raise ValueError("产品简介长度必须大于等于10")
        return value

# 创建 Pydantic 输出解析器：解析结果会转成 Product 实例并做校验
parser = PydanticOutputParser(pydantic_object=Product)

# 生成「格式说明」字符串，拼进 Prompt，引导模型按 Product 的字段输出 JSON
format_instructions = parser.get_format_instructions()

# 在 system 里放入 {format_instructions}，human 里放 {topic}
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI助手，你只能输出结构化的json数据\n{format_instructions}"),
        ("human", "请你输出标题为：{topic}的新闻内容"),
    ]
)

# 填入变量，生成最终的提示消息列表
prompt = prompt_template.format_messages(
    topic="华为Mate X7", format_instructions=format_instructions
)
logger.info(prompt)

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

result = model.invoke(prompt)
logger.info(f"模型原始输出:\n{result.content}")

# 解析：把 result 转成 Product 实例，若格式或校验不通过会抛错
response = parser.invoke(result)
logger.info(f"解析后的结构化结果:\n{response}")
logger.info(f"结果类型: {type(response)}")  # <class 'Product'>


"""
【输出示例】
2026-08-21 17:52:33.945 | INFO     | __main__:<module>:47 - [SystemMessage(content='你是一个AI助手，你只能输出结构化的json数据\nThe output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {"properties": {"foo": {"title":"Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}\nthe object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{"description": "产品信息：名称、类别、简介。简介长度需 ≥ 10，由下方 validator 校验。", "properties": {"name": {"description": "产品名称", "title": "Name", "type": "string"}, "category": {"description": "产品类别", "title": "Category", "type": "string"}, "description": {"description": "产品简介", "title": "Description", "type": "string"}}, "required": ["name","category", "description"]}\n```', additional_kwargs={}, response_metadata={}), HumanMessage(content='请你输出标题为：华为Mate X7的新闻内容', additional_kwargs={}, response_metadata={})]
2026-08-21 17:52:46.995 | INFO     | __main__:<module>:58 - 模型原始输出:
{
  "name": "华为Mate X7",
  "category": "折叠屏智能手机",
  "description": "华为最新发布的Mate X7折叠屏手机，搭载了全新一代麒麟芯片与升级版玄武水滴铰链，机身更加轻薄，影像系统也迎来了全面跃升，为用户带来极致的科技体验。"
}
2026-08-21 17:52:46.997 | INFO     | __main__:<module>:62 - 解析后的结构化结果:
name='华为Mate X7' category='折叠屏智能手机' description='华为最新发布的Mate X7折叠屏手机，搭载了全新一代麒麟芯片与升级版玄武水滴铰链，机身更加轻薄，影像系统也迎来了全面跃升，为用户带来极致的科技体验。'
2026-08-21 17:52:46.997 | INFO     | __main__:<module>:63 - 结果类型: <class '__main__.Product'>
"""