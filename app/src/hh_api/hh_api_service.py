import json
import requests
from datetime import datetime, timedelta


def get_response_object(request_url):
    json_request = requests.get(request_url)
    json_string = json_request.text
    return json.loads(json_string)


def get_dictionaries():
    return get_response_object('https://api.hh.ru/dictionaries')


def get_vacancies():
    print('searching for vacancies...')

    result = {
        'search_data': [],
        'full_data': {}
    }

    periods = get_date_periods()

    for period in periods:
        # print('period: {0}, {1} -- {2}'.format(
        #     period['date_from'].date(),
        #     period['date_to'].date(),
        #     datetime.now()))

        start_page = 0

        search_url = get_search_url(
            period['date_from'].date(),
            period['date_to'].date(),
            start_page)

        response = get_response_object(search_url)
        max_page = response['pages'] - 1
        current_page = start_page

        while current_page <= max_page:
            # print('page {0} of {1} -- {2}'.format(
            #     current_page,
            #     max_page,
            #     datetime.now().time()))

            if current_page != start_page:
                search_url = get_search_url(
                    period['date_from'].date(),
                    period['date_to'].date(),
                    current_page)

                response = get_response_object(search_url)

            result['search_data'].extend(response['items'])
            current_page += 1

    print('gathering additional info (it can take up to 15 minutes)...')
    for item in result['search_data']:
        result['full_data'][item['id']] = get_vacancy(item['id'])

    return result


def get_date_periods():
    periods = []
    temp = datetime.now()

    for i in range(5):
        periods.append({
            'date_from': temp - timedelta(days=5),
            'date_to': temp
        })

        temp -= timedelta(days=6)

    return periods


def get_search_url(date_from, date_to, page_number):
    search_url = 'https://api.hh.ru/vacancies?area=2&employer_type=company' \
                 + '&industry=7.538&industry=7.539&industry=7.540&industry=7.541' \
                 + '&date_from={0}&date_to={1}'.format(date_from, date_to) \
                 + '&order_by=publication_time&per_page=100&page={}'.format(page_number)
    return search_url


def get_vacancy(vacancy_id):
    url = 'https://api.hh.ru/vacancies/{}?host=hh.ru'.format(vacancy_id)
    response = get_response_object(url)

    if response['description'] == 'Not Found':
        return None
    else:
        return response
