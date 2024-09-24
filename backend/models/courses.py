from backend import db
from backend.functions import create_uid


class Courses(db.Model):
  uid = db.Column(db.String(10), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  description = db.Column(db.Text, nullable=True)
  info = db.Column(db.Text, nullable=True)
  groups = db.Column(db.Text, nullable=True)

  def __init__(self, name, description=None, info=None) -> None:
    self.uid = create_uid(10, [a.uid for a in self.query.all()])
    self.name = name
    self.description = description
    self.info = info
    db.session.add(self)
    db.session.commit()

  @property
  def _groups(self) -> list:
    return self.groups.split(',')
  
  @_groups.setter
  def groups(self, group_uid):
    self._groups.append(group_uid)
    self.groups = ','.join(self._groups)
    db.session.commit()
  
  def __repr__(self):
    return f'<Course ${self.uid} with {len(self._groups)} groups>'
