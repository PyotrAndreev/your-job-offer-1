# Используем официальный образ Python 3.9 в качестве базового
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей requirements.txt в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения в контейнер
COPY . /app/

# Открываем порт, который будет использоваться FastAPI (по умолчанию 8000)
EXPOSE 8000

# Команда для запуска приложения с помощью Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]