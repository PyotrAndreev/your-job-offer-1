import requests
from datetime import datetime, timedelta
import time
import json
from requests.exceptions import HTTPError, Timeout, ConnectionError
from dataclasses import dataclass
import logging

from sqlalchemy.orm import sessionmaker
from models import Vacancy as DB_Vacancy, engine
from updating_bd import update_time, get_last_update

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


## айдишник hh - 1
## айдишник hc - 2
## айдишник sj - 3
## айдишник zp - 4

@dataclass
class Vacancy:
    """Класс для хранения информации о вакансиях."""
    job_title: str
    vacancy_id_in_hh: int = 0
    vacancy_id_in_hc: int = 0
    vacancy_id_in_sj: int = 0
    vacancy_id_in_zp: int = 0
    response_letter_required: bool = False
    country: str = ""
    city: str = ""
    district: str = ""
    salary: str = None
    office_address: str = ""
    subway_station: str = ""
    employer_information: str = ""
    requirements: str = ""
    work_schedule_working_days: list = None
    work_schedule_time_intervals: list = None
    experience: str = ""
    remote_work: bool = False


# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()


def create_vacancy(vacancy):
    # Создание новой вакансии
    new_vacancy = DB_Vacancy(
        vacancy_id_in_hh=vacancy.vacancy_id_in_hh,
        vacancy_id_in_hc=vacancy.vacancy_id_in_hc,
        vacancy_id_in_sj=vacancy.vacancy_id_in_sj,
        vacancy_id_in_zp=vacancy.vacancy_id_in_zp,
        job_title=vacancy.job_title,
        response_letter_required=vacancy.response_letter_required,
        country=vacancy.country,
        city=vacancy.city,
        district=vacancy.district,
        salary=str(vacancy.salary),
        office_address=vacancy.office_address,
        subway_station=vacancy.subway_station,
        employer_information=vacancy.employer_information,
        requirements=vacancy.requirements,
        work_schedule_working_days=str(vacancy.work_schedule_working_days),
        work_schedule_time_intervals=str(vacancy.work_schedule_time_intervals),
        experience=vacancy.experience,
        remote_work=vacancy.remote_work,
        created_at=datetime.now()  # Устанавливаем текущее время
    )

    # Добавление вакансии в сессию и коммит
    session.add(new_vacancy)
    session.commit()

    print(f"Vacancy created: {new_vacancy.vacancy_id}, Title: {new_vacancy.job_title}")



def getAreas():
    """ Получение названия страны по идентификатору региона. :param area_id: Идентификатор региона.
    :type area_id: str :return: Название страны. :rtype: str """
    req = requests.get('https://api.hh.ru/areas')
    data = req.content.decode()
    req.close()
    jsObj = json.loads(data)
    areas = []
    for k in jsObj:
        for i in range(len(k['areas'])):
            if len(k['areas'][i]['areas']) != 0:
                for j in range(len(k['areas'][i]['areas'])):
                    areas.append([k['id'],
                                  k['name'],
                                  k['areas'][i]['areas'][j]['id'],
                                  k['areas'][i]['areas'][j]['name']])
            else:
                areas.append([k['id'],
                              k['name'],
                              k['areas'][i]['id'],
                              k['areas'][i]['name']])
    return areas


def get_country(area_id):
    """ Получение названия страны по идентификатору региона. Args: area_id
    (str): Идентификатор региона. Returns: Название страны или None, если регион не найден. """
    areas = getAreas()
    for i in areas:
        if i[2] == area_id:
            return i[1]
    return None


file_handler = logging.FileHandler('hh_vacancies', mode='w', encoding='utf-8')
logger.addHandler(file_handler)
#stream_handler = logging.StreamHandler(stream=sys.stdout)
#logger.addHandler(stream_handler)

def get_hh_vacancies(start_date):
    """ Получение списка вакансий с сайта HeadHunter начиная с указанной даты до текущего дня.
    :param start_date: Начальная дата поиска вакансий. :type start_date: datetime
    :return: Список объектов типа Vacancy. :rtype: list """
    file = open('hh_vacancies_for_DB', 'w', encoding="utf-8")
    current_date = start_date
    hh_vacancies = []
    logger.info("Начинаем сбор вакансий с hh.ru")
    while current_date.strftime("%Y-%m-%d") != datetime.today().strftime("%Y-%m-%d"):
        logger.info(f"Собираем объекты вакасний за {str(current_date)}")
        page = 0
        retries = 5
        while True:
            logger.info(f"Текущая страница: {page}")
            params = {"date_from": str(current_date)[:10] + "T" + str(current_date)[11:] + "+0300",
                      "date_to": str(timedelta(hours=1) + current_date)[:10] + "T" + str(timedelta(hours=1) + current_date)[11:] + "+0300",
                      'page': page,
                      'per_page': 100}
            try:
                hh_req = requests.get(hh_vacancies_url, params = params)
            except (Timeout, ConnectionError, ConnectionResetError):
                if retries > 0:
                    retries -= 1
                    logger.warning("Ошибка соединения, повторная попытка через 20 секунд")
                    time.sleep(20)
                else:
                    logger.error("Повторное соединение не удалось, переходим к следующему запросу")
                    break
            except HTTPError as exc:
                if exc.response.status_code == 429:
                    logger.warning("Превышено допустимое число запросов, задержка 20 секунд")
                    time.sleep(20)
                    continue
                logger.error(f"Ошибка {exc.response.status_code}")
                break
            else:
                hh_req_json = hh_req.json()
                try:
                    hh_req_json['items']
                except KeyError:
                    break
                for j in hh_req_json['items']:
                    if j['archived'] == True:
                        continue
                    vacancy = Vacancy(
                        vacancy_id_in_hh = int(j['id']),
                        job_title = j['name'],
                        response_letter_required = j['response_letter_required']
                    )
                    if j['employer'] != None:
                        vacancy.employer_information = j['employer']['name']
                    if j['snippet'] != None:
                        vacancy.requirements = j['snippet']['requirement']
                    if j['schedule'] != None:
                        if j['schedule']['name'] == 'Удалённая работа':
                            vacancy.remote_work = True
                    if j['area'] != None:
                        vacancy.country = get_country(j['area']['id'])
                    if j['address'] != None:
                        vacancy.city = j['address']['city']
                        vacancy.district = j['address']['street']
                        vacancy.office_address = j['address']['raw']
                        if j['address']['metro'] != None:
                            vacancy.subway_station = j['address']['metro']['station_name']
                    if j['experience'] != None:
                        vacancy.experience = j['experience']['name']
                    salary_from = "?"
                    salary_to = "?"
                    currency = "?"
                    if not ((j['salary'] is None) or (j['salary']['from'] is None)):
                        if not j['salary']['from'] == None:
                            salary_from = j['salary']['from']
                        if not j['salary']['to'] == None:
                            salary_to = j['salary']['to']
                        currency = j['salary']['currency']
                    vacancy.salary = str(salary_from) + " " +str(salary_to) + " " + str(currency)
                    hh_vacancies.append(vacancy)
                    create_vacancy(vacancy)
                    update_time(1, datetime.utcnow())
                    file.write(str(j['published_at']) + ": " + str(vacancy) + '\n' + '\n')
                logger.info(f"Текущее количество собранных c hh.ru вакансий: {len(hh_vacancies)}")
            time.sleep(3)
            page += 1
        current_date += timedelta(hours=1)
    logger.info("Сбор вакансий с hh.ru завершён")
    return hh_vacancies

file_handler = logging.FileHandler('sj_vacancies', mode='w', encoding='utf-8')
logger.addHandler(file_handler)

def get_sj_vacancies(start_date):
    """ Получение списка вакансий с сайта Superjob начиная с указанной даты до текущего дня.
    :param start_date: Начальная дата поиска вакансий. :type start_date: datetime
    :return: Список объектов типа Vacancy. :rtype: list """
    current_date = start_date
    sj_vacancies = []
    logger.info("Начинаем сбор вакансий с superjob.ru")
    while current_date.strftime("%Y-%m-%d") != datetime.today().strftime("%Y-%m-%d"):
        logger.info(f"Собираем объекты вакансий за {str(current_date)[:10]}")
        page = 0
        retries = 5
        while True:
            logger.info(f"Текущая страница: {page}")
            params = {"date_published_from": str(int(current_date.timestamp())),
                      "date_published_to": str(int((timedelta(hours=1) + current_date).timestamp())),
                      'page': page,
                      'per_page': 100}
            try:
                sj_req = requests.get(sj_vacancies_url, params = params, headers = sj_headers)
            except (Timeout, ConnectionError):
                if retries > 0:
                    retries -= 1
                    logger.warning("Ошибка соединения, повторная попытка через 20 секунд")
                    time.sleep(20)
                else:
                    logger.error("Повторное соединение не удалось, переходим к следующему запросу")
                    break
            except HTTPError as exc:
                if exc.response.status_code == 429:
                    logger.warning("Превышено допустимое число запросов, задержка 20 секунд")
                    time.sleep(20)
                    continue
                logger.error(f"Ошибка {exc.response.status_code}")
                break
            else:
                sj_req_json = sj_req.json()
                try:
                    sj_req_json['objects']
                except KeyError:
                    print("err KeyErr")
                    break
                for j in sj_req_json['objects']:
                    if j['is_archive'] == True or j['is_closed'] == True or j['is_storage'] == True:
                        continue
                    vacancy = Vacancy(
                        vacancy_id_in_sj = j['id'],
                        job_title = j['profession'],
                        office_address = j['address']
                    )
                    salary_from = "?"
                    salary_to = "?"
                    currency = "?"
                    if not j['payment_from'] == None:
                        salary_from = j['payment_from']
                    if not j['payment_to'] == None:
                        salary_to = j['payment_to']
                    if not j['currency'] == None:
                        currency = j['currency']
                    vacancy.salary = str(salary_from) + " " +str(salary_to) + " " + str(currency)
                    if j['experience'] != None:
                        vacancy.experience = j['experience']['title']
                    if j['town'] != None:
                        vacancy.city = j['town']['title']
                    vacancy.employer_information = j['firm_name']
                    vacancy.requirements = j['candidat']
                    vacancy.subway_station = j['metro']
                    if j['type_of_work'] != None:
                        vacancy.work_schedule_working_days = j['type_of_work']['title']
                    if j['place_of_work'] != None:
                        if j['place_of_work']['title'] == 'Удалённая работа (на дому)':
                            vacancy.remote_work = True
                    sj_vacancies.append(vacancy)
                    create_vacancy(vacancy)
                    update_time(3, datetime.utcnow)
                logger.info(f"Текущее количество собранных с superjob.ru вакансий: {len(sj_vacancies)}")
                #time.sleep(5)
            page += 1
        current_date += timedelta(days=1)
    logger.info("Сбор вакансий с superjob.ru завершён")
    return sj_vacancies

file_handler = logging.FileHandler('hc_vacancies', mode='w', encoding='utf-8')
logger.addHandler(file_handler)

def get_hc_vacancies(start_date):
    """ Получение списка вакансий с сайта Habr карьера начиная с указанной даты до текущего дня.
    :param start_date: Начальная дата поиска вакансий. :type start_date: datetime
    :return: Список объектов типа Vacancy. :rtype: list """
    current_date = start_date
    hc_vacancies = []
    logger.info("Начинаем сбор вакансий с career.habr.ru")
    while current_date.strftime("%Y-%m-%d") != datetime.today().strftime("%Y-%m-%d"):
        logger.info(f"Собираем объекты вакансий за {str(current_date)[:10]}")
        page = 0
        retries = 5
        while True:
            logger.info(f"Текущая страница: {page}")
            params = {"date_published_from": str(int(current_date.timestamp())),
                      "date_published_to": str(int((timedelta(days=1) + current_date).timestamp())),
                      'page': page,
                      'per_page': 100}
            try:
                hc_req = requests.get(hc_vacancies_url, params = params)
            except (Timeout, ConnectionError):
                if retries > 0:
                    retries -= 1
                    logger.warning("Ошибка соединения, повторная попытка через 20 секунд")
                    time.sleep(20)
                else:
                    logger.error("Повторное соединение не удалось, переходим к следующему запросу")
                    break
            except HTTPError as exc:
                if exc.response.status_code == 429:
                    logger.warning("Превышено допустимое число запросов, задержка 20 секунд")
                    time.sleep(20)
                    continue
                logger.error(f"Ошибка {exc.response.status_code}")
                break
            else:
                try:
                    hc_req_json = hc_req.json()
                except json.JSONDecodeError as e:
                    print("Ошибка декодирования JSON:", e)
                    break

                try:
                    hc_req_json['vacancies']
                except KeyError:
                    print("err KeyErr")
                    break
                for j in hc_req_json['vacancies']:
                    if j['published'] == False:
                        continue
                    vacancy = Vacancy(
                        vacancy_id_in_hc=j['id'],
                        job_title = j['title']
                    )
                    if j['expanded_salary']:
                        salary_from = j['expanded_salary']['from']
                        salary_to = j['expanded_salary']['to']
                        currency = j['expanded_salary']['currency']
                        vacancy.salary = [salary_from, salary_to, currency]
                    vacancy.experience = j['candidate']
                    vacancy.city = j['city']
                    if j['company'] != None:
                        vacancy.employer_information = j['company']['name']
                    if j['team'] != None:
                        vacancy.employer_information = j['team']
                    req = ""
                    if j['skills'] != None:
                        for skill in j['skills']:
                            req += (skill['name'])
                    vacancy.requirements = req
                    vacancy.remote_work = j['remote']
                    hc_vacancies.append(vacancy)
                    create_vacancy(vacancy)
                    update_time(2, datetime.utcnow)
                logger.info(f"Текущее количество собранных с career.habr.ru вакансий: {len(hc_vacancies)}")
                #time.sleep(5)
            page += 1
        current_date += timedelta(days=1)
    logger.info("Сбор вакансий с career.habr.ru завершён")
    return hc_vacancies

zarplata_vacancies_url = "https://api.zarplata.ru/vacancies"
hh_vacancies_url = "https://api.hh.ru/vacancies/"
sj_vacancies_url = "https://api.superjob.ru/2.0/vacancies/"
hc_vacancies_url = "https://career.habr.com/api/v1/vacancies"


sj_headers = {'X-Api-App-Id' : 'v3.r.138675629.1b08282275f198c10779eb794c1e45919b231c2b.f7d459dd38d21c4693828ee2248cc1128d62e5f1',
          'Content-Type': 'application / x - www - form - urlencoded'}


sj_req = requests.get(sj_vacancies_url, headers=sj_headers)
zarplata_req = requests.get(zarplata_vacancies_url)
hh_req = requests.get(hh_vacancies_url)

get_hh_vacancies(datetime(2025, 4, 17))


session.close()