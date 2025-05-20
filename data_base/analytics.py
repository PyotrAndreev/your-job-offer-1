import time
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
import matplotlib.pyplot as plt
import textwrap


from data_base.db_functions import get_all_vacancies
from gigachat_queries import query_gigachat

currency = {'RUB': 1,
            'BYN': 31.05,
            'KZT': 0.19,
            'AMD': 0.25,
            'KGS': 1.16,
            'MDL': 5.5,
            'TJS': 9.22,
            'UZS': 0.0078}

vacancies = get_all_vacancies()
data = [(vacancy.job_title, float(vacancy.salary.split()[0]) * currency[vacancy.salary.split()[2]],
         vacancy.requirements) for vacancy in vacancies
        if (vacancy.salary.split()[0] != "?" and vacancy.salary.split()[2] in currency)]
## print(data)

stop_words = set(stopwords.words('russian'))


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text


data = [(vacancy[0], vacancy[1], vacancy[2]) for vacancy in data]

vacancy_categories = {
    "Frontend Developer" : [],
    "Backend Developer" : [],
    "Mobile Developer" : [],
    "Fullstack Developer" : [],
    "DevOps Engineer" : [],
    "Data Scientist" : [],
    "QA Engineer" : [],
    "Cybersecurity Specialist" : [],
    "Game Developer" : [],
    "System Administrator" : [],
    "ML Engineer" : [],
    "Database Administrator" : [],
    "Infrastructure Architect" : [],
    "Data Analyst" : [],
    "Big Data Specialist" : [],
    "Embedded Software Developer" : [],
    "Business Analyst" : [],
    "Cloud Platform Developer" : [],
    "Blockchain Developer" : [],
    "API Designer" : [],
    "Other" : []
}

for vacancy in data:
    category = query_gigachat(vacancy[0])
    try:
        vacancy_categories[category].append(vacancy)
    except KeyError:
        continue
    time.sleep(1)


average_salaries = {}
median_salaries = {}
for category, vacancies in vacancy_categories.items():
    salaries = [vacancy[1] for vacancy in vacancies if vacancy[1] is not None]
    if salaries:

        average_salaries[category] = np.mean(salaries)
        median_salaries[category] = np.median(salaries)

categories = list(average_salaries.keys())
average_values = list(average_salaries.values())
median_values = list(median_salaries.values())
x = np.arange(len(categories))
width = 0.35
fig, ax = plt.subplots()
bars1 = ax.bar(x - width/2, average_values, width, label='Средняя зарплата', color='skyblue')
bars2 = ax.bar(x + width/2, median_values, width, label='Медианная зарплата', color='navy')
for bar in bars1:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{round(yval)}', ha='center', va='bottom', fontsize=4)
for bar in bars2:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, f'{round(yval)}', ha='center', va='bottom', fontsize=4)
ax.set_ylabel('Зарплата (руб. в месяц)')
ax.set_title('Средняя и медианная зарплаты по категориям')
ax.set_xticks(x)
max_label_width = 15
wrapped_labels = []
for label in categories:
    wrapped = textwrap.fill(label, max_label_width)
    wrapped_labels.append(wrapped)
ax.set_xticklabels(wrapped_labels, rotation=0, ha='center', fontsize=4)
ax.margins(y=0.1)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), ncol=2)
plt.tight_layout()
plt.show()