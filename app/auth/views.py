import os
from PIL import Image
from flask import session, render_template, flash, redirect, url_for, request, Response, app
from app.auth import auth
from app.auth.forms import LoginForm, UserregisterForm, DriverregisterForm, PasswordChangeForm, \
    PicChangeForm
from app.auth.verifycode import verifycode
from datetime import datetime
from app import db
from flask_login import login_user, login_required, logout_user, current_user

verify_code = verifycode()


@auth.route('/', methods=['GET', 'POST'])   #登陆主界面
def index():
    from ..models import User
    form = LoginForm()
    if form.validate_on_submit():
        cur_user = User.query.filter_by(username=form.name.data).first()
        if cur_user and cur_user.verify_password(form.password.data):
            login_user(cur_user)
            if request.args.get('next') is not None:
                return redirect(request.args.get('next'))
            else:
                if form.selectRole.data == '1':
                    if cur_user.confirm == True:
                        return redirect(url_for('users.driverorder'))
                    else:
                        return redirect(url_for('auth.driverregister'))
                if form.selectRole.data == '2':
                    return redirect(url_for('users.passenger'))
                if form.selectRole.data == '3':
                    return redirect(url_for('users.digger'))
            flash(session.get('name') + ', welcome to gogoCar')
        else:
            flash('Invalid username or password.')
    return render_template('auth/index.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():  #注册
    from ..models import User
    form = UserregisterForm()
    if form.validate_on_submit():
        if session.get('code_text') == form.verification_code.data:
            user = User()
            user.username = form.name.data
            user.password = form.password.data
            user.tel = form.phonenum.data
            user.confirm = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.index'))
        else:
            flash('验证码输入错误，请重新输入')
            form.verification_code.data = ''
    return render_template('auth/register.html', form=form,
                           current_time=datetime.utcnow())


@auth.route('/driverregister', methods=['GET', 'POST'])   #司机的注册界面
def driverregister():   #注册
    from ..models import User
    form = DriverregisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=current_user.id).first()
        user.IDcard = form.IDCARD.data
        user.license_num = form.LICENSENUM.data
        user.license_type = form.LICENSETYPE.data
        user.number = form.CARNUM.data
        user.type = form.CARTYPE.data
        user.confirm = True
        #提交用户头像
        avatar = request.files['avatar']  #声明一个对象
        fanme = str(user.id) + '.png'
        # ALLOWER_EXIT = ['pang', 'jpg', 'jpeg', 'jig', 'png']
        # flag = '.' in fanme and fanme.split('.')[1] in ALLOWER_EXIT
        # if not flag:
        #     return render_template('/auth/driverregister.html', form=form)
        avatar.save(os.getcwd()+'/app/static/avatar/'+fanme)
        user.pic = '/static/avatar/{}'.format(fanme)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.driverorder'))
    return render_template('auth/driverregister.html', form=form, current_time=datetime.utcnow())


@auth.route('/userself')
@login_required
def userself():

    return render_template('auth/userself.html')


@auth.route('/userself/success')
@login_required
def change_success():

    return render_template('auth/success.html')


@auth.route('/userself/changepassword', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpassword.data):
            current_user.password = form.newpassword.data
            db.session.merge(current_user)
            db.session.commit()
        return redirect(url_for('auth.change_success'))
    return render_template('auth/change_password.html', form=form)


@auth.route('/userself/changepic', methods=['GET', 'POST'])
@login_required
def change_pic():
    form = PicChangeForm()
    if form.validate_on_submit():
        avatar = request.files['avatar']
        fanme = str(current_user.id) + '.png'
        avatar.save(os.getcwd() + '/app/static/avatar/' + fanme)
        current_user.pic = '/static/avatar/{}'.format(fanme)
        db.session.merge(current_user)
        db.session.commit()
        return redirect(url_for('auth.change_success'))
    return render_template('auth/change_pic.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    from ..models import OnlineUser
    user = OnlineUser.query.filter_by(user_id=current_user.id)
    if user:
        db.session.delete(user)
        db.session.commit()
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.index'))


@auth.route('/verifycode/')
def generate_verify_code():
    if request.args.get('imageid'):
        code_path, code_text = verify_code.generate_img()
        with open(code_path, 'rb') as f:
            code_img = f.read()
        session['code_text'] = code_text
        resp = Response(code_img, mimetype="image/jpeg")

        return resp




