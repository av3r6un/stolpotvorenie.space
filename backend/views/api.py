from backend.models import Bookings, Admins
from flask_jwt_extended import jwt_required, current_user
from flask import Blueprint, jsonify, request as req
from backend.functions import accessible_for_bots
from backend.exceptions import ValidationError
from datetime import datetime as dt

api = Blueprint('api', __name__)

@api.route('/', methods=['GET'])
def main():
  return jsonify(dict(ok=True))

@api.route('/bookings', methods=['POST', 'GET'])
@jwt_required(optional=True)
@accessible_for_bots(current_user)
def rw_booking():
  def_date = dt.now().timestamp()
  if req.method == 'POST':
    user_data = req.get_json()
    try:
      booking = Bookings(**user_data)
      return jsonify(dict(status='success', body=booking.json))
    except ValidationError as valid:
      return jsonify(valid.json), 400
  bookings = [a.json for a in Bookings.query.all()]
  if req.args.get('day'): bookings = Bookings.get_by_day(int(req.args.get('day', def_date)))
  return jsonify(status='success', body=bookings)


@api.route('/booking/<string:uid>', methods=['DELETE', 'PATCH', 'GET', 'PUT'])
@jwt_required(optional=True)
@accessible_for_bots(current_user)
def manage_booking(uid):
  booking = Bookings.query.filter_by(uid=uid).first()
  if not booking:
    return jsonify(status='error', message='Not Found'), 404
  if req.method == 'DELETE':
    booking.delete()
    return jsonify(status='success', message='Booking was deleted.')
  if req.method == 'PATCH':
    user_data = req.get_json()
    resp = booking.edit(**user_data)
    return jsonify(status='success', body=resp)
  if req.method == 'GET':
    return jsonify(status='success', body=booking.json)
  if req.method == 'PUT':
    booking.confirm()
    return jsonify(status='success', message='Booking was confirmed.', body=booking.base_info)


@api.route('/clients', methods=['POST'])
@jwt_required(optional=True)
@accessible_for_bots()
def add_clients():
  if req.method == 'POST':
    data = req.get_data()
    json = req.get_json()
    print('Data:', data, 'JSON:', json)
    return jsonify(dict(status='success', message='received'))


@api.route('/admins/<int:user_id>', methods=['GET'])
@jwt_required(optional=True)
@accessible_for_bots()
def check_admin(user_id):
  admin = Admins.query.filter_by(tg_id=user_id).one_or_none()
  if not admin:
    return jsonify(dict(status="success", body=None)), 404
  
  return jsonify(dict(status="success", body=admin.base_info))
