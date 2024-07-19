from flask_jwt_extended import create_access_token, create_refresh_token
from phonenumbers import parse as parse_num, is_valid_number
from backend.exceptions import ValidationError
from backend.functions import create_uid
from backend import db, bcrypt, settings
from datetime import datetime as dt
import re


class Users(db.Model):
  uid = db.Column(db.String(6), primary_key=True)
  name = db.Column(db.String(50), nullable=True)
  phone = db.Column(db.Integer, nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=True, unique=True)
  password = db.Column(db.String(255), nullable=False)
  reg_date = db.Column(db.Integer, nullable=False, default=int(dt.now().timestamp()))
  last_date = db.Column(db.Integer, nullable=False)
  reg_ip = db.Column(db.String(15), nullable=False)
  last_ip = db.Column(db.String(15), nullable=False)

  def __init__(self, phone, password, reg_ip, email=None, name=None) -> None:
    self.uid = create_uid(6, [a.uid for a in self.query.all()])
    self.phone = self._validate_phone(phone)
    self.password = self._validate_password(password)
    self.reg_ip = reg_ip
    self.reg_date = int(dt.now().timestamp())
    self.last_ip = reg_ip
    self.last_date = self.reg_date
    self.email = self._validate_email(email) if email else None
    self.name = name

    db.session.add(self)
    db.session.commit()

  @classmethod
  def login(cls, phone, password, last_ip) -> dict:
    phone = parse_num(phone)
    user = cls.query.filter_by(phone=phone.national_number).first()
    if not user:
      raise ValidationError('login', 'not_found')
    return user._login(password, last_ip)
  
  @classmethod
  def refresh(cls, iden) -> str:
    return create_access_token(iden, fresh=False)
  
  @property
  def base_info(self):
    return dict(uid=self.uid, phone=self.phone, email=self.email, type=self.user_type, name=self.name)

  @property
  def json(self):
    return self.base_info

  def _validate_phone(self, number) -> int:
    number = parse_num(number)
    if not is_valid_number(number):
      raise ValidationError('register', 'not_valid_phone')
    if number.national_number in [a.phone for a in self.query.all()]:
      raise ValidationError('register', 'phone_already_registered')
    return number.national_number
  
  @staticmethod
  def _validate_password(password: str) -> str:
    pattern = rf'{settings.STRONG_PASSWORD_PATTERN}'
    if not re.match(pattern, password) and password != 'admin':
      raise ValidationError('register', 'weak_password')
    return bcrypt.generate_password_hash(password)
  
  def _validate_email(self, email) -> str:
    email_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if email_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('register', 'not_valid_email')
    return email
  
  def _login(self, password, last_ip) -> dict:
    if not bcrypt.check_password_hash(self.password, password):
      raise ValidationError('login', 'passwords_mismatch')
    self.last_ip = last_ip
    self.last_date = int(dt.now().timestamp())
    accs_token = create_access_token(self.uid, fresh=False)
    rfsh_token = create_refresh_token(self.uid)
    extra = dict(accs_token=accs_token, rfsh_token=rfsh_token)
    db.session.commit()
    return self.collect_info(**extra)
  
  def collect_info(self, **kwargs) -> dict:
    info = self.base_info
    info.update(kwargs)
    return info
  
