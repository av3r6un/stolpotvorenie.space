from flask_jwt_extended import create_access_token, create_refresh_token
from backend.exceptions import ValidationError
from backend.functions import create_uid
from backend import db, bcrypt, settings
from datetime import datetime as dt
import re


class Admins(db.Model):
  uid = db.Column(db.String(4), primary_key=True)
  login = db.Column(db.String(50), nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=True, unique=True)
  tg_id = db.Column(db.Integer, nullable=False, unique=True)
  password = db.Column(db.String(255), nullable=False)
  superuser = db.Column(db.Boolean, nullable=False, default=False)

  def __init__(self, login: str, password: str, tg_id: int, email: str = None, **kwargs) -> None:
    self.uid = create_uid(4, [a.uid for a in self.query.all()])
    self.login = self._validate_login(login)
    self.tg_id = tg_id
    self.email = self._validate_email(email) if email else None
    self.password = self._validate_password(password)

    db.session.add(self)
    db.session.commit()

  @property
  def base_info(self):
    return dict(uid=self.uid, login=self.login, email=self.email)

  def _validate_email(self, email) -> str:
    email_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if email_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('register', 'email_invalid')
    return email

  def _validate_login(self, login) -> str:
    import string
    user = self.query.filter_by(login=login).first()
    alp = string.ascii_letters + string.digits + '-._'
    if user:
      raise ValidationError('register', 'login_exists')
    if len(login) <= 4 and login != 'admin':
      raise ValidationError('register', 'short_username')
    for letter in login:
      if letter not in alp: raise ValidationError('register', 'lang')
    return login

  @staticmethod
  def _validate_password(password) -> str:
    pattern = f'{settings.STRONG_PASSWORD_PATTERN}'
    if not re.match(pattern, password):
      raise ValidationError('register', 'weak_password')
    return bcrypt.generate_password_hash(password)

  @property
  def base_info(self) -> dict:
    return dict(uid=self.uid, login=self.login, superuser=self.superuser)
  
  @property
  def json(self) -> dict:
    bi = self.base_info
    bi.update(dict(email=self.email))
    return bi
  
  def collect_info(self, **kwargs) -> dict:
    info = self.base_info
    info.update(kwargs)
    return info

  @classmethod
  def log_in(cls, login, password, rm=False, **kwargs) -> dict:
    user = cls.query.filter_by(login=login).first()
    if not user:
      raise ValidationError('login', 'not_found')
    return user._login(password, rm)
  
  @classmethod
  def refresh(cls, iden) -> str:
    return create_access_token(iden, fresh=False)
  
  @classmethod
  def restore(cls, uid, password) -> bool:
    admin = cls.query.filter_by(uid=uid).first()
    if not admin:
      return ValidationError('login', 'not_found')
    return admin._restore(password)
  
  def _login(self, password, rm=False) -> dict:
    if not bcrypt.check_password_hash(self.password, password):
      raise ValidationError('register', 'passwords_mismatch')
    accs_token = create_access_token(self.uid, fresh=not rm)
    rfsh_token = create_refresh_token(self.uid)
    extra = dict(accs_token=accs_token, rfsh_token=rfsh_token)
    db.session.commit()
    return self.collect_info(**extra)
  
  def _restore(self, password) -> bool:
    self.password = bcrypt.generate_password_hash(password)
    db.session.commit()
    return True


