from api import DsgApi, KsipApi
from catalog import Catalog
from common import DynamicObject
import json


def main():
    with open("config.json", "r") as config_file:
        config = DynamicObject(json.loads(config_file.read()))

    dsg = config.api.dsg
    ksip = config.api.ksip
    cases = config.cases
    settings = config.test_settings

    dsg_api = DsgApi(dsg.server, dsg.login, dsg.password)
    ksip_api = KsipApi(ksip.server, ksip.login, ksip.password)

    mines = Catalog.get_mines(dsg_api, settings.work_order.date)

    for mine in mines:
        catalog = Catalog(dsg_api, ksip_api, mine)
        catalog.update_catalogs(settings.work_order.date)

        if cases.work_order_request:
            catalog.request_work_orders(
                settings.work_order.date,
                settings.work_order.shift)

        if cases.locomotive_order_request:
            catalog.request_locomotive_order(
                settings.locomotive_order.date,
                settings.locomotive_order.shift)

        if cases.skip_order_request:
            catalog.request_skip_order(
                settings.skip_order.date,
                settings.skip_order.shift)

        if cases.sdo_fact_request:
            catalog.request_sdo_fact(
                ksip.fact_method,
                settings.sdo_fact.date,
                settings.sdo_fact.shift)

        if cases.vgu_fact_request:
            catalog.request_vgu_fact(
                ksip.fact_method,
                settings.vgu_fact.date,
                settings.vgu_fact.shift)


def test():
    d = dict(ab=2)
    print(d.get(None, 'abc'))


if __name__ == '__main__':
    main()
