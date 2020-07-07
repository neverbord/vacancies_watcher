from .. import utils
from db import db_service
from datetime import datetime
from hh_api import hh_api_service


def collect_entity(table_name, key_field, data_dictionary):
    if len(data_dictionary) == 0:
        return

    db_records = select_from_db(table_name, key_field)
    buckets = utils.sort_out(data_dictionary.keys(), db_records)
    first_key = [*data_dictionary.keys()][0]

    if len(buckets['new']) > 0:
        entity_fields = data_dictionary[first_key].__dict__.keys()
        values_in_sql = [item.to_sql_string()
                         for item in [data_dictionary[key] for key in buckets['new']]]

        table_info = '{0} ({1})'.format(table_name, ', '.join(entity_fields))

        db_service.insert_values(
            table_info=table_info,
            key_field=key_field,
            values_in_sql=values_in_sql
        )

    if len(buckets['same']) > 0:
        values_to_append = {key: data_dictionary[key].__dict__
                            for key in buckets['same']}

        db_service.update_values(
            table_name=table_name,
            conditions={
                'key_field': key_field,
                'key_vals': buckets['same']
            },
            values=values_to_append
        )

    if table_name != 'vacancies':
        return

    if len(buckets['old']) > 0:
        # update old vacancies
        values = {}
        closed_dt = datetime.now().astimezone().replace(microsecond=0).isoformat()

        for old_id in buckets['old']:
            response = hh_api_service.get_vacancy(old_id)

            if response is None:
                # if it really doesn't exist
                values[old_id] = {'closed_at': closed_dt}
            else:
                # if it's just old for selection
                values[old_id] = {'closed_at': '9999-12-31'}

        db_service.update_values(
            table_name=table_name,
            conditions={
                'key_field': 'id',
                'key_vals': values.keys() #buckets['old']
            },
            values=values
        )


def select_from_db(table_name, key_field):
    db_selection = db_service.execute_s_sql_command(
        command_template='select ' + key_field + ' from {}',
        table_name=table_name)
    return [item[key_field] for item in db_selection[table_name]]
