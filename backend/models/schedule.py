from backend import db
from backend.functions import create_uid
from backend.exceptions import ValidationError


class Schedule(db.Model):
  uid = db.Column(db.String(4), primary_key=True)
  day = db.Column(db.Integer, nullable=False)
  time_start = db.Column(db.Integer, nullable=False)
  time_end = db.Column(db.Integer, nullable=False)
  active = db.Column(db.Boolean, nullable=False, default=True)
  course_uid = db.Column(db.String(10), db.ForeignKey('Courses.uid'), nullable=False)

  def __init__(self, day, time_start, time_end, course_uid, active=None) -> None:
    self.uid = create_uid(4, [a.uid for a in self.query.all()])
    self.day = self._validate_day(day)
    self.time_start = self._validate_time('start', time_start)
    self.time_end = self._validate_time('end', time_end)
    self.course_uid = self._validate_course_uid(course_uid)
    self.active = active
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def _validate_time(period, timing) -> int:
    pass

  def _validate_course_uid(self, course_uid) -> str:
    from .courses import Courses
    if not course_uid:
      raise ValueError('Undefined COURSE_UID')
    course = Courses.query.filter_by(uid=course_uid).one_or_none()
    if not course:
      raise ValidationError('uid', 'not_found')
    return course.uid

  @staticmethod
  def _validate_day(day) -> int:
    pass
