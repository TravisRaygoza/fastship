from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore",
    )


### To configure the database settings using pydantic settings
class DatabaseSettings(BaseSettings):
    
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config


    @property # To create the Postgres URL from the individual components
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    def REDIS_URL(self, db):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}"




class AppSettings(BaseSettings):
    APP_NAME: str = "Delivery Service API"
    APP_DOMAIN: str = "localhost:8000"

class SecuritySettings(BaseSettings):

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    model_config = _base_config


class NotificationSettings(BaseSettings):

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True


    TWILIO_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str


    model_config = _base_config
    
### Database settings instance
db_settings = DatabaseSettings()
db_settings.POSTGRES_URL

### Security settings instance
security_settings = SecuritySettings()

## Notification settings instance
notification_settings = NotificationSettings()

### AppBase settings instance
app_settings = AppSettings()



