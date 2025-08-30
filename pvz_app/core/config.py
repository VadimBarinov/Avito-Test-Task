from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import (
    BaseModel,
    PostgresDsn,
)
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    app: str = "main:app"
    host: str = "0.0.0.0"
    port: int = 8080
    reload: bool = True


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    pvz: str = "/pvz"
    reception: str = "/reception"
    product: str = "/product"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10


class AuthJWT(BaseSettings):
    PRIVATE_KEY_PATH: Path = BASE_DIR.parent / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR.parent / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(BASE_DIR / ".env.template", BASE_DIR / ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWT = AuthJWT()
    db: DatabaseConfig


settings = Settings()