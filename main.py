from api import DsgApi
from catalog import Catalog

server = 'http://snr05228:8094'
login = 'Integrator'
password = '123'
test_date = '2019-07-07'
test_shift = 2

api = DsgApi(server, login, password)

mines = Catalog.get_mines(api, test_date)

for mine in mines:
    catalog = Catalog(api, mine, test_date)
    catalog.update_catalogs()
    catalog.request_priority(test_date, test_shift)
    catalog.request_workorders(test_date, test_shift)
    catalog.print_workorders()
