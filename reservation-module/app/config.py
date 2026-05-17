import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY          = os.environ.get("SECRET_KEY", "change-moi-en-prod")
    JWT_SECRET_KEY      = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-moi")

    DB_USER     = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_HOST     = os.environ.get("DB_HOST", "localhost")
    DB_PORT     = os.environ.get("DB_PORT", "3306")
    DB_NAME     = os.environ.get("DB_NAME", "trajets_saas")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Durée du blocage temporaire d'une place (en minutes)
    RESERVATION_EXPIRATION_MINUTES = int(
        os.environ.get("RESERVATION_EXPIRATION_MINUTES", 15)
    )
