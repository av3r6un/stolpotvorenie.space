from backend.exceptions import ValidationError
from backend.functions import create_uid
from datetime import datetime as dt, timedelta as delta
from backend import db, settings


class Events(db.Model):
  uid = db.Column(db.String(10), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  date = db.Column(db.Integer, nullable=False)
  time_start = db.Column(db.Integer, nullable=False)
  time_end = db.Column(db.Integer, nullable=False)
  executive_uid = db.Column(db.String(4), db.ForeignKey('admins.uid'), nullable=False)
  age = db.Column(db.Integer, nullable=False, default=0)
  comment = db.Column(db.Text, nullable=True)

  def __init__(self, name, date, duration, executiveUid, age=None, comment=None, **kwargs) -> None:
    self.uid = self._create_uid()
    self.name = name
    self.date, self.time_start, self.time_end = self._validate_date(date, duration)
    self.executive_uid = self._validate_admin(executiveUid)
    self.age = self._validate_age(age) if age else None
    self.comment = comment
    db.session.add(self)
    db.session.commit()

  @classmethod
  def all(cls) -> list:
    return [a.json for a in cls.query.all()]

  @property
  def executive(self) -> dict:
    from .admins import Admins
    admin = Admins.query.filter_by(uid=self.executive_uid).first()
    return admin.executive_info
  
  @property
  def start_time(self) -> str:
    time_text = str(self.time_start)
    return f'{time_text[0:2]}:{time_text[2:]}'

  @property
  def end_time(self) -> str:
    time_text = str(self.time_end)
    return f'{time_text[0:2]}:{time_text[2:]}'
  
  @property
  def type(self) -> str:
    return 'event'
  
  @property
  def json(self):
    return dict(uid=self.uid, name=self.name, date=int(self.date), time=dict(start=self.start_time, end=self.end_time),
                executive=self.executive, age=self.age, type=self.type, comment=self.comment)

  def _create_uid(self) -> str:
    from .courses import Courses
    return create_uid(10, [a.uid for a in Courses.query.all()] + [a.uid for a in self.query.all()])
  
  def _validate_date(self, date, duration) -> tuple[int, int, int]:
    if not date:
      raise ValidationError('event', 'date_not_found')
    event_date_obj = dt.fromisoformat(date)
    event_date = dt(year=event_date_obj.year, month=event_date_obj.month, day=event_date_obj.day, hour=event_date_obj.hour, minute=0 if event_date_obj.minute != 30 else event_date_obj.minute)
    date = int(dt(year=event_date.year, month=event_date.month, day=event_date.day).timestamp())
    time_start = int(event_date.strftime('%H%M'))
    time_end = int((event_date + delta(hours=int(duration))).strftime('%H%M'))
    exists = self.query.filter_by(date=date, time_start=time_start, time_end=time_end).first()
    if exists:
      raise ValidationError('event', 'already_exists')
    return date, time_start, time_end
  
  @staticmethod
  def _validate_admin(admin_uid) -> str:
    from .admins import Admins
    admin = Admins.query.filter_by(uid=admin_uid).first()
    if not admin:
      raise ValidationError('event', 'admin_not_found')
    return admin.uid
  
  @staticmethod
  def _validate_age(age: str) -> int:
    age_string = age.replace('+', '')
    return int(age_string)
  
  def delete(self) -> None:
    db.session.delete(self)
    db.session.commit()
