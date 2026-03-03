import asyncio
import sys
sys.path.insert(0, '.')

from app.database import AsyncSessionLocal, engine, Base
from app.models import User, Habit, HabitLog
from app.auth import get_password_hash
from sqlalchemy import select

async def test():
    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as db:
        # Проверка пользователя
        result = await db.execute(select(User).where(User.email == "test@test.com"))
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(email="test@test.com", hashed_password=get_password_hash("123"))
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"Создан пользователь: {user.email}, id={user.id}")
        else:
            print(f"Пользователь существует: {user.email}, id={user.id}")
        
        # Проверка привычки
        result = await db.execute(select(Habit).where(Habit.user_id == user.id))
        habit = result.scalar_one_or_none()
        
        if not habit:
            habit = Habit(
                title="Пить воду",
                description="2 литра в день",
                user_id=user.id,
                is_quantitative=True,
                target_value=2000,
                unit="мл"
            )
            db.add(habit)
            await db.commit()
            await db.refresh(habit)
            print(f"Создана привычка: {habit.title}, id={habit.id}")
        else:
            print(f"Привычка существует: {habit.title}, id={habit.id}")
        
        # Добавление лога
        log = HabitLog(habit_id=habit.id, value=500)
        db.add(log)
        await db.commit()
        await db.refresh(log)
        print(f"Добавлен лог: id={log.id}, value={log.value}")
        
        # Проверка статистики
        from sqlalchemy import func
        result = await db.execute(
            select(func.sum(HabitLog.value)).where(
                HabitLog.habit_id == habit.id
            )
        )
        total = result.scalar() or 0
        print(f"Всего выполнено: {total}")

if __name__ == "__main__":
    asyncio.run(test())
    print("\n✅ Тест пройден успешно!")
