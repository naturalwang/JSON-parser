from tokenizer import json_tokens
from analyzer import parsed_json
from utils import *


def test_json_tokens():
    # 测试转义符号
    data1 = '{"na\\tme": "gua","hei\\ngh\\\"t": 169}'
    tokens1 = ["{", "na\tme", ":", "gua", ",", "hei\ngh\"t", ":", "169", "}"]
    values1 = [t.value for t in json_tokens(data1)]
    ensure(values1 == tokens1, 'json_tokens test 1')
    # 测试嵌套
    data2 = '{"data": 1,{"key": [1, 2]}}'
    tokens2 = ["{", "data", ":", "1", ",", "{", "key", ":", "[", "1", ",", "2", "]", "}", "}"]
    values2 = [t.value for t in json_tokens(data2)]
    ensure(values2 == tokens2, 'json_tokens test 2')
    # 测试 true false null
    data3 = '{"data": 1,{"key": [true, false, null]}}'
    tokens3 = ["{", "data", ":", "1", ",", "{", "key", ":", "[", "true", ",", "false", ",", "null", "]", "}", "}"]
    values3 = [t.value for t in json_tokens(data3)]
    ensure(values3 == tokens3, 'json_tokens test 3')


def test_parsed_json():
    # 测试 true false null 关键字和 \r\t\n 转移符
    json1 = {"na\tme": "gua", "hei\rgh\nt": 169}
    data1 = '{"na\\tme": "gua","hei\\rgh\\nt": 169}'
    tokenList1 = json_tokens(data1)
    result1 = parsed_json(tokenList1)
    ensure(dict_equal(result1, json1), 'parsed_json test 1')
    # 测试 true false null
    json2 = {"data": True, 'gua': {"key": [False, None]}}
    data2 = '{"data": true, "gua": {"key": [false, null]}}'
    tokenList2 = json_tokens(data2)
    result2 = parsed_json(tokenList2)
    ensure(dict_equal(result2, json2), 'parsed_json test 2')
    # 测试嵌套
    json3 = {
        'juzi': {
            'guagua': {
                'xiao': 123
            }
        },
        'sun': [1, 2, [3, 4]]
    }
    data3 = '{"juzi": {"guagua": {"xiao": 123}}, "sun": [1, 2, [3, 4]]}'
    tokenList3 = json_tokens(data3)
    result3 = parsed_json(tokenList3)
    ensure(dict_equal(result3, json3), 'parsed_json test 3')


def test():
    test_json_tokens()
    test_parsed_json()
