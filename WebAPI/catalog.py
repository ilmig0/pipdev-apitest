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
        self.__skips = dict()
        self.__operators = dict()
        self.__job_kinds = dict()
        self.__units = dict()

        self.__priority = list()

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

    def __update_skips(self):
        skip_list = self.__api.get_skip(self.__date, self.__mine)
        self.__skips.update(Catalog.dict_by_key('idSkip', skip_list))

    def __update_operators(self):
        operators_list = self.__api.get_operator(self.__date, self.__mine)
        self.__operators.update(Catalog.dict_by_key('idOperator', operators_list))

    def __update_job_kind(self):
        job_kind_list = self.__api.get_job_kind(self.__date, self.__mine)
        self.__job_kinds.update(Catalog.dict_by_key('idJobKind', job_kind_list))

    def __update_unit(self):
        unit_list = self.__api.get_unit(self.__date)
        self.__units.update(Catalog.dict_by_key('idUnit', unit_list))

    def request_work_orders(self, date, shift):
        work_orders = list()
        for section in self.__sections.values():
            work_orders = work_orders + self.__api.get_work_order(date, self.__mine, section.idShaft, section.idSection, shift)

        self.__print_work_orders(work_orders)

    def request_locomotive_order(self, date, shift):
        locomotive_orders = self.__api.get_locomotive_order(date, shift, self.__mine)
        self.__print_locomotive_orders(locomotive_orders)

    def request_skip_order(self, date, shift):
        skip_orders = self.__api.get_skip_order(date, shift, self.__mine)
        self.__print_skip_orders(skip_orders)

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
        self.__update_skips()

    def __print_locomotive_orders(self, locomotive_orders):
        fs = '{0:20s}  {1:45s}  {2:10s}  {3:10s} \n'

        print(fs.format('Электровоз', 'Машинист', 'План', 'Ед. изм'))

        for locomotive_order in locomotive_orders:
            equipment = Catalog.__get_item_attr(self.__equipments, locomotive_order.idEquipment, 'number')

            operator = Catalog.__get_item_attr(self.__operators, locomotive_order.idOperator, 'name')

            plan = Catalog.__value_to_str(locomotive_order.plan)

            print(fs.format(equipment, operator, plan, 'вагонов'))

        print('\n')

    def __print_skip_orders(self, skip_orders):
        fs = '{0:20s}  {1:45s}  {2:10s}  {3:10s} \n'

        print(fs.format('Рудоспуск', 'Скиповой ствол', 'План', 'Ед. изм'))

        for skip_order in skip_orders:

            ore_pass = Catalog.__get_item_attr(self.__orepass, skip_order.idSource, 'name')

            skip = Catalog.__get_item_attr(self.__skips, skip_order.idDestination, 'name')

            plan = Catalog.__value_to_str(skip_order.plan)

            print(fs.format(ore_pass, skip, plan, 'вагонов'))

        print('\n')

    def __print_work_orders(self, work_orders):

        fs = '{0:2s}  {1:2s}  {2:45s}  {3:30s}  {4:35s}  {5:25s}  {6:25s}  {7:40s}  {8:5s}  {9:10s}  {10:7s}  {11}\n'

        print(fs.format(
                'Ш',
                'У',
                'Выработка',
                'Рудоспуск',
                'Вид работ',
                'Тип оборудования',
                'Оборудование',
                'Оператор',
                'План',
                'Ед. изм',
                'Порядок',
                'Доп. инф.'))

        # print('-------------------------------------------------------------------' +
        #       '-------------------------------------------------------------------\n')

        for work_order in work_orders:
            location_model = self.__locations[work_order.idLocation]
            location = Catalog.__get_item_attr(self.__locations, location_model.idLocation, 'name')

            ore_pass = Catalog.__get_item_attr(self.__orepass, work_order.idOrePass, 'name')

            section_model = self.__sections[location_model.idSection]
            section = Catalog.__get_item_attr(self.__sections, section_model.idSection, 'name', print_id=False)

            shaft = Catalog.__get_item_attr(self.__shafts, section_model.idShaft, 'name', print_id=False)

            job_kind = Catalog.__get_item_attr(self.__job_kinds, work_order.idJobKind, 'name')

            equipment_type = Catalog.__get_item_attr(self.__equipment_types, work_order.idEquipmentType, 'name')

            equipment = Catalog.__get_item_attr(self.__equipments, work_order.idEquipment, 'number')

            operator = Catalog.__get_item_attr(self.__operators, work_order.idOperator, 'name')

            plan = Catalog.__value_to_str(work_order.plan)

            unit = Catalog.__get_item_attr(self.__units, work_order.idUnit, 'name', print_id=False)

            order = Catalog.__value_to_str(work_order.order)

            description = Catalog.__value_to_str(work_order.description)

            print(fs.format(
                        shaft,
                        section,
                        location,
                        ore_pass,
                        job_kind,
                        equipment_type,
                        equipment,
                        operator,
                        plan,
                        unit,
                        order,
                        description))

        print('\n')

    @staticmethod
    def __get_item_attr(items, item_id, attr, print_id=True):
        if item_id is not None:
            if print_id:
                item_str = '({0}) '.format(str(item_id)) + getattr(items[item_id], attr)
            else:
                item_str = getattr(items[item_id], attr)
        else:
            item_str = '-'

        return item_str

    @staticmethod
    def __value_to_str(value):
        if value is not None:
            value_str = str(value)
        else:
            value_str = '-'

        return value_str

    @staticmethod
    def dict_by_key(key, items):
        return dict((getattr(item, key), item) for item in items)



