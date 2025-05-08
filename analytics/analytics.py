import nltk
from nltk.corpus import stopwords
import re
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from data_base.db_functions import get_all_vacancies

vacancies = get_all_vacancies()
data = [(vacancy.job_title, vacancy.salary, vacancy.requirements) for vacancy in vacancies]
## print(data)

nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

data = [(preprocess_text(vacancy[0]), vacancy[1], vacancy[2]) for vacancy in data][:1000]
##print(data[:10])

df = pd.DataFrame([vacancy[0] for vacancy in data], columns=['job_title'])

vectorizer = TfidfVectorizer()
vectorized_titles = vectorizer.fit_transform(df['job_title']).toarray()

sse = []
for k in range(1, len(data), 100):
    print(f"Current num of clusters: {k}")
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(vectorized_titles)
    sse.append(kmeans.inertia_)

plt.plot(range(1, int(len(data) / 100) + 1), sse, marker='o')
plt.title('Метод "Локтя"')
plt.xlabel('Количество кластеров')
plt.ylabel('Сумма квадратов расстояний')
plt.show()
