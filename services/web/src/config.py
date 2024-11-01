from dotenv import load_dotenv

import os

load_dotenv()

class Settings:
    DB_URL = os.getenv("DB_URL")
    DB_URL_MIGRATION = os.getenv("DB_URL_MIGRATION")
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    PICTURE_TOPIC = os.getenv("PICTURE_TOPIC")
    URL_PICTURE_PROCESSOR = os.getenv("URL_PICTURE_PROCESSOR")


