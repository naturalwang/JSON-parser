from type import Type


class Token(object):
    def __init__(self, token_type, token_value):
        super(Token, self).__init__()
        d = {
            ':': Type.colon,
            ',': Type.comma,
            '{': Type.braceLeft,
            '}': Type.braceRight,
            '[': Type.bracketLeft,
            ']': Type.bracketRight,
        }
        if token_type == Type.auto:
            self.type = d[token_value]
        else:
            self.type = token_type
        self.value = token_value

    def __repr__(self):
        # return '<{}>: ({})'.format(self.type, self.value)
        return '{}'.format(self.value)

    def valueByType(self):
        value = self.value
        if self.type == Type.number:
            return int(value) if '.' not in value else float(value)
        elif self.type == Type.keyword:
            keywords = {
                'true': True,
                'false': False,
                'null': None,
            }
            return keywords[value]
        else:
            return value
