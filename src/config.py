"""Central configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    @property
    def has_api_key(self) -> bool:
        return bool(self.anthropic_api_key)

    # Postgres
    postgres_dsn: str = "postgresql+asyncpg://uplevel_ai:uplevel_ai@localhost:5432/uplevel_ai"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "uplevel_ai"

    # Ingestion — optional integrations
    google_client_id: str = ""
    google_client_secret: str = ""
    github_token: str = ""
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    ado_org: str = ""
    ado_pat: str = ""

    # App
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
