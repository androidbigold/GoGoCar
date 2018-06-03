from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, PasswordField, BooleanField, FileField, \
    FloatField
from wtforms.validators import DataRequired, Length, NumberRange


class DriverForm(FlaskForm):   #定义一个Driverform类,司机主页面用来显示订单的页面
    IDCARD = StringField('What is your idcard?', validators=[DataRequired()])
    LICENSENUM = StringField('What is your license_number?', validators=[DataRequired()])
    LICENSETYPE = SelectField('What is your license type?', validators=[DataRequired()], choices=[
        ('0', '请选择驾驶证类型'), ('1', 'C1'), ('2', 'C2'), ('3', 'C3'), ('4', 'C4'), ('5', 'A1'), ('6', 'A2'),
        ('7', 'A3'), ('8', 'B1'), ('9', 'B2'), ('10', 'D'), ('11', 'E'), ('12', 'F'), ('13', 'M'),
        ('14', 'N'), ('15', 'P')])
    CARNUM = StringField('What is your car number?', validators=[DataRequired()])
    CARTYPE = StringField('What is your car type?', validators=[DataRequired()])
    avatar = FileField('请上传照片')
    submit = SubmitField('Submit')


class PlaceForm(FlaskForm):
    startp = StringField('Startplace', validators=[DataRequired()])
    endp = StringField('Destination', validators=[DataRequired()])
    tel = StringField('Tel',validators=[DataRequired()])
    counts = SelectField('passenger counts', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
                           validators=[DataRequired()])
    addtip = StringField('Tips')
    driverid = IntegerField('Driver ID')
    drivertel = StringField('Driver Tel')
    cartype = StringField('Car Type')
    carnumber = StringField('Car Number')
    distance = IntegerField('Distance')



