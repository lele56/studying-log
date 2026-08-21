from langchain_core.prompts import PromptTemplate
from datetime import datetime
import time

# ---------- PromptTemplate 创建 ----------
# 用 from_template 方法创建 PromptTemplate 对象,自动解析模板中的变量名
template = PromptTemplate.from_template(
    "你是一个专业的{role}工程师，请回答我的问题给出回答，我的问题是：{question}"
)

# format 填入变量，最终生成提示字符串
prompt = template.format(role="前端工程师", question="你好")
print(prompt)
print("\n\n")

# ---------- PromptTemplate 拼接 ----------
prompt_a = PromptTemplate.from_template("你是一个专业的{role}工程师，")
prompt_b = PromptTemplate.from_template("请回答我的问题给出回答，我的问题是：{question}")

# 拼接多个 PromptTemplate 对象
prompt_all = prompt_a + prompt_b
prompt2 = prompt_all.format(role="前端工程师", question="你好")


# ---------- PromptTemplate 部分填入 ----------
template2 = PromptTemplate.from_template(
    "现在时间是：{time},请对我的问题给出答案，我的问题是：{question}"
)

# 使用 partial 方法部分填入变量，返回一个新的 PromptTemplate 对象
partial = template2.partial(time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
prompt2 = partial.format(question="今天是几号？")
print(prompt2)