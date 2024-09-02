from pydantic_settings import BaseSettings, SettingsConfigDict

# class BaseConfig(BaseSettings):
#     model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
#     class Config:
#         case_sensitive = True
        
# class DBConfig(BaseSettings):
#     IPADDRESS : str = "127.0.0.1"
#     PORT : str = "3307"
#     USER : str = "root"
#     PASSWORD : str = "blackant"
#     NAME : str = "db"
    
#     def DB_ENGINE(self)->str:
#         return "mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}".format(
#             user=self.USER,
#             port=self.PORT,
#             password=self.PASSWORD,
#             hostname=self.IPADDRESS,
#             database=self.NAME,
#         )
        
# class RABBITMQConfig(BaseSettings):
#     IPADDRESS : str = "192.168.40.5"
#     PORT : str = "5672"
#     USER : str = "semut"
#     PASSWORD : str = "blackant"
#     VHOST : str = "semut-dev"
    
#     def CELERY_ENGINE(self)->str:
#         return "amqp://{user}:{password}@{hostname}:{ports}//{vhost}".format(
#     user=self.USER,
#     password=self.PASSWORD,
#     hostname=self.IPADDRESS,
#     ports=self.PORT,
#     vhost=self.VHOST,
# )
        
class Config(BaseSettings):
    APP_NAME : str ="FastAPI-Clean-Structure"
    APP_DESCRIPTIOIN : str = "This is a very fancy project, with auto docs for the API and everything."
    
    SECRET_TEXT : str = "HxekWSNWYKyOsezYRQxFEJNgbUroNzDT"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
    ALGORITHM : str = "HS256"
    
    # DATABASE : DBConfig
    # RABBITMQ : RABBITMQConfig
    
    
config: Config = Config()