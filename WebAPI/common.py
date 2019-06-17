class Dynamic(object):
    def __init__(self, json: dict):
        self.__json = json

    def __getattr__(self, item):
        if item in self.__json:
            self.__dict__[item] = Dynamic.__instance(self.__json[item])
        else:
            raise AttributeError

        return self.__dict__[item]

    @staticmethod
    def __instance(node):
        if node is not None:
            if isinstance(node, dict):
                return Dynamic(node)
            elif isinstance(node, list):
                return list(Dynamic.__instance(x) for x in list(node))
        return node
