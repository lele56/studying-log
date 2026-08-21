# LangChain 框架学习

## 📅 学习信息
- **日期**: 2026-08-21
- **主题**: LangChain 框架基础 - OutputParser
- **目标**: 理解 LangChain 框架中 StrOutputParser 类、JsonOutputParser 类和 PydanticOutputParser 类的基本使用

## 📚 核心知识点

### 1. StrOutputParser 类、JsonOutputParser 类和 PydanticOutputParser 类是什么？
- 将模型输出变成不同类别的输出，方便后续处理。

### 2. 关键概念
- **StrOutputParser**: 提取模型回复中的 content 字段，将其转换成 str 类型。
- **JsonOutputParser**: 将模型回复变成 JSON 格式。
- **PydanticOutputParser**: 借助 Pydantic 模型，对模型输出进行结构化解析。
- **Pydantic**: 用于定义数据类，有数据检验的功能。
- **TypedDict**：用于定义数据类，但没有数据校验功能。

### 3. 重要函数
- `get_format_instructions`: 将输出要求转换成格式说明，拼接到 Prompt 中。
- `with_structured_output`: 省去创建 parser 过程，直接让模型输出相关格式。
- `Field`: 定义 Pydantic 字段，可添加 `description` 描述（会传给 LLM 作为生成指引）

## 💻 代码示例

### 示例 1: StrOutputParser
```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
result = parser.invoke(ai_message)  # 返回字符串
```

### 示例 2: JsonOutputParser
```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()
result = parser.invoke(ai_message)  # 返回字典
```

### 示例 3: PydanticOutputParser
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Product(BaseModel):
    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")

parser = PydanticOutputParser(pydantic_object=Product)
format_instructions = parser.get_format_instructions()
result = parser.invoke(ai_message)  # 返回 Product 对象
```

### 示例 4: with_structured_output（推荐）
```python
model = model.with_structured_output(Product)
result = model.invoke("生成产品信息")  # 直接返回 Product 对象
```



## 🐛 问题与思考

### Q1: 为什么“模型输出了 JSON”不等于“程序可以放心使用”？
**答**: JSON 语法正确只是第一步，字段是否齐全、类型是否正确、值是否符合业务规则还需要校验。解析解决“能读”，校验解决“能不能信”。

### Q2: 什么时候 StrOutputParser 就够了，什么时候应该上 Pydantic？
**答**: 当只需要纯文本展示时，字符串解析足够了；结果要进入数据库、接口、流程分支或自动执行时，应考虑 Pydantic 这类强校验。越靠近业务动作，越不能只靠自然语言。

### Q3: Structured Output 和 Output Parser 的关系应该怎么理解？
**答**: Structured Output 更偏让模型按结构生成，Parser 更偏在输出后解析和转换。两者可以配合使用：前面约束生成，后面兜底解析和校验。

### Q4: TypedDict、Pydantic、JSON Schema 的选择取决于什么？
**答**: TypedDict 适合轻量类型说明，Pydantic 适合 Python 内部强校验和错误提示，JSON Schema 适合跨语言、接口协议或外部系统对齐。不是越重越好，要看边界在哪里。

## 📝 学习总结

### 输出解析器的作用
输出解析器是 Model I/O 里的 Parse 环节，负责把模型输出转成程序可直接使用的数据。
- `StrOutputParser` 适合纯文本场景
- `JsonOutputParser` 适合快速得到 dict
- `PydanticOutputParser` 适合强类型、强校验场景

### 结构化输出
结构化输出是本章真正的重点。LangChain 官方常见的三种 schema 方式是：
- `TypedDict`: 适合描述结构，无校验
- `Pydantic`: 适合描述结构并做运行时校验
- `Annotated`: 主要用于补充字段说明，本身不是校验器
- `JSON Schema`: 适合跨语言、接口协议对齐