import os
import dotenv
dotenv.load_dotenv()


class AppConfig:
    USER = os.environ['OMNIDESK_USER_EMAIL']
    TOKEN = os.environ['OMNIDESK_TOKEN']
    RESULT_PER_API_PAGE = 100
    CPU_MULTIPLIER = 5
    API_CALLS_LEFT_ALERT = 200
    OMNIDESK_API_URL = 'https://prochanev.omnidesk.ru/api/'
    STORAGE_DB_URL = 'sqlite:///cases.db'
