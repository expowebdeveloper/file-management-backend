from fastapi import FastAPI
from app.routers.router import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Document Management API",
    openapi_url="/openapi.json",
    docs_url="/"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
