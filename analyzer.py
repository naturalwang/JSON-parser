from Type import Type
from Token import Token
from utils import *


def value_of_token(token):
    if token.type == Type.string:
        value = str(token.value)
    elif token.type == Type.number:
        value = int(token.value)
    elif token.type == Type.null:
        value = None
    elif token.type == Type.boolean:
        if token.value == 'true':
            value = True
        else:
            value = False
    else:
        # error
        pass
    return value


def parse_json_array(tokens):
    result = []
    ts = tokens[1:-1]
    cursor = 0
    elements = [Type.colon, Type.comma]
    for i, token in enumerate(ts):
        if i <= cursor or token.type in elements:
            if i != 0:
                continue
        # 找到对应的值
        if token.type == Type.braceLeft:
            cursor = i
            while ts[cursor].type != Type.braceRight:
                cursor += 1
            cursor += 1
            value = parse_json_dict(ts[i:cursor+1])
        elif token.type == Type.bracketLeft:
            cursor = i
            while ts[cursor].type != Type.bracketRight:
                cursor += 1
            cursor += 1
            value = parse_json_array(ts[i:cursor+1])
        else:
            value = value_of_token(token)
        result.append(value)
    return result


def parse_json_dict(tokens):
    result = {}
    ts = tokens[1:-1]
    cursor = 0
    elements = [Type.colon, Type.comma]
    #
    key, value = None, None
    for i, token in enumerate(ts):
        if i <= cursor or token.type in elements:
            if i != 0:
                continue
        if key is None:
            # 处理字符串作为 key 的情况
            if token.type == Type.string:
                key = token.value
            cursor = i
        else:
            # 已经有 key, 找对应的值
            if token.type == Type.braceLeft:
                # 处理对象
                cursor = i
                while ts[cursor].type != Type.braceRight:
                    cursor += 1
                cursor += 1
                value = parse_json_dict(ts[i:cursor+1])
            elif token.type == Type.bracketLeft:
                # 处理数组
                cursor = i
                while ts[cursor].type != Type.bracketRight:
                    cursor += 1
                cursor += 1
                value = parse_json_array(ts[i:cursor+1])
            else:
                value = value_of_token(token)
            result[key] = value
            key, value = None, None
    return result


def parsed_json(tokens):
    """
    tokens 是一个包含各种 JSON token 的数组（ json_tokens 的返回值）
    返回解析后的字典
    """
    # 数组形式的 json 数据
    if tokens[0].type == Type.bracketLeft:
        return parse_json_array(tokens)
    # 字典形式的 json 数据
    elif tokens[0].type == Type.braceLeft:
        return parse_json_dict(tokens)
    else:
        log('json 数据格式不合法')
        return None
