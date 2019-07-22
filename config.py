import os

class Settings:
    JOB_PREFIX = "job"
    JOB_VERSION = 1
    DEFAULT_CI_FILE = ".anchorci.yml"

class NonprodSettings(Settings):
    SQLALCHEMY_DATABASE_URI = f"postgres://postgres:docker@{os.environ.get('DB_URL', 'db')}:{os.environ.get('DB_PORT', 5432)}"
    REDIS_CONNECTION_URL = "redis"
    REDIS_CONNECTION_PORT = 6379
    AUTH_SVC_URL = "http://auth:9000"
    AUTH_FILE_ENDPOINT = "".join([AUTH_SVC_URL, "/proxy/file"])

class ProdSettings(Settings):
    pass

def get_settings():
    env = os.environ.get('ENVIRONMENT', 'nonprod')

    if env == 'nonprod':
        return NonprodSettings()

    if env == 'prod':
        return ProdSettings()

    raise ValueError("ENVIRONMENT is not set")
