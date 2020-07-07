from datetime import datetime
from db import db_service
from hh_api import hh_api_service
from ..vacancies_data_parser import VacanciesDataParser
from . import entity_collector, relation_collector


def collect_vacancies():
    api_vacancies = download_vacancies()
    vacancies_parser = VacanciesDataParser()

    for vacancy_search_data in api_vacancies['search_data']:
        if vacancy_search_data['type']['id'] == 'anonymous':
            continue

        vacancy_full_data = api_vacancies['full_data'][vacancy_search_data['id']]

        vacancies_parser.parse_vacancy_data(
            vacancy_full_data,
            vacancy_search_data
        )

    # collect entities
    entity_collector.collect_entity('areas', 'id', vacancies_parser.areas)
    entity_collector.collect_entity('metro_lines', 'id', vacancies_parser.metro_lines)
    entity_collector.collect_entity('metro_stations', 'id', vacancies_parser.metro_stations)
    entity_collector.collect_entity('profareas', 'id', vacancies_parser.profareas)
    entity_collector.collect_entity('specializations', 'id', vacancies_parser.specializations)
    entity_collector.collect_entity('employers', 'id', vacancies_parser.employers)
    entity_collector.collect_entity('insider_interviews', 'id', vacancies_parser.insider_interviews)
    entity_collector.collect_entity('addresses', 'id', vacancies_parser.addresses)
    entity_collector.collect_entity('vacancies', 'id', vacancies_parser.vacancies)

    # collect relations
    addresses_metro_stations = {}

    for k in vacancies_parser.addresses_metro_stations.keys():
        stations_dict = vacancies_parser.addresses_metro_stations[k]
        addresses_metro_stations[k] = [stations_dict[s] for s in stations_dict.keys()]

    relation_collector.collect_relation('addresses_metro_stations', 'address_id',
                                        addresses_metro_stations)

    employer_departments = {}
    for employer_key in vacancies_parser.employer_departments.keys():
        for department_key in vacancies_parser.employer_departments[employer_key]:
            employer_departments[department_key] = \
                vacancies_parser.employer_departments[employer_key][department_key]

    entity_collector.collect_entity('employer_departments', 'id',
                                    employer_departments)

    relation_collector.collect_relation('vacancy_key_skills', 'vacancy_id',
                                        vacancies_parser.vacancies_key_skills)

    relation_collector.collect_relation('vacancy_phones', 'vacancy_id',
                                        vacancies_parser.vacancies_phones)

    relation_collector.collect_relation('vacancy_driver_license_types', 'vacancy_id',
                                        vacancies_parser.vacancies_driver_license_types)


def download_vacancies():
    return hh_api_service.get_vacancies()
