# 1、形参双引号

```python
def create_default_state(**overrides) -> ImportGraphState:
    state = copy.deepcopy(GRAPH_DEFAULT_STATE)
    state.update(overrides)
    return state

# 调用
state = create_default_state(
	task_id="task_001",
	import_file_path="doc.pdf"
)

# 相当于在 create_default_state内部，先组装成一个字典。
overrides = {
    "task_id": "task_001",
    "import_file_path": "doc.pdf"
}
```

+ `**overrides` 是 Python 的可变关键字参数语法。
  + `**` 表示：收集任意数量的关键字参数，打包成一个字典。
  + `overrides` 只是变量名，可以换成任何名字，比如：`kwargs`

# 2、形参单引号

```python
def f(*args, **kwargs):
    print(args)    # 元组，收集位置参数
    print(kwargs)  # 字典，收集关键字参数
    
# 调用
f(1, 2, a=3, b=4)

# 结果
args   == (1, 2)
kwargs == {"a": 3, "b": 4}
```

+ `*args`：收集任意多个**位置参数**，得到元组。
+ `**kwargs` / `**overrides`：收集任意多个**关键字参数**，得到字典。

# 3、实参 双引号

```python
# 调用
create_default_state(**{"task_id": "task_001"})

# 这里的 ** 是“字典解包”，等价于：
create_default_state(task_id="task_001")
```

# 4、@abstractmethod 抽象函数

```python
from abc import ABC, abstractmethod

class BaseNode(ABC):

    @abstractmethod
    def process(self, state: T) -> T:
        pass
```

+ `@abstractmethod` 是 Python 中 `abc`（Abstract Base Class，抽象基类）模块提供的一个**装饰器**，用来声明“抽象方法”。
  + “抽象方法”就是**只声明、不实现**的方法。它表达一种契约：
  + 任何继承 `BaseNode` 的子类，都必须自己实现 `process` 方法。
+ `ABC`：类继承的抽象基类，配合 `@abstractmethod` 使用。
+ `@abstractmethod` 要生效，类必须继承 `ABC`。

# 5、核心容器类型

## 5.1 字典（Dict）

**定义**：键值对集合，键必须可哈希（不可变），Python 3.7+ 保持插入顺序。

```python
# ---- 定义 ----
d = {"a": 1, "b": 2}
d = dict(a=1, b=2)
d = dict([("a", 1), ("b", 2)])

# ---- 获取 ----
v = d["a"]                 # 1，键不存在会 KeyError
v = d.get("c")             # None，键不存在返回 None
v = d.get("c", 0)          # 0，可指定默认值
keys = list(d.keys())      # ['a', 'b']
vals = list(d.values())    # [1, 2]
items = list(d.items())    # [('a', 1), ('b', 2)]

# ---- 设置/更新 ----
d["c"] = 3                 # 新增或覆盖
d.update({"d": 4})         # 批量更新
d.setdefault("e", 5)       # 键不存在时设默认值
del d["a"]                 # 删除，不存在会 KeyError
d.pop("b", None)           # 安全删除

# ---- 其他常用 ----
"c" in d                   # 判断键是否存在
len(d)                     # 键值对数量
for k, v in d.items():     # 遍历
    pass
d1 | d2                    # 合并（3.9+，返回新字典）
d.clear()                  # 清空
```

## 5.2 对象（自定义类实例）

**定义**：由 `class` 定义的数据+行为封装体。属性本质上也存放在 `__dict__` 中。

```python
# ---- 定义 ----
class User:
    species = "human"                 # 类属性

    def __init__(self, name, age):
        self.name = name              # 实例属性
        self.age = age

    def greet(self):
        return f"hi, {self.name}"

u = User("Tom", 18)

# ---- 获取 ----
name = u.name                         # 'Tom'
name = getattr(u, "name")             # 'Tom'
name = getattr(u, "nickname", "无")   # '无'，安全获取
print(u.__dict__)                     # {'name': 'Tom', 'age': 18}

# ---- 设置 ----
u.age = 20                            # 直接赋值
setattr(u, "age", 21)                 # 等价写法
u.email = "tom@x.com"                 # 动态新增属性
del u.email                           # 删除属性

# ---- 其他常用 ----
u.greet()
hasattr(u, "name")                    # True
isinstance(u, User)                   # True
```

## 5.3 列表 list

**定义**：有序、可变的序列，元素可重复。

```python
# ---- 定义 ----
lst = [1, 2, 3]
lst = list((1, 2, 3))
lst = [i * 2 for i in range(3)]      # [0, 2, 4]

# ---- 获取 ----
lst[0]                    # 0
lst[-1]                   # 4，负索引
lst[0:2]                  # [0, 2]，切片
idx = lst.index(2)        # 元素下标
n = lst.count(2)          # 元素出现次数
len(lst)

# ---- 设置 ----
lst[0] = 10               # 按下标修改
lst[0:2] = [1, 2]         # 切片赋值，可改变长度
lst.append(99)            # 尾部追加
lst.insert(0, -1)         # 指定位置插入
lst.extend([7, 8])        # 批量追加
lst += [9]                # 等价于 extend

# ---- 删除 ----
lst.pop()                 # 弹出最后一个
lst.pop(0)                # 弹出指定位置
lst.remove(2)             # 删除第一个值为 2 的元素
del lst[0]                # 按下标删除
lst.clear()

# ---- 其他常用 ----
lst.sort()                # 原地排序
lst.sort(key=lambda x: -x)
lst.reverse()
sorted(lst)               # 返回新列表
2 in lst                  # 成员判断
[x for x in lst if x > 0] # 过滤
```

## 5.4 集合 set

**定义**：无序、可变、元素唯一，元素必须可哈希，常用于去重和集合运算。

```python
# ---- 定义 ----
s = {1, 2, 3}
s = set([1, 2, 3])
s = set("abc")            # {'a','b','c'}
empty = set()             # 注意：{} 是空字典，不是空集合

# ---- 获取 ----
1 in s                    # True
len(s)
list(s)                   # 转列表，但顺序不保证

# ---- 设置/更新 ----
s.add(4)                  # 添加
s.update({5, 6})          # 批量添加
s.remove(4)               # 删除，不存在 KeyError
s.discard(100)            # 删除，不存在不报错
s.pop()                   # 随机弹出一个
s.clear()

# ---- 集合运算 ----
a = {1, 2, 3}; b = {3, 4}
a | b                     # 并集 {1,2,3,4}
a & b                     # 交集 {3}
a - b                     # 差集 {1,2}
a ^ b                     # 对称差 {1,2,4}
a.union(b); a.intersection(b); a.difference(b)
a.issubset(b); a.issuperset(b); a.isdisjoint(b)

# ---- 常用场景 ----
list(set([1, 1, 2, 3]))   # 去重
```

## 5.5 元组 tuple

**定义**：有序、**不可变**序列，可哈希（元素都可哈希时可作 dict 键）。

```
# ---- 定义 ----
t = (1, 2, 3)
t = 1, 2, 3               # 括号可省
t = tuple([1, 2, 3])
one = (1,)                # 单元素必须带逗号
empty = ()

# ---- 获取 ----
t[0]                      # 1
t[-1]                     # 3
t[0:2]                    # (1, 2)，切片返回新元组
t.index(2)
t.count(2)
len(t)

# ---- "设置" ----
# 不可变，不能 t[0] = 10
# 只能重建：
t2 = t + (4,)             # 拼接
t3 = t[:1] + (10,) + t[2:]  # 修改某位
x, y, z = t               # 解包
first, *rest = t          # 星号解包

# ---- 常用 ----
hash(t)                   # 可哈希，可作 dict 键
d = {(1, 2): "point"}
```

## 5.6 数据类 dataclass

**定义**：`dataclasses` 提供的类装饰器，自动生成 `__init__`、`__repr__`、`__eq__` 等，适合“以数据为主”的对象。

**作用**：

+ 自动生成 `__init__`、`__repr__`、`__eq__` 等函数。
+ 安全的默认值
+ 转字典 / 嵌套结构

**函数&参数详解：**

+ `field` 是 `dataclasses` 模块提供的**函数**，用来给某个字段做精细配置。

+ `default_factory` 是 `field()` 的参数，值必须是**一个无参可调用对象**（函数/类）。

+ 每次创建实例时，调用这个工厂生成默认值。

+ `list` 是工厂函数，每次 `User()` 都会调用 `list()` 生成**新的空列表**。

+ ```python
  # 常见工厂写法
  @dataclass
  class Demo:
      a: list = field(default_factory=list)          # []
      b: dict = field(default_factory=dict)          # {}
      c: set  = field(default_factory=set)           # set()
      d: tuple = field(default_factory=tuple)        # ()
      e: list = field(default_factory=lambda: [0, 0]) # 自定义
      f: "Demo" = field(default_factory=lambda: Demo())
    
  ```

  

```python
from dataclasses import dataclass, field, asdict

# ---- 定义 ----
@dataclass
class User:
    # 不可变——>用 default：
    name: str
    age: int = 0
    pair: tuple = (0, 0)
    # 可变 ——>用 default_factory
    tags: list = field(default_factory=list)
  
u = User("Tom", 18)

# ---- 获取 ----
u.name                    # 'Tom'
u.age                     # 18
getattr(u, "age")         # 18

# ---- 设置 ----
u.age = 20
setattr(u, "age", 21)
u.tags.append("vip")

# ---- 常用 ----
asdict(u)                 # {'name':'Tom','age':21,'tags':['vip']}
u == User("Tom", 21)      # True，自动生成 __eq__
repr(u)                   # User(name='Tom', age=21, tags=['vip'])
# 不可变版本：
# @dataclass(frozen=True)
```



**为什么不直接写 `tags: list = []`？**

```python
@dataclass
class A:
    tags: list = []       # ❌ ValueError: mutable default ...
    

# dataclass 会直接报错，因为可变默认值在 Python 里是危险共享：
class B:
    def __init__(self, tags=[]):
        self.tags = tags

b1 = B(); b2 = B()
b1.tags.append("x")
print(b2.tags)    # ['x'] ❌ 共享了同一个 list


# default_factory 保证每个实例拿到独立的新对象：
@dataclass
class A:
    tags: list = field(default_factory=list)

a1 = A(); a2 = A()
a1.tags.append("x")
print(a2.tags)    # [] ✅ 独立
```

## 5.7 枚举 Enum

**定义**：`enum` 模块，定义一组命名常量的类型，成员唯一、可迭代。

```python
from enum import Enum, IntEnum, auto

# ---- 定义 ----
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = auto()          # 自动赋值 3

class Status(IntEnum):     # 可与 int 比较
    OK = 200
    NG = 500

# ---- 获取 ----
Color.RED                  # 成员
Color.RED.value            # 1
Color.RED.name             # 'RED'
Color(1)                   # Color.RED，按值取
Color["RED"]               # Color.RED，按名取
list(Color)                # 所有成员

# ---- "设置" ----
# 枚举成员不可修改
# Color.RED.value = 10    # 报错

# ---- 常用 ----
Color.RED is Color.RED     # True，单例
Status.OK == 200           # True（IntEnum）
for c in Color: ...
```

# 6、字符串字面量前缀

```python
# r = raw string（原始字符串）
# 作用：关闭转义字符，反斜杠 \ 不再有特殊含义，原样保留。
a = r"D:\test"

# f = f-string（格式化字符串，Python 3.6+）
# 作用：在字符串里用 {} 嵌入表达式，运行时求值并格式化。
b = f"name={name}"    # 格式化字符串

# b = bytes 字面量
# 作用：生成 bytes 对象（二进制），而不是 str。常用于：网络传输、文件二进制读写
data = b"\x00\x01\x02"
with open("a.bin", "wb") as f:
    f.write(data)
```

# 7、Python 标准库模块

## 7.1 `json`标准库

它提供两组核心函数：

- `json.dumps(...)`：Python 对象 → JSON 字符串（**d**ump **s**tring）
- `json.loads(...)`：JSON 字符串 → Python 对象（**l**oad **s**tring）

还有：

- `json.dump(...)`：Python 对象 → 写入文件
- `json.load(...)`：从文件读取 → Python 对象

注意 `json` 是模块名，`dumps` 是模块里的函数，用 `.` 调用。

```python
import json

# 参数1：Python 对象
data = {"name": "Tom", "age": 18}
s = json.dumps(data)
print(s)          # '{"name": "Tom", "age": 18}'
print(type(s))    # <class 'str'>

# 参数2：indent，控制缩进。
data = {"a": 1, "b": {"c": 2}}
print(json.dumps(data))
# {"a": 1, "b": {"c": 2}}
print(json.dumps(data, indent=2))
# {
#   "a": 1,
#   "b": {
#     "c": 2
#   }
# }

# 参数3：ensure_ascii=False。控制非 ASCII 字符（如中文）是否转义。
# ensure_ascii=True（默认）：所有非 ASCII 字符转成 \uXXXX 转义形式。
# ensure_ascii=False：保留原字符，中文正常显示。
data = {"name": "张三"}
print(json.dumps(data))
# {"name": "\u5f20\u4e09"}          ← 默认转义，中文变乱码样
print(json.dumps(data, ensure_ascii=False))
# {"name": "张三"}                  ← 中文正常

```

