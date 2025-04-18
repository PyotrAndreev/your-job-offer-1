from rapidfuzz import fuzz
import requests
from concurrent.futures import ThreadPoolExecutor
import heapq

from db_functions import get_all_vacancies, get_resume, create_resume


## модель: на вход принимаем айдишник пользователя -> находим в бд его резюме (если есть) ->
## по его скиллам ищем при помощи метрики Левенштайна наиболее подходящие вакансии + чекаем по другим критериям

## функция для поиска похожих на target слов в text при помощи сходства по Левенштайну
def lev_check(text, target):
    return fuzz.partial_ratio(text.lower(), target.lower()) / 100


## функция сопоставления скиллов пользователя и описания вакансии
def match_skills_and_requirements(requirements, skills):
    if requirements == None or skills == None:
        return 0
    similarity = 0
    for skill in skills:
        similarity += lev_check(requirements, skill.lower())
    return similarity


## получение текущего курса для перевода в рубли
def get_rate(currency_code):
    api_key = '7bee4100c63bb001f46aa891'
    response = requests.get(f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_code}')
    if response.ok:
        data = response.json()
        rate = int(data['conversion_rates']['RUB'])
        return rate
    else:
        return 0

## подбора вакансии по различным параметрам (место, зп, скиллы)
def process_vacancy(vacancy, resume):
    skills = resume.skills
    similarity = 0
    if vacancy.salary and vacancy.salary.split()[0] != "?":
        salary = vacancy.salary.split()
        if salary[2] != "?":
            if salary[2] == 'RUR':
                salary[2] = 'RUB'
            rate = get_rate(salary[2])
            if salary[1] != "?" and resume.min_salary * 0.9 <= int(salary[1]) * rate:
                similarity += 2
            elif salary[1] == "?" and resume.min_salary * 1.1 >= int(salary[0]) * rate:
                similarity += 2
    if vacancy.requirements:
        requirements = vacancy.requirements.lower()
        similarity += match_skills_and_requirements(requirements, skills)
    job_title = vacancy.job_title.lower()
    similarity += match_skills_and_requirements(job_title, skills)
    return similarity, vacancy.vacancy_id, vacancy.job_title


## итоговая функция подбора вакансий с использованием нескольких потоков
def search_vacancies_for_user(user_id, num_of_vacancies):
    vacancies = get_all_vacancies()
    best_vacancies = []
    with ThreadPoolExecutor(max_workers=40) as executor:
        resume = get_resume(user_id)
        for vacancy in executor.map(lambda vacancy: process_vacancy(vacancy, resume), vacancies):
            similarity, vacancy_id, job_title = vacancy
            if len(best_vacancies) < num_of_vacancies:
                best_vacancies.append((similarity, vacancy_id, job_title))
            else:
                min_similarity_index = min(range(len(best_vacancies)), key=lambda i: best_vacancies[i][0])
                if similarity > best_vacancies[min_similarity_index][0]:
                    best_vacancies[min_similarity_index] = (similarity, vacancy_id, job_title)
    return best_vacancies

""" print(1)
create_resume(1, "", "", "", "", "", 100000, 0,
                  "", "",
                  "", False, "", ['C++', 'Linux', 'Python', 'Go', 'Разработчик', 'IT'])
print(2)
create_resume(2, "", "", "", "", "", 0, 0,
              "", "",
              "", False, "", ['курьер', 'доставка'])
print(3)
create_resume(3, "", "", "", "", "", 0, 0,
              "", "",
              "", False, "", ['пирсинг', 'тату-мастер']) """

print(search_vacancies_for_user(1, 5))
