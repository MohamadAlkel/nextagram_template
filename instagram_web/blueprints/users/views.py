from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.user import User
from app import login_manager
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    pass


@users_blueprint.route('/create_acc', methods=['POST'])
def create_acc():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    hashed_password = generate_password_hash(password)
    create = User(username=username, email= email, password = hashed_password)

    if create.save():
        return redirect(url_for("users.new"))
    else:
        return  render_template('users/new.html', username=username, email= email, password = password , errors = create.errors)




# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#    user = User.get_by_id(current_user.id)
#    return render_template('editprofile.html', user=user)


@users_blueprint.route('/<username>/update', methods=['POST'])
def update(username):
    user = User.get_or_none(User.username==username)

    if current_user == user:
        if request.form['email']:
            user.email = request.form['email']
        if request.form['username']:
            user.username = request.form['username']

    if user.save():
        flash('Profile successfully updated', 'primary')
        return redirect(url_for('users.show'))
    else:
        flash('Error encounted, profile did not update', 'danger')
        return redirect(url_for('users.show'))


        

        


@users_blueprint.route('/myprofile', methods=["GET"])
def show():
    return render_template('users/user_pag.html')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


# @users_blueprint.route('/<int:id>', methods=['POST'])
# def update(id):
#     pass


 
