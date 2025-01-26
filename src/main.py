import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.exception.exceptions import CurrencyException
from src.routes import currencies, exchange_rates, exchange

app = FastAPI()

app.include_router(currencies.router)
app.include_router(exchange_rates.router)
app.include_router(exchange.router)

# @app.get("/currency")
# async def get_currencies():
#     return {"message": "Hello curr"}

@app.exception_handler(CurrencyException)
async def database_unavailable_exception_handler(request, exc: CurrencyException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message},
    )

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)