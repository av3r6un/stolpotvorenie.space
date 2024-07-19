import yaml
import sys
import os

class Settings:
  ROOT = None
  extra = dict()

  def __init__(self, root_fp=None) -> None:
    self.ROOT = root_fp if root_fp else 'backend'
    self._load_settings()

  def _load_settings(self) -> None:
    fp = os.path.join(self.ROOT, 'config', 'settings.yaml')
    try:
      with open(fp, 'r', encoding='utf-8') as f:
        data: dict = yaml.safe_load(f)
      self.__dict__.update(data)
    except FileNotFoundError:
      print('Settings file not found!')
      sys.exit(-1)
    
  @property
  def root(self):
    return self.ROOT
  
  @root.setter
  def root(self, path):
    self.ROOT = path
