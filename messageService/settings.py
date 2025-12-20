from environ import Env
from os.path import join
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
if Env().bool("DJANGO_READ_DOT_ENV_FILE", default=False):
    Env.read_env(join(BASE_DIR, ".env"))

env = Env()

EMAIL_PASSWORD = env("EMAIL_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_EMAIL_FROM = env("DEFAULT_EMAIL_FROM")
SMTP_SERVER = env("SMTP_SERVER")
KAFKA_SERVER = env("KAFKA_SERVER")
