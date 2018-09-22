from flask import render_template,url_for,flash,redirect,jsonify,request,g,session,current_app
from datetime import datetime
from appFolder import app,db
from appFolder.forms import LoginForm
from appFolder.models import User,Logs, User_Id_Store
from flask_login import login_user, current_user, logout_user, login_required

@app.before_request
def session_management():
    # make the session last indefinitely until it is cleared
    session.permanent = True

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login", methods = ['GET','POST'])
def login():
    session.permanent = True
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username =  form.username.data).first()
        if user and (user.password==form.password.data):
            login_user(user)
            s = User_Id_Store.query.first()
            s.store = user.id
            db.session.commit()
            return redirect(url_for('home'))
        else :
            flash('Unsucessful Login! Please check username and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    user = User.query.filter_by(username=current_user.username).first()
    user.last_login = datetime.now()
    db.session.commit()
    s = User_Id_Store.query.first()
    s.store = -1
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile/<userid>")
@login_required
def profile(userid):
    return render_template('profile.html',title='profile', id=userid)

@app.route("/viz1")
def viz1():
    return render_template('viz1.html')

@app.route("/viz2")
def viz2():
    return render_template('viz2.html')

@app.route("/bardata", methods = ['GET'])
def bardata():
    upvote=[]
    downvote=[]
    aaa_upvote_count = Logs.query.filter_by(user_id=1).filter_by(activity='upvote').count()
    upvote.append(aaa_upvote_count)
    aaa_downvote_count = Logs.query.filter_by(user_id=1).filter_by(activity='downvote').count()
    downvote.append(aaa_downvote_count)
    bbb_upvote_count = Logs.query.filter_by(user_id=2).filter_by(activity='upvote').count()
    upvote.append(bbb_upvote_count)
    bbb_downvote_count = Logs.query.filter_by(user_id=2).filter_by(activity='downvote').count()
    downvote.append(bbb_downvote_count)
    ccc_upvote_count = Logs.query.filter_by(user_id=3).filter_by(activity='upvote').count()
    upvote.append(ccc_upvote_count)
    ccc_downvote_count = Logs.query.filter_by(user_id=3).filter_by(activity='downvote').count()
    downvote.append(ccc_downvote_count)
    retjson = [upvote,downvote]
    return jsonify({"votes": retjson})

@app.route("/donutdata", methods = ['GET'])
def donutdata():
    activity = ['vote','post', 'comment', 'search','bookmark']
    unit = ['#activity','#activity','#activity']
    user_ids = ['aaa','bbb','ccc']
    i=0
    dataset = []
    while(i<len(user_ids)):
        data = []
        total =0
        j=0
        while(j<len(activity)):
            if(activity[j] == 'vote'):
                value = Logs.query.filter_by(user_id=i + 1).filter_by(activity='upvote').count()
                value += Logs.query.filter_by(user_id=i + 1).filter_by(activity='downvote').count()
            else:
                value = Logs.query.filter_by(user_id=i+1).filter_by(activity=activity[j]).count()
            total+=int(value)
            data.append({
                "cat" : activity[j],
                "val": int(value)
            })
            j+=1
        dataset.append({
            "type" : user_ids[i],
            "unit" : unit[i],
            "data" : data,
            "total" : total
        })
        i+=1
    return jsonify({"dataset": dataset})


@app.route("/getUserActivity/<id>", methods=['GET'])
def useractvity(id):
    activities = Logs.query.filter_by(user_id=id).all()
    userlogs = []
    for activity in activities:
        temp=[]
        temp.append({"activity": activity.activity})
        temp.append({"message": activity.message})
        temp.append({"timestamp":activity.timestamp})
        userlogs.append(temp)
    return jsonify({"activities": userlogs})


@app.route("/postapi", methods = ['POST'])
def postapi():
    user_id = request.json["user"]
    if(user_id=="-1"):
        s = User_Id_Store.query.first()
        user_id = s.store
    if(user_id!=-1):
        user_log = Logs(activity = request.json["activity"], message = request.json["message"],
                        timestamp =  request.json["timestamp"], user_id = user_id)
        db.session.add(user_log)
        db.session.commit()
    return ""

