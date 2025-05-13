from rapidfuzz import fuzz
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from database.db_functions import get_all_vacancies, get_resume

# Cache for exchange rates to avoid repeated API calls
@lru_cache(maxsize=32)
def get_rate(currency_code):
    api_key = '7bee4100c63bb001f46aa891'
    try:
        response = requests.get(
            f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency_code}',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        return int(data['conversion_rates']['RUB'])  # Changed to RUB (ISO code)
    except (requests.RequestException, ValueError, KeyError):
        return 1  # Fallback to 1:1 for RUB or failed requests

def normalize_text(text):
    return text.lower() if text else ""

def lev_check(text, target):
    return fuzz.partial_ratio(normalize_text(text), normalize_text(target)) / 100

def match_skills_and_requirements(requirements, skills):
    if not requirements or not skills:
        return 0
    return sum(lev_check(requirements, skill) for skill in skills)

def process_salary(salary_str, min_salary):
    if not salary_str:
        return 0
    
    parts = salary_str.split()
    if len(parts) < 3 or parts[0] == "?" or parts[2] == "?":
        return 0
    
    currency = 'RUB' if parts[2] == 'RUR' else parts[2]
    rate = get_rate(currency)
    
    try:
        if parts[1] != "?":
            salary_value = int(parts[1]) * rate
            return 2 if min_salary * 0.9 <= salary_value else 0
        else:
            min_vacancy_salary = int(parts[0]) * rate
            return 2 if min_vacancy_salary >= min_salary * 1.1 else 0
    except (ValueError, IndexError):
        return 0

def process_vacancy(vacancy, resume):
    if not resume:
        return 0, vacancy.vacancy_id, vacancy.job_title, vacancy.vacancy_id_in_hh
    
    similarity = 0
    
    # Salary matching
    similarity += process_salary(vacancy.salary, resume.min_salary)
    
    # Skills matching
    if vacancy.requirements:
        similarity += match_skills_and_requirements(vacancy.requirements, resume.skills)
    
    # Job title matching
    job_title = normalize_text(vacancy.job_title)
    similarity += match_skills_and_requirements(job_title, resume.skills)
    similarity += match_skills_and_requirements(job_title, resume.job_title)
    
    return similarity, vacancy.vacancy_id, job_title, vacancy.vacancy_id_in_hh

def search_vacancies_for_user(user_id, num_of_vacancies=5):
    vacancies = get_all_vacancies()
    if not vacancies:
        return []
    
    resume = get_resume(user_id)
    if not resume:
        return []
    
    # Process vacancies in parallel
    with ThreadPoolExecutor(max_workers=min(40, len(vacancies))) as executor:
        results = list(executor.map(lambda v: process_vacancy(v, resume), vacancies))
    
    # Sort by similarity and return top N
    results.sort(key=lambda x: x[0], reverse=True)
    return results[:int(num_of_vacancies)]