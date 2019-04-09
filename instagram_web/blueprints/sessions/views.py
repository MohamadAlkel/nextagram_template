from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user, logout_user
from models.user import User
import os
from helpers.google_oauth import oauth
import config
from models.user import User

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')


@sessions_blueprint.route('/signin', methods=['GET'])
def new():
    return render_template('signin.html')


@sessions_blueprint.route('/delete', methods=["POST"])
def logout():
   logout_user()
   flash("logged out", "success")
   return redirect(url_for('sessions.new'))
    


@sessions_blueprint.route('/login', methods=['POST'])
def login():
    # session["user_id"] = user.id # tells the browser to store `user.id` in session with the key as `user_id`
# then redirect them somewhere
    username = request.form["username"]
    password = request.form["password"]
    user = User.get_or_none((User.username == username) | (User.email == username) )
    # user_email = User.get_or_none(User.email == username)

    if not user:
       flash("Username or password incorrect", "danger")
    #    next = request.args.get('next')
       return render_template('signin.html', username =username, password=password , no="Username or password incorrect")
    else:
       if check_password_hash(user.password, password):
           login_user(user)
        #    flash('You have logged in successfully!', 'success')
           return redirect(url_for('users.show'))
       else:
           flash(" password incorrect", "danger")
           return redirect(url_for('sessions.new'))

        

@sessions_blueprint.route('/google_sing_in', methods=['POST', "GET"])
def google_sign_in():
   return oauth.google.authorize_redirect(url_for("sessions.authorize", _external=True))



@sessions_blueprint.route('/authorize', methods=['POST',"GET"])
def authorize():
   token = oauth.google.authorize_access_token()
   info = oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo").json()
   email = info["email"]
   user = User.get_or_none(User.email == email)
   
   if user:
      login_user(user)
      return redirect(url_for("users.upload_file_pro"))
   else:
      u = User(email=email, username=email, password=generate_password_hash(os.urandom()))
      u.save()
      # return render_template("signin.html")   

   return redirect(url_for("users.upload_file_pro"))
   # email = oauth.google.get(User.email == email)
   # return oauth.google.authorize_redirect(url_for("authorize"))









# from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
# from models.user import User
# from flask_login import login_user, logout_user
# from werkzeug.security import check_password_hash

# sessions_blueprint = Blueprint('sessions',
#                            __name__)

# @sessions_blueprint.route('/login', methods=['POST'])
# def login():
#    username = request.form.get('username')
#    password = request.form.get('password')
#    user = User.get(User.username == username)

#    if not user:
#        flash("Username or password incorrect", "danger")
#        next = request.args.get('next')
#        return render_template('home.html')
#    else:
#        if check_password_hash(user.password, password):
#            login_user(user)
#            flash('You have logged in successfully!', 'success')
#            return redirect(url_for('users.show', username=user.username))
#        else:
#            flash("username or password incorrect", "danger")
#            return redirect(url_for('home'))


# @sessions_blueprint.route('/delete')
# def logout():
#    logout_user()
#    flash("logged out", "success")
#    return redirect(url_for('home'))