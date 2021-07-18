def SelectAuthor(value):
    authors = []
    for i in value:
        authors.append(i["name"])
    return authors


class SelectFields:
    def __init__(self, fields):
        self.fields = fields

    def __call__(self, values):
        Fields = {}
        for f in self.fields:
            if f in values:
                Fields[f] = values.get(f)
            else:
                Fields[f] = None
        return Fields


class TakeTheFirst:

    def __init__(self, num):
        self.num = num

    def __call__(self, values):
        return values[0:self.num]
