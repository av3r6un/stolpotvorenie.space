from phonenumbers import parse as parse_num, is_valid_number
from backend.exceptions import ValidationError
from datetime import datetime as dt
from backend.functions import create_uid
from backend import db, settings


class CalendarConstants(db.Model):
  uid = db.Column(db.String(3), primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  linked_person = db.Column(db.String(6), db.ForeignKey('users.uid'), nullable=False)
  day = db.Column(db.Integer, nullable=False)
  time_start = db.Column(db.Integer, nullable=False)
  time_end = db.Column(db.Integer, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=True)

  def __init__(self, name, linked_person, day, time_start, time_end) -> None:
    self.uid = create_uid(3, [a.uid for a in self.query.all()])
    self.name = name
    self.linked_person = linked_person
    self.day = self._validate_day(day)
    self.time_start = self._validate_time(time_start)
    self.time_end = self._validate_time(time_end)
    db.session.add(self)
    db.session.commit()

  def _validate_day(self, day):
    day_in_out_system = ''
  

class Bookings(db.Model):
  uid = db.Column(db.String(8), primary_key=True)
  date_start = db.Column(db.Integer, nullable=False)
  date_end = db.Column(db.Integer, nullable=False)
  duration = db.Column(db.Integer, nullable=False)
  contact_name = db.Column(db.String(100), nullable=False)
  contact_number = db.Column(db.Integer, nullable=False)
  confirmed = db.Column(db.Boolean, nullable=False, default=False)

  def __init__(self, date_start, date_end, contact_name, contact_number, **kwargs) -> None:
    self.uid = create_uid(8, [a.uid for a in self.query.all()])
    self.date_start = self._validate_date(date_start)
    self.date_end = self._validate_date(date_end)
    self.duration = self._count_duration(self.date_start, self.date_end)
    self.contact_name = contact_name
    self.contact_number = self._validate_number(contact_number)
    db.session.add(self)
    db.session.commit()

  @property
  def base_info(self):
    date_cnv = dt.fromtimestamp(self.date_start).strftime('%d-%m-%Y')
    time_cnv = f'c {dt.fromtimestamp(self.date_start).strftime("%H-%M")} до {dt.fromtimestamp(self.date_end).strftime("%H-%M")}'
    return dict(uid=self.uid, date=date_cnv, time=time_cnv, confirmed=self.confirmed)

  @property
  def json(self):
    return dict(uid=self.uid, date=self.date_start, duration=self.duration, name=self.contact_name, number=self.contact_number,
                confirmed=self.confirmed)
  
  @staticmethod
  def _validate_date(date):
    dd = dt.fromtimestamp(date)
    dn = dt.now()
    if not date > dn.timestamp():
      raise ValidationError('booking', 'previous_date')
    return dd.timestamp()

  @staticmethod
  def _count_duration(date_start, date_end):
    date_start = dt.fromtimestamp(date_start)
    date_end = dt.fromtimestamp(date_end)
    duration = int(date_end.hour - date_start.hour)
    return duration
  
  @staticmethod
  def _validate_number(phone):
    number = parse_num(phone)
    if not is_valid_number(number):
      raise ValidationError('booking', 'not_valid_phone')
    return number.national_number
  
  @classmethod
  def get_by_day(cls, day):
    day = dt.fromtimestamp(day)
    day_start = dt(day.year, day.month, day.day, 0, 0).timestamp()
    day_end = dt(day.year, day.month, day.day, 23, 59).timestamp()
    res = cls.query.filter(day_start < Bookings.date_start, Bookings.date_end < day_end).all()
    return dict(booked=[a.json for a in res])

  def confirm(self):
    self.confirmed = True
    db.session.commit()

  def edit(self, date_start = None, date_end = None, name = None, number = None, **kwargs):
    if date_start: self.date_start = self._validate_date(date_start)
    if date_end: self.date_end = self._validate_date(date_end)
    if name: self.contact_name = name
    if number: self.contact_number = self._validate_number(number)
    return self.json
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    return True
  