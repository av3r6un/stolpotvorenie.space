from backend import db
from datetime import datetime as dt
from backend.functions import create_uid
from backend.exceptions import ValidationError

class Attendance(db.Model):
  uid = db.Column(db.String(12), primary_key=True)
  client_uid = db.Column(db.String(7), nullable=False)
  is_mature = db.Column(db.Boolean, nullable=False, default=True)
  date = db.Column(db.Integer, nullable=False)
  event_type = db.Column(db.String(20), nullable=False)
  event_uid = db.Column(db.String(11), nullable=False)
  attended = db.Column(db.Boolean, nullable=False, default=True)

  def __init__(self, client_uid, date, uid, type, attended=None, **kwargs) -> None:
    self._validate_self(client_uid, date, uid)
    self.uid = create_uid(12, [a.uid for a in self.query.all()])
    self.client_uid, self.is_mature = self._validate_client_uid(client_uid)
    self.event_type = 'event' if type == 'event' else 'course'
    self.date = self._validate_date(date)
    self.event_uid = uid
    self.attended = attended
    temp_uid = self.uid
    db.session.add(self)
    db.session.commit()
    db.session.flush()
    # self._add_to_history(temp_uid)

  @property
  def client(self):
    from .clients import Clients, Children
    if self.is_mature:
      info = Clients.query.filter_by(uid=self.client_uid).first().json
    else:
      info = Children.query.filter_by(uid=self.client_uid).first().json
    return info
  
  @property
  def event(self):
    from .events import Events
    from .courses import Courses
    data = {'type': self.event_type, 'uid': self.event_uid, 'date': self.date}
    if self.event_type != 'event':
      event = Courses.query.filter_by(uid=self.event_uid).first()
    else:
      event = Events.query.filter_by(uid=self.event_uid).first()
    data['name'] = event.name
    return data
  
  @property
  def event_week(self):
    return dt.fromtimestamp(self.date).isocalendar().week

  @property
  def json(self):
    return dict(uid=self.uid, client=self.client, is_mature=self.is_mature, date=self.date, event=self.event, attended=self.attended)
  
  @classmethod
  def weekly(cls, week_num) -> list:
    return [a.json for a in cls.query.all() if a.event_week == int(week_num)]
  
  @classmethod
  def all(cls) -> list:
    return [a.json for a in cls.query.order_by(cls.date.desc()).all()]

  def _validate_client_uid(self, client_uid) -> tuple[str, bool]:
    from .clients import Clients, Children
    if not client_uid:
      raise ValidationError('attendance', 'uid_not_found')
    mature = True
    client = Clients.query.filter_by(uid=client_uid).one_or_none()
    if not client:
      mature = False
      client = Children.query.filter_by(uid=client_uid).one_or_none()
    if not client:
      raise ValidationError('uid', 'not_found')
    return client.uid, mature
  
  @staticmethod
  def _validate_date(date):
    subject_date = int(dt.fromisoformat(date).timestamp())
    current_date = int(dt.now().timestamp())
    if subject_date > current_date:
      raise ValidationError('attendance', 'too_big')
    return subject_date

  def _add_to_history(self, temp_uid) -> None:
    from .clients import Clients, Children
    from .schedule_old import Schedule
    just_created = self.query.filter_by(uid=temp_uid).first()
    client = (
      Clients.query.filter_by(uid=just_created.client_uid).one_or_none()
      if just_created.is_mature else
      Children.query.filter_by(uid=just_created.client_uid).one_or_none()
    )
    client_name = f'{client.name} {client.surname}' if just_created.is_mature else client.name
    date = dt.fromtimestamp(just_created.date).strftime('%d-%m-%Y %H:%M')
    course_name = Schedule.query.filter_by(uid=just_created.schedule_uid).first().course_name
    AttendanceHistory(client_name, date, course_name)

  def _validate_self(self, client_uid, date, event_uid):
    exists = self.query.filter_by(client_uid=client_uid, date=int(dt.fromisoformat(date).timestamp()), event_uid=event_uid).first()
    if exists:
      raise ValidationError('attendance', 'exists')
    return True

  def __repr__(self) -> str:
    return f'<Attendence for {"child " if not self.is_mature else ""} client {self.client_uid}>'


class AttendanceHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  client_name = db.Column(db.String(100), nullable=False)
  date = db.Column(db.String(16), nullable=False)
  course_name = db.Column(db.String(50), nullable=False)

  def __init__(self, client_name, date, course_name) -> None:
    self.client_name = client_name
    self.date = date
    self.course_name = course_name 
    db.session.add(self)
    db.session.commit()
