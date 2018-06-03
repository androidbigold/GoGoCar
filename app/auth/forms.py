from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, PasswordField, IntegerField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Required


class LoginForm(FlaskForm):  #定义一个LoginForm类，用来写登陆界面的表单
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    selectRole = SelectField('Role', choices=[('1', 'driver'), ('2', 'passenger')],
                             validators=[DataRequired()])
    submit = SubmitField('Log In')


class UserregisterForm(FlaskForm):   #定义一个nameform类,用来写注册界面的表单
    name = StringField('What is your name?', validators=[DataRequired()])
    password = PasswordField('What is your password?', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=100)])
    sex = SelectField('Sex', validators=[DataRequired()], choices=[('0', '点击进行选择'), ('1', '男'), ('2', '女')])
    phonenum = StringField('What is your phone number?', validators=[DataRequired()])
    verification_code = StringField(u'验证码', validators=[DataRequired(), Length(4, 4, message=u'填写4位验证码')])
    submit = SubmitField('Submit')


class DriverregisterForm(FlaskForm):   #定义一个Driverregisterform类,司机注册表
    IDCARD = StringField('What is your idcard?', validators=[DataRequired()])
    LICENSENUM = StringField('What is your license_number?', validators=[DataRequired()])
    LICENSETYPE = SelectField('What is your license type?', validators=[DataRequired()], choices=[
        ('0', '请选择驾驶证类型'), ('1', 'C1'), ('2', 'C2'), ('3', 'C3'), ('4', 'C4'), ('5', 'A1'), ('6', 'A2'),
        ('7', 'A3'), ('8', 'B1'), ('9', 'B2'), ('10', 'D'), ('11', 'E'), ('12', 'F'), ('13', 'M'),
        ('14', 'N'), ('15', 'P')])
    CARNUM = StringField('What is your car number?', validators=[DataRequired()])
    CARTYPE = StringField('What is your car type?', validators=[DataRequired()])
    avatar = FileField(u'选择上传的头像', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], u'只能上传图片！')
        ])
    submit = SubmitField('Submit')


class PasswordChangeForm(FlaskForm):
    oldpassword = PasswordField('What is your old password?')
    newpassword = PasswordField('What is your new password?', validators=[Required(), EqualTo('newpassword2', message='Passwords must match.')])
    newpassword2 = PasswordField('confirm new password', validators=[Required()])
    submit = SubmitField('Submit')


class PicChangeForm(FlaskForm):
    avatar = FileField(u'更换头像', validators=[FileAllowed(['jpg', 'jpeg', 'png'], u'只能上传图片！')])
    submit = SubmitField('Submit')