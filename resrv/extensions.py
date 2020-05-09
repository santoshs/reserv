from flask_login import LoginManager
from flask_assets import Environment
from flask_humanize import Humanize

from resrv.models import User

# init flask assets
assets_env = Environment()

login_manager = LoginManager()
login_manager.login_view = "main.login"
login_manager.login_message_category = "warning"
humanize = Humanize()

@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
