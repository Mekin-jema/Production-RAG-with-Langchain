"""
 Centerilized Configuration 
 Uses pydantic-settings for vlidated environment variables

"""



from pydantic_settings import BaseSettings # used to  load env ,validate and store them
from functools  import lru_cache # used to cache the settings instance


class Settings(BaseSettings): # inherit from BaseSettings to load env variables

    # LLM Configuration
    # openai_api_key:str
    openrouter_api_key: str
    primary_model:str="gpt-4o-mini"
    fallback_model:str="gpt-5-mini"

  

    # Langsmith
    langsmith_tracing_v2: bool=True
    langsmith_endpoint: str=""
    langsmith_project: str="production-api"
    
    # Application
    app_env:str ="development"
    log_level:str="INFO"
    rate_limit:str= "20/min"
    cache_ttl_seconds:int=300
    max_retries:int = 3


    model_config={
        "env_file":".env",
        "extra":"ignore"  # ignore env variables that are not defined in the class
    }
    
    @property
    def is_production(self)->bool:
        return self.app_env.lower() == "production"

@lru_cache
def get_settings() -> Settings:
    """ Cached settings instance - Loaded once , retused  everywhere"""
    return Settings()
     
    
    # Agent Configuration
    