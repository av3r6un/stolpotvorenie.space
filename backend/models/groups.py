from backend import db


class Groups(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  course_uid = db.Column(db.String(10), db.ForeignKey('courses.uid'), nullable=False)
  type = db.Column(db.String(6), nullable=False) # ['mature', 'children', 'mixed']
  steaded = db.Column(db.Boolean, nullable=False, default=True)
  pupils = db.Column(db.Text, nullable=True)
  
  def __init__(self, courseUid, type, steaded, **kwargs) -> None:
    self.course_uid = courseUid
    self.type = type
    self.steaded = steaded
    db.session.add(self)
    db.session.commit()
  
  @property
  def group_type(self) -> str:
    return self._types[self.type]
  
  @classmethod
  def all_types(cls):
    return {'mature': 'Взрослая', 'children': 'Детская', 'mixed': 'Смешанная'}
  
  @classmethod
  def all(cls):
    return [a.json for a in cls.query.all()]
  
  @property
  def _types(self) -> dict:
    return {'mature': 'Взрослая', 'children': 'Детская', 'mixed': 'Смешанная'}
  
  @property
  def name(self) -> str:
    return f'{self.course["name"]} ({self.group_type} группа)'
  
  @property
  def course(self) -> str:
    from .courses import Courses
    course = Courses.query.filter_by(uid=self.course_uid).first()
    return course.json

  @property
  def _pupils(self) -> list:
    return self.pupils.split(',')
  
  @_pupils.setter
  def pupils(self, client_uid):
    self._pupils.append(client_uid)
    self.groups = ','.join(self._pupils)
    db.session.commit()
  
  @property
  def json(self) -> dict:
    return dict(type=self.type, group_type=self.group_type, steaded=self.steaded, course=self.course, name=self.name, id=self.id)
