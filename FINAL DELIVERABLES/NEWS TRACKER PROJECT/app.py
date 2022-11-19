from flask import Flask,render_template,redirect,request,url_for
from dao import dbCon
from ibm_db import fetch_assoc,exec_immediate,prepare,bind_param,execute
from flask_apscheduler import APScheduler
from hourlyScheduler import sample

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
userID = None
total_Categories = ["business","entertainment","environment","food","health","politics","science","sports","technology","top","world"]

@app.route("/",methods=['GET','POST'])
def home():
    global userID
    if userID!=None:
        getUserCat = "Select CATEGORY,EMAIL_PREF from user_credentials where ID = \'"+userID+"\'"
        stmt = exec_immediate(dbCon,getUserCat)
        dict = fetch_assoc(stmt)
        user_Categories = dict['CATEGORY'].split(",")
        user_email_pref = dict['EMAIL_PREF']
        if(request.method=='POST'):
            sel_Categories = list(request.form.keys())
            sel_Categories.remove("email_pref")
            updateUserCat = "Update user_credentials set CATEGORY =?,EMAIL_PREF=?  where ID = ?"
            prep_stmt = prepare(dbCon, updateUserCat)
            bind_param(prep_stmt, 1, ",".join(sel_Categories))
            bind_param(prep_stmt, 2, request.form.get('email_pref'))
            bind_param(prep_stmt, 3, userID)
            execute(prep_stmt)
            return redirect(url_for('home'))
        return render_template("index.html",total = total_Categories,user= user_Categories,email_pref=user_email_pref,userID = userID)
    else:
        return redirect(url_for('login'))

@app.route("/login",methods=['GET','POST'])
def login():
    global userID
    user_cred = []
    stmt = exec_immediate(dbCon,"Select * from user_credentials")
    dict = fetch_assoc(stmt)
    while dict!= False:
        user_cred.append(dict)
        dict = fetch_assoc(stmt)
    if(request.method == 'POST'):
        userID = request.form['status']
        return redirect(url_for('home'))
    return render_template("login.html",cred = user_cred)

@app.route("/register",methods=['GET','POST'])
def register():
    reg_email = []
    stmt = exec_immediate(dbCon,"Select * from user_credentials")
    dict = fetch_assoc(stmt)
    while dict!= False:
        reg_email.append(dict['USERNAME'])
        dict = fetch_assoc(stmt)
    if(request.method=='POST'):
        insert_sql = "insert into user_credentials (USERNAME,PASSWORD,NAME,Category) values(?,?,?,?)"
        reg_info = list(request.form.keys())
        userCred = {key: request.form[key] for key in reg_info}
        prep_stmt = prepare(dbCon, insert_sql)
        bind_param(prep_stmt, 1, userCred['username'])
        bind_param(prep_stmt, 2, userCred['password'])
        bind_param(prep_stmt, 3, userCred['name'])
        bind_param(prep_stmt, 4, "top")
        execute(prep_stmt)
        return redirect(url_for('login'))
    return render_template("register.html",reg = reg_email)

@app.route('/logout')
def logout():
    global userID
    userID = None
    return redirect(url_for('search'))

@app.route('/search',methods=['GET','POST'])
def search():
    global userID
    news_data = []
    pref_news = []
    non_pref_news = []
    if request.method == 'POST' and request.form['query']!='':
        stmt = exec_immediate(dbCon,"Select * from news_data where title like \'%"+request.form['query']+"%\'")
        dict = fetch_assoc(stmt)
        while dict!= False:
            news_data.append(dict)
            dict = fetch_assoc(stmt)
    else:
        stmt = exec_immediate(dbCon,"Select * from news_data")
        dict = fetch_assoc(stmt)
        while dict!= False:
            news_data.append(dict)
            dict = fetch_assoc(stmt)
    print(userID)
    if(userID != None):
        getUserCat = "Select CATEGORY from user_credentials where ID = \'"+userID+"\'"
        stmt = exec_immediate(dbCon,getUserCat)
        dict = fetch_assoc(stmt)
        user_Categories = dict['CATEGORY'].split(",")
        for i in news_data:
            if any(check in user_Categories for check in i['CATEGORY'].split(",")):
                pref_news.append(i)
            else:
                non_pref_news.append(i)
    else:
        non_pref_news = news_data
    print(userID)
    print(len(pref_news),"---",len(non_pref_news))
    return render_template("home.html",pref_news = pref_news,non_pref_news = non_pref_news,userID=userID)


if __name__ == "__main__":
    #t1 = threading.Thread(target=schedule)
    #t1.start()
    app.apscheduler.add_job(func = sample,trigger = 'cron',hour='1,4,7,10,14,19,21,23',id="0")
    app.run(debug=True,host="0.0.0.0")