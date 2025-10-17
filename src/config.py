from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', extra='allow', env_file_encoding='utf-8',
    )


class TelegramConfig(BaseConfig):
    token: str = Field(..., validation_alias='TOKEN')


# class PostgresConfig(BaseConfig):
#     host: str = Field(..., validation_alias='POSTGRES_HOST')
#     port: int = Field(..., validation_alias='POSTGRES_PORT')
#     user: str = Field(..., validation_alias='POSTGRES_USER')
#     password: str = Field(..., validation_alias='POSTGRES_PASSWORD')
#     database: str = Field(..., validation_alias='POSTGRES_DATABASE')
#     pool_size: int = Field(20, validation_alias='POSTGRES_POOL_SIZE')
#     max_overflow: int = Field(10, validation_alias='POSTGRES_MAX_OVERFLOW')
#     echo: bool = Field(False, validation_alias='POSTGRES_ECHO')
#
#     @property
#     def dsn(self) -> str:
#         return f'postgresql+psycopg_async://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'



# class RedisConfig(BaseConfig):
#     host: str = Field(..., validation_alias='REDIS_HOST')
#     port: int = Field(..., validation_alias='REDIS_PORT')
#     user: str | None = Field(None, validation_alias='REDIS_USER')
#     password: str | None = Field(None, validation_alias='REDIS_PASSWORD')
#     database: int = Field(0, validation_alias='REDIS_DATABASE')
#
#     @property
#     def dsn(self) -> str:
#         if self.user and self.password:
#             return f'redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
#         if self.password:
#             return f'redis://:{self.password}@{self.host}:{self.port}/{self.database}'
#         return f'redis://{self.host}:{self.port}/{self.database}'


class Config(BaseConfig):
    # postgres: PostgresConfig = PostgresConfig()  # type: ignore[call-arg]
    # redis: RedisConfig = RedisConfig()  # type: ignore[call-arg]
    telegram: TelegramConfig = TelegramConfig() # type: ignore[call-arg]


config = Config()
