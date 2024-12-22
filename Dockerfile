# Используем официальный образ Python
FROM python:3.13

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
COPY ./packages /packages
RUN pip install --no-cache-dir /packages/*

# Копируем все файлы проекта в контейнер
COPY . .

# Указываем порт, который будет использовать приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "main.py"]
