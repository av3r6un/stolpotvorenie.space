from backend.models import Groups, Clients, Teachers, Courses, Schedule
from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend.exceptions import ValidationError
from backend import settings


cp = Blueprint('cp', __name__)


@cp.route('/groups', methods=['GET', 'POST'])
@jwt_required()
def cp_manage_groups():
  if req.method == 'POST':
    group = Groups(**req.get_json())
    return jsonify(dict(status="success", message='Группа успешно создана!', body=group.json))
  return jsonify(dict(status="success", body=Groups.all(), extra=Groups.all_types()))


@cp.route('/group/<int:group_id>', methods=['PUT'])
@jwt_required()
def cp_populate_group(group_id):
  group = Groups.query.filter_by(id=group_id).first()
  if not group:
    return jsonify(dict(status='error', message="Неверный ID группы!"))
  if req.method == 'PUT':
    us_info = req.get_json()
    user = Clients.query.filter_by(uid=us_info['uid']).first()
    if not user:
      return jsonify(dict(status="error", message="Неверный ID пользователя!"))
    group._pupils += user.uid
    return jsonify(dict(status="success", message="Пользователь успешно добавлен в группу!"))


@cp.route('/groups/main', methods=['GET'])
@jwt_required()
def main_groups():
  response = {
    'courses': Courses.all(),
    'groups': Groups.all(),
    'clients': Clients.all(),
  }
  extra = Groups.all_types()
  return jsonify(dict(status='success', body=response, extra=extra))


@cp.route('/teachers', methods=['GET', 'POST'])
@jwt_required()
def cp_teachers():
  if req.method == 'POST':
    teacher = Teachers(**req.get_json())
    return jsonify(dict(status="success", body=teacher.uid, message="Преподаватель успешно добавлен!"))
  return jsonify(dict(status="success", body=Teachers.all()))


@cp.route('/schedule', methods=['GET', 'POST'])
@jwt_required()
def cp_schedule():
  if req.method == 'POST':
    try:
      schedule = Schedule(**req.get_json())
      return jsonify(dict(status='success', body=schedule.json))
    except ValidationError as valid:
      return jsonify(valid.json)
  extra = {'working_days': settings.WORKING_DAYS}
  extra['time_open'], extra['time_close'] = settings.WORKING_HOURS
  return jsonify(dict(status="success", body=Schedule.all(), extra=extra))


@cp.route('/schedule/main', methods=['GET'])
@jwt_required()
def main_schedule():
  response = {
    'teachers': Teachers.all(),
    'courses': Courses.all(),
    'schedule': Schedule.all(),
    'groups': Groups.all(),
  }
  extra = {'working_days': settings.WORKING_DAYS}
  extra['time_open'], extra['time_close'] = settings.WORKING_HOURS
  return jsonify(dict(status='success', body=response, extra=extra))


@cp.route('/courses', methods=['GET', 'POST'])
@jwt_required()
def cp_courses():
  if req.method == 'POST':
    course = Courses(**req.get_json())
    return jsonify(dict(status='success', body=course.uid))
  return jsonify(dict(status='success', body=Courses.all()))


@cp.route('/clients/main', methods=['GET'])
@jwt_required()
def main_clients():
  response = {
    'clients': Clients.all()
  }
  return jsonify(status="success", body=response)


@cp.route('/clients', methods=['POST', 'GET'])
@jwt_required()
def cp_clients():
  if req.method == 'POST':
    try:
      client = Clients(**req.get_json())
      return jsonify(dict(status='success', message='Пользователь успешно добавлен', body=client.json))
    except ValidationError as valid:
      return jsonify(valid.json)
  return jsonify(dict(status='success', body=Clients.all()))
