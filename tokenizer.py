from token import Token
from type import Type
from utils import *


def string_end(code, index):
    s = ''
    offset = index
    escape_map = {
        '"': '"',
        'n': '\n',
        't': '\t',
        'r': '\r',
        '\\': '\\',
    }
    while offset < len(code):
        c = code[offset]
        if c == '"':
            # 找到了字符串的结尾
            # s = code[index:offset]
            return (s, offset)
        elif c == '\\':
            next_char = code[offset+1]
            # 处理转义符, 现在只支持 \"
            if next_char in escape_map.keys():
                s += escape_map[next_char]
                offset += 2
            else:
                # 这是一个错误, 非法转义符
                pass
        else:
            s += c
            offset += 1
    # 程序出错, 没有找到反引号 "
    pass


def number_end(code, i):
    end = 0
    for offset, char in enumerate(code[i:]):
        if not is_numeric(char):
            end = offset
            break
    n = code[i-1:i+end]
    return (n, end)


def keyword_end(code, i):
    end = 0
    keywords = ['true', 'false', 'null']
    for offset, char in enumerate(code[i:]):
        if not char.isalpha():
            end = offset
            break
    word = code[i-1:i+end]
    if word not in keywords:
        # error
        pass
    return (word, end)


def json_tokens(code):
    length = len(code)
    tokens = []
    spaces = '\n\t\r'
    # 当前下标
    i = 0
    while i < length:
        c = code[i]
        i += 1
        # 跳过空白符号
        if c in spaces:
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
        elif is_numeric(c):
            # 处理数字
            num, offset = number_end(code, i)
            i += offset
            t = Token(Type.number, num)
            tokens.append(t)
        elif c in 'tfn':
            # 处理 keyword
            keyword, offset = keyword_end(code, i)
            i += offset
            t = Token(Type.keyword, keyword)
            tokens.append(t)
        else:
            # 出错了
            pass
    return tokens
