from phonenumbers import parse as parse_num, is_valid_number
from backend.exceptions import ValidationError
from backend.functions import create_uid
from datetime import datetime as dt
from backend import db, settings
import re


class Clients(db.Model):
  uid = db.Column(db.String(7), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  surname = db.Column(db.String(50), nullable=False)
  patronymic = db.Column(db.String(50), nullable=True)
  phone = db.Column(db.Integer, nullable=False, unique=True)
  email = db.Column(db.String(100), nullable=False, unique=True)
  registered = db.Column(db.Integer, nullable=False, default=int(dt.now().timestamp()))

  def __init__(self, name, surname, phone, email, patronymic=None) -> None:
    self.uid = create_uid(7, [a.uid for a in self.query.all()])
    self.name = name
    self.surname = surname
    self.patronymic = patronymic
    self.phone = self._validate_phone(phone)
    self.email = self._validate_email(email)
    self.registered = int(dt.now().timestamp())

  @property
  def json(self):
    return dict(uid=self.uid, name=self.name, surname=self.surname, phone=self.phone, email=self.email)
  
  def _validate_phone(self, phone: str) -> int:
    number = parse_num(number)
    if not is_valid_number(number):
      raise ValidationError('register', 'not_valid_phone')
    if number.national_number in [a.phone for a in self.query.all()]:
      raise ValidationError('register', 'phone_already_registered')
    return number.national_number

  def _validate_email(self, email: str) -> str:
    email_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if email_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('register', 'not_valid_email')
    return email

  def __repr__(self) -> str:
    return f'<Client +7{self.phone}>'
