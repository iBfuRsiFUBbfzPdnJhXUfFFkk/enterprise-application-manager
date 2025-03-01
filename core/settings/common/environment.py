from os.path import join
from pathlib import Path

from environ import Env

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent

env: Env = Env()
Env.read_env(env_file=join(BASE_DIR, '.env'))
