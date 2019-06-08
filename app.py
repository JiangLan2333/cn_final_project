# encoding = utf-8
from flask import Flask
from flask import request, render_template, session, jsonify, redirect, url_for, g
from random import Random
from flask_sqlalchemy  import SQLAlchemy
from flask_login import UserMixin, login_user, current_user, LoginManager, logout_user, login_required, AnonymousUserMixin
from hashlib import md5
from datetime import timedelta
import time as time

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'Thisissupposedtobesecret!',
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://dong:jia67020200@140.143.10.91:3306/belongings207'
)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'guest'
    def is_anonymous(self):
        return true

login_manager.anonymous_user = AnonymousUser

class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.String(40), primary_key=True)
    password = db.Column(db.String(40))

    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def get_id(self):
        return self.uid
    def is_anonymous(self):
        return False

class Belongings(db.Model):
    __tablename__ = 'belongings'
    tid = db.Column(db.String(40), primary_key=True)
    b_desc = db.Column(db.String(100))
    b_status = db.Column(db.Integer)
    uid = db.Column(db.String(40), db.ForeignKey('user.uid'))
    safe = db.Column(db.Boolean)

@app.before_request
def before_request():
    g.user = current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['POST', 'GET'])
def test():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def signin():
    if request.method == 'POST':
        if len(request.json) == 0:
            if current_user.is_anonymous:
                print('guest')
                return jsonify({'identity': 'guest'})
            else:
                print('student')
                return jsonify({'identity': 'student'})
        if len(request.json) == 1:
            session['salt'] = ''
            chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
            len_chars = len(chars) - 1
            random = Random()
            for i in range(4):
                session['salt'] += chars[random.randint(0, len_chars)]
            session['send_salt_time'] = time.time()
            return jsonify({'salt': session['salt']})
        if len(request.json) == 3:
            id = request.json['id']
            passwd = request.json['password']
            now_time = request.json['time']
            first = md5()
            second = md5()
            if float(now_time)/1000.0 - session['send_salt_time'] > 120:
                return jsonify({'op': 'error'})
            user = User.query.filter_by(uid=id).first()
            if user:
                first.update((user.password + session['salt']).encode(encoding='utf-8'))
                second.update((first.hexdigest() + session['salt']).encode(encoding='utf-8'))
                if second.hexdigest() == passwd:
                    login_user(user, remember=True, duration=timedelta(days=1))
                    session['identity'] = 'student'
                    print(id)
                    if id == "000000000000":
                        return jsonify({'op': 'admin'})
                    elif id == '000000000001':
                        return jsonify({'op': 'addbook'})
                    else:
                        return jsonify({'op': 'generaluser'})
            return jsonify({'op': 'error'})

@app.route('/changeStatus', methods=['POST'])
def changeStatus():
    cur_status = request.json['status']
    uid = request.json['uid']
    tid = request.json['tid']
    n_status = 1 - int(cur_status)
    book = db.session.query(Belongings).filter_by(uid=uid, tid=tid).first()
    book.b_status = n_status
    db.session.commit()

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return render_template('login.html')

@app.route('/controlStudent', methods=['POST', 'GET'])
@login_required
def controlStudent():
    return render_template('controlStudent.html')

@app.route('/controlBelongings', methods=['POST', 'GET'])
@login_required
def controlBelongings():
    return render_template('controlBelonging.html')

@app.route('/deleteBelonging', methods=['POST'])
@login_required
def deleteBelonging():
    tid = request.json['tid']
    book = db.session.query(Belongings).filter_by(tid=tid).first()
    db.session.delete(book)
    db.session.commit()
    return '删除成功！'

@app.route('/showBelongings', methods=['POST', 'GET'])
@login_required
def showBelongings():
    # 读取数据库 返回[item,..]
    if request.method == 'POST':
        uid = current_user.uid
        books = db.session.query(Belongings).filter_by(uid=uid).all()
        belongingList = []
        for item in books:
            if item.b_status == 1:
                status = "是"
            elif item.b_status == 0:
                status = "否"
            if item.safe == 0:
                safe = "是"
            elif item.safe == 1:
                safe = "否"
            obj = {'tid': item.tid, 'desc': item.b_desc, 'status': status, 'safe': safe}
            belongingList.append(obj)
        return jsonify({'belongingList': belongingList})
    if request.method == 'GET':
        return render_template('showBelongings.html')

@app.route('/showBelongingInfo', methods=['POST'])
def showBelongingInfo():
    tid = request.json['id']
    book = db.session.query(Belongings).filter_by(tid=tid).first()
    return jsonify({'tid': book.tid, 'desc': book.b_desc, 'status': book.b_status, 'safe': book.safe})

@app.route('/checkTag', methods=['POST', 'GET'])
@login_required
def checkTag():
    return render_template('checkTag.html')

@app.route('/uploadBelongings')
def uploadBelongings():
    return render_template('uploadBelonging.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port='8000', debug=True)

