# auth.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Преобразует пароль в хеш с использованием bcrypt"""
    return pwd_context.hash(password)  # <--- Настоящее хеширование

def verify_password(password: str, db_password_hash: str) -> bool:
    """
    Сравнивает введенный пароль с хешем из базы данных
    """
    try:
        return pwd_context.verify(password, db_password_hash)
    except Exception as e:
        # Логируем ошибки верификации
        from Myshop.app  import logger  # Импортируйте ваш логгер
        logger.error(f"Password verification error: {str(e)}")
        return False