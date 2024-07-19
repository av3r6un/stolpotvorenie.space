from dotenv import load_dotenv
import yaml
import sys
import os

class Config:
  ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

  def __init__(self) -> None:
    load_dotenv(os.path.join(self.ROOT, 'config', '.env'))
    self.SECRET_KEY = os.environ.get('SECRET_KEY')
    self.BOT_TOKENS = os.environ.get('BOT_TOKENS')
    self.JWT_SECRET_KEY = self.SECRET_KEY
    self._load_settings(os.path.join(self.ROOT, 'config', 'backend.yaml'))

  def _load_settings(self, path) -> None:
    try:
      with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
      if os.environ.get('DB_TYPE') == 'local':
        self.SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(self.ROOT, os.environ.get("DB_URI"))}'
      else:
        self.SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
      self.__dict__.update(data)
    except FileNotFoundError:
      print('Backend settings file not found!')
      sys.exit(-1)
  