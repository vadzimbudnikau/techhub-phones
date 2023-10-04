# Используйте официальный образ Python
FROM python:3.11-slim

# Установите переменную окружения PYTHONUNBUFFERED для предотвращения буферизации вывода
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE  1

# Создайте и установите рабочую директорию
WORKDIR /OnSt

# Установите зависимости, указав requirements.txt из вашего проекта
COPY ./requirements.txt /OnSt/
RUN pip install -r /OnSt/requirements.txt

# Скопируйте все файлы из текущей директории в рабочую директорию
COPY . /OnSt/

# Определите порт, который будет слушать ваше приложение
EXPOSE 8000

# Запустите ваше Django приложение с помощью команды gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
