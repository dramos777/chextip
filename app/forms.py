from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegisterUserForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Cadastrar')

class RegisterBranchForm(FlaskForm):
    location = StringField('Local', validators=[DataRequired()])
    branch_number = StringField('Identificador / Número', validators=[DataRequired()])
    model = StringField('Modelo', validators=[DataRequired()])
    manufacturer = StringField('Fabricante', validators=[DataRequired()])
    condominium_name = SelectField('Condomínio', choices=[], coerce=int, validators=[DataRequired()])
    #condominium_id = StringField('ID do Condomínio', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Dispositivo')

class EditBranchForm(FlaskForm):
    location = StringField('Local', validators=[DataRequired()])
    branch_number = StringField('Identificador / Número', validators=[DataRequired()])
    model = StringField('Modelo', validators=[DataRequired()])
    manufacturer = StringField('Fabricante', validators=[DataRequired()])
    condominium_name = SelectField('Condomínio', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar Alterações')

class EditUserForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    is_admin = BooleanField('Administrador')
    password = PasswordField('Nova senha (opcional)', validators=[Length(min=6, max=100)])
    submit = SubmitField('Salvar Alterações')

class RegisterCondominiumForm(FlaskForm):
    name = StringField('Nome do Condomínio', validators=[DataRequired()])
    rb_host_ip = StringField('RB HOST IP', validators=[DataRequired()])
    submit = SubmitField('Cadastrar Condomínio')

