from data_management.dm_collect import model


class VacanciesDataParser:
    def __init__(self):
        self.vacancies = {}
        self.areas = {}
        self.metro_stations = {}
        self.metro_lines = {}
        self.addresses = {}
        self.addresses_metro_stations = {}
        self.specializations = {}
        self.profareas = {}
        self.employers = {}
        self.employer_departments = {}
        self.insider_interviews = {}
        self.vacancies_driver_license_types = {}
        self.vacancies_phones = {}
        self.vacancies_key_skills = {}

    def parse_vacancy_data(self, full_data, search_data):
        vacancy_id = full_data['id']
        try:
            vacancy = model.Vacancy(full_data, search_data)
        except KeyError:
            print('----->Error')
            print(search_data)
            print(full_data)
            print('<-----Error')
            return

        self.vacancies[vacancy_id] = vacancy

        if full_data['area'] is not None \
                and full_data['area']['id'] not in self.areas.keys():
            self.areas[full_data['area']['id']] = model.Area(full_data['area'])

        if search_data['address'] is not None \
                and search_data['address']['id'] not in self.addresses.keys():
            address_id = search_data['address']['id']
            self.addresses[address_id] = model.Address(search_data['address'])

            for station in search_data['address']['metro_stations']:
                station_id = station['station_id']

                if station_id not in self.metro_stations.keys():
                    self.metro_stations[station_id] = model.MetroStation(station)

                line_id = station['line_id']

                if line_id not in self.metro_lines.keys():
                    self.metro_lines[line_id] = model.MetroLine(station)

                if address_id not in self.addresses_metro_stations.keys():
                    self.addresses_metro_stations[address_id] = {}

                if station_id not in self.addresses_metro_stations[address_id].keys():
                    self.addresses_metro_stations[address_id][station_id] = \
                        model.AddressMetroStation(address_id, station_id)

        for spec in full_data['specializations']:
            if spec['id'] not in self.specializations.keys():
                self.specializations[spec['id']] = model.Specialization(spec)

            if spec['profarea_id'] not in self.profareas.keys():
                self.profareas[spec['profarea_id']] = model.Profarea(spec)

        employer_id = full_data['employer']['id']
        if employer_id not in self.employers.keys():
            self.employers[employer_id] = model.Employer(full_data['employer'])

        if full_data['department'] is not None:
            if employer_id not in self.employer_departments.keys():
                self.employer_departments[employer_id] = {}

            department_id = full_data['department']['id']
            if department_id not in self.employer_departments[employer_id].keys():
                self.employer_departments[employer_id][department_id] = \
                    model.EmployerDepartment(full_data)

        if full_data['insider_interview'] is not None:
            insider_interview_id = full_data['insider_interview']['id']
            if insider_interview_id not in self.insider_interviews.keys():
                self.insider_interviews[insider_interview_id] = \
                    model.InsiderInterview(full_data['insider_interview'])

        if len(full_data['driver_license_types']) > 0:
            self.vacancies_driver_license_types[vacancy_id] = []

        for d_license in full_data['driver_license_types']:
            if d_license['id'] not in \
                    [d.driver_license_id for d in
                     self.vacancies_driver_license_types[vacancy_id]]:
                self.vacancies_driver_license_types[vacancy_id].append(
                    model.VacancyDriverLicenseType(vacancy_id, d_license['id']))

        if full_data['contacts'] is not None:
            if len(full_data['contacts']['phones']) > 0:
                self.vacancies_phones[vacancy_id] = []

            for phone in full_data['contacts']['phones']:
                if phone['number'] not in \
                        [p.number for p in self.vacancies_phones[vacancy_id]]:
                    self.vacancies_phones[vacancy_id].append(
                        model.VacancyPhone(vacancy_id, phone))

        if len(full_data['key_skills']) > 0:
            self.vacancies_key_skills[vacancy_id] = []

            for key_skill in full_data['key_skills']:
                if key_skill['name'] not in \
                        [k.skill_name for k in self.vacancies_key_skills[vacancy_id]]:
                    self.vacancies_key_skills[vacancy_id].append(
                        model.VacancyKeySkill(vacancy_id, key_skill['name']))
