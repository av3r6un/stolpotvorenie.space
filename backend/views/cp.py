from backend.models import Clients, Courses, Events, Admins, Dismissed, Children, Groups
from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend.exceptions import ValidationError
from backend import settings


cp = Blueprint('cp', __name__)


@cp.route('/schedule/main', methods=['GET'])
@jwt_required()
def main_schedule():
  response = {
    'admins': Admins.all_executive(),
    'events': Courses.all() + Events.all(),
    'dismissed': Dismissed.all(),
  }
  extra = {'working_days': settings.WORKING_DAYS}
  extra['time_open'], extra['time_close'] = settings.WORKING_HOURS
  return jsonify(dict(status='success', body=response, extra=extra))


@cp.route('/courses', methods=['GET', 'POST'])
@jwt_required()
def cp_courses():
  if req.method == 'POST':
    course = Courses(**req.get_json())
    return jsonify(dict(status='success', body=course.json))
  return jsonify(dict(status='success', body=Courses.all()))


@cp.route('/course/<string:uid>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def cp_manage_course(uid: str):
  if req.method == 'PUT':
    try:
      dm = Dismissed(course_uid=uid, by=current_user.uid, **req.get_json())
      return jsonify(dict(status='success', message='Занятие успешно отменено.', body=dm.json))
    except ValidationError as valid:
      return jsonify(valid.json)
  if req.method == 'DELETE':
    Courses.delete(uid)
    return jsonify(status='success', message='Курс успено удален')
  course = Courses.query.filter_by(uid=uid).one_or_none()
  if not course:
    return jsonify(status='error', message='Указанный курс не найден'), 404
  return course.json


@cp.route('/events', methods=['GET', 'POST'])
@jwt_required()
def cp_events():
  if req.method == 'POST':
    event = Events(**req.get_json())
    return jsonify(dict(status="success", body=event.json))
  return jsonify(dict(status="success", body=Events.all()))


@cp.route('/clients/main', methods=['GET'])
@jwt_required()
def main_clients():
  response = {
    'clients': Clients.all(),
    'groups': Groups.all(),
  }
  return jsonify(status="success", body=response)


@cp.route('/clients', methods=['POST', 'GET', 'PUT'])
@jwt_required()
def cp_clients():
  if req.method == 'PUT':
    try:
      child = Children(**req.get_json())
      return jsonify(dict(status='success', body=child.json, message='Ребенок успешно добавлен'))
    except ValidationError as valid:
      return jsonify(valid.json)
  if req.method == 'POST':
    try:
      client = Clients(**req.get_json())
      return jsonify(dict(status='success', message='Пользователь успешно добавлен', body=client.json))
    except ValidationError as valid:
      return jsonify(valid.json)
  return jsonify(dict(status='success', body=Clients.all()))


@cp.route('/client/<string:uid>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def cp_manage_client(uid):
  client = Clients.query.filter_by(uid=uid).one_or_none()
  if not client:
    return jsonify(dict(status="error", message="Клиент не найден"))
  if req.method == 'PUT':
    client.edit(**req.get_json())
    return jsonify(dict(status="success", message="Клиент успешно изменен", body=client.json))
  if req.method == 'DELETE':
    client.delete()
    return jsonify(dict(status="success", message="Клиент успешно удален"))
  return jsonify(dict(status="success", body=client.json))


@cp.route('/me', methods=['GET'])
@jwt_required()
def cp_info_about_me():
  return jsonify(dict(status="success", body=current_user.json))


@cp.route('/admins/info', methods=['POST', 'PUT'])
@jwt_required()
def cp_change_admin_info():
  if req.method == 'POST':
    try:
      current_user.edit_persona(**req.get_json())
      return jsonify(status="success", message="Информация успешно обновлена")
    except ValidationError as valid:
      return jsonify(valid.json)
  if req.method == 'PUT':
    try:
      current_user.update_password(**req.get_json())
      return jsonify(dict(status="success", message="Пароль успешно обновлён"))
    except ValidationError as valid:
      return jsonify(valid.json)
