from backend import db
from backend.functions import create_uid


class Courses(db.Model):
  uid = db.Column(db.String(10), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  description = db.Column(db.Text, nullable=True)
  info = db.Column(db.Text, nullable=True)
  teacher_uid = db.Column(db.String(8), db.ForeignKey('teachers.uid'), nullable=True)

  def __init__(self, name, teacherUid, description=None, info=None, **kwargs) -> None:
    self.uid = create_uid(10, [a.uid for a in self.query.all()])
    self.name = name
    self.description = description
    self.info = info
    self.teacher_uid = teacherUid
    db.session.add(self)
    db.session.commit()

  @property
  def json(self) -> dict:
    return dict(uid=self.uid, name=self.name, description=self.description, info=self.info,
                teacher_uid=self.teacher_uid, type=self.type)
  
  @property
  def type(self) -> str:
    if self.name == 'Живопись':
      return 'artwork'
    elif self.name == 'Керамика':
      return 'ceramic'
    else:
      return 'lecture'
  
  @classmethod
  def all(cls):
    return [a.json for a in cls.query.all()]

  def __repr__(self):
    return f'<Course ${self.uid} with {len(self._groups)} groups>'
