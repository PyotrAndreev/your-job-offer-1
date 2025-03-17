# Шаг 1: Установка зависимостей и сборка проекта
# Используем официальный образ Node.js в качестве базового для сборки
FROM node:18 AS build

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем package.json и package-lock.json в контейнер
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем весь исходный код проекта
COPY . .

# Строим проект
RUN npm run build

# Шаг 2: Настройка веб-сервера для обслуживания статики
# Используем официальный образ Nginx
FROM nginx:alpine

# Копируем собранные статические файлы из предыдущего шага
COPY --from=build /app/dist /usr/share/nginx/html

# Копируем конфигурацию Nginx
COPY --from=build /app/nginx.conf /etc/nginx/conf.d/default.conf


# Открываем порт 3000 для доступа к приложению
EXPOSE 3000

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
