# Настройка CORS
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешенные домены
        allow_credentials=True,  # Разрешить куки и учетные данные
        allow_methods=["*"],  # Разрешенные HTTP-методы (например, GET, POST)
        allow_headers=["*"],  # Разрешенные заголовки
    )
