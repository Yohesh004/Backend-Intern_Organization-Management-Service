from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MASTER_DB: str = "master_db"
    JWT_SECRET: str = "change_this_to_a_strong_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_HOURS: int = 6

    class Config:
        env_file = ".env"

settings = Settings()
