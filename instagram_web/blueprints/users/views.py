from flask import Blueprint, render_template, request, redirect, url_for, flash, Flask,send_from_directory
from werkzeug.security import generate_password_hash
from models.user import User, User_img
from app import login_manager, app
from flask_login import current_user
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "C:\\Users\\TOSHIBA\\Desktop\\nextagram\\nextagram_template\\static\\img"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER    


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == user_id)

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/myprofile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user = current_user
            user.img = filename
            user.save()
            return redirect(url_for("users.upload_file"))
    return render_template('users/edit.html') 





@users_blueprint.route('/myprofile/pro', methods=['GET', 'POST'])
def upload_file_pro():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user = current_user
            image = User_img(user_id = user.id, img=filename)
            image.save()
            return redirect(url_for("users.upload_file_pro"))
    return render_template('users/edit.html') 








@users_blueprint.route("/image/<name>")
def img(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@users_blueprint.route("/toggle", methods=["POST"])
def private():
    private = request.form.get("private", False)
    user = current_user
    if private:
        user.private = True
    else:
        user.private = False
    user.save()
    return redirect(url_for("users.upload_file"))    





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
    return render_template('users/edit.html')


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


# @users_blueprint.route('/<int:id>', methods=['POST'])
# def update(id):
#     pass


 
