from backend.exceptions import ValidationError
from datetime import datetime as dt
from backend import db


class Dismissed(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  course_uid = db.Column(db.String(10), db.ForeignKey('courses.uid'), nullable=False)
  by = db.Column(db.String(4), db.ForeignKey('admins.uid'), nullable=False)
  date = db.Column(db.Integer, nullable=False)

  def __init__(self, course_uid, by, date, **kwargs) -> None:
    course, self.course_uid = self._validate_course(course_uid)
    self.by = by
    self.date = self._validate_date(course, date)
    db.session.add(self)
    db.session.commit()

  @classmethod
  def all(cls):
    return [a.json for a in cls.query.all()]

  @staticmethod
  def _validate_course(uid):
    from .courses import Courses
    course = Courses.query.filter_by(uid=uid).first()
    if not course:
      raise ValidationError('course', 'not_found')
    return course, course.uid
  
  @staticmethod
  def _validate_date(course, date) -> int:
    dtime = dt.fromtimestamp(date)
    course_dtime = int(dtime.strftime("%H%M"))
    if course.day != dtime.weekday() or course_dtime != course.time_start:
      raise ValidationError('course', 'invalid_date')
    return int(dt(dtime.year, dtime.month, dtime.day, dtime.hour).timestamp())
  
  @property
  def executive(self) -> dict:
    from .admins import Admins
    admin = Admins.query.filter_by(uid=self.by).first()
    return admin.executive_info
  
  @property
  def course(self) -> dict:
    from .courses import Courses
    course = Courses.query.filter_by(uid=self.course_uid).first()
    return course.json
  
  @property
  def json(self) -> dict:
    return dict(id=self.id, course=self.course, by=self.executive, date=self.date)
  
  def __repr__(self) -> str:
    return f'<Dismissed Course for {dt.fromtimestamp(self.date).strftime("%d-%m-%Y %H:%M")}>'
  

  
