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
  group_uid = db.Column(db.String(8), db.ForeignKey('Groups.uid'), nullable=True)

  def __init__(self, name, surname, phone, email, patronymic=None, group_uid=None) -> None:
    self.uid = create_uid(7, [a.uid for a in self.query.all()] + [a.uid for a in Children.query.all()])
    self.name = name
    self.surname = surname
    self.patronymic = patronymic
    self.phone = self._validate_phone(phone)
    self.email = self._validate_email(email)
    self.registered = int(dt.now().timestamp())
    self.group_uid = group_uid

  @property
  def json(self):
    return dict(uid=self.uid, name=self.name, surname=self.surname, phone=self.phone, email=self.email,
                group_uid=self.group_uid)
  
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
  
  def _validate_group_uid(self, group_uid=None):
    if not group_uid:
      return None
    from .groups import Groups
    group_uids = [a.uid for a in Groups.query.all()]
    if group_uid not in group_uids:
      return ValueError('Undefined group UID')
    return group_uid

  def __repr__(self) -> str:
    return f'<Client +7{self.phone}>'


class Children(db.Model):
  uid = db.Column(db.String(7), primary_key=True)
  parent_uid = db.Column(db.ForeignKey(Clients.uid), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  age = db.Column(db.Integer, nullable=False)
  group_uid = db.Column(db.String(8), db.ForeignKey('Groups.uid'), nullable=True)

  def __init__(self, parent_uid, name, age, group_uid=None) -> None:
    self.uid = create_uid(7, [a.uid for a in self.query.all()] + [a.uid for a in Clients.query.all()])
    self.parent_uid = self._validate_parent_uid(parent_uid)
    self.name = name
    self.age = age
    self.group_uid = self._validate_group_uid(group_uid)

  def _validate_parent_uid(self, parent_uid):
    parent_uids = [a.uid for a in Clients.query.all()]
    if parent_uid not in parent_uids:
      raise ValueError('Undefined parent UID')
    return parent_uid
    
  def _validate_group_uid(self, group_uid=None):
    if not group_uid:
      return None
    from .groups import Groups
    group_uids = [a.uid for a in Groups.query.all()]
    if group_uid not in group_uids:
      return ValueError('Undefined group UID')
    return group_uid
  