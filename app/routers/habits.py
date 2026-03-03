from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from ..database import get_db
from ..models import User, Habit, HabitLog
from ..schemas import HabitCreate, HabitUpdate, HabitResponse, HabitWithLogs, HabitLogResponse, HabitStats
from ..auth import get_current_user

router = APIRouter(prefix="/api/habits", tags=["Habits"])


async def _get_habit_by_id(habit_id: int, user: User, db: AsyncSession) -> Habit:
    result = await db.execute(
        select(Habit).where(Habit.id == habit_id, Habit.user_id == user.id)
    )
    habit = result.scalar_one_or_none()
    if not habit:
        raise HTTPException(status_code=404, detail="Привычка не найдена")
    return habit


@router.post("/", response_model=HabitResponse)
async def create_habit(
    habit_data: HabitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = Habit(
        title=habit_data.title,
        description=habit_data.description,
        user_id=current_user.id,
        is_quantitative=habit_data.is_quantitative,
        target_value=habit_data.target_value,
        unit=habit_data.unit
    )
    db.add(habit)
    await db.commit()
    await db.refresh(habit)
    return habit


@router.get("/", response_model=list[HabitWithLogs])
async def get_habits(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Habit).where(Habit.user_id == current_user.id)
    )
    habits = result.scalars().all()
    
    today = datetime.utcnow().date()
    response = []
    for habit in habits:
        logs_result = await db.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit.id,
                func.date(HabitLog.date) == today
            ).order_by(HabitLog.date.desc())
        )
        logs = logs_result.scalars().all()
        today_value = sum(log.value for log in logs)
        
        habit_dict = {
            "id": habit.id,
            "title": habit.title,
            "description": habit.description,
            "is_active": habit.is_active,
            "created_at": habit.created_at,
            "user_id": habit.user_id,
            "is_quantitative": habit.is_quantitative,
            "target_value": habit.target_value,
            "unit": habit.unit,
            "logs": logs,
            "today_value": today_value
        }
        response.append(habit_dict)
    return response


@router.get("/{habit_id}", response_model=HabitWithLogs)
async def get_habit_detail(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await _get_habit_by_id(habit_id, current_user, db)
    logs_result = await db.execute(
        select(HabitLog).where(HabitLog.habit_id == habit.id).order_by(HabitLog.date.desc())
    )
    logs = logs_result.scalars().all()
    
    today = datetime.utcnow().date()
    today_result = await db.execute(
        select(func.sum(HabitLog.value)).where(
            HabitLog.habit_id == habit.id,
            func.date(HabitLog.date) == today
        )
    )
    today_value = today_result.scalar() or 0
    
    return {
        "id": habit.id,
        "title": habit.title,
        "description": habit.description,
        "is_active": habit.is_active,
        "created_at": habit.created_at,
        "user_id": habit.user_id,
        "is_quantitative": habit.is_quantitative,
        "target_value": habit.target_value,
        "unit": habit.unit,
        "logs": logs,
        "today_value": today_value
    }


@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await _get_habit_by_id(habit_id, current_user, db)
    
    update_data = habit_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(habit, field, value)
    
    await db.commit()
    await db.refresh(habit)
    return habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await _get_habit_by_id(habit_id, current_user, db)
    await db.delete(habit)
    await db.commit()


@router.post("/{habit_id}/log", response_model=HabitLogResponse)
async def log_habit(
    habit_id: int,
    value: int = Query(default=1, ge=1, description="Значение выполнения"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        habit = await _get_habit_by_id(habit_id, current_user, db)
        log = HabitLog(habit_id=habit.id, value=value)
        db.add(log)
        await db.commit()
        await db.refresh(log)
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{habit_id}/stats", response_model=HabitStats)
async def get_habit_stats(
    habit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    habit = await _get_habit_by_id(habit_id, current_user, db)

    # Всего выполнений (сумма значений)
    total_result = await db.execute(
        select(func.sum(HabitLog.value)).where(HabitLog.habit_id == habit_id)
    )
    total_completions = total_result.scalar() or 0

    # Текущая серия (дней подряд)
    today = datetime.utcnow().date()
    streak = 0
    for i in range(365):
        check_date = today - timedelta(days=i)
        result = await db.execute(
            select(HabitLog).where(
                HabitLog.habit_id == habit_id,
                func.date(HabitLog.date) == check_date
            )
        )
        if result.scalars().first():
            streak += 1
        elif i > 0:
            break

    # Процент выполнения
    if habit.is_quantitative and habit.target_value > 0:
        # Для количественных - сколько дней цель достигнута
        days_tracked = 1  # Минимум 1 день
        days_completed = 0

        # Проверяем последние 30 дней
        for i in range(30):
            check_date = today - timedelta(days=i)
            result = await db.execute(
                select(func.sum(HabitLog.value)).where(
                    HabitLog.habit_id == habit_id,
                    func.date(HabitLog.date) == check_date
                )
            )
            day_value = result.scalar() or 0
            if day_value >= habit.target_value:
                days_completed += 1
            if day_value > 0:
                days_tracked = max(days_tracked, i + 1)

        completion_rate = round((days_completed / max(days_tracked, 1)) * 100, 2)
    else:
        # Для обычных - процент завершений
        all_logs_result = await db.execute(
            select(func.count()).select_from(HabitLog).where(HabitLog.habit_id == habit_id)
        )
        total_logs = all_logs_result.scalar() or 1
        completion_rate = round((total_completions / max(total_logs, 1)) * 100, 2)

    # Сегодняшнее значение
    today_result = await db.execute(
        select(func.sum(HabitLog.value)).where(
            HabitLog.habit_id == habit_id,
            func.date(HabitLog.date) == today
        )
    )
    today_value = today_result.scalar() or 0
    
    # Прогресс за сегодня в процентах
    progress_percent = 0
    if habit.is_quantitative and habit.target_value > 0:
        progress_percent = min(100, int((today_value / habit.target_value) * 100))
    elif today_value > 0:
        progress_percent = 100

    return HabitStats(
        habit_id=habit_id,
        title=habit.title,
        total_completions=total_completions,
        current_streak=streak,
        completion_rate=completion_rate,
        is_quantitative=habit.is_quantitative,
        target_value=habit.target_value,
        unit=habit.unit,
        today_value=today_value,
        progress_percent=progress_percent
    )
