from flask import Flask,Blueprint,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from shop.config import Config,EmailConfig,ConfigGoogle
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required,current_user
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth
from shop.utils import generate_slug
from flask_session import Session
from datetime import timedelta
import redis,os


db=SQLAlchemy()
app = Flask(__name__,static_folder=os.path.join(os.path.dirname(__file__),'static'),static_url_path='/shop/static')
bcrypt=Bcrypt(app)
app.config.from_object(EmailConfig)
mail=Mail(app)
app.jinja_env.filters['slug']=generate_slug
session=Session()
app.config['SESSION_TYPE']='redis'
app.config['SESSION_PERMANENT']=False
app.config['SESSION_USE_SIGNER']=True
app.config['SESSION_REDIS']=redis.StrictRedis(host='localhost',port=6379,db=0)
session.init_app(app)
app.config.from_object(ConfigGoogle)
oauth=OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url=app.config['GOOGLE_ACCESS_TOKEN_URL'],
    authorize_url=app.config['GOOGLE_AUTHORIZE_URL'],
    userinfo_endpoint=app.config['GOOGLE_USERINFO_ENDPOINT'],
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
)

login_manager=LoginManager()
def create_app():
    
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view='secure.login'

    #route backend
    #import đường dẫn
    from shop.controllers.backend.manager_controller import m_route
    from shop.controllers.backend.category_controller import cate_route
    from shop.controllers.backend.product_controller import pro_route
    from shop.controllers.backend.account_controller import acc_route
    from shop.controllers.backend.menu_controller import menu_route

    #đăng ký đường dẫn
    hethong_route=Blueprint('hethong',__name__)
    @hethong_route.before_request
    @login_required
    def check_admin():
        if not current_user.has_role("admin"):
            flash("Bạn không có quyền truy cập","error")
            return redirect(url_for('secure.login'))
    hethong_route.register_blueprint(m_route,url_prefix='/manager')
    hethong_route.register_blueprint(cate_route,url_prefix='/category')
    hethong_route.register_blueprint(pro_route,url_prefix='/product')
    hethong_route.register_blueprint(acc_route,url_prefix='/account')
    hethong_route.register_blueprint(menu_route,url_prefix='/menu')

    app.register_blueprint(hethong_route,url_prefix='/hethong')

    #route frontend
    from shop.controllers.frontend.home_controller import h_route
    from shop.controllers.frontend.secure_controller import secure_route
    app.register_blueprint(h_route,url_prefix='/')
    app.register_blueprint(secure_route,url_prefix='/secure')


    return app