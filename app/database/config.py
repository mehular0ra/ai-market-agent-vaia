import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    HOST = os.getenv("DATABASE_HOST", "localhost")
    PORT = os.getenv("DATABASE_PORT", "5432")
    NAME = os.getenv("DATABASE_NAME", "market_analyst")
    USER = os.getenv("DATABASE_USER", "postgres")
    PASSWORD = os.getenv("DATABASE_PASSWORD", "postgres")

    @classmethod
    def get_connection_string(cls):
        return (
            f"postgresql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.NAME}"
        )
