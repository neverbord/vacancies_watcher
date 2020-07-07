from db import db_service
from hh_api import hh_api_service
from .. import model
from .. import utils


def collect_dictionaries():
    api_dictionaries = download_dictionaries()
    db_dictionaries = select_dictionaries_ids()

    for d_name in api_dictionaries.keys():
        api_d = api_dictionaries[d_name]
        db_d = db_dictionaries[d_name]

        buckets = utils.sort_out(api_d.keys(), db_d)

        if len(buckets['new']) > 0:
            db_service.insert_values(
                table_info=d_name,
                key_field='id',
                values_in_sql=[item.to_sql_string()
                               for item in [api_d[key] for key in buckets['new']]]
            )

        if len(buckets['same']) > 0:
            db_service.update_values(
                table_name=d_name,
                conditions={
                    'key_field': 'id',
                    'key_vals': buckets['same']
                },
                values={key: api_d[key].__dict__
                        for key in buckets['same']}
            )


def download_dictionaries():
    # employment - тип занятости
    # experience - опыт работы
    # schedule - график работы
    # vacancy_type - тип вакансии
    # vacancy_billing_type - варианты размещения вакансии с точки зрения биллинга
    # vacancy_relation - типы связи вакансии с пользователем

    api_dictionaries_data = hh_api_service.get_dictionaries()

    result = {
        'employments': {item['id']: model.Employment(item)
                        for item in api_dictionaries_data['employment']},
        'experiences': {item['id']: model.Experience(item)
                        for item in api_dictionaries_data['experience']},
        'schedules': {item['id']: model.Schedule(item)
                      for item in api_dictionaries_data['schedule']},
        'vacancy_types': {item['id']: model.VacancyType(item)
                          for item in api_dictionaries_data['vacancy_type']},
        'vacancy_billing_types': {item['id']: model.VacancyBillingType(item)
                                  for item in api_dictionaries_data['vacancy_billing_type']}
    }

    return result


def select_dictionaries_ids():
    dict_names = [
        'employments',
        'experiences',
        'schedules',
        'vacancy_types',
        'vacancy_billing_types'
    ]

    result = {}

    for name in dict_names:
        db_data = db_service.execute_s_sql_command('select id from {}', name)
        result[name] = [item['id'] for item in db_data[name]]

    return result
