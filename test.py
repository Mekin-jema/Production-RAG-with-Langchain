from app.config import get_settings
settings=get_settings()

print(
   f'Environment:{settings.app_env}'
)
print(f'Primary model: {settings.primary_model}')
print(f'Fallback model: {settings.fallback_model}')
