from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    api_token: str
    api_host: str
    fast_forward_number: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
