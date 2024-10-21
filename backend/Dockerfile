FROM python:3.12-slim AS backend-build

WORKDIR /app

# Устанавливаем необходимые системные пакеты
#RUN apt-get update && apt-get install -y gcc libffi-dev

# Копируем файл зависимостей и устанавливаем их
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы бэкенда
COPY backend/ .

# Stage 3: Final container
FROM nginx:alpine

# Копируем конфигурационный файл Nginx
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Копируем статические файлы фронтенда в Nginx
COPY frontend/ /usr/share/nginx/html

# Копируем файлы бэкенда
COPY --from=backend-build /app /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Порт для Nginx
EXPOSE 80

# Запуск backend (FastAPI через __main__.py), Telegram-бота и Nginx
CMD ["sh", "-c", "python __main__.py & python app/bot.py & nginx -g 'daemon off;'"]
