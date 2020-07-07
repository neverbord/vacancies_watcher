from db import db_service
from datetime import datetime
import texttable


def print_tables():
    result_lines = ['Open vacancies\n']
    result_lines.extend(get_start_info())
    result_lines.append('\n\nClosed vacancies\n')
    result_lines.extend(get_results())

    for rl in result_lines:
        print(rl)

    with open('results.txt', 'w') as ouf:
        ouf.writelines(result_lines)


def get_start_info():
    result_lines = []
    result_lines.extend(get_vacs_by_level())
    result_lines.append('\n\n')
    result_lines.extend(get_vacs_by_specialty())
    return result_lines


def get_vacs_by_level():
    sql = '''select v.level, count(v.id)
               from vacancies as v
               group by v.level
               order by v.level'''

    db_data = db_service.execute_sql(sql)

    result_lines = ['Vacancies by level\n']
    table_lines = [['level', 'count']]

    for row in db_data:
        table_lines.append([row['level'], row['count']])

    out_table = texttable.Texttable()
    out_table.add_rows(table_lines)
    result_lines.append(out_table.draw())

    return result_lines


def get_vacs_by_specialty():
    sql = '''select v.specialty, count(v.id)
               from vacancies as v
               group by v.specialty
               order by v.specialty'''

    db_data = db_service.execute_sql(sql)

    result_lines = ['Vacancies by specialty\n']
    table_lines = [['specialty', 'count']]

    for row in db_data:
        table_lines.append([row['specialty'], row['count']])

    out_table = texttable.Texttable()
    out_table.add_rows(table_lines)
    result_lines.append(out_table.draw())

    return result_lines


def get_vacs_by_spec_level_salary():
    sql = '''select v.specialty, v.level, v.salary_from, v.salary_currency, count(v.id)
             from vacancies as v
             group by v.specialty, v.level, v.salary_from, v.salary_currency
             order by count(v.id) desc, v.salary_from desc'''

    db_data = db_service.execute_sql(sql)

    result_lines = ['Vacancies by specialty, level and salary\n']
    table_lines = [['specialty', 'level', 'salary_from', 'salary_currency', 'count']]

    for row in db_data:
        table_lines.append(
            [row['specialty'],
             row['level'],
             row['salary_from'],
             row['salary_currency'],
             row['count'],
             ])

    out_table = texttable.Texttable()
    out_table.add_rows(table_lines)
    result_lines.append(out_table.draw())

    return result_lines


def get_results():
    sql = '''select v.level, count(v.id)
                   from vacancies as v
                   where v.closed_at <= '{}'
                   group by v.level
                   order by v.level'''.format(datetime.now().date())

    db_data = db_service.execute_sql(sql)

    result_lines = ['Vacancies by level\n']
    table_lines = [['level', 'count']]

    for row in db_data:
        table_lines.append([row['level'], row['count']])

    out_table = texttable.Texttable()
    out_table.add_rows(table_lines)
    result_lines.append(out_table.draw())

    sql = '''select v.specialty, count(v.id)
                   from vacancies as v
                   where v.closed_at <= '{}'
                   group by v.specialty
                   order by v.specialty'''.format(datetime.now().date())

    db_data = db_service.execute_sql(sql)

    result_lines.append('\n\nVacancies by specialty\n')
    table_lines = [['specialty', 'count']]

    for row in db_data:
        table_lines.append([row['specialty'], row['count']])

    out_table = texttable.Texttable()
    out_table.add_rows(table_lines)
    result_lines.append(out_table.draw())

    return result_lines
