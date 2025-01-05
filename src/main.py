import uvicorn
from fastapi import FastAPI

from src.routes import currencies
app = FastAPI()

app.include_router(currencies.router)


# @app.get("/currency")
# async def get_currencies():
#     return {"message": "Hello curr"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)