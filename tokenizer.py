from Type import Type
from Token import Token
from utils import *


def string_end(code, index):
    """
    code = "abc"
    index = 1
    """
    escape = 'ntr'
    escape_map = {
        'n': '\n',
        't': '\t',
        'r': '\r',
    }
    s = ''
    offset = index
    while offset < len(code):
        c = code[offset]
        if c == '"':
            # 找到了字符串的结尾
            # s = code[index:offset]
            return (s, offset)
        elif c == '\\':
            # 处理转义符, 现在只支持 \"
            escaped = code[offset+1]
            if escaped == '"':
                s += '"'
                offset += 2
            elif escaped in escape:
                s += escape_map[escaped]
                offset += 2
            else:
                # 这是一个错误, 非法转义符
                pass
        else:
            s += c
            offset += 1
    # 程序出错, 没有找到反引号 "
    pass


def json_tokens(code):
    """
    返回解析后的 Token 列表
    """
    length = len(code)
    tokens = []
    spaces = '\n\t\r '
    digits = '1234567890'
    # 当前下标
    i = 0
    while i < length:
        # 先看看当前应该处理啥
        c = code[i]
        i += 1
        if c in spaces:
            # 空白符号要跳过, space tab return
            continue
        elif c in ':,{}[]':
            # 处理 6 种单个符号
            t = Token(Type.auto, c)
            tokens.append(t)
        elif c == '"':
            # 处理字符串
            s, offset = string_end(code, i)
            i = offset + 1
            # print('i, offset', i, offset, s, code[offset])
            t = Token(Type.string, s)
            tokens.append(t)
        elif c in digits:
            # 处理数字, 现在不支持小数和负数
            end = 0
            for offset, char in enumerate(code[i:]):
                if char not in digits:
                    end = offset
                    break
            n = code[i-1:i+end]
            i += end
            t = Token(Type.number, n)
            tokens.append(t)
        elif c in 'tfn':
            # 处理 true false null 关键字
            if c == 't' and code[i-1:i+3] == 'true':
                t = Token(Type.boolean, 'true')
                i += 3
            elif c == 'f' and code[i-1:i+4] == 'false':
                t = Token(Type.boolean, 'false')
                i += 4
            elif c == 'n' and code[i-1:i+3] == 'null':
                t = Token(Type.null, 'null')
                i += 3
            tokens.append(t)
        else:
            # 出错了
            pass
    return tokens
