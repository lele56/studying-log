from pydantic import BaseModel, ValidationError, StrictInt

# 继承 BaseModel：实例化时按类型注解校验，不合规则抛出 ValidationError
class User(BaseModel):
    # id: int  # 普通 int 时，传入 "41" 会被自动转成 41
    id: StrictInt  # 严格整数：不接受字符串等，必须已是 int，否则报错
    name: str
    age: int = 0  # 可选字段，默认 0；传入值会被校验并转换

try:
    # 合法：id=42 为 int，实例化成功
    u = User(id=42, name="z3")
except ValidationError as e:
    print(e)
print(u.id, type(u.id))  # 42 <class 'int'>

print()
print()

# 非法：id="abc" 不是 int，StrictInt 不做模糊转换，直接抛出 ValidationError
try:
    User(id="abc", name="Bob")
except ValidationError as e:
    print(e)


"""
【输出示例】
42 <class 'int'>


1 validation error for User
id
  Input should be a valid integer [type=int_type, input_value='abc', input_type=str]
    For further information visit https://errors.pydantic.dev/2.12/v/int_type
"""