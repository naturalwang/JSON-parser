from enum import Enum


class Type(Enum):
    auto = 0            # auto 就是 6 个单字符符号, 用来方便写代码的
    colon = 1           # :
    comma = 2           # ,
    braceLeft = 3       # {
    braceRight = 4      # }
    bracketLeft = 5     # [
    bracketRight = 6    # ]
    number = 7          # 169
    string = 8          # "name"
    keyword = 9         # true / false / null
