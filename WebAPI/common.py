class DynamicObject(object):
    def __init__(self, json):
        self.__dict = dict()
        self.__dict.update(json)

    def __getattr__(self, item):
        if item not in self.__dict__ and item in self.__dict:
            self.__dict__[item] = DynamicObject.create_instance(self.__dict[item])
        return self.__dict__[item]

    @staticmethod
    def create_instance(json):
        if json is not None:
            if isinstance(json, dict):
                return DynamicObject(json)
            elif isinstance(json, list):
                return list(DynamicObject.create_instance(x) for x in list(json))
        return json
