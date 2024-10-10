from backend import db
from datetime import datetime as dt
from backend.functions import create_uid
from backend.exceptions import ValidationError

class Attendance(db.Model):
  uid = db.Column(db.String(12), primary_key=True)
  client_uid = db.Column(db.String(7), db.ForeignKey('clients.uid'), nullable=False)
  is_mature = db.Column(db.Boolean, nullable=False, default=True)
  date = db.Column(db.Integer, nullable=False, default=int(dt.now().timestamp()))
  schedule_uid = db.Column(db.String(11), db.ForeignKey('schedule.uid'), nullable=False)
  attended = db.Column(db.Boolean, nullable=False, default=True)

  def __init__(self, client_uid, schedule_uid, date=None, attended=None, **kwargs) -> None:
    self.uid = create_uid(12, [a.uid for a in self.query.all()])
    self.client_uid, self.is_mature = self._validate_client_uid(client_uid)
    self.schedule_uid = schedule_uid
    self.date = date if date else int(dt.now().timestamp())
    self.attended = attended
    temp_uid = self.uid
    db.session.add(self)
    db.session.commit()
    db.session.flush()
    self._add_to_history(temp_uid)
  
  @property
  def json(self):
    return dict(uid=self.uid, client_uid=self.client_uid, is_mature=self.is_mature,
                date=self.date, schedule_uid=self.schedule_uid, attended=self.attended)
  
  def _validate_client_uid(self, client_uid) -> tuple[str, bool]:
    from .clients import Clients, Children
    if not client_uid:
      raise ValueError('Undefined CLIENT_UID')
    mature = True
    client = Clients.query.filter_by(uid=client_uid).one_or_none()
    if not client:
      mature = False
      client = Children.query.filter_by(uid=client_uid).one_or_none()
    if not client:
      raise ValidationError('uid', 'not_found')
    return client.uid, mature
  
  def _add_to_history(self, temp_uid) -> None:
    from .clients import Clients, Children
    from .schedule import Schedule
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
