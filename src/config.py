import os

class Settings:
    JOB_PREFIX = "job"
    JOB_VERSION = 1
    DEFAULT_CI_FILE = ".anchorci.yml"

class NonprodSettings(Settings):
    DB_URL = os.environ.get('DB_URL')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SQLALCHEMY_DATABASE_URI = f"postgres://{DB_USER}:{DB_PASS}@{DB_URL}:{DB_PORT}"
    REDIS_CONNECTION_URL = os.environ.get('REDIS_URL')
    REDIS_CONNECTION_PORT = os.environ.get('REDIS_PORT')
    AUTH_SVC_URL = os.environ.get('AUTH_URL')
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
