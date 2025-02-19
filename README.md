# Проект “Обмен валют” на FastAPI

REST API для описания валют и обменных курсов. Позволяет просматривать и редактировать списки валют и обменных курсов, и совершать расчёт конвертации произвольных сумм из одной валюты в другую.

[Техническое задание проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/)

## Реализация проекта с использованием следующих технологиий:
<img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/fastapi/fastapi-original.svg" title="Fastapi" alt="Fastapi" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-original-wordmark.svg" title="Docker" alt="Docker" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/sqlalchemy/sqlalchemy-original.svg" title="sqlalchemy" alt="sqlalchemy" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/postgresql/postgresql-original-wordmark.svg" title="postgresql" alt="postgresql" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/poetry/poetry-original.svg" title="postgresql" alt="postgresql" width="40" height="40"/>&nbsp;
<img src="https://github.com/devicons/devicon/blob/master/icons/pytest/pytest-original-wordmark.svg" title="pytest" alt="pytest" width="40" height="40"/>&nbsp;
![Uvicorn](https://img.shields.io/badge/Uvicorn-255?style=for-the-badge&logo=Uvicorn)
![Alembic](https://img.shields.io/badge/Alembic-255?style=for-the-badge&logo=Uvicorn)
![Asyncio](https://img.shields.io/badge/Asyncio-255?style=for-the-badge&logo=Uvicorn)
## Установка 

Для успешного запуска приложения выполните следующие шаги:

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/Pashosi/currency_exchange_FastAPI.git
    ```
2. Установка Docker
3. Создайте **.env** файл опираясь на **.env_example**
4. Сборка и запуск проекта:
- Prod версия
```shell
docker-compose -f docker-compose.prod.yml up --build
```
	
- Dev версия
```shell
docker-compose -f docker-compose.dev.yml up --build
```

## REST API

### Валюты

#### Получение списка валют

**GET /currencies**

Пример ответа:
```json
[
    {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    }
]
```
Коды ответов:
    Успех - 200
    Ошибка (например, база данных недоступна) - 500

#### Получение конкретной валюты.

**GET /currency/EUR**
Пример ответа:
```json
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```
HTTP коды ответов:
    Успех - 200
    Код валюты отсутствует в адресе - 400
    Валюта не найдена - 404
    Ошибка (например, база данных недоступна) - 500

**POST /currencies**
#### Добавление новой валюты в базу.
 Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Поля формы - name, code, sign. 
 Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```json
{
    "id": 0,
    "name": "Euro",
    "code": "EUR",
    "sign": "€"
}
```
HTTP коды ответов:
    Успех - 200
    Отсутствует нужное поле формы - 400
    Валюта с таким кодом уже существует - 409
    Ошибка (например, база данных недоступна) - 500
#### Обменные курсы
**GET /exchangeRates**
Получение списка всех обменных курсов. Пример ответа:
```json
[
    {
        "id": 0,
        "baseCurrency": {
            "id": 0,
            "name": "United States dollar",
            "code": "USD",
            "sign": "$"
        },
        "targetCurrency": {
            "id": 1,
            "name": "Euro",
            "code": "EUR",
            "sign": "€"
        },
        "rate": 0.99
    }
]
```
HTTP коды ответов:
    Успех - 200
    Ошибка (например, база данных недоступна) - 500
**GET /exchangeRate/USDRUB**
#### Получение конкретного обменного курса. 
Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Пример ответа:
```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```
HTTP коды ответов:
    Успех - 200
    Коды валют пары отсутствуют в адресе - 400
    Обменный курс для пары не найден - 404
    Ошибка (например, база данных недоступна) - 500
**POST /exchangeRates**
#### Добавление нового обменного курса в базу. 

Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Поля формы - baseCurrencyCode, targetCurrencyCode, rate. Пример полей формы:
    baseCurrencyCode - USD
    targetCurrencyCode - EUR
    rate - 0.99
Пример ответа - JSON представление вставленной в базу записи, включая её ID:
```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```
HTTP коды ответов:
Успех - 200
Отсутствует нужное поле формы - 400
Валютная пара с таким кодом уже существует - 409
Одна (или обе) валюта из валютной пары не существует в БД - 404
Ошибка (например, база данных недоступна) - 500

**PATCH /exchangeRate/USDRUB**
#### Обновление существующего в базе обменного курса. 
Валютная пара задаётся идущими подряд кодами валют в адресе запроса. Данные передаются в теле запроса в виде полей формы (x-www-form-urlencoded). Единственное поле формы - rate.

Пример ответа - JSON представление обновлённой записи в базе данных, включая её ID:
```json
{
    "id": 0,
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Euro",
        "code": "EUR",
        "sign": "€"
    },
    "rate": 0.99
}
```
HTTP коды ответов:
    Успех - 200
    Отсутствует нужное поле формы - 400
    Валютная пара отсутствует в базе данных - 404
    Ошибка (например, база данных недоступна) - 500

#### Обмен валюты
**GET /exchange?from=BASE_CURRENCY_CODE&to=TARGET_CURRENCY_CODE&amount=$AMOUNT**
Расчёт перевода определённого количества средств из одной валюты в другую. Пример запроса - GET /exchange?from=USD&to=AUD&amount=10.

Пример ответа:
```json
{
    "baseCurrency": {
        "id": 0,
        "name": "United States dollar",
        "code": "USD",
        "sign": "$"
    },
    "targetCurrency": {
        "id": 1,
        "name": "Australian dollar",
        "code": "AUD",
        "sign": "A€"
    },
    "rate": 1.45,
    "amount": 10.00
    "convertedAmount": 14.50
}
```

Для всех запросов, в случае ошибки, ответ может выглядеть так:
```json
{
    "message": "Валюта не найдена"
}
```
