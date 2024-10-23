# Используем базовый Python образ
FROM python:3.12-slim

# Устанавливаем рабочий каталог
WORKDIR /app

# Устанавливаем необходимые системные пакеты для работы с PostgreSQL и диагностики
RUN apt-get update && apt-get install -y \
    libpq-dev \
    nginx \
    gcc \
    iputils-ping \
    net-tools \
    procps \
    curl \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем их
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы backend
COPY backend/ .

# Копируем файлы frontend для сервировки через Nginx
COPY frontend/ /usr/share/nginx/html

# Копируем конфигурацию для Nginx
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Копируем конфигурацию для supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Открываем порт для Nginx
EXPOSE 80

# Запуск supervisord для управления всеми процессами
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
