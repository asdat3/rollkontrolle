import json, datetime, random, string
from flask import Flask, request, render_template, redirect, send_file, url_for, jsonify, session, flash, after_this_request
from flask_login import current_user, login_user, LoginManager, UserMixin, login_required, login_user, logout_user
from flask_mobility import Mobility
from flask_caching import Cache
from flask_ipban import IpBan
from device_detector import DeviceDetector


app = Flask(__name__)

app.config.update(
    DEBUG = False,
    SECRET_KEY = 'secret_password_' + ''.join(str(random.choice(string.ascii_lowercase)) for i in range(20))
)

with open("config.json","r") as f:
    configg = json.load(f)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
        
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

@login_manager.user_loader
def load_user(userid):
    return User(userid)

def get_username(self):
    return self.username


@app.route('/login', methods=['GET',"POST"])
def reg_login_m():
    if request.method == "POST":
        username = request.form['username']
        password_login = request.form['password_login']

        all_users_list = configg["login"]["data"]
        matching_user_json = None
        for user_now in all_users_list:
            if user_now["username"].lower() == username.lower():
                if user_now["password"] == password_login:
                    matching_user_json = user_now
        
        if not matching_user_json == None:
            var_user_to_login = User(matching_user_json["username"])
            login_user(var_user_to_login)
            return redirect("/d1")
        else:
            return render_template("login/invalid_credentials_noti.html")
    else:
        return render_template("login/main_login.html")


@app.route("/", methods=['GET'])
def home_index():
    if current_user.is_authenticated or not configg["login"]["enabled"]:
        return("my Wiener is big")
    else:
        return redirect("/login")

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True, port=80)