import common


class Catalog:

    def __init__(self, api, mine, date):
        self.__api = api
        self.__mine = mine
        self.__date = date

        self.__shafts = dict()
        self.__sections = dict()
        self.__locations = dict()
        self.__equipments = dict()
        self.__equipment_types = dict()
        self.__orepass = dict()
        self.__operators = dict()
        self.__job_kinds = dict()
        self.__units = dict()

        self.__priority = list()
        self.__workorders = list()

    @staticmethod
    def get_mines(api, date):
        mines_list = api.get_mine(date)
        return Catalog.dict_by_key('idMine', mines_list)

    def __update_shafts(self):
        shafts_list = self.__api.get_shaft(self.__date, self.__mine)
        self.__shafts.update(Catalog.dict_by_key('idShaft', shafts_list))

    def __update_sections(self):
        for shaft in self.__shafts.values():
            sections_list = self.__api.get_section(self.__date, self.__mine, shaft.idShaft)
            self.__sections.update(Catalog.dict_by_key('idSection', sections_list))

    def __update_locations(self):
        location_list = self.__api.get_location(self.__date, self.__mine)
        self.__locations.update(Catalog.dict_by_key('idLocation', location_list))

    def __update_equipment_types(self):
        equipment_types_list = self.__api.get_equipment_type(self.__date)
        self.__equipment_types.update(Catalog.dict_by_key('idEquipmentType', equipment_types_list))

    def __update_equipment(self):
        equipment_list = self.__api.get_equipment(self.__date, self.__mine)
        self.__equipments.update(Catalog.dict_by_key('idEquipment', equipment_list))

    def __update_orepass(self):
        orepass_list = self.__api.get_orepass(self.__date, self.__mine)
        self.__orepass.update(Catalog.dict_by_key('idOrePass', orepass_list))

    def __update_operators(self):
        operators_list = self.__api.get_operator(self.__date, self.__mine)
        self.__operators.update(Catalog.dict_by_key('idOperator', operators_list))

    def __update_job_kind(self):
        job_kind_list = self.__api.get_job_kind(self.__date, self.__mine)
        self.__job_kinds.update(Catalog.dict_by_key('idJobKind', job_kind_list))

    def __update_unit(self):
        unit_list = self.__api.get_unit(self.__date)
        self.__units.update(Catalog.dict_by_key('idUnit', unit_list))

    def request_workorders(self, date, shift):
        for section in self.__sections.values():
            self.__workorders = self.__workorders + self.__api.get_workorder(date, self.__mine, section.idShaft, section.idSection, shift)

    def request_priority(self, date, shift):
        self.__priority = self.__priority + self.__api.get_priority(date, self.__mine, shift)

    def update_catalogs(self):
        self.__update_shafts()
        self.__update_sections()
        self.__update_orepass()
        self.__update_locations()
        self.__update_equipment_types()
        self.__update_equipment()
        self.__update_operators()
        self.__update_job_kind()
        self.__update_unit()

    def print_workorders(self):

        print('{0:2s} | {1:2s} | {2:40s} | {3:30s} | {4:40s} | {5:20s} | {6:25s} | {7:40s} | {8:5s}\t | \t{9:10s} | {10}\n'
            .format(
                'Ш.',
                'У.',
                'Выработка',
                'Рудоспуск',
                'Вид работ',
                'Тип оборудования',
                'Оборудование',
                'Оператор',
                'План',
                'Порядок',
                'Доп. инф.'))

        #print('-------------------------------------------------------------------' +
        #     '-------------------------------------------------------------------\n')

        for order in self.__workorders:
            orepass_id = order.idOrePass
            if orepass_id is not None:
                orepass_str = '({0}) '.format(orepass_id) + self.__orepass[orepass_id].name
            else:
                orepass_str = '-'

            if order.order is not None:
                order_str = order.order
            else:
                order_str = '-'

            print('{0:2s} | {1:2s} | {2:40s} | {3:30s} | {4:40s} | {5:20s} | {6:25s} | {7:40s} | {8:5.0f}\t | \t{9:10} | {10}\n'
                .format(
                    self.__shafts[self.__sections[self.__locations[order.idLocation].idSection].idShaft].name,
                    self.__sections[self.__locations[order.idLocation].idSection].name,
                    ' ({0}) '.format(order.idLocation) + self.__locations[order.idLocation].name,
                    orepass_str,
                    self.__job_kinds[order.idJobKind].name,
                    self.__equipment_types[order.idEquipmentType].name,
                    ' ({0}) '.format(order.idEquipment) + self.__equipments[order.idEquipment].number,
                    ' ({0}) '.format(order.idOperator) + self.__operators[order.idOperator].name,
                    order.plan,
                    order_str,
                    str(order.description)))

    @staticmethod
    def dict_by_key(key, items):
        return dict((getattr(item, key), item) for item in items)



