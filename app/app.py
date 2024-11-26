from forms import LoginForm, RegisterBranchForm, RegisterUserForm, RegisterCondominiumForm, EditBranchForm, EditUserForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Flask, render_template, redirect, url_for, flash, request
from logging.handlers import RotatingFileHandler
from models import db, User, Condominium, Branch
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import subprocess
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER', 'admin')}:{os.getenv('MYSQL_PASSWORD', 'admin')}@{os.getenv('MYSQL_HOST', '127.0.0.1')}/{os.getenv('MYSQL_DATABASE', 'condominios_db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secreta-chave-chextip'
app.config['LOG_ACCESS_PATH'] = '/var/log/chextip/web_chextip_access.log'
app.config['LOG_AUDIT_PATH'] = '/var/log/chextip/web_chextip_audit.log'

# Initializing extensions
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure access and audit logs
access_log_handler = RotatingFileHandler(app.config['LOG_ACCESS_PATH'], maxBytes=10000, backupCount=1)
access_log_handler.setLevel(logging.INFO)

audit_log_handler = RotatingFileHandler(app.config['LOG_AUDIT_PATH'], maxBytes=10000, backupCount=1)
audit_log_handler.setLevel(logging.INFO)

app.logger.addHandler(access_log_handler)
app.logger.addHandler(audit_log_handler)

# Function to create tables automatically if they do not exist
@app.before_first_request
def create_tables_and_admin():
    db.create_all()
    print("Tabelas verificadas/criadas com sucesso.")

    # Check if admin user exists, create if necessary
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_user = User(username='admin', is_admin=True)
        admin_user.set_password('admin')
        db.session.add(admin_user)

        db.session.add(admin_user)
        db.session.commit()
        print("Usuário admin criado com sucesso.")
    else:
        print("Usuário admin já existe.")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    # Verificar se o usuário está autenticado
    if 'logged_in' in session and session['logged_in']:
        return "Bem-vindo à sua página principal!"
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            logging.info(f'{user.username} logged in')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check username and password.')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    condominiums = Condominium.query.order_by(Condominium.name.asc()).all()
    return render_template('dashboard.html', condominiums=condominiums)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Você saiu com sucesso.')
    return redirect(url_for('login'))

@app.route('/condominium/<int:condo_id>')
@login_required
def show_condominium(condo_id):
    condo = Condominium.query.get_or_404(condo_id)
    branches = Branch.query.filter_by(condominium_id=condo_id).order_by(Branch.branch_number.asc()).all()

    return render_template('condominium.html', condo=condo, branches=branches)

@app.route('/register_branch', methods=['GET', 'POST'])
@login_required
def register_branch():
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    form = RegisterBranchForm()
    condominiums = Condominium.query.all()
    form.condominium_name.choices = [(condo.id, condo.name) for condo in condominiums]
    if form.validate_on_submit():
        # Check if extention already exist
        existing_branch = Branch.query.filter_by(branch_number=form.branch_number.data, condominium_id=form.condominium_name.data).first()
        if existing_branch:
            flash('Ramal já existe para este condomínio.')
            return redirect(url_for('register_branch'))

        branch = Branch(
            location=form.location.data,
            branch_number=form.branch_number.data,
            model=form.model.data,
            manufacturer=form.manufacturer.data,
            condominium_id=form.condominium_name.data
        )
        db.session.add(branch)
        db.session.commit()
        logging.info(f'Branch {form.branch_number.data} added')
        flash('Ramal cadastrado com sucesso.')
        return redirect(url_for('dashboard'))
    return render_template('cadastro_ramal.html', form=form)

@app.route('/restart_branch/<int:branch_id>')
@login_required
def restart_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    output = ""
    try:
        result = subprocess.run(['./scripts/bin/chextip', str(branch.branch_number), branch.model],
                                check=True, capture_output=True, text=True)
        output = result.stdout
        logging.info(f'Branch {branch.branch_number} restarted by {current_user.username}')
        flash(f'Ramal {branch.branch_number} reiniciado com sucesso.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Failed to restart branch {branch.branch_number}. Error: {e}')
        flash('Falha ao reiniciar o ramal.')
        output = e.stderr  # Armazena a saída de erro

    return render_template('output.html', output=output, condo_id=branch.condominium_id)

@app.route('/register_user', methods=['GET', 'POST'])
@login_required
def register_user():
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    form = RegisterUserForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Usuário já existe. Escolha outro nome de usuário.')
            return redirect(url_for('register_user'))

        user = User(username=form.username.data, is_admin=form.is_admin.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Usuário {form.username.data} criado com sucesso.')
        logging.info(f'User {form.username.data} created by {current_user.username}')
        return redirect(url_for('dashboard'))
    return render_template('register_user.html', form=form)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('Você não pode se excluir!')
        return redirect(url_for('dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {user.username} removido com sucesso.')
    logging.info(f'User {user.username} deleted by {current_user.username}')
    return redirect(url_for('dashboard'))

@app.route('/edit_branch/<int:branch_id>', methods=['GET', 'POST'])
@login_required
def edit_branch(branch_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    branch = Branch.query.get_or_404(branch_id)
    form = EditBranchForm(obj=branch)
    if form.validate_on_submit():
        branch.location = form.location.data
        branch.branch_number = form.branch_number.data
        branch.model = form.model.data
        branch.manufacturer = form.manufacturer.data
        db.session.commit()
        logging.info(f'Branch {branch.branch_number} edited by {current_user.username}')
        flash(f'Ramal {branch.branch_number} editado com sucesso.')
        return redirect(url_for('show_condominium', condo_id=branch.condominium_id))
    return render_template('edit_branch.html', form=form, branch=branch)

@app.route('/delete_branch/<int:branch_id>', methods=['POST'])
@login_required
def delete_branch(branch_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    flash(f'Ramal {branch.branch_number} removido com sucesso.')
    logging.info(f'Branch {branch.branch_number} deleted by {current_user.username}')
    return redirect(url_for('show_condominium', condo_id=branch.condominium_id))

@app.route('/register_condominium', methods=['GET', 'POST'])
@login_required
def register_condominium():
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    form = RegisterCondominiumForm()
    if form.validate_on_submit():
        existing_condo = Condominium.query.filter_by(name=form.name.data).first()
        if existing_condo:
            flash('Condomínio já existe. Escolha outro nome.')
            return redirect(url_for('register_condominium'))

        condo = Condominium(name=form.name.data,
                            rb_host_ip=form.rb_host_ip.data)
        db.session.add(condo)
        db.session.commit()
        flash(f'Condomínio {form.name.data} cadastrado com sucesso.')
        logging.info(f'Condominium {form.name.data} created by {current_user.username}')
        return redirect(url_for('dashboard'))
    return render_template('register_condominium.html', form=form)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.is_admin = form.is_admin.data

        # Atualiza a senha somente se o campo estiver preenchido
        if form.password.data:
            user.set_password(form.password.data)

        db.session.commit()
        logging.info(f'User {user.username} updated by {current_user.username}')
        flash(f'Usuário {user.username} editado com sucesso.')
        return redirect(url_for('dashboard'))

    return render_template('edit_user.html', form=form, user=user)

@app.route('/edit_condominium/<int:condo_id>', methods=['GET', 'POST'])
@login_required
def edit_condominium(condo_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    condominium = Condominium.query.get_or_404(condo_id)
    form = RegisterCondominiumForm(obj=condominium)

    if form.validate_on_submit():
        condominium.name = form.name.data
        condominium.rb_host_ip = form.rb_host_ip.data
        db.session.commit()
        logging.info(f'Condominium {condominium.name} updated by {current_user.username}')
        flash(f'Condomínio {condominium.name} editado com sucesso.')
        return redirect(url_for('dashboard'))

    return render_template('edit_condominium.html', form=form, condominium=condominium)

@app.route('/delete_condominium/<int:condo_id>', methods=['POST'])
@login_required
def delete_condominium(condo_id):
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    condominium = Condominium.query.get_or_404(condo_id)
    branches = Branch.query.filter_by(condominium_id=condo_id).all()

    for branch in branches:
        db.session.delete(branch)

    db.session.delete(condominium)
    db.session.commit()

    flash('Condomínio e ramais removidos com sucesso!')
    return redirect(url_for('dashboard'))

@app.route('/users')
@login_required
def users():
    if not current_user.is_admin:
        flash('Ação não permitida.')
        return redirect(url_for('dashboard'))

    all_users = User.query.order_by(User.username.asc()).all()
    return render_template('users.html', users=all_users)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
