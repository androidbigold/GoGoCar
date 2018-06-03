from flask import render_template, request, session, redirect, url_for, jsonify
from app.users.forms import PlaceForm
from . import users
from app import db, socketio
import time
from flask_socketio import emit
from flask_login import login_required, current_user


# for passenger

@users.route('/passenger', methods=['GET', 'POST'])
@login_required
def passenger():
    from ..models import OnlineUser, User
    onlineusers = OnlineUser.query.all()
    getlats = []
    getlngs = []
    tels = []
    scords = []
    pics = []
    ids = []
    for onlineuser in onlineusers:
        user = User.query.filter_by(onliner=onlineuser).first()
        if user.confirm == 1:
            getlats.append(user.curlat)
            getlngs.append(user.curlng)
            tels.append(user.tel)
            scords.append(user.scord)
            pics.append(user.pic)
            ids.append(user.id)
    if request.method == 'POST':
        user_pos = request.get_json(force=True)
        cur_user = User.query.filter_by(id=current_user.id).first()
        cur_user.curlng = user_pos['curlng']
        cur_user.curlat = user_pos['curlat']
        global u_start
        u_start = user_pos['startp']
        db.session.merge(cur_user)
        db.session.commit()
    # global user_pos
    # user_pos = {'startp': "北京邮电大学"}
    return render_template('users/passenger.html', tels=tels, scords=scords, pics=pics,
                           getlats=getlats, getlngs=getlngs, ids=ids)


@users.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    from ..models import User, OnlineUser
    form = PlaceForm()
    driver_id = request.args.get('id')
    cur_driver = User.query.filter_by(id=driver_id).first()
    if request.method == 'POST':
        global orders
        order_data = request.get_json(force=True)
        orders = {"code": 1, "pubkey": order_data["pubkey"], "msg": order_data["msg"], "order": order_data["order"]}
        driver = OnlineUser.query.filter_by(user_id=driver_id).first()
        if driver:
            socketio.emit('server_response', orders, room=driver.ipadd)
            time.sleep(5)
    return render_template('users/order.html', form=form, driverid=cur_driver.id,
                           drivertel=cur_driver.tel, driverpic=cur_driver.pic, cartype=cur_driver.type,
                           carnum=cur_driver.number, startp=u_start, distance=request.args.get('distance'))


@users.route('/orderfinish')
@login_required
def orderfinish():
    from ..models import User
    d_user = User.query.filter_by(id=request.args.get('id')).first()
    d_lat = d_user.curlat
    d_lng = d_user.curlng
    p_user = User.query.filter_by(id=current_user.id).first()
    p_lat = p_user.curlat
    p_lng = p_user.curlng
    return render_template('users/orderfinish.html', d_lat=d_lat, d_lng=d_lng, p_lat=p_lat, p_lng=p_lng)


# for driver


@users.route('/driverorder', methods=['GET', 'POST'])
@login_required
def driverorder():
    from ..models import User
    if request.method == 'POST':
        positiondata = request.get_json(force=True)
        cur_user = User.query.filter_by(id=current_user.id).first()
        cur_user.curlat = positiondata["curLat"]
        cur_user.curlng = positiondata["curLng"]
        db.session.merge(cur_user)
        db.session.commit()
    return render_template('users/driverorder.html')


@users.route('/orderback', methods=['GET', 'POST'])
@login_required
def orderback():
    from ..models import User
    d_user = User.query.filter_by(id=current_user.id).first()
    d_lat = d_user.curlat
    d_lng = d_user.curlng
    p_user = User.query.filter_by(id=request.args.get('id')).first()
    p_lat = p_user.curlat
    p_lng = p_user.curlng
    if request.method == 'POST':
        positiondata = request.get_json(force=True)
        d_user.curlat = positiondata["curLat"]
        d_user.curlng = positiondata["curLng"]
        db.session.merge(d_user)
        db.session.commit()
    return render_template('users/orderback.html', d_lat=d_lat, d_lng=d_lng, p_lat=p_lat, p_lng=p_lng)


# for all


@users.route('/navigation', methods=['GET', 'POST'])
@login_required
def navigation():
    global orders
    if request.method == 'POST':
        cost = request.get_json(force=True)
        orders['fee'] = cost

    return render_template('users/navigation.html', startp="北京邮电大学", endp="北京师范大学")


@socketio.on('connect')
def handle_connect():
    from ..models import OnlineUser, User
    cur_user = User.query.filter_by(id=current_user.id).first()
    have_driver = OnlineUser.query.filter_by(user_id=cur_user.id).first()
    if have_driver:
        have_driver.ipadd = request.sid
        db.session.merge(have_driver)
        db.session.commit()
    else:
        cur_driver = OnlineUser()
        cur_driver.user = cur_user
        cur_driver.ipadd = request.sid
        db.session.add(cur_driver)
        db.session.commit()
    emit('server_response', {'data': 'Connected'})


# @socketio.on('disconnect')
# def handle_disconnect():
#     from ..models import OnlineUser
#     cur_driver = OnlineUser.query.filter_by(user_id=current_user.id).first()
#     db.session.delete(cur_driver)
#     db.session.commit()


@socketio.on('feedback')
def test_msg(data):
    from ..models import OnlineUser
    sen_to_id = data['id']
    send_to_user = OnlineUser.query.filter_by(user_id=sen_to_id).first()
    send_to_ip = send_to_user.ipadd
    emit('acceptorder', {'data': 1}, room=send_to_ip)

