def get_value_to_set(value, default_value):
    return value if value is not None else default_value


class BaseModel:
    def get_obj_attr_list(self):
        # attr_names = [a for a in dir(self)
        #               if not a.startswith('__')
        #               and not callable(getattr(self, a))]

        attr_names = self.__dict__.keys()

        return [getattr(self, a) for a in attr_names]

    def to_sql_string(self):
        obj_attrs = self.get_obj_attr_list()
        result_str = '('

        for i in range(len(obj_attrs)):
            if isinstance(obj_attrs[i], str):
                result_str += '\'' + obj_attrs[i].replace('\'', "''") + '\', '
            elif isinstance(obj_attrs[i], bool):
                result_str += '\'' + str(obj_attrs[i]).lower() + '\', '
            elif obj_attrs[i] is None:
                result_str += 'null, '
            else:
                result_str += str(obj_attrs[i]) + ', '

        result_str = result_str[:-2]
        result_str += ')'
        return result_str


class Area(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.url = data['url']


class VacancyBillingType(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class VacancyType(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class MetroLine(BaseModel):
    def __init__(self, data):
        self.id = data['line_id']
        self.name = data['line_name']


class MetroStation(BaseModel):
    def __init__(self, data):
        self.id = data['station_id']
        self.name = data['station_name']
        self.line_id = data['line_id']
        self.lat = data['lat']
        self.lng = data['lng']


class Employment(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class Experience(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class Schedule(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']


class Specialization(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.profarea_id = data['profarea_id']


class Profarea(BaseModel):
    def __init__(self, data):
        self.id = data['profarea_id']
        self.name = data['profarea_name']


class Employer(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.url = data['url']
        self.alternate_url = data['alternate_url']
        self.vacancies_url = data['vacancies_url']
        self.trusted = data['trusted']


class EmployerDepartment(BaseModel):
    def __init__(self, data):
        self.id = data['department']['id']
        self.name = data['department']['name']
        self.employer_id = data['employer']['id']


class InsiderInterview(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']


class Vacancy(BaseModel):
    def __init__(self, data, search_data):
        self.id = data['id']
        self.allow_messages = data['allow_messages']
        self.premium = data['premium']
        self.name = data['name']

        self.department_id = data['department']['id'] \
            if data['department'] is not None \
            else ''

        self.has_test = data['has_test']
        self.response_letter_required = data['response_letter_required']
        self.area_id = data['area']['id']
        self.type_id = data['type']['id']

        if search_data['address'] is not None:
            self.address_id = search_data['address']['id']
        else:
            self.address_id = ''

        self.response_url = get_value_to_set(data['response_url'], '')
        self.code = get_value_to_set(data['code'], '')

        self.employer_id = data['employment']['id'] \
            if data['employment'] is not None \
            else ''

        self.experience_id = data['experience']['id'] \
            if data['experience'] is not None \
            else ''

        self.schedule_id = data['schedule']['id'] \
            if data['schedule'] is not None \
            else ''

        self.sort_point_distance = get_value_to_set(search_data['sort_point_distance'], 0)
        self.employer_id = data['employer']['id']
        self.published_at = data['published_at']
        self.archived = data['archived']
        self.apply_alternative_url = data['apply_alternate_url']

        self.insider_interview_id = data['insider_interview']['id'] \
            if data['insider_interview'] is not None \
            else ''

        self.url = search_data['url']
        self.alternate_url = data['alternate_url']
        self.billing_type_id = data['billing_type']['id']
        self.accept_incomplete_resumes = data['accept_incomplete_resumes']

        if search_data['snippet'] is not None:
            self.snippet_requirement = search_data['snippet']['requirement']
            self.snippet_requirement = search_data['snippet']['responsibility']
        else:
            self.snippet_requirement = ''
            self.snippet_responsibility = ''

        if data['contacts'] is not None:
            self.contact_name = data['contacts']['name']
            self.contact_email = data['contacts']['email']
        else:
            self.contact_name = ''
            self.contact_email = ''

        if data['salary'] is not None:
            salary = data['salary']
            self.salary_from = get_value_to_set(salary['from'], 0)
            self.salary_to = get_value_to_set(salary['to'], 0)
            self.salary_currency = get_value_to_set(salary['currency'], '')
            self.salary_gross = salary['gross']
        else:
            self.salary_from = 0
            self.salary_to = 0
            self.salary_currency = ''
            self.salary_gross = False

        # дата закрытия вакансии
        self.closed_at = '9999-12-31T00:00:00+0300'

        # уровень junior/middle/senior
        self.level = 'not specified'
        levels = ['junior', 'senior', 'middle']

        for level in levels:
            if level in self.name.lower():
                self.level = level
                break

        # специализация frontend/backend/fullstack/mobile/DevOps/data
        self.specialty = 'not specified'
        specialties = [
            'frontend',
            'backend',
            'fullstack',
            'mobile',
            'devops',
            'data']

        for specialty in specialties:
            if specialty in self.name.lower():
                self.specialty = specialty
                break


class Address(BaseModel):
    def __init__(self, data):
        self.id = data['id']
        self.city = get_value_to_set(data['city'], '')
        self.street = get_value_to_set(data['street'], '')
        self.building = get_value_to_set(data['building'], '')
        self.description = get_value_to_set(data['description'], '')
        self.lat = get_value_to_set(data['lat'], 0.)
        self.lng = get_value_to_set(data['lng'], 0.)
        self.raw = get_value_to_set(data['raw'], '')

        if data['metro'] is not None:
            self.primary_metro_station_id = data['metro']['station_id']
        else:
            self.primary_metro_station_id = None


class AddressMetroStation(BaseModel):
    def __init__(self, address_id, station_id):
        self.address_id = address_id
        self.metro_station_id = station_id


class VacancyDriverLicenseType(BaseModel):
    def __init__(self, vac_id, license_id):
        self.vacancy_id = vac_id
        self.driver_license_id = license_id


class VacancyPhone(BaseModel):
    def __init__(self, vac_id, data):
        self.vacancy_id = vac_id
        self.comment = get_value_to_set(data['comment'], '')
        self.city = get_value_to_set(data['city'], '')
        self.number = get_value_to_set(data['number'], '')
        self.country = get_value_to_set(data['country'], '')


class VacancyKeySkill(BaseModel):
    def __init__(self, vacancy_id, skill_name):
        self.vacancy_id = vacancy_id
        self.skill_name = skill_name


class VacancySpecialization(BaseModel):
    def __init__(self, vacancy_id, specialization_id):
        self.vacancy_id = vacancy_id
        self.specialization_id = specialization_id
