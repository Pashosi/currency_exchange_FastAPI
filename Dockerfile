# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Отключаем виртуальное окружение Poetry
ENV POETRY_VIRTUALENVS_CREATE=false

# Устанавливаем базовые зависимости
RUN #apk update && apk add --no-cache gcc musl-dev postgresql-dev

# Устанавливаем Poetry
#RUN #pip install poetry
# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi
# Устанавливаем зависимости, исключая dev
RUN #poetry install

# Копируем исходный код приложения
COPY . .

# Команда для запуска FastAPI приложения
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]