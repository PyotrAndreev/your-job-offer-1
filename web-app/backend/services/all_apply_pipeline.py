from new_matcher import search_vacancies_for_user
from db_functions import get_hh_access_token
from hhru_api import get_users_last_resume_id, apply_for_vacancy

user_id = 1 # Настоящее значение передается от фронта
count_of_vacancies = 7 # Настоящее значение передается от фронта

list_of_best_vacancies = search_vacancies_for_user(user_id, count_of_vacancies)
job_titles = [lst[2] for lst in list_of_best_vacancies]
vacancies_id = [lst[1] for lst in list_of_best_vacancies]

# Можно возвращать фронту эти списки, дальше будет подача

access_token = get_hh_access_token(user_id)

resume_id = get_users_last_resume_id(access_token)
# Оказалось, мы вообще не храним resume_id и даже не заполняем его, пока можно взять последнее resume пользователя

for vacancy_id in vacancies_id:
	apply_for_vacancy(access_token, resume_id, vacancy_id)
	create_submission(resume_id, "started", datetime.now(), vacancy_id)
