from functools import wraps
import secrets
import string

def create_uid(length, uids):
  alp = string.ascii_letters + string.digits
  while True:
    uid = ''.join(secrets.choice(alp) for _ in range(length))
    if uid not in uids:
      return uid
    
def superuser_access(current_user):
  def endpoint_wrapper(func):
    @wraps(func)
    def is_superuser(*args, **kwargs):
      from backend.models import Admins
      from flask import request as req, jsonify
      if not current_user.superuser:
        return jsonify(dict(status='error', message='Not Allowed')), 401
      return func(*args, **kwargs)
    return is_superuser
  return endpoint_wrapper
  
def accessible_for_bots(current_user):
  def endpoint_wrapper(func):
    @wraps(func)
    def is_bot(*args, **kwargs):
      user = None
      from backend import app
      from flask import request as req, jsonify
      if not current_user:
        token = req.headers.get('X-API-TOKEN')
        if not token:
          return jsonify(dict(status='error', message='Token not found!')), 401
        if token in app.config['BOT_TOKENS']:
          user = True
      else:
        user = current_user
      if not user:
        return jsonify(dict(status='error', message='You are not allowed!')), 401
      return func(*args, **kwargs)
    return is_bot
  return endpoint_wrapper
