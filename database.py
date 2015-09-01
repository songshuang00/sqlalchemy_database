import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=\'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db=SQLAlchemy(app)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('shell',shell(make_context=make_shell_context))

class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64),unique=True)

    def __repr__(self):
        return '<Role %r>' %self.name

    users=db.relationship('User',backref='role',lazy='dynamic')

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64),unique=True,index=True)

    def __repr__(self):
        return '<Role %r>' %self.username

    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))

@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.name.data).first()
        if user is None:
            user=User(username=form.name.data)
            db.session.add(user)
            session['known']=False
            else:
                session['known']=True
            session['name']=form.name.data
            form.name.data=''
            return redirect(url_for('index'))
        return render_template('index.html',form=form,name=session.get('name'),known=session.get('known',False))




