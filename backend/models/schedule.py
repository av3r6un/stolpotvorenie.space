from backend import db, settings
from backend.functions import create_uid
from backend.exceptions import ValidationError


class Schedule(db.Model):
  uid = db.Column(db.String(4), primary_key=True)
  day = db.Column(db.Integer, nullable=False)
  time_start = db.Column(db.Integer, nullable=False)
  time_end = db.Column(db.Integer, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=True)
  group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

  def __init__(self, day, timeStart, timeEnd, groupId, active=None, **kwargs) -> None:
    self.uid = create_uid(4, [a.uid for a in self.query.all()])
    self.time_start = self._validate_daytime('start', day, timeStart)
    self.time_end = self._validate_daytime('end', day, timeEnd)
    self.group_id = self._validate_group_id(groupId)
    self.active = active
    db.session.add(self)
    db.session.commit()

  @classmethod
  def all(cls) -> list:
    return [a.json for a in cls.query.all()]
  
  @property
  def group(self) -> dict:
    from .groups import Groups
    group = Groups.query.filter_by(id=self.group_id).first()
    return group.json
  
  @property
  def ts_text(self):
    time_text = str(self.time_start)
    return f'{time_text[0:2]}:{time_text[2:]}'

  @property
  def te_text(self):
    time_text = str(self.time_end)
    return f'{time_text[0:2]}:{time_text[2:]}'

  @property
  def json(self) -> dict:
    return dict(uid=self.uid, day=self.day, timeStart=self.ts_text, timeEnd=self.te_text,
                group=self.group)

  def _validate_daytime(self, period: str, day, timing: str) -> int:
    week_day, day = self._validate_day(day)
    time = int(timing.replace(':', ''))

    if period == 'end':
      if time <= self.time_start or day != self.day:
        raise ValidationError('timing', 'small_than_start')
      return time
    if not self.day: self.day = day
    return time

  def _validate_group_id(self, group_id) -> str:
    from .groups import Groups
    if not group_id:
      raise ValueError('Undefined COURSE_UID')
    group = Groups.query.filter_by(id=group_id).one_or_none()
    if not group:
      raise ValidationError('uid', 'not_found')
    return group.id

  @staticmethod
  def _validate_day(day) -> int:
    week_day = settings.WORKING_DAYS[day]
    return week_day, day
