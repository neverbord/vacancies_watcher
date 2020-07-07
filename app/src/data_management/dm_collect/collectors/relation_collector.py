from db import db_service


def collect_relation(table_name, key_field, data_dictionary):
    if len(data_dictionary) == 0:
        return

    db_service.delete_values(table_name, key_field, data_dictionary.keys())

    first_item = data_dictionary[[*data_dictionary.keys()][0]][0]
    entity_fields = first_item.__dict__.keys()
    table_info = '{0} ({1})'.format(table_name, ', '.join(entity_fields))
    all_items = []

    for k in data_dictionary.keys():
        all_items.extend(data_dictionary[k])

    db_service.insert_values(
        table_info=table_info,
        key_field=key_field,
        values_in_sql=[item.to_sql_string() for item in all_items],
        conflict=False
    )