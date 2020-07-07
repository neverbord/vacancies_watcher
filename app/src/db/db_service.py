import psycopg2
import psycopg2.extras
from db import db_creator


def init_db():
    print('Initialising database...')
    db_creator.create_tables()
    print('Database initialised')


def get_db_connection():
    # for development
    # return psycopg2.connect(
    #     dbname="postgres",
    #     user="postgres",
    #     password="example",
    #     host="localhost",
    #     port=5432
    # )

    possible_ips = ['172.{}.0.1'.format(i) for i in range(18, 25)]

    for ip in possible_ips:
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='example',
                host=ip,
                port=5432
            )

            return conn
        except psycopg2.OperationalError:
            pass


def insert_values(table_info, key_field, values_in_sql, conflict=True):
    # values_in_sql is an sql formatted string
    sql = 'insert into {} values '.format(table_info)

    for val in values_in_sql:
        sql += val + ', '

    sql = sql[:-2]

    if conflict:
        sql += ' on conflict ({}) do nothing'.format(key_field)

    execute_iud_sql_commands([sql])


def update_values(table_name, conditions, values):
    # сonstraints is a dict
    # { key_field: 'key_field_name', key_vals: ['key_val1', 'key_val2'...] }
    # values is a dict of dicts
    # { 'key_val': {'col1': 'val1', 'col2': 'val2'}...}

    update_commands = []
    base_sql = 'update {} set'.format(table_name)

    for key_val in conditions['key_vals']:
        sql = base_sql
        vals_dict = values[key_val]

        for val_key in vals_dict.keys():
            if val_key != conditions['key_field']:
                temp = vals_dict[val_key]

                if isinstance(temp, str):
                    temp = '\'{}\''.format(temp.replace('\'', "''"))
                elif isinstance(temp, bool):
                    temp = '\'{}\''.format(str(temp).lower())
                elif temp is None:
                    temp = 'null'
                else:
                    temp = str(temp)

                sql += ' {0} = {1},'.format(val_key, temp)

        sql = sql[:-1]
        sql += ' where {0} = \'{1}\''.format(
            str(conditions['key_field']), str(key_val))

        update_commands.append(sql)

    execute_iud_sql_commands(update_commands)


def delete_values(table_name, key_field, values):
    sql = 'delete from {0} where {1} in ({2})'.format(
        table_name, key_field,
        ', '.join(['\'{}\''.format(item) for item in values])
    )
    execute_iud_sql_commands([sql])


def execute_iud_sql_commands(commands):
    # insert, update, delete
    # for com in commands:
    #     print(com)
    # return

    connection = get_db_connection()
    cursor = connection.cursor()

    for com in commands:
        cursor.execute(com)
        connection.commit()

    cursor.close()
    connection.close()


def execute_s_sql_command(command_template, table_name):
    # select
    command = command_template.format(table_name)
    # print(command)
    # return {}

    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute(command)
    db_data = cursor.fetchall()

    cursor.close()
    connection.close()

    result = {table_name: []}
    for row in db_data:
        temp = {}
        for k in row.keys():
            temp[k] = row[k]

        result[table_name].append(temp)

    return result


def execute_sql(sql):
    connection = get_db_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(sql)
    db_data = cursor.fetchall()

    result = []
    for row in db_data:
        temp = {}
        for k in row.keys():
            temp[k] = row[k]

        result.append(temp)

    cursor.close()
    connection.close()

    return result