from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    la_api_token: str


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
