from backend.exceptions import ValidationError
from backend.functions import create_uid
from backend import db, settings


class Courses(db.Model):
  uid = db.Column(db.String(10), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  description = db.Column(db.Text, nullable=True)
  info = db.Column(db.Text, nullable=True)
  executive_uid = db.Column(db.String(4), db.ForeignKey('admins.uid'), nullable=True)
  day = db.Column(db.Integer, nullable=False)
  time_start = db.Column(db.Integer, nullable=False)
  time_end = db.Column(db.Integer, nullable=False)
  age = db.Column(db.Integer, nullable=False, default=0)

  def __init__(self, name, executiveUid, day, timeStart, timeEnd,
               description=None, info=None, age=None, **kwargs) -> None:
    self.uid = self._create_uid()
    self.name = name
    self.day, self.time_start, self.time_end = self._validate_date(day, timeStart, timeEnd)
    self.description = description
    self.info = info
    self.executive_uid = self._validate_admin(executiveUid)
    self.age = age
    db.session.add(self)
    db.session.commit()

  @classmethod
  def all(cls) -> list:
    return [a.json for a in cls.query.all()]
  
  @classmethod
  def delete(cls, uid) -> None:
    course = cls.query.filter_by(uid=uid).first()
    db.session.delete(course)
    db.session.commit()
  
  @property
  def executive(self):
    from .admins import Admins
    admin = Admins.query.filter_by(uid=self.executive_uid).first()
    return admin.executive_info

  @property
  def type(self) -> str:
    for k, v in settings.COURSES_TYPES.items():
      if v == self.name:
        return k
    return 'default'
  
  @property
  def start_time(self) -> str:
    time_text = str(self.time_start)
    return f'{time_text[0:2]}:{time_text[2:]}'

  @property
  def end_time(self) -> str:
    time_text = str(self.time_end)
    return f'{time_text[0:2]}:{time_text[2:]}'
  
  @property
  def json(self) -> dict:
    return dict(uid=self.uid, name=self.name, description=self.description, info=self.info, day=self.day,
                executive=self.executive, type=self.type, age=self.age, time=dict(start=self.start_time, end=self.end_time))
  
  @property
  def base_info(self) -> dict:
    return dict(uid=self.uid, name=self.name, type=self.type)
  
  @staticmethod
  def _validate_admin(admin_uid) -> str:
    from .admins import Admins
    admin = Admins.query.filter_by(uid=admin_uid).first()
    if not admin:
      raise ValidationError('event', 'admin_not_found')
    return admin.uid
  
  def _create_uid(self) -> str:
    from .events import Events
    return create_uid(10, [a.uid for a in self.query.all()] + [a.uid for a in Events.query.all()])
  
  def _validate_date(self, date, time_start, time_end) -> tuple[int, int, int]:
    if date is None:
      raise ValidationError('event', 'date_not_found')
    ts = int(time_start.replace(':', ''))
    te = int(time_end.replace(':', ''))
    if te <= ts:
      raise ValidationError('event', 'small_timing')
    exists = self.query.filter_by(day=int(date), time_start=ts, time_end=te).first()
    if exists:
      raise ValidationError('course', 'already_exists')
    return date, ts, te

  def __repr__(self):
    return f'<Course ${self.uid} with {len(self._groups)} groups>'
