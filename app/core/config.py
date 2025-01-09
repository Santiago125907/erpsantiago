from pydantic import BaseSettings

class Settings(BaseSettings):
    # Configuración de la base de datos
    DB_HOST: str = "database-1.cd4u8i8ymfwu.us-east-1.rds.amazonaws.com"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "Xago5547"

    # Configuración de JWT
    SECRET_KEY: str = "supersecretkey"  # Cambiar por una clave segura en producción
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"  # Cargar variables desde un archivo .env si es necesario

settings = Settings()
