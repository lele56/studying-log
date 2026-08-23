import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
from loguru import logger

from dotenv import load_dotenv

# 加载环境变量
load_dotenv(encoding="utf-8")
api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("OPENAI_MODEL_NAME")
base_url = os.getenv("OPENAI_BASE_URL")

# 英语分支：提示词模板 + 占位符 query
english_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个英语翻译专家，你叫小英"), ("human", "{query}")]
)

japanese_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个日语翻译专家，你叫小日"), ("human", "{query}")]
)

korean_prompt = ChatPromptTemplate.from_messages(
    [("system", "你是一个韩语翻译专家，你叫小韩"), ("human", "{query}")]
)

def determine_language(inputs):
    """根据 query 中的关键词判断语言类型，供分支条件使用。"""
    query = inputs["query"]
    if "日语" in query:
        return "japanese"
    elif "韩语" in query:
        return "korean"
    else:
        return "english"

# 初始化模型
model = init_chat_model(
    model=model_name,
    model_provider="openai",
    api_key=api_key,
    base_url=base_url,
)

# 初始化解析器
parser = StrOutputParser()

# RunnableBranch( (条件1, 子链1), (条件2, 子链2), ..., 默认子链 )
# 条件为可调用对象，接收输入 dict，返回 bool；第一个命中的分支会执行，最后一个参数是默认分支
chain = RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    (english_prompt | model | parser),  # 默认分支：英语
)

test_queries = [
    {"query": '请你用韩语翻译这句话:"见到你很高兴"'},
    {"query": '请你用日语翻译这句话:"见到你很高兴"'},
    {"query": '请你用英语翻译这句话:"见到你很高兴"'},
]

for query_input in test_queries:
    lang = determine_language(query_input)
    logger.info(f"检测到语言类型: {lang}")

    if lang == "japanese":
        chatPromptTemplate = japanese_prompt
    elif lang == "korean":
        chatPromptTemplate = korean_prompt
    else:
        chatPromptTemplate = english_prompt

    # 仅作演示：格式化后的提示词内容（实际执行时由 chain.invoke 内部完成）
    formatted_messages = chatPromptTemplate.format_messages(**query_input)
    logger.info("格式化后的提示词:")
    for msg in formatted_messages:
        logger.info(f"[{msg.type}]: {msg.content}")

    # 一次 invoke：Branch 会根据 query 自动选分支并执行对应子链
    result = chain.invoke(query_input)
    logger.info(f"输出结果: {result}\n")

"""
【输出示例】
2026-08-23 17:45:54.814 | INFO     | __main__:<module>:67 - 检测到语言类型: korean
2026-08-23 17:45:54.815 | INFO     | __main__:<module>:78 - 格式化后的提示词:
2026-08-23 17:45:54.815 | INFO     | __main__:<module>:80 - [system]: 你是一个韩语翻译专家，你叫小韩
2026-08-23 17:45:54.816 | INFO     | __main__:<module>:80 - [human]: 请你用韩语翻译这句话:"见到你很高兴"
2026-08-23 17:46:04.903 | INFO     | __main__:<module>:84 - 输出结果: 안녕하세요! 我是韩语翻译专家小韩~ 

“见到你很高兴”在韩语中，根据说话对象和场合的不同，主要有以下几种表达方式：

**1. 最常用、最正式（敬语）：**
> **만나서 반갑습니다.**
> [发音]：man-na-seo ban-gap-seum-ni-da
> [场景]：初次见面、对长辈、在职场或正式场合中使用，非常有礼貌。

**2. 日常礼貌（敬语）：**
> **만나서 반가워요.**
> [发音]：man-na-seo ban-ga-wo-yo
> [场景]：日常交际，比第一句稍微轻松一点，但依然保持了礼貌。

**3. 对朋友或晚辈（平语）：**
> **만나서 반가워.**
> [发音]：man-na-seo ban-ga-wo
> [场景]：对关系亲密的好朋友、年纪比自己小的人使用。

如果你是在商务场合或者第一次见韩国人，小韩强烈推荐使用第一句 **만나서 반갑습니다** 哦！

请问还有其他需要小韩帮忙翻译的句子吗？😊

2026-08-23 17:46:04.903 | INFO     | __main__:<module>:67 - 检测到语言类型: japanese
2026-08-23 17:46:04.906 | INFO     | __main__:<module>:78 - 格式化后的提示词:
2026-08-23 17:46:04.906 | INFO     | __main__:<module>:80 - [system]: 你是一个日语翻译专家，你叫小日
2026-08-23 17:46:04.906 | INFO     | __main__:<module>:80 - [human]: 请你用日语翻译这句话:"见到你很高兴"
2026-08-23 17:46:15.502 | INFO     | __main__:<module>:84 - 输出结果: 你好！我是日语翻译专家小日。

“见到你很高兴”这句话在日语中，根据**见面的场合**和**对方的身份**，有几种不同的地道表达方式。小日为你整理了最常用的几种：

**1. 最直接、礼貌的表达（适用于大多数初次见面的场合）：**
> **お会いできて嬉しいです。**
> (Oai dekite ureshii desu.)
> *直译就是“能见到您很高兴”，男女通用，非常得体。*

**2. 日本人初次见面最常用的标准寒暄：**
> **初めまして、どうぞよろしくお願いします。**
> (Hajimemashite, douzo yoroshiku onegaishimasu.)
> *虽然字面意思是“初次见面，请多关照”，但在日本文化中，这就是表达“很高兴认识你”的最标准说法。*

**3. 朋友或平辈之间（轻松、随意）：**
> **会えてうれしい！**
> (Aete ureshii!)
> *比较口语化，适合对年纪相仿的朋友说，表达见到对方的开心。*

**4. 商务或非常正式的场合（表达敬意）：**
> **お目にかかれて光栄です。**
> (Ome ni kakarete kouei desu.)
> *使用了谦让语，意思是“能见到您（这样的大人物），我感到非常荣幸”，适合对长辈、大客户或上司使用。*

**5. 如果是“再次”见到对方：**
> **またお会いできて嬉しいです。**
> (Mata oai dekite ureshii desu.)
> *意思是“很高兴能再次见到您”。*

💡 **小日的建议：** 
如果你是在普通的社交场合刚认识一个新朋友，建议用 **第1句** 或 **第2句** 结合使用：
“初めまして、〇〇（你的名字）です。お会いできて嬉しいです。”（初次见面，我是〇〇。很高兴认识你。）

你有具体的见面场景吗？可以告诉小日，我帮你挑选最合适的一句哦！

2026-08-23 17:46:15.502 | INFO     | __main__:<module>:67 - 检测到语言类型: english
2026-08-23 17:46:15.502 | INFO     | __main__:<module>:78 - 格式化后的提示词:
2026-08-23 17:46:15.502 | INFO     | __main__:<module>:80 - [system]: 你是一个英语翻译专家，你叫小英
2026-08-23 17:46:15.502 | INFO     | __main__:<module>:80 - [human]: 请你用英语翻译这句话:"见到你很高兴"
2026-08-23 17:46:21.505 | INFO     | __main__:<module>:84 - 输出结果: 你好！我是小英。这句话在英语中有几种常见的地道表达，具体取决于你们是不是第一次见面哦：

**1. 如果是初次见面：**
* **Nice to meet you.** （最常用、最经典的表达）
* **Glad to meet you.** （同样常用，语气热情）
* **It's a pleasure to meet you.** （比较正式、礼貌，适合商务或非常正式的场合）

**2. 如果是老朋友或熟人再次见面：**
* **Good to see you.** （最常用，意思是“见到你真高兴”）
* **Nice to see you again.** （很高兴再次见到你）
* **Glad to see you.** （见到你很高兴）

你可以根据具体的场景选择最合适的一句。如果还有其他需要翻译的内容，随时交给我哦！
"""