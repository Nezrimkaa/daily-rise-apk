from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    def __init__(self, **kwargs):
        # Для Android используем директорию приложения
        if 'ANDROID_ARGUMENT' in os.environ:
            # Android: используем внутреннюю директорию приложения
            app_dir = os.environ.get('ANDROID_ARGUMENT')
            db_path = os.path.join(app_dir, 'habits.db')
            default_db = f"sqlite+aiosqlite:///{db_path}"
        else:
            # Desktop: используем текущую директорию
            default_db = "sqlite+aiosqlite:///./habits.db"
        
        super().__init__(
            DATABASE_URL=os.environ.get('DATABASE_URL', default_db),
            **kwargs
        )

    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
