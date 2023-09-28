from flask import Flask, flash, redirect, render_template, send_from_directory,request, session, abort, url_for,jsonify,current_app
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL
from functools import wraps
# from datetime import datetime, date, timedelta
from datetime import date
import datetime
import calendar
# from datetime import datetime, timedelta
import os
from flask_mail import Mail, Message

# password generator *****
import string
import random
# ****************************

# cors************************
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = b'_5#y2hj,mngghF4Q8z\n\xec]/'
CORS(app)

app.config['path']="C:/Users/home/Downloads/paliativecare ihrd/paliativecare/static/upload/"
app.config['paths'] = 'D:/paliativecare/static/pdf/'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'paliative'

dataTypesToDownload = [".jpg", ".jpeg", ".png", ".gif", ".ico", ".css", ".js", ".html"]
mysql = MySQL(app)
mysql.init_app(app)

# Mail configuration

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pcare7188@gmail.com'
app.config['MAIL_PASSWORD'] = 'prjctp_care7188'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def Mailer(sender,recipient,Subject,body):
    try:
        msg=Message(Subject,sender=sender,recipients=[recipient])
        msg.body=body
        # msg.html = render_template('Mail_Template.html',password=body)
        mail.send(msg)

        return "sended successfully"
    except:
        return "A Error occurred while perform mailing !"

def randomString(stringLength):

    """Generate a random string with the combination of lowercase and uppercase letters """
    # letters = string.ascii_letters
    # return ''.join(random.choice(letters) for i in range(stringLength))

    # """ Generate a random string of letters and digits """    query=""
    # cursor.execute(query)
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
    
def allow_for_loggined_users_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login',next=request.endpoint))
        return f(*args, **kwargs)
    return wrapper
# -----------------------------------------------------------------------------------------------------------------------------

 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/appointment')
def appointment():
    return render_template('appointment.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/single-blog-blog')
def SingleBlog():
    return render_template('single-blog.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/admin')
def admin():
    return render_template('admin_home.html')   

@app.route('/doctor',methods=['GET'])
def doctor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select count(*) as count from blood_donation where blood_group=%s",session['blood'])     
        rows = cursor.fetchone()
        return render_template('doctor_home.html',row=rows)   

@app.route('/donor',methods=['GET'])
def donor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select count(*) as count from blood_donation where blood_group=%s",session['blood'])     
        rows = cursor.fetchone()
        return render_template('donor_home.html',row=rows)  

@app.route('/patient',methods=['GET'])
def patient():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select count(*) as count from appointment where lid=%s and status='booking'",session['lid'])     
        noti = cursor.fetchone()
        return render_template('patient_home.html',notification=noti)       

@app.route('/hospital')
def hospital():
    return render_template('hospital_home.html')    


@app.route('/volunteer',methods=['GET'])
def volunteer():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select count(*) as count from blood_donation where blood_group=%s",session['blood'])     
        rows = cursor.fetchone()
        return render_template('volunteer_home.html',row=rows)               

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    if request.method == 'POST':
        conn =mysql.connect()
        cursor = conn.cursor()
        query="select * from login where username=%s and password=%s and provisionized=1"
        cursor.execute(query,(request.form['username'],request.form['password']))
        result=cursor.fetchone()
        print(result)
        conn.commit()                 
        if result:
            # print(result)
            session['loggedin'] =True
            session['username']= result[1] 
            session['lid']= result[0]  
            session['type']= result[3]
            if (result[3] == 'admin'):
                return redirect(url_for('admin'))
            elif (result[3] == 'donor'):
                conn= mysql.connect()
                cursor=conn.cursor()
                cursor.execute("select login.lid,registration.* from registration,login where login.lid=registration.lid and login.lid=%s",result[0])    
                rows = cursor.fetchone()
                session['blood']=rows[7]
                return redirect(url_for('donor'))  
            elif (result[3] == 'patient'):
                return redirect(url_for('patient'))   
            elif (result[3] == 'doctor'):
                conn= mysql.connect()
                cursor=conn.cursor()
                cursor.execute("select login.lid,registration.* from registration,login where login.lid=registration.lid and login.lid=%s",result[0])    
                rows = cursor.fetchone()
                session['blood']=rows[7]
                return redirect(url_for('doctor'))   
            elif (result[3] == 'volunteer'):
                conn= mysql.connect()
                cursor=conn.cursor()
                cursor.execute("select login.lid,registration.* from registration,login where login.lid=registration.lid and login.lid=%s",result[0])    
                rows = cursor.fetchone()
                session['blood']=rows[7]
                return redirect(url_for('volunteer'))     
            elif (result[3] == 'hospital'):
                conn =mysql.connect()
                cursor = conn.cursor()
                cursor.execute("select login.lid,login.type,hospital.* from hospital,login where login.lid=hospital.lid and login.type='hospital' and login.lid=%s",result[0])     
                rows = cursor.fetchone()
                session['hid']=rows[2]
                print(session['hid']) 
                return redirect(url_for('hospital'))                                                                    
        session['logged_in'] = True
    else:
        flash('wrong password!')
        
    return render_template('login.html',msg="Wrong Username and Password!")    
    
@app.route('/logout',methods=['GET'])
def logout():
    print(session['loggedin'])
    if session['loggedin']:
        session['loggedin']=False
        session.pop(id,None)
        session.pop('username',None)
        return redirect(url_for('login'))
    else:
        print("loging first")  
        return "something went wrong"    

@app.route('/hospital_reg')
def hospital_reg():
    return render_template('hospital_reg.html')

@app.route('/registration',methods=['GET','POST'])
# @allow_for_loggined_users_only
def registration():
    if request.method=='GET':
        return render_template('reg.html')  
    if request.method=='POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        password=randomString(10) 
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,type,created_on,provisionized) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['email'], data['phone'], 'donor', date,1))
        userid=cursor.lastrowid
        query = "INSERT INTO registration(name,email,phone,dob,gender,blood_group,address,city,district,pincode,other_phone,file,lid,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], data['email'], data['phone'], data['date'], data['gender'], data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],filename,userid,date))
        conn.commit()
        conn.close()
        return redirect(url_for('registration'))      


@app.route('/admin_add_hospital',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_add_hospital():
    if request.method=='GET':
        return render_template('hospital_reg.html')  
    if request.method=='POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        password=randomString(10) 
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,type,created_on,provisionized) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['email'], password, 'hospital', date,1))
        hospitalid=cursor.lastrowid
        query = "INSERT INTO hospital(hospital,description,phone,landline,district,city,address,pincode,email,file,lid,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], data['description'], data['phone'], data['landline'], data['district'], data['city'],data['address'],data['pincode'],data['email'],filename,hospitalid,date))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_add_hospital'))      


@app.route('/admin_view_hospital',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_hospital():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,hospital.* from hospital,login where login.lid=hospital.lid and login.type='hospital'")     
        rows = cursor.fetchall()
        return render_template('admin_view_hospital.html',row=rows)

@app.route('/view_question_reply', methods=['GET'])
@allow_for_loggined_users_only
def view_question_reply():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor.execute("SELECT complaint , reply ,reply_date FROM complaint")
        cursor.execute("select * from question where lid=%s", session['lid'])
        rows = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('view_question_reply.html', row=rows)

@app.route('/patient_view_complaint_reply', methods=['GET'])
@allow_for_loggined_users_only
def patient_view_complaint_reply():
    if request.method == 'GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        # cursor.execute("SELECT complaint , reply ,reply_date FROM complaint")
        cursor.execute("select * from complaint where lid=%s", session['lid'])
        rows = cursor.fetchall()
        # print(row)
        conn.commit()
        conn.close()
        return render_template('patient_view_complaint_reply.html', row=rows)
        

# File Download
@app.route('/return-files/<file_name>')  
def returnfiles(file_name):
    print(file_name)
    uploads = os.path.join(current_app.root_path, app.config['path'])
    return send_from_directory(directory=uploads, path=file_name) 


@app.route('/admin_delete_hospital',methods=['POST'])
@allow_for_loggined_users_only
def admin_delete_hospital():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        query = "delete from hospital where hid=%s"
        cursor.execute(query, data[0])
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_hospital')) 


@app.route('/admin_volunteers_reg',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_volunteers_reg():
    if request.method=='GET':
        return render_template('admin_volunteer.reg.html')  
    if request.method=='POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        password=randomString(10) 
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,type,created_on,provisionized) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['email'], password, 'volunteer', date,1))
        userid=cursor.lastrowid
        query = "INSERT INTO registration(name,email,phone,dob,gender,blood_group,address,city,district,pincode,other_phone,file,lid,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], data['email'], data['phone'], data['date'], data['gender'], data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],filename,userid,date))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_volunteers_reg'))      

@app.route('/admin_view_volunteer',methods=['GET','POST'])
def admin_view_volunteer():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='volunteer'")     
        rows = cursor.fetchall()
        # today = date.today()
        # print(today)
        # dt=[]
        # for age in rows:
        #     dt.append(
        #         {"age":age[6]}
        #     )
        # age =age-today
        # print(age)
        return render_template('admin_view_volunteer.html',row=rows)

@app.route('/admin_delete_volunteer',methods=['POST'])
@allow_for_loggined_users_only
def admin_delete_volunteer():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        query = "delete from registration where rid=%s"
        cursor.execute(query, data[0])
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_volunteer'))   

@app.route('/admin_view_donor',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_donor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='donor'")     
        rows = cursor.fetchall()
        return render_template('admin_view_donor.html',row=rows)     

@app.route('/admin_delete_donor',methods=['POST'])
@allow_for_loggined_users_only
def admin_delete_donor():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        query = "delete from registration where rid=%s"
        cursor.execute(query, data[0])
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_donor'))       

@app.route('/patient_reg',methods=['GET','POST'])
# @allow_for_loggined_users_only
def patient_reg():
    if request.method=='GET':
        return render_template('patient_reg.html')  
    if request.method=='POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        password=randomString(10) 
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        query = "insert into login(username,password,type,created_on,provisionized) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['email'], password, 'patient', date,1))
        userid=cursor.lastrowid
        query = "INSERT INTO registration(name,email,phone,dob,gender,blood_group,address,city,district,pincode,other_phone,file,lid,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], data['email'], data['phone'], data['date'], data['gender'], data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],filename,userid,date))
        conn.commit()
        conn.close()
        return redirect(url_for('patient_reg'))      

@app.route('/admin_view_patient',methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_patient():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='patient'")     
        rows = cursor.fetchall()
        return render_template('admin_view_patient.html',row=rows) 

@app.route('/admin_delete_patient',methods=['POST'])
@allow_for_loggined_users_only
def admin_delete_patient():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        query = "delete from registration where rid=%s"
        cursor.execute(query, data[0])
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_patient'))       

@app.route('/hospital_admin_add_doctor',methods=['GET','POST'])
@allow_for_loggined_users_only
def hospital_admin_add_doctor():
    if request.method=='GET':
        return render_template('doctor_reg.html')  
    if request.method=='POST':
        data = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        password=randomString(10) 
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
    
        query = "insert into login(username,password,type,created_on,provisionized) values (%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['email'], password, 'doctor', date,1))
        doctorid=cursor.lastrowid

        query = "INSERT INTO registration(name,email,phone,dob,gender,blood_group,address,city,district,pincode,other_phone,file,lid,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['name'], data['email'], data['phone'], data['date'], data['gender'], data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],filename,doctorid,date))
       
        id=cursor.lastrowid
        query = "INSERT INTO doctor_reg(rid,hid,specialization,exeperience,created_on) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query, (id,session['hid'], data['specialization'],data['experience'],date))
        conn.commit()
        conn.close()
        return redirect(url_for('hospital_admin_add_doctor'))      


@app.route('/hospital_admin_view_doctor',methods=['GET','POST'])
@allow_for_loggined_users_only
def hospital_admin_view_doctor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.*,doctor_reg.* from login,registration,doctor_reg where login.lid=registration.lid and login.type='doctor' and registration.rid=doctor_reg.rid and doctor_reg.hid=%s",session['hid'])     
        rows = cursor.fetchall()
        return render_template('hospital_admin_view_doctor.html',row=rows) 

# File Download
@app.route('/return-pdf/<file_name>')  
def returnpdf(file_name):
    print(file_name)
    uploads = os.path.join(current_app.root_path, app.config['path'])
    return send_from_directory(directory=uploads, path=file_name) 


@app.route('/hospital_admin_delete_doctor',methods=['POST'])
@allow_for_loggined_users_only
def hospital_admin_delete_doctor():
    if request.method == 'POST':
        data=request.form['delete_by_id']
        data=data.split()
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from login where lid=%s"
        cursor.execute(query, data[1])
        query = "delete from registration where rid=%s"
        cursor.execute(query, data[0])
        query = "delete from doctor_reg where did=%s"
        cursor.execute(query, data[2])
        conn.commit()
        conn.close()
        return redirect(url_for('hospital_admin_view_doctor'))       

@app.route('/donor_add_donation',methods=['GET','POST'])
@allow_for_loggined_users_only
def donor_add_donation():
    if request.method=='GET':
        return render_template('donor_add_donation.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        date=datetime.datetime.now()
        query = "INSERT INTO donation(lid,name,description,file,status,created_on) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['name'], data['description'], filename,'pending',date))
        conn.commit()
        conn.close()
        return redirect(url_for('donor_add_donation')) 

@app.route('/donor_view_donation',methods=['GET','POST'])
@allow_for_loggined_users_only
def donor_view_donation():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM donation where lid=%s",session['lid'])     
        rows = cursor.fetchall()
        return render_template('donor_view_donation.html',row=rows) 

@app.route('/donor_delete_donation',methods=['POST'])
@allow_for_loggined_users_only
def donor_delete_donation():
    if request.method == 'POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from donation where donation_id=%s"
        cursor.execute(query, data['delete_by_id'])       
        conn.commit()
        conn.close()
        return redirect(url_for('donor_view_donation'))  

@app.route('/patient_view_donation',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view_donation():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT needy_request.*,donation.*,donation_request.* from donation_request,donation,needy_request where needy_request.nid=donation.nid and donation.status='accept' and donation.donation_id=donation_request.did and donation_request.status='accept' and needy_request.lid=%s",session['lid'])     
        rows = cursor.fetchall()
        return render_template('patient_view_donation.html',row=rows)                            
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO donation_request(lid,did,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['did'],'pending',date))
        conn.commit()
        conn.close()
        return redirect(url_for('patient_view_donation')) 

@app.route('/patient_add_needy_request',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_add_needy_request():
    if request.method=='GET':
        return render_template('patient_add_needy_request.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO needy_request(lid,name,description,status,created_on) VALUES(%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['name'],data['description'],'pending',date))
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('patient_add_needy_request')) 

@app.route('/patient_view_needy_request',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view_needy_request():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM needy_request where lid=%s",session['lid'])     
        rows = cursor.fetchall()
        return render_template('patient_view_needy_request.html',row=rows)

@app.route('/patient_delete_needy_request',methods=['POST'])
@allow_for_loggined_users_only
def patient_delete_needy_request():
    if request.method == 'POST':
        data=request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from needy_request where nid=%s"
        cursor.execute(query, data['delete_by_id'])       
        conn.commit()
        conn.close()
        return redirect(url_for('patient_view_needy_request'))

@app.route('/patient_view_doctor',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view_doctor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.*,doctor_reg.* from doctor_reg,login,registration where login.lid=registration.lid and registration.rid=doctor_reg.rid and login.type='doctor'")     
        rows = cursor.fetchall()   
        userid=session['lid']   
        return render_template('patient_view_doctor.html',row=rows,userid=userid)  

@app.route('/patient_view',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view():   
    if request.method == 'GET': 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.*,doctor_reg.* from doctor_reg,login,registration where login.lid=registration.lid and registration.rid=doctor_reg.rid and login.type='doctor'")     
        rows = cursor.fetchall()  
        userid=session['lid']
        return render_template('patient_complaint.html',row=rows,userid=userid)       
    if request.method == 'POST':    
        data = request.json
        print(data)
        conn =mysql.connect()
        cursor = conn.cursor()
        query = "INSERT INTO complaint(lid,dvid,subject,complaint,reply,reply_date,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['lid'],data['avid'],data['subject'],data['complaint'],data['reply'],data['reply_date'],date))
        print(query)
        responseBody = { "message": "bla bla bla"}
        conn.commit()
        conn.close()

        return jsonify(responseBody)    

@app.route('/patient_add_complaint',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_add_complaint():   
    if request.method == 'GET': 
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.*,doctor_reg.* from doctor_reg,login,registration where login.lid=registration.lid and registration.rid=doctor_reg.rid and login.type='doctor'")     
        rows = cursor.fetchall()  
        userid=session['lid']
        return render_template('patient_add_complaint.html',row=rows,userid=userid)                 
    if request.method == 'POST':    
        data = request.form
        print(data)
        conn =mysql.connect()
        cursor = conn.cursor()
        dates=datetime.datetime.now()
        today=date.today()
        query = "INSERT INTO complaint(lid,dvid,subject,complaint,reply,reply_date,created_on) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['did'],data['subject'],data['complaint'],'',today,dates))
        print(query)     
        conn.commit()
        conn.close()
        return redirect(url_for('patient_add_complaint'))        

@app.route('/patient_add_booking/<string:id>',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_add_booking(id):    
        conn =mysql.connect()
        cursor = conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO appointment(did,lid,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (id,session['lid'],'pending',date))
        print(query)
        conn.commit()
        conn.close() 
        return redirect(url_for('patient_view_doctor'))      

@app.route('/patient_view_booking_details',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view_booking_details():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        print(session['lid'])
        cursor.execute("select * from appointment where lid=%s",session['lid'])     
        rows = cursor.fetchall()
        print(rows)             
        dt=[]
        for data in rows:
            dt.append({
                "status":data[3],
                "userid":data[2]
            }) 
            print(data[2])
            if data[3]=='pending':
                if data[2]==session['lid']:
                    cursor.execute("SELECT * FROM appointment where lid=%s and status='pending'",session['lid'])     
                    row = cursor.fetchall() 
                    print(row)
                    msg="Booking confirmation will inform later"
                    return render_template('patient_view_booking_details.html',row=row,msg=msg) 
                   
            elif data[3]=='booking':    
                if data[2]==session['lid']:
                    cursor.execute("SELECT appointment.*,appointment_status.*,doctor_time.* from appointment,appointment_status,doctor_time where appointment.apid=appointment_status.apid and doctor_time.tid=appointment_status.tid and appointment.status='booking' and appointment.lid=%s",session['lid'])     
                    row = cursor.fetchall() 
                    print(row)
                    msg="Your Booking is confirmed"
                    return render_template('patient_view_booking_details.html',row=row,msg=msg)
        return redirect(url_for('patient')) 
            
                                 

# @app.route('/patient_view_booking_details',methods=['GET','POST'])
# @allow_for_loggined_users_only
# def patient_view_booking_details():
#     if request.method=='GET':
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("select * from appointment where lid=%s and status='pending'",session['lid'])     
#         rows = cursor.fetchall()
#         print(rows) 
#         dt=[]
#         for data in rows:
#             dt.append({
#                 "userid":data[2]
#             }) 
#             print(data[2])
#             if data[2]==session['lid']:
#                 cursor.execute("SELECT * FROM appointment where lid=%s and status='pending'",session['lid'])     
#                 row = cursor.fetchall() 
#                 print(row)
#                 msg="Booking Date And Time"
#                 return render_template('patient_view_booking_details.html',row=row,msg=msg) 
            

@app.route('/patient_cancel_booking', methods=['POST'])
def patient_cancel_booking():
    if request.method=='POST':
        data=request.form
        print(data)
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "delete from appointment_status where aid=%s"
        cursor.execute(query,data['id'])
        query = "delete from appointment where apid=%s"
        cursor.execute(query,data['delete'])
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('patient_view_doctor'))



@app.route('/patient_view_doctor_time/<string:id>',methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_view_doctor_time(id):
    if request.method=='GET':       
        conn = mysql.connect()
        cursor = conn.cursor()
        today=date.today()
        cursor.execute("SELECT * FROM doctor_time where did=%s",id)     
        row = cursor.fetchall()
        dt=[]
        for data in row:
            dt.append({
                "date":data[6]
            })
            print(dt)
            print(data[6])
            if (data[6]==today):
                cursor.execute("SELECT * FROM doctor_time where did=%s",id)     
                value = cursor.fetchall()
                print(value)
                return render_template('patient_view_doctor_time.html',rows=value)             

            else:
                print("no data")
                return render_template('patient_view_message.html')  
    return "ok"                   

@app.route('/hospital_set_time/<string:id>',methods=['GET','POST'])
@allow_for_loggined_users_only
def hospital_set_time(id):
    if request.method=='GET':       
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='doctor' and login.lid=%s",id)     
        rows = cursor.fetchone()
        print(rows)
        return render_template('hospital_add_doctor_time.html',rows=rows)

@app.route('/test/<string:id>',methods=['GET','POST'])
@allow_for_loggined_users_only
def test(id):
    if request.method=='GET':       
        conn = mysql.connect()
        cursor = conn.cursor()
        today=date.today()
        print(today)
       
        dt=[]
        cursor.execute("select * from doctor_time where did=%s",session['lid'])     
        row = cursor.fetchall()
        for data in row:
            dt.append({
                "date":data[6]
            })
            print(data[6])
            if data[6]==today:
                cursor.execute("select * from doctor_time where date=%s",today)     
                rows = cursor.fetchall()
                print(rows)         
                return render_template('test.html',rows=rows,userid=id) 
    return render_template('doctor_msg.html',msg="Hospital not allocated time")                   

@app.route('/hospital_doctor_time',methods=['GET','POST'])
@allow_for_loggined_users_only
def hospital_doctor_time():
    if request.method=='POST':
        data= request.form
        print(data['did'])
        conn= mysql.connect()
        cursor=conn.cursor()
        # cursor.execute("select * from doctor_time where did=%s",session['did'])     
        # rows = cursor.fetchall()
        # print(rowsif row[]
        dates=datetime.datetime.now()
        today=date.today()
        print(today)
        query = "INSERT INTO doctor_time(did,day,from_time,created_on,to_time,date) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (data['did'],data['day'],data['fromtime'],dates,data['totime'],today))
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('hospital_admin_view_doctor'))

@app.route('/doctor_donate_blood',methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_donate_blood():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.lid=%s",session['lid'])     
        rows = cursor.fetchone()
        print(rows)
        return render_template('doctor_donate_blood.html',row=rows)
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO blood_donation(lid,blood_group,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['blood'],'pending',date))
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('doctor_donate_blood'))
        
@app.route('/patient_view_appointment')
@allow_for_loggined_users_only
def patient_view_appointment():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        print(session['lid'])
        cursor.execute("SELECT * FROM appointment where lid=%s",session['lid'])     
        rows = cursor.fetchone()
        print(rows)
        return render_template('patient_view_appointment.html',row=rows)        

@app.route('/patient_add_appointment',methods=['POST'])
@allow_for_loggined_users_only
def patient_add_appointment(): 
    if request.method=='POST':
        data= request.form
        print(data)
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO appointment(did,lid,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (data['appointment'],session['lid'],'pending',date))
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('patient_view_doctor'))
       

@app.route('/doctor_view_appointment' , methods=['GET'])
@allow_for_loggined_users_only
def doctor_view_appointment():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        print(session['lid'])
        cursor.execute("select login.lid,registration.*,appointment.* from registration,login,appointment where login.lid=registration.lid and appointment.lid=registration.lid and appointment.status='pending' and appointment.did=%s",session['lid'])     
        rows = cursor.fetchall()
        cursor.execute("SELECT * FROM doctor_time where did=%s",session['lid'])     
        time = cursor.fetchall()
        print(time)
        return render_template('doctor_view_appointments.html',row=rows,time=time)

        
@app.route('/appointments',methods=['POST'])
@allow_for_loggined_users_only
def appointments(): 
    if request.method=='POST':
        data= request.form
        print(data)
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO appointment_status(apid,tid,created_on) VALUES(%s,%s,%s)"
        cursor.execute(query, (data['userid'],data['tid'],date))
        query="update appointment set status='booking' where apid="+data['userid']
        cursor.execute(query)
        print(query)
        conn.commit()
        conn.close()        
        return redirect(url_for('doctor_view_appointment')) 

@app.route('/doctor_confirm_appointment',methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_confirm_appointment():
    if request.method=='POST':       
        data= request.form['app']
        data=data.split()
        print(data)
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO appointment_status(apid,tid,created_on) VALUES(%s,%s,%s)"
        cursor.execute(query, (data[0],data[1],date))
        query="update appointment set status='booking' where apid="+data[0]
        cursor.execute(query)
        print(query)
        conn.commit()
        conn.close()
        return redirect(url_for('doctor_view_appointment'))                  

@app.route('/patient_add_feedback', methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_add_feedback():
    if request.method=='GET':
        return render_template('patient_add_feedback.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO feedback(lid,subject,feedback,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['subject'],data['feedback'],date))
        conn.commit()
        conn.close()
        return redirect(url_for('patient_add_feedback'))     


@app.route('/patient_ask_questions', methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_ask_questions():
    if request.method=='POST':
        data= request.form
        print(data['did'])
        conn= mysql.connect()
        cursor=conn.cursor()
        dates=datetime.datetime.now()
        today = date.today()
        query = "INSERT INTO question(lid,did,question,reply,rdate,created_on) VALUES(%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['did'],data['question'],'',today,dates))
        conn.commit()
        conn.close()
        return redirect(url_for('patient_view_doctor')) 

# @app.route('/doctor_view_appointment' , methods=['GET'])
# @allow_for_loggined_users_only
# def doctor_view_appointment():
#     if request.method=='GET':
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         cursor.execute("select count(*) as count from appointment where lid=%s and status='booking'",session['lid'])     
#         time = cursor.fetchall()
#         print(time)
#         return render_template('doctor_view_appontments.html',row=rows,time=time)

# @app.route('/doctor_add_donation',methods=['GET','POST'])
# @allow_for_loggined_users_only
# def doctor_add_donation():
#     if request.method=='GET':       
#         return render_template('doctor_add_donation.html')  
#     if request.method=='POST':
#         data= request.form
#         conn= mysql.connect()
#         cursor=conn.cursor()
#         img = request.files['files']
#         filename = secure_filename(img.filename)
#         print(os.path.join(app.config['path']  + filename))
#         img.save(os.path.join(app.config['path']  + filename))
#         date=datetime.datetime.now()
#         query = "INSERT INTO donation(lid,name,description,file,status,created_on) VALUES(%s,%s,%s,%s,%s,%s)"
#         cursor.execute(query, (session['lid'],data['name'], data['description'], filename,'pending',date))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('doctor_add_donation')) 


@app.route('/doctor_reg')
def doctor_reg():
    return render_template('doctor_reg.html')

@app.route('/admin_view_needy_request',methods=['GET','POST'])
def admin_view_needy_request():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        print(session['lid'])
        cursor.execute("select login.lid,registration.*,needy_request.* from needy_request,registration,login where login.lid=registration.lid and registration.lid=needy_request.lid and needy_request.status='pending'")     
        rows = cursor.fetchall()
        return render_template('admin_view_needy_request.html',row=rows)
    
    
@app.route('/admin_request_needy_item/<string:id>')
def admin_request_needy_item(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    print(session['lid'])
    cursor.execute("SELECT * FROM needy_request where nid=%s",id)     
    rows = cursor.fetchone()
    return render_template('admin_add_donation.html',rows=rows)

@app.route('/admin_add_needy_request',methods=['GET','POST'])
def admin_add_needy_request():
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        img = request.files['files']
        filename = secure_filename(img.filename)
        print(os.path.join(app.config['path']  + filename))
        img.save(os.path.join(app.config['path']  + filename))
        date=datetime.datetime.now()
        query = "INSERT INTO donation(lid,name,description,file,status,created_on,nid) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['name'], data['description'], filename,'pending',date,data['nid']))
        query="update needy_request set status='request' where nid="+data['nid']
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_needy_request'))

@app.route('/donor_view_needy_donation',methods=['GET','POST'])
def donor_view_needy_donation():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        print(session['lid'])
        cursor.execute("SELECT donation.*,needy_request.* from needy_request,donation where needy_request.nid=donation.nid and needy_request.status='request' and donation.status='pending'")     
        rows = cursor.fetchall()
        return render_template('donor_view_needy_donation.html',rows=rows)  
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO donation_request(lid,did,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['accept'],'pending',date))
        query="update donation set status='request' where donation_id="+data['accept']
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('donor_view_needy_donation'))

@app.route('/admin_view_accepted_needy_request',methods=['GET','POST'])
def admin_view_accepted_needy_request():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select needy_request.*,donation.*,donation_request.*,registration.* from donation_request,donation,needy_request,registration where needy_request.nid=donation.nid and donation.donation_id=donation_request.did and needy_request.status='request' and donation.status='request'and registration.lid=donation_request.lid")     
        rows = cursor.fetchall()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where registration.lid=login.lid and login.type='volunteer'")     
        volunteer = cursor.fetchall()
        return render_template('admin_view_accepted_needy_request.html',rows=rows,volunteer=volunteer)
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO donation_assign(drid,vid,created_on) VALUES(%s,%s,%s)"
        cursor.execute(query, (data['drid'],data['vid'],date))
        query="update donation set status='accept' where donation_id="+data['did']
        cursor.execute(query)
        query="update needy_request set status='accept' where nid="+data['nid']
        cursor.execute(query)
        query="update donation_request set status='accept' where drid="+data['drid']
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('donor_view_needy_donation'))    

@app.route('/volunteers_view_task',methods=['GET','POST'])
def volunteers_view_task():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select needy_request.*,donation.*,donation_request.*,donation_assign.*,registration.* from donation_assign,donation_request,donation,needy_request,registration where needy_request.nid=donation.nid and donation.donation_id=donation_request.did and donation_request.drid=donation_assign.drid and needy_request.lid=registration.lid and donation_assign.vid=%s",session['lid'])     
        rows = cursor.fetchall()
        return render_template('volunteers_view_task.html',rows=rows)

@app.route('/volunteer_add_feedback', methods=['GET','POST'])
@allow_for_loggined_users_only
def volunteer_add_feedback():
    if request.method=='GET':
        return render_template('volunteer_add_feedback.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO feedback(lid,subject,feedback,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['subject'],data['feedback'],date))
        conn.commit()
        conn.close()
        return redirect(url_for('volunteer_add_feedback'))    

@app.route('/admin_add_notification', methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_add_notification():
    if request.method=='GET':
        return render_template('admin_add_notification.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        today_date=datetime.datetime.now()
        query = "INSERT INTO notification(subject,content,date,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (data['subject'],data['content'],data['date'],today_date))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_add_notification'))          

@app.route('/hospital_add_blood_request', methods=['GET','POST'])
@allow_for_loggined_users_only
def hospital_add_blood_request():
    if request.method=='GET':
        return render_template('hospital_add_blood_request.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        today_date=datetime.datetime.now()
        query = "INSERT INTO blood_donation(hid,blood_group,status,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['hid'],data['blood'],'pending',today_date))
        conn.commit()
        conn.close()
        return redirect(url_for('hospital_add_blood_request')) 

@app.route('/admin_view_blood_request', methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_blood_request():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,hospital.*,blood_donation.* from blood_donation,hospital,login where login.lid=hospital.lid and hospital.hid=blood_donation.hid and blood_donation.status='pending'")     
        rows = cursor.fetchall()
        return render_template('admin_view_blood_request.html',row=rows)
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        cursor.execute("select login.lid,registration.* from registration,login where login.lid=registration.lid and registration.blood_group=%s",data['blood'])     
        rows = cursor.fetchall()
        print(rows)
        print(data['blood'])
        dt=[]
        for data in rows:
            dt.append({
                "blood":data[7],
                "user":data[3]
            })
            print(data[3])
            response=Mailer("pcare7188@gmail.com",data[3],"New Requirements",('Urgently needed  '+data[7]+'Blood' ))
            print (response)     
            cursor.execute("select * from blood_donation where status='pending' and blood_group=%s",data[7])     
            blood = cursor.fetchone()            
            q=" UPDATE blood_donation SET status ='{}' WHERE bid='{}'"
            query= q.format('accept',blood[0])                        
            print(query)
            cursor.execute(query)
            conn.commit() 
            conn.close()
            return redirect(url_for('admin_view_blood_request'))   
        return 'No Users For This Blood Group'                    

@app.route('/doctor_view_blood_message', methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_view_blood_message():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,hospital.*,blood_donation.* from blood_donation,hospital,login where login.lid=hospital.lid and hospital.hid=blood_donation.hid and blood_donation.blood_group=%s",session['blood'])     
        rows = cursor.fetchone()
        return render_template('doctor_view_blood_message.html',row=rows)

@app.route('/donor_view_blood_message', methods=['GET','POST'])
@allow_for_loggined_users_only
def donor_view_blood_message():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,hospital.*,blood_donation.* from blood_donation,hospital,login where login.lid=hospital.lid and hospital.hid=blood_donation.hid and blood_donation.blood_group=%s",session['blood'])     
        rows= cursor.fetchone()
        return render_template('donor_view_blood_message.html',row=rows) 

@app.route('/volunteer_view_blood_message', methods=['GET','POST'])
@allow_for_loggined_users_only
def volunteer_view_blood_message():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,hospital.*,blood_donation.* from blood_donation,hospital,login where login.lid=hospital.lid and hospital.hid=blood_donation.hid and blood_donation.blood_group=%s",session['blood'])     
        rows = cursor.fetchone()
        return render_template('volunteer_view_blood_message.html',row=rows)           

@app.route('/doctor_view_questions' , methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_view_questions():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,registration.*,question.* from question,registration,login where login.lid=registration.lid and registration.lid=question.lid and question.did=%s",session['lid'])     
        row = cursor.fetchall()        
        return render_template('doctor_view_questions.html',row=row)
    if request.method=='POST':
        data= request.form
        print(data)
        conn= mysql.connect()
        cursor=conn.cursor()
        today=date.today()
        q=" UPDATE question SET reply ='{}',rdate='{}' WHERE qid='{}'"
        query= q.format(data['reply'],today,data['qid'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('doctor_view_questions'))

@app.route('/doctor_view_complaint', methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_view_complaint():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM complaint where dvid=%s",session['lid'])     
        rows = cursor.fetchall()
        return render_template('doctor_view_complaint.html',row=rows)

@app.route('/doctor_add_feedback', methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_add_feedback():
    if request.method=='GET':
        return render_template('doctor_add_feedback.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO feedback(lid,subject,feedback,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['subject'],data['feedback'],date))
        conn.commit()
        conn.close()
        return redirect(url_for('doctor_add_feedback'))  

@app.route('/admin_view_complaint_against_doctor' , methods=['GET','POST'])
@allow_for_loggined_users_only
def admin_view_complaint_against_doctor():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,registration.*,complaint.* from login,registration,complaint where login.lid=registration.lid and registration.lid=complaint.lid")     
        row = cursor.fetchall()        
        return render_template('admin_view_complaint_against_doctor.html',row=row)
    if request.method=='POST':
        data= request.form
        print(data)
        conn= mysql.connect()
        cursor=conn.cursor()
        today=date.today()
        q=" UPDATE complaint SET reply ='{}',reply_date='{}' WHERE cid='{}'"
        query= q.format(data['reply'],today,data['cid'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('admin_view_complaint_against_doctor'))        

@app.route('/admin_view_feedback',methods=['GET','POST'])
def admin_view_feedback():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT feedback.*,registration.* from registration,feedback where feedback.lid=registration.lid")     
        row = cursor.fetchall()    
        return render_template('admin_view_feedback.html',row=row)

@app.route('/donor_add_feedback', methods=['GET','POST'])
@allow_for_loggined_users_only
def donor_add_feedback():
    if request.method=='GET':
        return render_template('donar_add_feedback.html')
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        date=datetime.datetime.now()
        query = "INSERT INTO feedback(lid,subject,feedback,created_on) VALUES(%s,%s,%s,%s)"
        cursor.execute(query, (session['lid'],data['subject'],data['feedback'],date))
        conn.commit()
        conn.close()
        return redirect(url_for('donor_add_feedback')) 

@app.route('/patient_edit_profile', methods=['GET','POST'])
@allow_for_loggined_users_only
def patient_edit_profile():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.* from registration,login where login.lid=registration.lid and login.type='patient' and login.lid=%s",session['lid'])     
        row = cursor.fetchone()  
        return render_template('patient_edit_profile.html',row=row)
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        q=" UPDATE registration SET name ='{}',email='{}',phone ='{}',dob='{}',gender ='{}',blood_group='{}',address ='{}',city='{}',district ='{}',pincode='{}',other_phone='{}' WHERE rid='{}'"
        query= q.format(data['name'],data['email'],data['phone'],data['dob'],data['gender'],data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],data['rid'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('patient_edit_profile')) 

@app.route('/doctor_edit_profile', methods=['GET','POST'])
@allow_for_loggined_users_only
def doctor_edit_profile():
    if request.method=='GET':
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select login.lid,login.type,registration.*,doctor_reg.* from registration,login,doctor_reg where login.lid=registration.lid and login.type='doctor' and doctor_reg.rid=registration.rid and login.lid=%s",session['lid'])     
        row = cursor.fetchone()  
        return render_template('doctor_edit_profile.html',row=row)
    if request.method=='POST':
        data= request.form
        conn= mysql.connect()
        cursor=conn.cursor()
        q=" UPDATE registration SET name ='{}',email='{}',phone ='{}',dob='{}',gender ='{}',blood_group='{}',address ='{}',city='{}',district ='{}',pincode='{}',other_phone='{}' WHERE rid='{}'"
        query= q.format(data['name'],data['email'],data['phone'],data['dob'],data['gender'],data['blood'],data['address'],data['city'],data['district'],data['pincode'],data['phonenum'],data['rid'])                        
        print(query)
        cursor.execute(query)
        q=" UPDATE doctor_reg SET specialization ='{}',exeperience='{}' WHERE did='{}'"
        query= q.format(data['specialization'],data['experience'],data['did'])                        
        print(query)
        cursor.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('doctor_edit_profile'))                 

@app.route('/add_notification')
def add_notification():
    return render_template('add_notification.html')


if __name__=='__main__':
    app.run(debug=True)