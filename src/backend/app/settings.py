from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    app_secret: str = "devkit-cli-dev"
    database_url: str = "sqlite:///./devkit.db"
