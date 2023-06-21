from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime

local_server=True
with open('config.json','r') as c:
    params = json.load(c)
app = Flask(__name__)
app.config.update(
    MAIL_SERVER ="smtp.gmail.com",
    MAIL_PORT ='465',
    MAIL_USE_SSL =True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pwd']
)

mail=Mail(app)
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:@localhost/mydata"
app.secret_key="super-secret-key"
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=True,nullable=False)
    phone_num=db.Column(db.String(12),unique=True,nullable=False)
    msg=db.Column(db.String(120),unique=True,nullable=False)
    date=db.Column(db.String(12),unique=True,nullable=False)
    email=db.Column(db.String(20),unique=True,nullable=False)


class Posts(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(12),unique=True,nullable=False)
    content=db.Column(db.String(200),unique=True,nullable=False)
    date=db.Column(db.String(12),unique=True,nullable=False)

@app.route("/",methods=['GET', 'POST'])
def login():
    if ('user' in session and session['user']==params['admin_user']):
        return render_template('index.html')
   
    if request.method=="POST":
        username= request.form.get('uname')
        password = request.form.get('pass1')
        if (username == params["admin_user"] and password==params["admin_password"]):
            session['user']=username
            return render_template('index.html') 

    else:
        return render_template('login.html',params=params)
    return render_template('login.html')

@app.route("/home")
def home():
    contacts=Contacts.query.filter_by().all()
    if 'user' in session and session['user'] == params['admin_user']:
        return render_template('index.html',contacts=contacts)
    else:
        return redirect(url_for('login'))


@app.route("/about",methods=['GET','POST'])
def about():
    if request.method == 'POST':
        title= request.form.get('title')
        content= request.form.get('content')
        newentry = Posts(title=title,content=content,date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(newentry)
        db.session.commit()
    return render_template('about.html')


@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        phone_num=request.form.get('phone_num')
        message=request.form.get('message')
        if not message:
            # Return an error or display a message indicating that the message field is required
            return render_template('contact.html', error_message='Message field is required')

        entry=Contacts(name=name,email=email,phone_num=phone_num,msg=message, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        db.session.add(entry)
        db.session.commit()
        #mail.send_message("New Message from admin-portal" + name,sender=email,recipients=[params['gmail-user']],body=message + "\n" + phone_num)
    return render_template('contact.html')

@app.route("/posts")
def posts():
    posts=Posts.query.filter_by().all()
    return render_template('posts.html',posts=posts)

@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)