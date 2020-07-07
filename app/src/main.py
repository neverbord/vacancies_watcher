from db import db_service
from data_management import dm_service


db_service.init_db()
dm_service.collect_data()
dm_service.export_data()
print('\nfinished!')
