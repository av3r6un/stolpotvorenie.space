from backend.functions import create_uid
from backend import db

class Teachers(db.Model):
  uid = db.Column(db.String(8), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  surname = db.Column(db.String(50), nullable=False)
  patronymic = db.Column(db.String(50), nullable=True) 

  def __init__(self, name, surname, patronymic = None, **kwargs) -> None:
    self.uid = create_uid(8, [a.uid for a in self.query.all()])
    self.name = name
    self.surname = surname
    self.patronymic = patronymic
    db.session.add(self)
    db.session.commit()

  @property
  def full_name(self) -> str:
    return f'{self.surname} {self.name} {self.patronymic}'

  @property
  def json(self) -> dict:
    return dict(uid=self.uid, name=self.name, surname=self.surname,
                patronymic=self.patronymic, full_name=self.full_name)

  @classmethod
  def all(cls):
    return [a.json for a in cls.query.all()]
