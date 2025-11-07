from pydantic_settings import BaseSettings

# [SETTINGS]
# [Classe de configurações da aplicação usando Pydantic BaseSettings para carregar variáveis de ambiente]
# [ENTRADA: variáveis de ambiente do arquivo .env - database_url, test_database_url, jwt_secret_key, etc.]
# [SAIDA: instância Settings com todas as configurações validadas e carregadas]
# [DEPENDENCIAS: BaseSettings, pydantic_settings]
class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int
    redis_url: str
    environment: str
    dev_email: str
    dev_password: str

    # [CONFIG]
    # [Classe de configuração interna do Pydantic que define de onde carregar as variáveis de ambiente]
    # [ENTRADA: nenhuma - configuração estática]
    # [SAIDA: configuração indicando que deve usar o arquivo .env]
    # [DEPENDENCIAS: nenhuma]
    class Config:
        env_file = ".env"
    
    # [GET DATABASE URL]
    # [Retorna a URL do banco de dados baseada no ambiente - test_database_url para desenvolvimento, database_url para outros ambientes]
    # [ENTRADA: self - instância da classe Settings]
    # [SAIDA: str - URL de conexão com o banco de dados]
    # [DEPENDENCIAS: self.environment, self.test_database_url, self.database_url]
    def get_database_url(self) -> str:
        if self.environment == "development":
            return self.test_database_url
        return self.database_url


settings = Settings()