from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Construction Asset Search API"
    
    # Anthropic Settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    MAX_TOKENS: int = 8000
    
    # Search Settings
    TARGET_WEBSITES: List[str] = [
        "https://www.forestrytrader.com/listings/search?sort=1",
        "https://www.rbauction.com/",
        "https://www.ritchiespecs.com",
        "https://www.lectura-specs.com/en/specs/forklifts/diesel-forklifts",
        "https://www.ironplanet.com/",
        "https://www.forkliftinventory.com/",
        "https://www.machinerytrader.com/listings/for-sale/forklifts/1036"
    ]
    
    # Storage Settings
    DATA_DIR: str = "data"
    LOGS_DIR: str = "logs"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 