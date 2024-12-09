from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from .config import Settings
from flask import Flask

app = Flask(__name__)
db = SQLAlchemy()
bcrypt = Bcrypt(app)
jwt = JWTManager()
settings = None
ROOT = None

def create_app():
  from .config import Config
  cfg = Config()
  global ROOT, settings
  ROOT = cfg.ROOT
  app.config.from_object(cfg)
  settings = Settings()
  settings.root = cfg.ROOT
  
  db.init_app(app)

  from .views import api, auth, cp
  app.register_blueprint(api, url_prefix='/api')
  app.register_blueprint(auth, url_prefix='/auth')
  app.register_blueprint(cp, url_prefix='/cp')

  jwt.init_app(app)

  from .models import Users, Admins

  @jwt.expired_token_loader
  def expired_token_callback(_jwt_header, jwt_payload):
    return dict(msg='THE'), 403
  
  @jwt.invalid_token_loader
  def invalid_token_callback(reason):
    return dict(msg='TNF'), 401
  
  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_payload):
    iden = jwt_payload['sub']
    # user = Users.query.filter_by(username=iden).one_or_none()
    # if user:
    #   return user
    admin = Admins.query.filter_by(uid=iden).one_or_none()
    return admin
  
  with app.app_context():
    db.create_all()

  return app
