from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router as api_v1_router

app = FastAPI(title="Moral Navigator API")

# Разрешаем всё (DEV), чтобы CORS точно не мешал
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # <- временно "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")
