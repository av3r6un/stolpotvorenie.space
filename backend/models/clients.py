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
  children = db.relationship('Children', backref='children', lazy='dynamic')

  def __init__(self, name, surname, phone, email, patronymic=None, **kwargs) -> None:
    self.uid = create_uid(7, [a.uid for a in self.query.all()] + [a.uid for a in Children.query.all()])
    self.name = name
    self.surname = surname
    self.patronymic = patronymic
    self.phone = self._validate_phone(phone)
    self.email = self._validate_email(email)
    self.registered = int(dt.now().timestamp())
    db.session.add(self)
    db.session.commit()

  @property
  def json(self):
    return dict(uid=self.uid, name=self.name, surname=self.surname, phone=self.phone_number, email=self.email,
                fullName=self.full_name, children=self.children, patronymic=self.patronymic)
  
  @property
  def phone_number(self):
    return f'+7{self.phone}'

  @property
  def full_name(self):
    return f'{self.surname} {self.name} {self.patronymic if self.patronymic else ""}'.strip()

  @property
  def base_info(self):
    return dict(uid=self.uid, full_name=self.full_name, phone=self.phone)
  
  @property
  def children(self):
    children = Children.query.filter_by(parent_uid=self.uid).all()
    return [a.json for a in children]

  @classmethod
  def all(cls) -> dict:
    return [a.json for a in cls.query.all()]
  
  def delete(self) -> None:
    if self.children:
      [child.delete() for child in self.children]
    db.session.delete(self)
    db.session.commit()

  def edit(self, name, surname, phone, email, patronymic=None, **kwargs) -> None:
    if self.name != name: self.name = name
    if self.surname != surname: self.surname = surname
    if self.phone != self._validate_phone(phone, True): self.phone = self._validate_phone(phone, True)
    if self.email != email: self.email = self._validate_email(email)
    if self.patronymic != patronymic: self.patronymic = patronymic
    db.session.commit()
  
  def _validate_phone(self, phone: str, revalidate: bool = False) -> int:
    number = parse_num(phone)
    if not is_valid_number(number):
      raise ValidationError('register', 'not_valid_phone')
    if number.national_number in [a.phone for a in self.query.all()] and not revalidate:
      raise ValidationError('register', 'phone_already_registered')
    return number.national_number

  def _validate_email(self, email: str) -> str:
    email_exists = self.query.filter_by(email=email).first()
    pattern = rf'{settings.EMAIL_PATTERN}'
    if email_exists:
      raise ValidationError('register', 'email_exists')
    if not re.match(pattern, email):
      raise ValidationError('register', 'email_invalid')
    return email

  def __repr__(self) -> str:
    return f'<Client +7{self.phone}>'


class Children(db.Model):
  uid = db.Column(db.String(7), primary_key=True)
  parent_uid = db.Column(db.ForeignKey(Clients.uid), nullable=False)
  name = db.Column(db.String(50), nullable=False)
  age = db.Column(db.Integer, nullable=False)

  def __init__(self, parentUid, name, age, **kwargs) -> None:
    self.uid = create_uid(7, [a.uid for a in self.query.all()] + [a.uid for a in Clients.query.all()])
    self.parent_uid = self._validate_parent_uid(parentUid)
    self.name = name
    self.age = age
    db.session.add(self)
    db.session.commit()

  def _validate_parent_uid(self, parent_uid):
    parent_uids = [a.uid for a in Clients.query.all()]
    if parent_uid not in parent_uids:
      raise ValueError('Undefined parent UID')
    return parent_uid
  
  @property
  def json(self) -> dict:
    return dict(uid=self.uid, name=self.name, age=self.age)
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @classmethod
  def all(cls):
    return [a.json for a in cls.query.all()]
    
  # def _validate_group_uid(self, group_uid=None):
  #   if not group_uid:
  #     return None
  #   # from .groups import Groups
  #   # group_uids = [a.uid for a in Groups.query.all()]
  #   # if group_uid not in group_uids:
  #   #   return ValueError('Undefined group UID')
  #   return group_uid
  