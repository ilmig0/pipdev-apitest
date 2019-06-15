from api import DsgApi, KsipApi
from catalog import Catalog
from common import DynamicObject
import json


def main():
    with open("config.json", "r") as config_file:
        config = DynamicObject(json.loads(config_file.read()))

    dsg = config.dsg
    ksip = config.ksip

    dsg_api = DsgApi(dsg.server, dsg.login, dsg.password)
    ksip_api = KsipApi(ksip.server, ksip.login, ksip.password)

    mines = Catalog.get_mines(dsg_api, dsg.test_date)

    for mine in mines:
        catalog = Catalog(dsg_api, mine, dsg.test_date)
        catalog.update_catalogs()
        catalog.request_priority(dsg.test_date, dsg.test_shift)
        catalog.request_work_orders(dsg.test_date, dsg.test_shift)
        catalog.request_locomotive_order(dsg.test_date, dsg.test_shift)
        catalog.request_skip_order(dsg.test_date, dsg.test_shift)
        catalog.request_fact(ksip_api, ksip.get_fact_method, ksip.test_date, dsg.test_shift)


def test():
    d = dict(ab=2)
    print(d.get(None, 'abc'))


if __name__ == '__main__':
    main()
