# service to manage data collection and analysis
from .dm_collect.collectors import dictionaries_collector, vacancies_collector
from .dm_analyze import result_tables_manager


def collect_data():
    print('processing data...')
    dictionaries_collector.collect_dictionaries()
    vacancies_collector.collect_vacancies()


def export_data():
    print('printing results...\n')
    result_tables_manager.print_tables()
