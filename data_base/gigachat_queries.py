import os
import json
import re
from gigachat import GigaChat
from dotenv import load_dotenv
import requests
import openai

load_dotenv()


# Initialize GigaChat once
model = GigaChat(
    credentials=auth_key,
    scope="GIGACHAT_API_PERS",
    model="GigaChat-Max",
    verify_ssl_certs=False
)


# Function to Query GigaChat
def query_gigachat(vacancy_title):
    try:
        prompt = """
        Пожалуйста, определи область деятельности, к которой относится данная вакансия 
        с учётом следующих категорий. (ответ выведи СТРОГО на английском)
        Вот области, среди которых нужно выбрать одну, наиболее подходящую под описание:
        
        Frontend Developer
        Backend Developer
        Mobile Developer
        Fullstack Developer
        DevOps Engineer
        Data Scientist
        QA Engineer
        Cybersecurity Specialist
        Game Developer
        System Administrator
        ML Engineer
        Database Administrator
        Infrastructure Architect
        Data Analyst
        Big Data Specialist
        Embedded Software Developer
        Business Analyst
        Cloud Platform Developer
        Blockchain Developer
        API Designer
        Other
        
        Не добавляй никакого дополнительного текста перед или после указания области.
        
        Если описание вакансии не относится ни к одной области из предложенных,
        то выведи Other.
        Ответ должен быть только областью из категории или Other, не нужно
        добавлять области, соответствующие вакансии, если их нет в предложенном списке.
        
        Все ответы выводи на английском языке, в точности как представлено в списке  
        
        Описание вакансии:
        """ + vacancy_title

        print("Sending request to GigaChat...")
        answer = model.chat(prompt)
        raw_data = str(answer)
        start_idx = raw_data.find('content=\'') + len('content=\'')
        end_idx = raw_data.find('\'', start_idx)

        content = raw_data[start_idx:end_idx]
        print(vacancy_title, content)
        print("Response received from GigaChat.")
        return content
    except Exception as e:
        raise ValueError(f"Error querying GigaChat: {e}")


# Main Script to Test the Query
if __name__ == "__main__":
    try:
        answer = query_gigachat('Анализ и обработка данных для обучения моделей')
        print(answer)
    except Exception as e:
        print(f"Error: {e}")
