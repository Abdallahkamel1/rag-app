from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name : str
    app_version : str
    openai_api_key : str

    file_allowed_types : list[str]
    file_max_size : int
    default_chunk_size : int

    mongo_url : str
    mongo_db : str
    

    class Config:
        env_file = ".env"
def get_settings() -> Settings:
    return Settings()        