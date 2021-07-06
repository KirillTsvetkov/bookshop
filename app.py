from flask import Flask, render_template
from models import db, User
from flask_migrate import Migrate
from flask_login import LoginManager
from api.views import api
from crud.views import crud
from shop.views import shop
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/bookshop'
app.config['SECRET_KEY'] = 'secret'
app.config['JSON_AS_ASCII'] = False
csrf = CSRFProtect(app)


app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(crud, url_prefix='/crud')
app.register_blueprint(shop, url_prefix='/shop')


csrf.exempt(crud)
csrf.exempt(api)


db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/api_guid', methods=["GET"])
def api_guid():
    return render_template("api-guid.html")


if __name__ == "__main__":
    app.run(debug=True)
