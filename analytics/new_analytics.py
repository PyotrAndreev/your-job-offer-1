"""Объяснение категорий

Web Development: Включает в себя разработку веб-приложений и интерфейсов.

Mobile Development: Включает в себя создание мобильных приложений для различных платформ.

Data Science: Включает в себя анализ данных и работу с большими данными.

Game Development: Включает в себя разработку игр на различных платформах.

Project Management: Включает в себя управление проектами в IT.

Frontend Development: Включает в себя разработку пользовательских интерфейсов.

Backend Development: Включает в себя разработку серверной части приложений.

Database Administration: Включает в себя работу с базами данных.

Embedded Systems: Включает в себя разработку программного обеспечения для встраиваемых систем.

Software Testing: Включает в себя тестирование программного обеспечения.

Cloud Computing: Включает в себя разработку облачных решений.

Chatbot Development: Включает в себя создание чат-ботов.

Big Data: Включает в себя работу с большими данными.

Machine Learning: Включает в себя разработку систем машинного обучения.

DevOps: Включает в себя управление процессами DevOps и CI/CD.

Cybersecurity: Включает в себя разработку систем кибербезопасности.

Data Analytics: Включает в себя анализ данных и нахождение зависимостей"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
import re


# Функция нормализации текста
def normalize_text(text):
    # Приводим текст к нижнему регистру
    text = text.lower()

    # Токенизация текста
    tokens = word_tokenize(text)

    # Лемматизация
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(w) for w in tokens]

    # Удаление стоп-слов и знаков препинания
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word for word in tokens if word not in stopwords.words('english')]

    return ' '.join(tokens)


# Исходные данные
data = {
    'job_description': [
        'Development of web applications using Python and Django framework.',
        'Creating mobile applications with Java for Android devices.',
        'Analyzing data using Python libraries like Pandas and NumPy.',
        'Developing games using C# programming language and Unity engine.',
        'Project management following Agile methodologies.',
        'Building user interfaces with JavaScript and React library.',
        'Designing RESTful APIs using Node.js backend technology.',
        'Creating databases and optimizing queries with SQL.',
        'Programming embedded systems using C++ language.',
        'Testing software quality with Selenium tool.',
        'Implementing cloud solutions on the AWS platform.',
        'Developing chatbots using Python and natural language processing tools.',
        'Processing big data with Apache Spark.',
        'Front-end development with Vue.js framework.',
        'Training machine learning models with TensorFlow.',
        'Building web applications with Ruby on Rails.',
        'Handling DevOps processes including CI/CD pipelines.',
        'Creating dynamic websites with PHP and Laravel framework.',
        'Developing games using Java and LibGDX game engine.',
        'Ensuring cybersecurity measures to protect sensitive information.',
        'Business intelligence reporting with Excel and Power BI.'
    ],
    'category': [
        'Web Development',
        'Mobile Development',
        'Data Science',
        'Game Development',
        'Project Management',
        'Frontend Development',
        'Backend Development',
        'Database Administration',
        'Embedded Systems',
        'Software Testing',
        'Cloud Computing',
        'Chatbot Development',
        'Big Data',
        'Frontend Development',
        'Machine Learning',
        'Web Development',
        'DevOps',
        'Web Development',
        'Game Development',
        'Cybersecurity',
        'Data Analytics'
    ]
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Нормализуем текст
df['normalized_job_description'] = df['job_description'].apply(normalize_text)

# Создаем TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['normalized_job_description'])
y = df['category']

# Разбивка на тренировочный и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Выбор модели и настройка гиперпараметров
models = [
    {'name': 'Logistic Regression', 'estimator': LogisticRegression()},
    {'name': 'Random Forest', 'estimator': RandomForestClassifier()},
    {'name': 'Gradient Boosting', 'estimator': GradientBoostingClassifier()}
]

best_params = {}
for model in models:
    print(f"\n\nOptimizing {model['name']}...")
    param_grid = {
        'C': [0.1, 1, 10],  # Параметр регуляризации для LR
        'solver': ['lbfgs', 'liblinear'],  # Метод оптимизации для LR
        'n_estimators': [50, 100, 200],  # Количество деревьев для RF и GB
        'max_depth': [None, 10, 20],  # Максимальная глубина дерева
        'min_samples_leaf': [1, 2, 4],  # Минимальное число образцов в листовом узле
    }

    grid_search = GridSearchCV(model['estimator'], param_grid, cv=StratifiedKFold(n_splits=2), scoring='accuracy')
    grid_search.fit(X_train, y_train)

    best_params[model['name']] = grid_search.best_params_
    print(f"Best parameters found: {grid_search.best_params_}")

# Тренировка лучших моделей с найденными гиперпараметрами
best_models = []
for model in models:
    estimator = model['estimator'].set_params(**best_params.get(model['name']))
    estimator.fit(X_train, y_train)
    best_models.append((model['name'], estimator))

# Тестирование всех моделей
for name, model in best_models:
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred)
    print(f'\nPerformance of {name}:\n{report}')

new_data = [
    # Web Development
    'Создание адаптивных веб-сайтов с использованием HTML, CSS и JavaScript',
    'Разработка SPA приложений на Angular',
    'Оптимизация производительности веб-приложений на React',

    # Mobile Development
    'Разработка кроссплатформенных мобильных приложений на Flutter',
    'Создание приложений для iOS с использованием Swift',
    'Разработка игр для мобильных устройств на Unity',

    # Data Science
    'Построение предсказательных моделей с использованием машинного обучения',
    'Анализ данных с помощью Python и библиотек Scikit-learn',
    'Визуализация данных с использованием Matplotlib и Seaborn',

    # Game Development
    'Создание 2D игр на C# с использованием Unity',
    'Разработка многопользовательских игр на Unreal Engine',
    'Оптимизация игровых механик и производительности',

    # Project Management
    'Управление проектами в IT с использованием Scrum',
    'Координация команды разработчиков и тестировщиков',
    'Планирование и контроль сроков выполнения проектов',

    # Frontend Development
    'Разработка пользовательских интерфейсов с использованием Vue.js',
    'Создание интерактивных элементов на веб-страницах с помощью jQuery',
    'Оптимизация UX/UI для повышения удобства использования',

    # Backend Development
    'Разработка серверной части приложений на Python с использованием Flask',
    'Создание микросервисов на Java с использованием Spring Boot',
    'Оптимизация баз данных и написание сложных SQL-запросов',

    # Database Administration
    'Управление реляционными базами данных на PostgreSQL',
    'Настройка резервного копирования и восстановления данных',
    'Оптимизация производительности запросов в MySQL',

    # Embedded Systems
    'Разработка программного обеспечения для встраиваемых систем на C',
    'Создание прошивок для микроконтроллеров',
    'Оптимизация работы устройств IoT',

    # Software Testing
    'Автоматизация тестирования веб-приложений с использованием Selenium',
    'Проведение функционального и регрессионного тестирования',
    'Разработка тестовых сценариев и документации',

    # Cloud Computing
    'Разработка облачных приложений на Azure',
    'Настройка CI/CD процессов для облачных решений',
    'Оптимизация затрат на облачные ресурсы',

    # Chatbot Development
    'Создание чат-ботов для мессенджеров с использованием Python',
    'Интеграция NLP для улучшения взаимодействия с пользователями',
    'Разработка сценариев общения для чат-ботов',

    # Big Data
    'Обработка и анализ больших данных с использованием Hadoop',
    'Создание ETL процессов для загрузки данных в хранилище',
    'Оптимизация работы с данными в Apache Spark',

    # Machine Learning
    'Разработка моделей машинного обучения для предсказания',
    'Обучение нейронных сетей с использованием Keras',
    'Анализ и обработка данных для обучения моделей',

    # DevOps
    'Настройка инфраструктуры как кода с использованием Terraform',
    'Автоматизация развертывания приложений с помощью Ansible',
    'Мониторинг и логирование приложений в облаке',

    # Cybersecurity
    'Аудит безопасности веб-приложений и систем',
    'Разработка систем защиты от DDoS атак',
    'Проведение тестов на проникновение и анализ уязвимостей',

    # Data Analytics
    'Анализ бизнес-данных с использованием Power BI',
    'Создание отчетов и дашбордов для визуализации данных',
    'Проведение A/B тестирования для оптимизации бизнес-процессов'
]

'''new_X = vectorizer.transform(new_data)

predictions = model.predict(new_X)
for description, category in zip(new_data, predictions):
    print(f'Описание: "{description}" -> Область: {category}')'''