from dataclasses import dataclass


@dataclass(slots=True)
class BotConfig:
    token: str


@dataclass(slots=True)
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass(slots=True)
class NatsConfig:
    host: str
    port: int


@dataclass(slots=True)
class Config:
    bot: BotConfig
    database: DatabaseConfig
    nats: NatsConfig
