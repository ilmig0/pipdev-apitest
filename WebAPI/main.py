from api import DsgApi, KsipApi
from catalog import Catalog
from common import Dynamic
import json


def main():
    with open("config.json", "r") as config_file:
        config = Dynamic(json.loads(config_file.read()))

    dsg = config.api.dsg
    ksip = config.api.ksip
    cases = config.cases
    settings = config.test_settings

    dsg_api = DsgApi(dsg.server, dsg.login, dsg.password)
    ksip_api = KsipApi(ksip.proxy, ksip.login, ksip.password)

    mines = Catalog.get_mines(dsg_api, settings.work_order.date)

    for mine in mines:
        catalog = Catalog(dsg_api, ksip_api, mine)
        catalog.update_catalogs(settings.catalog.date)

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
                ksip.fact_method.sdo,
                settings.sdo_fact.date,
                settings.sdo_fact.shift)

        if cases.skip_fact_request:
            catalog.request_skip_fact(
                ksip.fact_method.skip,
                settings.skip_fact.date,
                settings.skip_fact.shift)

        if cases.ore_pass_fact_request:
            catalog.request_ore_pass_fact(
                ksip.fact_method.ore_pass,
                settings.ore_pass_fact.date,
                settings.ore_pass_fact.shift)


def test():
    d = dict(ab=2)
    print(d.get(None, 'abc'))


if __name__ == '__main__':
    main()
