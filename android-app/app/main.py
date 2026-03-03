from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import engine, Base
from .routers import users, habits
import os

# Создание таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title="Habit Tracker", description="Трекер привычек для резюме")

# CORS - разрешаем все запросы с localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await create_tables()
    
    # Монтируем статику
    static_path = os.path.join(os.path.dirname(__file__), "static")
    app.mount("/static", StaticFiles(directory=static_path), name="static")


app.include_router(users.router)
app.include_router(habits.router)


@app.get("/")
async def root():
    return FileResponse(os.path.join(os.path.dirname(__file__), "static", "index.html"))
