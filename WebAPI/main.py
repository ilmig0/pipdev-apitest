from api import DsgApi
from catalog import Catalog
from common import DynamicObject
import json

with open("config.json", "r") as config_file:
    config = DynamicObject(json.loads(config_file.read()))

api = DsgApi(config.dsg_server, config.login, config.password)

mines = Catalog.get_mines(api, config.test_date)

for mine in mines:
    catalog = Catalog(api, mine, config.test_date)
    catalog.update_catalogs()
    catalog.request_priority(config.test_date, config.test_shift)
    catalog.request_work_orders(config.test_date, config.test_shift)
    catalog.request_locomotive_order(config.test_date, config.test_shift)
    catalog.request_skip_order(config.test_date, config.test_shift)
