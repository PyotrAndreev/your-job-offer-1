from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import engine, User, Vacancy, Resume, Tokens, Submission
from sqlalchemy import func, and_

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

## функция добавления нового пользователя в базу данных
def create_user(name, sex, age, email, phone, password_hash):
    new_user = User(
        name=name,
        sex=sex,
        age=age,
        email=email,
        phone=phone,
        password_hash=password_hash,
        created_at=datetime.now()
    )
    session.add(new_user)
    session.commit()
    print(f"User created: {new_user.user_id}, Name: {new_user.name}")

## функция для получения списка всех пользователей, хранящихся в бд
def get_all_users():
    users = session.query(User).all()
    return users

## функция для получения списка всех вакансий, хранящихся в бд
def get_all_vacancies():
    vacancies = session.query(Vacancy).all()
    return vacancies

## функция для получения пользователя по id
def get_user(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    return user

## по email проверяет наличие пользователя
def exist_user(email):
    user = session.query(User).filter(User.email == email).first()
    return user is not None

## всякие функции для обновления информации о пользователе
def update_user_name(user_id, new_name):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.name = new_name

def update_user_sex(user_id, new_sex):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.sex = new_sex

def update_user_age(user_id, new_age):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.age = new_age

def update_user_phone(user_id, new_phone):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.phone = new_phone

def update_user_email(user_id, new_email):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.email = new_email

def update_user_pass(user_id, new_pass):
    user = session.query(User).filter(User.user_id == user_id).first()
    user.password_hash = new_pass

def delete_user(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} удалён.")
        return True
    else:
        print(f"Пользователь с ID {user_id} не найден.")
        return False

## получение хэша пароля по айдишнику пользователя
def get_hash(user_id):
    user = session.query(User).filter(User.user_id == user_id).first()
    return user.password_hash

## получение айдишника пользователя по хэшу и почте
def get_user_by_mail(email):
    user = session.query(User).filter(
        and_(User.email == email)).first()
    if user == None:
        return None
    return {hash: user.password_hash, id: user.user_id}

## функция для получения вакансии по id
def get_vacancy(vacancy_id):
    vacancy = session.query(Vacancy).filter(Vacancy.vacancy_id == vacancy_id).first()
    return vacancy

## функция добавления нового отклика в базу данных
def create_submission(resume_id, status, sent_at, vacancy_id):
    new_submission = Submission(
        resume_id=resume_id,
        status=status,
        sent_at=sent_at,
        vacancy_id=vacancy_id,
        created_at=datetime.now()
    )
    session.add(new_submission)
    session.commit()
    print(f"User created: {new_submission.submission_id}, Vacancy_id: {new_submission.vacancy_id}, Resume_id: {new_submission.resume_id}")

## функция для обновления статуса отклика
def update_status(submission_id, new_status):
    submission = session.query(Submission).filter(Submission.submission_id == submission_id).first()
    submission.status = new_status

## функция добавления нового резюме в базу данных
def create_resume(user_id, title, job_title, country, city, district, min_salary, max_salary,
                  work_schedule_working_days, work_schedule_time_intervals,
                  experience, remote_work, education, skills):
    new_resume = Resume(
        user_id=user_id,
        title=title,
        job_title=job_title,
        country=country,
        city=city,
        district=district,
        min_salary=min_salary,
        max_salary=max_salary,
        work_schedule_working_days=work_schedule_working_days,
        work_schedule_time_intervals=work_schedule_time_intervals,
        experience=experience,
        remote_work=remote_work,
        education=education,
        skills=skills
    )
    session.add(new_resume)
    session.commit()
    print(f"Resume created: {new_resume.resume_id}, Title: {new_resume.title}")

## функция для получения резюме по id пользователя
def get_resume(user_id):
    resume = session.query(Resume).filter(Resume.user_id == user_id).first()
    return resume

## функция для сохранения токенов пользователя в бд
def add_tokens(user_id, refresh_token, access_token):
    new_tokens = Tokens(
        user_id=user_id,
        refresh_token=refresh_token,
        access_token=access_token
    )
    session.add(new_tokens)
    session.commit()

## функция для обновления токенов
def refresh_tokens(tokens_id, new_refresh, new_access):
    tokens = session.query(Tokens).filter(Tokens.tokens_id == tokens_id).first()
    tokens.refresh_token = new_refresh
    tokens.access_token = new_access

## функция получения аксес токена по айдишнику пользователя
def get_hh_access_token(user_id):
    tokens = session.query(Tokens).filter(Tokens.user_id == user_id).scalar()
    if tokens == None:
        return None
    return tokens.access_token

## функция получения последнего добавленного пользователя (его айдишника)
def get_last_user_id():
  last_id = session.query(func.max(User.user_id)).scalar()
  return last_id


session.close()
