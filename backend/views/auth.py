from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask import Blueprint, jsonify, request as req
from backend.exceptions import ValidationError
from backend.functions import superuser_access
from backend.models import Users, Admins


auth = Blueprint('auth', __name__)


@auth.route('/', methods=['POST'])
def login():
  user_data = req.get_json()
  user_data['last_ip'] = req.remote_addr
  try:
    creds = Users.login(**user_data)
    return jsonify(dict(status='success', body=creds, message="Вы авторизованы"))
  except ValidationError as valid:
    return jsonify(valid.json), 400
  

@auth.route('/me', methods=['GET'])
@jwt_required()
def user_info():
  return jsonify(dict(status='success'), granted=bool(current_user), body=current_user.json)


@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  iden = get_jwt_identity()
  token = Users.refresh(iden)
  return jsonify(dict(status='success', token=token))


@auth.route('/admins/new', methods=['POST'])
@jwt_required(optional=True)
@superuser_access(current_user)
def new_admin():
  user_data = req.get_json()
  print(user_data)
  try:
    Admins(**user_data)
    return jsonify(dict(status='success', message='Администратор успешно создан!'))
  except ValidationError as valid:
    return jsonify(valid.json), 400
  

@auth.route('/admins', methods=['POST'])
def login_admin():
  user_data = req.get_json()
  try:
    creds = Admins.log_in(**user_data)
    return jsonify(dict(status='success', body=creds, message="Вы авторизованы"))
  except ValidationError as valid:
    return jsonify(valid.json), 400


@auth.route('/admins/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_admins():
  iden = get_jwt_identity()
  token = Admins.refresh(iden)
  return jsonify(dict(status='success', token=token))


@auth.route('/admins/restore', methods=['POST'])
@jwt_required(optional=True)
@superuser_access(current_user)
def restore_admins():
  if req.method == 'POST':
    user_data = req.get_json()
    Admins.restore(**user_data)
    return jsonify(dict(status="success", message="Пароль успешно сброшен"))
