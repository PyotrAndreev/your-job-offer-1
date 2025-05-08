import numpy as np
import re
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pymorphy2 import MorphAnalyzer

# from sklearn import feature_extraction
import torch
from dataclasses import dataclass
# from sklearn.metrics.pairwise import cosine_similarity

from side_files.create_users import get_all_vacancies, get_resume
from nn_helper import tokenizer, model

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt_tab')

vacancies = get_all_vacancies()
print(len(vacancies))
for vacancy in vacancies:
    print(vacancy.country)
resume_tmp = get_resume()


@dataclass
class Resume_res:
    resume_id: int
    user_id: int
    title: str = ""
    job_title: str = ""
    country: str = ""
    city: str = ""
    district: str = ""
    salary: int = 0
    work_schedule_working_days: list = None
    work_schedule_time_intervals: list = None
    experience: int = 0
    remote_work: bool = False
    education: str = ""
    additional_information: str = ""


@dataclass
class Vacancy_res:
    """Класс для хранения информации о вакансиях."""
    vacancy_id: int
    job_title: str
    response_letter_required: bool = False
    country: str = ""
    city: str = ""
    district: str = ""
    salary: list = None
    office_address: str = ""
    subway_station: str = ""
    employer_information: str = ""
    requirements: str = ""
    work_schedule_working_days: list = None
    work_schedule_time_intervals: list = None
    experience: str = ""
    remote_work: bool = False


def make_resume(resume):
    if resume == None:
        return
    new_resume = Resume_res(resume_id=resume.resume_id,
                            uer_id=resume.user_id,
                            title=str(resume.title),
                            job_title=str(resume.job_title),
                            country=str(resume.country),
                            district=str(resume.district),
                            salary=resume.min_salary,
                            experience=str(resume.experience),
                            additional_information=str(resume.additional_information),
                            education=str(resume.education),
                            remote_work=resume.remote_work)
    return new_resume


def make_vacancy(vacancies):
  hh_vacancies = []
  for vacancy in vacancies:
    new_vacancy = Vacancy_res(vacancy_id = vacancy.vacancy_id,
                              job_title = str(vacancy.job_title),
                              response_letter_required = vacancy.response_letter_required,
                              country = str(vacancy.country),
                              city = str(vacancy.city),
                              district = str(vacancy.district),
                              office_address = str(vacancy.office_address),
                              subway_station = str(vacancy.subway_station),
                              employer_information = str(vacancy.employer_information),
                              requirements = str(vacancy.requirements),
                              experience = str(vacancy.experience),
                              remote_work = vacancy.remote_work)
    hh_vacancies.append(new_vacancy)
  return hh_vacancies

vacancies = make_vacancy(vacancies)


resume = make_resume(resume_tmp)


def clean(word):
    return re.sub(r"[^A-ZА-Яa-zа-я+\s]", "", word)


stop_words = stopwords.words('russian') + ["опыт",
                                           "навык",
                                           "знание",
                                           "понимание",
                                           "работа",
                                           "умение",
                                           "большой",
                                           "хороший",
                                           "прикладной",
                                           "некоторый",
                                           "небольшой"]


def tokenize_text(text):
    if text == None:
        return
    text = text.lower()
    text = text.translate(
        str.maketrans(punctuation, " " * len(punctuation))
    )
    word_tokens = word_tokenize(text)
    word_tokens = [clean(word) for word in word_tokens]
    morph = MorphAnalyzer()
    lemmatize_words = [morph.normal_forms(word)[0] for word in word_tokens]
    filtered_tokens = [word for word in lemmatize_words if word not in stop_words]
    return filtered_tokens


def get_word_embeddings(words):
    inputs = tokenizer(words, padding=True, truncation=True, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model(**inputs)
    last_hidden_states = outputs.last_hidden_state
    embeddings = last_hidden_states[:, 0, :].cpu().numpy()
    return embeddings


def cosine_similarity(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return float(dot_product / (norm_a * norm_b))


def check_vacancy(requirements, skills):
    tok_req = tokenize_text(requirements)
    tok_skills = tokenize_text(skills)
    print(tok_req)
    print(tok_skills)
    if tok_req == None or tok_skills == None:
        return False
    for i in tok_req:
        for j in tok_skills:
            if str(i) == str(j):
                return True
    return False


def match_skills_and_requirements(requirements, skills):
    if requirements == None or skills == None:
        return 0
    emb_requirements = get_word_embeddings(requirements)
    emb_skills = get_word_embeddings(skills)
    similarity = 0
    max_similarity = 0
    for i in emb_requirements:
        for j in emb_skills:
            similarity += cosine_similarity(i, j)
            max_similarity += 1
    return similarity / max_similarity


currency = {'RUB': 1,
            'BYN': 31.05,
            'KZT': 0.19,
            'AMD': 0.25,
            'KGS': 1.16,
            'MDL': 5.5,
            'TJS': 9.22,
            'UZS': 0.0078}


def match_vacancies(vacancies, resume):
    similarity_with_vacancies = {}
    idx = 0
    for vacancy in vacancies:
        similarity = 0
        idx += 1
        if resume.country != "" and vacancy.country != "" and vacancy.country != resume.country:
            continue
        if resume.city != "" and vacancy.city != "" and vacancy.city != resume.city:
            continue
        if vacancy.remote_work == False and resume.remote_work == True:
            continue
        if check_vacancy(vacancy.requirements, resume.additional_information) == False:
            print(1)
            continue
        if vacancy.salary != None and vacancy.salary[0] != None and vacancy.salary[2] in currency:
            if vacancy.salary[1] != None and resume.salary * 0.9 <= vacancy.salary[1] * currency[vacancy.salary[2]]:
                similarity += 0.1
            elif vacancy.salary[1] == None and resume.salary * 1.1 >= vacancy.salary[0] * currency[vacancy.salary[2]]:
                similarity += 0.1
        experience_min = 0
        if vacancy.experience == 'От 1 года до 3 лет':
            experience_min = 1
        elif vacancy.experience == 'От 3 до 6 лет':
            experience_min = 3
        elif vacancy.experience == 'Более 6 лет':
            experience_min = 6
        if resume.experience >= experience_min:
            similarity += 0.1
        similarity += match_skills_and_requirements(vacancy.requirements, resume.additional_information)
        similarity += match_skills_and_requirements(vacancy.job_title, resume.job_title)
        if similarity in similarity_with_vacancies:
            similarity_with_vacancies[similarity].append(vacancy)
        else:
            similarity_with_vacancies[similarity] = [vacancy]
        print(len(similarity_with_vacancies))
    return sorted(similarity_with_vacancies)


resume = Resume_res(resume_id=1,
                user_id=1,
                additional_information="эскиз")
print(resume.country)
sim = match_vacancies(vacancies[:100], resume)
sim = sorted(sim, reverse=True)
num = 10
print(sim[:num])
