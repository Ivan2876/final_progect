from fastapi import FastAPI
from api_router import api_router


app = FastAPI(
    title='final project'
)

app.include_router(api_router, tags=['BOOKS'])