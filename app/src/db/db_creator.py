from db import db_service


def create_tables():
    create_tables_commands = []

    create_tables_commands.append(
        '''create table if not exists schedules(
            id text not null primary key,
            name text
        )
        '''
    )
    create_tables_commands.append(
        '''create table if not exists vacancy_billing_types(
              id text not null primary key,
              name text
           )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancy_types(
            id text not null primary key,
            name text
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists employments(
            id text not null primary key,
            name text
        )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists experiences(
            id text not null primary key,
            name text
        )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists areas(
            id text not null primary key,
            name text,
            url text
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists metro_lines(
            id text not null primary key,
            name text
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists metro_stations(
            id text not null primary key,
            name text,
            line_id text,
            lat double precision,
            lng double precision,
            foreign key (line_id) references metro_lines(id)
            on delete cascade
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists profareas(
            id text not null primary key,
            name text
        )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists specializations(
            id text not null primary key,
            name text,
            profarea_id text,
            foreign key (profarea_id) references profareas(id)
        )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists employers(
            id text not null primary key,
            name text,
            url text,
            alternate_url text,
            vacancies_url text,
            trusted boolean
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists employer_departments(
            id text not null primary key,
            name text,
            employer_id text, 
            foreign key (employer_id) references employers(id)
            on delete cascade
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancies(
            id text not null primary key,
            allow_messages boolean,
            premium boolean,
            name text,
            department_id text,
            has_test boolean,
            response_letter_required boolean,
            area_id text,
            type_id text,
            address_id text,
            response_url text,
            code text, 
            employment_id text,
            experience_id text,
            schedule_id text, 
            sort_point_distance integer,
            employer_id text,
            published_at timestamptz,
            created_at timestamptz,
            closed_at timestamptz,
            archived boolean,
            apply_alternative_url text,
            insider_interview_id text,
            url text, 
            alternate_url text,
            billing_type_id text,
            accept_incomplete_resumes boolean,
            snippet_requirement text,
            snippet_responsibility text,
            contact_name text,
            contact_email text,
            salary_from integer,
            salary_to integer,
            salary_currency text,
            salary_gross boolean,
            level text,
            specialty text,
            foreign key (employer_id) references employers(id) 
            on delete cascade
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists insider_interviews(
            id text not null primary key,
            url text
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists addresses(
            id text not null primary key,
            city text,
            street text,
            building text,
            description text,
            lat double precision,
            lng double precision,
            raw text,
            primary_metro_station_id text,
            foreign key (primary_metro_station_id) references metro_stations(id)
            on delete set null
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists addresses_metro_stations(
            address_id text not null,
            metro_station_id text not null,
            primary key (address_id, metro_station_id), 
            foreign key (address_id) references addresses(id)
            on delete cascade,
            foreign key (metro_station_id) references metro_stations(id)
            on delete cascade            
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancy_driver_license_types(
            vacancy_id text,
            driver_license_id text not null,
            primary key (vacancy_id, driver_license_id),
            foreign key (vacancy_id) references vacancies(id)
            on delete cascade
           )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancy_key_skills(
            vacancy_id text,
            skill_name text,
            primary key (vacancy_id, skill_name),
            foreign key (vacancy_id) references vacancies(id)
            on delete cascade
           )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancy_phones(
            vacancy_id text,
            comment text,
            city text,
            number text,
            country text,
            primary key (vacancy_id, number),
            foreign key (vacancy_id) references vacancies(id)
            on delete cascade
         )
        '''
    )

    create_tables_commands.append(
        '''create table if not exists vacancy_specializations(
            vacancy_id text,
            specialization_id text,
            primary key (vacancy_id, specialization_id),
            foreign key (vacancy_id) references vacancies(id)
            on delete cascade,
            foreign key (specialization_id) references specializations(id)
         )
        '''
    )

    db_service.execute_iud_sql_commands(create_tables_commands)