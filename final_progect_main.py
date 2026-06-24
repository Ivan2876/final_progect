from fastapi import FastAPI
from final_progect_api_router import api_router


app = FastAPI(
    title='Final Project'
)

app.include_router(api_router, tags=['TRAVELS'])