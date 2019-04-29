from utils import *
from token import Token
from type import Type


def get_tokens_offset(tokens):
    stack = []
    offset = 0
    for token in tokens:
        offset += 1
        if token.type in [Type.bracketLeft, Type.braceLeft]:
            stack.append(token)
        elif token.type in [Type.bracketRight, Type.braceRight]:
            stack.pop(-1)
            if is_empty(stack):
                return offset + 1
        else:
            pass
    # error
    return None


def parse_dict(tokens):
    obj = {}
    ts = tokens[1:-1]
    pair = []
    signs = [Type.comma, Type.colon]
    cursor = 0
    for i, token in enumerate(ts):
        if i < cursor:
            continue
        if token.type in signs:
            cursor += 1
            continue
        #
        if is_empty(pair):
            # key 不能是 list 或 dict
            pair.append(token)
            continue
        elif len(pair) == 1:
            if token.type == Type.bracketLeft:
                # 处理数组
                offset = get_tokens_offset(ts[i:])
                value = parse_array(ts[i:i+offset])
                key = pair[0].valueByType()
                obj[key] = value
                cursor += offset
            elif token.type == Type.braceLeft:
                # 处理对象
                offset = get_tokens_offset(ts[i:])
                value = parse_dict(ts[i:i+offset])
                key = pair[0].valueByType()
                obj[key] = value
                cursor += offset
            else:
                key = pair[0].valueByType()
                obj[key] = token.valueByType()
                cursor += 1
            pair = []
    return obj


def parse_array(tokens):
    array = []
    ts = tokens[1:-1]
    signs = [Type.colon, Type.comma]
    cursor = 0
    for i, token in enumerate(ts):
        if token.type in signs:
            cursor += 1
            continue
        if i < cursor:
            continue
        #
        if token.type == Type.bracketLeft:
            offset = get_tokens_offset(ts[i:])
            value = parse_array(ts[i:i+offset])
            array.append(value)
            cursor += offset
        elif token.type == Type.braceLeft:
            offset = get_tokens_offset(ts[i:])
            value = parse_dict(ts[i:i+offset])
            array.append(value)
            cursor += offset
        else:
            array.append(token.valueByType())
            cursor += 1
    return array


def parsed_json(tokens):
    value = None
    if tokens[0].type == Type.braceLeft:
        value = parse_dict(tokens)
    elif tokens[0].type == Type.bracketLeft:
        value = parse_array(tokens)
    else:
        pass
    return value
