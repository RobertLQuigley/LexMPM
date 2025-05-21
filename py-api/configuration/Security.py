from passlib.context import CryptContext

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_config : dict = {
    "schemes": ["bcrypt",],
    "deprecated": "auto",
    "bcrypt__rounds": 12,
    "truncate_error": True
}


