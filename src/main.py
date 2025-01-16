import uvicorn
from fastapi import FastAPI

from src.routes import currencies, exchange_rates, exchange

app = FastAPI()

app.include_router(currencies.router)
app.include_router(exchange_rates.router)
app.include_router(exchange.router)

# @app.get("/currency")
# async def get_currencies():
#     return {"message": "Hello curr"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)