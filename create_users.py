from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import User, engine, Vacancy
import json
# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

def create_user(user_id, name, email, phone):
    # Создание нового пользователя
    new_user = User(
        user_id = user_id,
        name=json.dumps(name),  # Сохраняем имя в формате JSON
        email=json.dumps(email),  # Сохраняем email в формате JSON
        phone=phone,
        created_at=datetime.now()  # Устанавливаем текущее время
    )
    
    # Добавление пользователя в сессию и коммит
    session.add(new_user)
    session.commit()
    
    print(f"User created: {new_user.user_id}, Name: {new_user.name}")
# create_user(5, "name1", "email1", 23423)
def get_all_users():
    users = session.query(User).all()
    return users

# Пример использования
all_users = get_all_users()
for user in all_users:
    print(user)

def get_all_vacancies():
    vacancies = session.query(Vacancy).all()
    return vacancies

# Пример использования
all_vacancies = get_all_vacancies()
for vacancy in all_vacancies:
    print(vacancy.job_title)


session.close()

