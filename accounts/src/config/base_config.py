from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # general settings
    debug: bool = True

    # Database Config
    database_hostname: str
    database_username: str
    database_password: str
    database_name: str
    database_url: str

    # JWT Config
    secret_key: str
    algorithm: str = "HS256"
    access_token_lifetime: int = 3600  # seconds
    refresh_token_lifetime: int = 20  # 20 days
    reset_pass_access_token_lifetime: int = 10 * 60  # minutes

    # RabbitMQ Config
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_vhost: str = "/"
    rabbitmq_url: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.database_url = (
            f"postgresql+asyncpg://{self.database_username}:{self.database_password}"
            f"@{self.database_hostname}/{self.database_name}"
        )
        self.rabbitmq_url = (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}"
            f"@{self.rabbitmq_host}:{self.rabbitmq_port}{self.rabbitmq_vhost}"
        )

    class Config:
        env_file = ".env"


settings: Settings = Settings()
