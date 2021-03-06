from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.payments.views import payments_blueprint
import os
from helpers.google_oauth import oauth
import config
from flask_assets import Environment, Bundle
from .util.assets import bundles
from flask_wtf.csrf import CSRFProtect
from models.user import User, User_img

assets = Environment(app)
assets.register(bundles)
# some other code here
oauth.init_app(app)
csrf = CSRFProtect(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(payments_blueprint, url_prefix="/payments")




@app.route("/")
def home():
    users = User.select()
    user_img = User_img.select()    
    return render_template('home.html', users=users, user_img=user_img)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('500.html'), 404


