import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app

async def test():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Регистрация
        r = await ac.post("/api/auth/register", json={"email": "test@test.com", "password": "123"})
        print(f"Register: {r.status_code} - {r.text}")
        
        # Логин
        r = await ac.post("/api/auth/login", json={"email": "test@test.com", "password": "123"})
        print(f"Login: {r.status_code} - {r.text}")
        token = r.json().get("access_token")
        
        # Создать привычку
        headers = {"Authorization": f"Bearer {token}"}
        r = await ac.post("/api/habits/", json={"title": "Пить воду"}, headers=headers)
        print(f"Create habit: {r.status_code} - {r.text}")
        
        # Получить привычки
        r = await ac.get("/api/habits/", headers=headers)
        print(f"Get habits: {r.status_code} - {r.text}")

asyncio.run(test())
