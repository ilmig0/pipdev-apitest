from client import HttpClient
from common import DynamicObject


class DsgApi:

    def __init__(self, server, login, password):
        self.__server = server
        self.__client = HttpClient(server, {'Content-type': 'application/json'})
        self.__client.authorize_bearer('token', login, password)

    def get_mine(self, date):
        return self.__get_items('api/references/mine/{0}'
                                .format(date))

    def get_shaft(self, date, mine_id):
        return self.__get_items('api/references/shaft/{0}/{1}'
                                .format(date, mine_id))

    def get_section(self, date, mine_id, shaft_id):
        return self.__get_items('api/references/section/{0}/{1}/{2}'
                                .format(date, mine_id, shaft_id))

    def get_orepass(self, date, mine_id):
        return self.__get_items('api/references/orepass/{0}/{1}'
                                .format(date, mine_id))

    def get_skip(self, date, mine_id):
        return self.__get_items('api/references/skip/{0}/{1}'
                                .format(date, mine_id))

    def get_location(self, date, mine_id):
        return self.__get_items('api/references/location/{0}/{1}'
                                .format(date, mine_id))

    def get_location_kind(self, date):
        return self.__get_items('api/references/locationkind/{0}'
                                .format(date))

    def get_development_type(self, date):
        return self.__get_items('api/references/developmenttype/{0}'
                                .format(date))

    def get_equipment_category(self, date):
        return self.__get_items('api/references/equipmentcategory/{0}'
                                .format(date))

    def get_equipment_type(self, date, equipment_category_id='Null'):
        return self.__get_items('api/references/equipmenttype/{0}/{1}'
                                .format(date, equipment_category_id))

    def get_equipment(self, date, mine_id, equipment_type_id='Null'):
        return self.__get_items('api/references/equipment/{0}/{1}/{2}'
                                .format(date, mine_id, equipment_type_id))

    def get_operator(self, date, mine_id):
        return self.__get_items('api/references/operator/{0}/{1}'
                                .format(date, mine_id))

    def get_job_kind(self, date, mine_id, job_category_id='Null'):
        return self.__get_items('api/references/jobkind/{0}/{1}/{2}'
                                .format(date, mine_id, job_category_id))

    def get_priority(self, date, mine_id, shift):
        return self.__get_items('api/references/priority/{0}/{1}/{2}'.format(date, mine_id, shift),
                                root='priorityCollection')

    def get_unit(self, date):
        return self.__get_items('api/references/unit/{0}'.format(date))

    def get_work_order(self, date, mine_id, shaft_id, section_id, shift):
        orders = self.__get_items('api/workorder/{0}/{1}/{2}/{3}/{4}'.format(date, mine_id, shaft_id, section_id, shift))
        orders_list = list()

        if len(orders) > 0:
            for order in orders:
                orders_list = orders_list + order.body

        return orders_list

    def get_locomotive_order(self, date, shift, mine_id):
        return self.__get_items('api/locomotiveorder/{0}/{1}/{2}'.format(date, shift, mine_id))

    def get_skip_order(self, date, shift, mine_id):
        return self.__get_items('api/skiporder/{0}/{1}/{2}'.format(date, shift, mine_id))

    def __get_items(self, uri, root='data'):
        response = self.__client.get(uri)
        items = getattr(DynamicObject(response), root)
        if items is None:
            items = list()
        return items
