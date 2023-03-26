from flask import Flask,render_template,request,redirect,url_for,session
from werkzeug.utils import secure_filename
import time
import os
from mylib import *

app=Flask(__name__)
app.secret_key="super secret key"
app.config['UPLOAD_FOLDER']='./static/photos'

#welcome
@app.route("/welcome",methods=['GET','POST'])
def welcome():
    return render_template("welcome.html")

#Login
@app.route("/",methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        regno=request.form["T1"]
        email=request.form["T2"]
        pas=request.form["T3"]
        cur=make_connection()
        sql="select * from logindata where email='"+email+"'AND password='"+pas+"'"
        cur.execute(sql)
        n=cur.rowcount
        if(n>0):
            data=cur.fetchone()
            ut=data[2]
            session["email"]=email
            session["usertype"]=ut
            session["reg"]=regno
            if(ut=="admin"):
                return redirect(url_for("admin_home"))
            elif(ut=="accountant"):
                return redirect(url_for("accountant_home"))
            else:
                return render_template("login.html",msg="Invalid usertype,Contact to Admin")
        else:
            return render_template("login.html",msg="Either userid or password is incrrect")
    else:
       return render_template("login.html")

#Admin Upload Photo ,Admin Home
@app.route("/admin_home",methods=['GET','POST'])
def admin_home():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            name=get_admin_name(email)
            if(request.method=="POST"):
                file=request.files["F1"]
                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur=make_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template("admin_home.html",e1=email, photo=filename,name=name)
                        else:
                            return render_template("admin_home.html",result="Failure",phot="no")
                    except:
                        return render_template("admin_home.html",result="Duplicate",photo="no")
            else:
                photo=check_photo(email)
                return render_template("admin_home.html",e1=email,photo=photo,name=name)
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Change Photo
@app.route("/admin_ch_photo")
def admin_ch_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="admin"):
            photo=check_photo(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/" + photo)
                return render_template("admin_ch_photo.html",data="success")
            else:
                return render_template("admin_ch_photo.html",data="Failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin reg
@app.route("/admin_reg",methods=['GET','POST'])
def admin_reg():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                nm=request.form["T1"]
                ad=request.form["T2"]
                con=request.form["T3"]
                em=request.form["T4"]
                pas=request.form["T5"]
                usertype="admin"
                cur=make_connection()
                sql="insert into admindata values('"+nm+"','"+ad+"','"+con+"','"+em+"')"
                sql1="insert into logindata values('"+em+"','"+pas+"','"+usertype+"')"
                try:
                    cur.execute(sql)
                    n=cur.rowcount

                    cur.execute(sql1)
                    m=cur.rowcount

                    if(n==1 and m==1):
                        msg="Data Saved"
                    else:
                        msg="Data Not Saved "
                except pymysql.err.IntegrityError:
                    msg="Data is already registered"
                return render_template("admin_reg.html",admin=msg)
            else:
                return render_template("admin_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin profile
@app.route("/admin_pro")
def admin_pro():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            cur=make_connection()
            e1=session["email"]
            sql="select * from admindata where email='"+e1+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchone()
                return render_template("admin_pro.html",kota=data)
            else:
                return render_template("admin_pro.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Profile1
@app.route("/admin_pro1",methods=['GET','POST'])
def admin_pro1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                cur=make_connection()
                e1=session["email"]
                sql="select * from admindata where email='"+e1+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("admin_pro1.html",kota=data,msg="Data Saved")
                else:
                    return render_template("admin_pro1.html",msg="Data Not Saved")
            else:
                return redirect(url_for("admin_pro"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Profile2
@app.route("/admin_pro2",methods=['GET','POST'])
def admin_pro2():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                nm=request.form["T1"]
                ad=request.form["T2"]
                co=request.form["T3"]
                email=session["email"]
                cur=make_connection()
                sql="update admindata set name='"+nm+"',address='"+ad+"',contact='"+co+"'where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("admin_pro2.html",msg="Data Updated")
                else:
                    return render_template("admin_pro2.html",msg="Data Is Not  Updated")
            else:
                return redirect(url_for("admin_pro"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Admin Chnage Password
@app.route("/admin_ch_pass",methods=['GET','POST'])
def admin_ch_pass():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                e1=session["email"]
                oldpass=request.form["T1"]
                newpass=request.form["T2"]
                cur=make_connection()
                sql="update logindata set password='"+newpass+"'where email='"+e1+"' AND password='"+oldpass+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return  render_template("admin_ch_pass.html",msg="Password Changed Successfully")
                else:
                    return render_template("admin_ch_pass.html",msg="Password Not Changed")
            else:
                return render_template("admin_ch_pass.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#accountant reg
@app.route("/accountant_reg",methods=['GET','POST'])
def accountant_reg():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                emp=request.form["T1"]
                nm=request.form["T2"]
                des=request.form["T3"]
                co=request.form["T4"]
                email=request.form["T5"]
                pas=request.form["T6"]
                usertype="accountant"
                cur=make_connection()
                sql="insert into accountant values('"+emp+"','"+nm+"','"+des+"','"+co+"','"+email+"')"
                sql1="insert into logindata values('"+email+"','"+pas+"','"+usertype+"')"
                try:
                    cur.execute(sql)
                    n=cur.rowcount

                    cur.execute(sql1)
                    m=cur.rowcount

                    if(n==1 and m==1):
                        msg="Data Saved"
                    else:
                        msg="Data Not Saved"
                except pymysql.err.IntegrityError:
                    msg="Data already exist"
                return render_template("accountant_reg.html",msg=msg)
            else:
                return render_template("accountant_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show Accountant
@app.route("/show_accounant")
def show_accountant():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            cur=make_connection()
            sql="select * from accountant"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("show_accountant.html",kota=data)
            else:
                return render_template("show_accountant.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))

#Edit_Accountant
@app.route("/edit_accountant",methods=['GET','POST'])
def edit_accountant():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                emp=request.form["H1"]
                cur=make_connection()
                sql="Select * from accountant where empno='"+emp+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edit_accountant.html",kota=data)
                else:
                    return render_template("edit_accountant.html",msg="Data Not Found")
            else:
                return redirect(url_for("show_accountant"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit_Accountant1
@app.route("/edit_accountant1",methods=['GET','POST'])
def edit_accountant1():
    if("usertype" in session ):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                emp=request.form["T1"]
                nm=request.form["T2"]
                des=request.form["T3"]
                con=request.form["T4"]
                email=request.form["T5"]
                cur=make_connection()
                sql="update accountant set name='"+nm+"',designation='"+des+"',contact='"+con+"',email='"+email+"'where empno='"+emp+"' "
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return  render_template("edit_accountant1.html",msg="Data Saved")
                else:
                    return render_template("edit_accountant1.html",msg="Data Not Saved")
            else:
                return redirect(url_for("show_accountant"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Delete_Accountant
@app.route("/delete_accountant",methods=['GET','POST'])
def delete_accountant():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                emp=request.form["H1"]
                cur=make_connection()
                sql="Select * from accountant where empno='"+emp+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("delete_accountant.html",kota=data)
                else:
                    return render_template("delete_accountant.html",msg="Data Not Found")
            else:
                return redirect(url_for("show_accountant"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Delete_Accountant1
@app.route("/delete_accountant1",methods=['GET','POST'])
def delete_accountant1():
    if("usertype" in session ):
        ut=session["usertype"]
        if(ut=="admin"):
            if(request.method=="POST"):
                emp=request.form["T1"]
                nm=request.form["T2"]
                des=request.form["T3"]
                con=request.form["T4"]
                email=request.form["T5"]
                cur=make_connection()
                sql="delete from accountant where empno='"+emp+"'"
                sql1="delete from logindata where email='"+email+"'"
                cur.execute(sql)
                n=cur.rowcount

                cur.execute(sql1)
                m=cur.rowcount
                if(n==1 and m==1):
                    return  render_template("delete_accountant1.html",msg="Data Saved")
                else:
                    return render_template("delete_accountant1.html",msg="Data Not Saved")
            else:
                return redirect(url_for("show_accounant"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Accountant Home
@app.route("/accountant_home",methods=['GET','POST'])
def accountant_home():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="accountant"):
            name=get_accountant_name(email)
            if(request.method=="POST"):
                file=request.files["F1"]
                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)
                    cur=make_connection()
                    sql="insert into photodata values('"+email+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                            return render_template("accountant_home.html",e1=email, photo=filename,name=name)
                        else:
                            return render_template("accountant_home.html",result="Failure",photo="no")
                    except:
                        return render_template("accountant_home.html",result="Duplicate",photo="no")
            else:
                photo=check_photo(email)
                return render_template("accountant_home.html",e1=email,photo=photo,name=name)

        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Accountant Change Photo
@app.route("/accountant_ch_photo")
def accountant_ch_photo():
    if("usertype" in session):
        ut=session["usertype"]
        email=session["email"]
        if(ut=="accountant"):
            photo=check_photo(email)
            cur=make_connection()
            sql="delete from photodata where email='"+email+"'"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                os.remove("./static/photos/" + photo)
                return render_template("accountant_ch_photo.html",data="success")
            else:
                return render_template("accountant_ch_photo.html",data="Failure")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Student Registration
@app.route("/st_reg",methods=['GET','POST'])
def st_reg():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):

            if(request.method=="POST"):
                file=request.files['F1']
                reg=request.form["T1"]
                nm=request.form["T2"]
                ad=request.form["T3"]
                con=request.form["T4"]
                em=request.form["T5"]
                if(file):
                    path=os.path.basename(file.filename)
                    file_ext=os.path.splitext(path)[1][1:]
                    filename=str(int(time.time()))+'.'+file_ext
                    filename=secure_filename(filename)

                    cur=make_connection()
                    sql="insert into stdata values('"+reg+"','"+nm+"','"+ad+"','"+con+"','"+em+"','"+filename+"')"
                    try:
                        cur.execute(sql)
                        n=cur.rowcount
                        if(n==1):
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

                            return render_template("student_reg.html",msg="Data Saved")
                        else:
                            return render_template("student_reg.html",msg="Data Not Saved")
                    except pymysql.err.IntegrityError:
                            return render_template("student_reg.html",msg="Data H")
            else:
                return render_template("student_reg.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show Student
@app.route("/show_student", methods=['GET'])
def show_student():
    if("usertype" in session):
        ut=session["usertype"]

        if(ut=="accountant"):
            cur=make_connection()
            sql="select * from stdata"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()

                return render_template("show_student.html",kota=data)
            else:
                return render_template("show_student.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit Student
@app.route("/edit_student",methods=['GET','POST'])
def edit_student():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["H1"]
                cur=make_connection()
                sql="select * from stdata where regno='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edit_student.html",kota=data)
                else:
                    return render_template("edit_student.html",msg="No data found")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit Student1
@app.route("/edit_student1",methods=['GET','POST'])
def edit_student1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["T1"]
                nm=request.form["T2"]
                ad=request.form["T3"]
                co=request.form["T4"]
                email=request.form["T5"]

                cur=make_connection()
                sql="update stdata set name='"+nm+"',address='"+ad+"',contact='"+co+"',email='"+email+"' where regno='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("edit_student1.html",msg="Changes saved")
                else:
                    return render_template("edit_student1.html",msg="Error")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Delete Student
@app.route("/delete_student",methods=['GET','POST'])
def delete_student():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["H1"]
                cur=make_connection()
                sql="select * from stdata where regno='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("delete_student.html",kota=data)
                else:
                    return render_template("delete_student.html",msg="No data found")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Delete Student1
@app.route("/delete_student1",methods=['GET','POST'])
def delete_student1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["T1"]
                nm=request.form["T2"]
                ad=request.form["T3"]
                co=request.form["T4"]
                email=request.form["T5"]

                cur=make_connection()
                sql="delete from stdata where regno='"+reg+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("delete_student1.html",msg="Changes saved")
                else:
                    return render_template("delete_student1.html",msg="Error")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Student Course
@app.route("/st_course",methods=['GET','POST'])
def st_course():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg=request.form["T2"]
                cou=request.form["T3"]
                fee=request.form["T4"]
                rm=request.form["T5"]
                cur=make_connection()
                sql="insert into stcourse values(0,'"+reg+"','"+cou+"',"+fee+",'"+rm+"')"

                try:
                    cur.execute(sql)
                    n=cur.rowcount

                    if(n==1):
                        msg="Data Saved"
                    else:
                        msg="Data Not Saved "
                except pymysql.err.IntegrityError:
                    msg="Data is already registered"
                return render_template("student_course.html",msg=msg)
            else:
                return render_template("student_course.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show course
@app.route("/show_course")
def show_course():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            cur=make_connection()
            sql="select * from stcourse"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("show_course.html",kota=data)
            else:
                return render_template("show_course.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit Course
@app.route("/edit_course",methods=['GET','POST'])
def edit_course():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                couid=request.form["H1"]
                cur=make_connection()
                sql="select * from stcourse where courseid='"+couid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    data=cur.fetchone()
                    return render_template("edit_course.html",kota=data)
                else:
                    return render_template("edit_course.html",msg="No data found")
            else:
                return redirect(url_for("info"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Edit Course1
@app.route("/edit_course1",methods=['GET','POST'])
def edit_course1():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                couid=request.form["T1"]
                reg = request.form["T2"]
                cou = request.form["T3"]
                fee = request.form["T4"]
                re= request.form["T5"]

                cur=make_connection()
                sql="update stcourse set regno='"+reg+"',course='"+cou+"',fee='"+fee+"',remark='"+re+"' where courseid='"+couid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n==1):
                    return render_template("edit_course1.html",msg="Changes saved")
                else:
                    return render_template("edit_course1.html",msg="Data not saved")
            else:
                return redirect(url_for("info"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Student fee
@app.route("/st_fee",methods=['GET','POST'])
def st_fee():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                reg = request.form["T1"]
                couid=request.form["T2"]
                amt=request.form["T3"]
                dep=request.form["T4"]
                rm=request.form["T5"]
                cur=make_connection()
                sql="insert into stfee values(0,'"+reg+"','"+couid+"',"+amt+",'"+dep+"','"+rm+"')"

                try:
                    cur.execute(sql)
                    n=cur.rowcount

                    if(n==1):
                        msg="Data Saved"
                    else:
                        msg="Data Not Saved "
                except pymysql.err.IntegrityError:
                    msg="Data is already registered"
                return render_template("student_fee.html",msg=msg)
            else:
                return render_template("student_fee.html")
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Show Fee
@app.route("/show_fee")
def show_fee():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            cur=make_connection()
            sql="select * from stfee"
            cur.execute(sql)
            n=cur.rowcount
            if(n>0):
                data=cur.fetchall()
                return render_template("show_fee.html",kota=data)
            else:
                return render_template("show_fee.html",msg="No Data Found")
        else:
            return redirect(url_for("auth_error"))
    else:
        return  redirect(url_for("auth_error"))

#info
@app.route("/info",methods=['GET','POST'])
def info():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                regno=request.form["H1"]
                cur=make_connection()
                sql="select * from stcourse where regno='"+regno+"'"
                sql1="select * from stfee where regno='"+regno+"'"
                cur.execute(sql)
                n=cur.rowcount
                if(n>0):
                    kota=cur.fetchall()
                    cur.execute(sql1)
                    m=cur.rowcount
                    if(m>0):
                        kota1=cur.fetchall()
                        return render_template("info.html",data1=kota,data2=kota1)
                    else:
                        return render_template("info.html",msg="Fees not deposited")
                else:
                    return render_template("info.html",msg="No Course")
            else:
                return redirect(url_for("show_student"))
        else:
            return redirect(url_for("auth_error"))
    else:
        return redirect(url_for("auth_error"))

#Search
@app.route("/search",methods=['GET','POST'])
def search():
    if("usertype" in session):
        ut=session["usertype"]
        if(ut=="accountant"):
            if(request.method=="POST"):
                name=request.form["T1"]
                cur=make_connection()
                sql="select * from stdata where name='"+name+"'"
                cur.execute(sql)
                data=cur.fetchall()
                return render_template("search.html",kota=data)
            else:
                return render_template("search.html")
        else:
            return redirect(url_for("auth_error"))
    else:
       return redirect(url_for("auth_error"))

#Logout
@app.route("/logout",methods=['GET','POST'])
def logout():
    if("usertype" in session):
        session.pop("usertype", None)
        session.pop("email",None)
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

#Auth_error
@app.route("/auth_error")
def auth_error():
    return render_template("auth_error.html")

#main function
if __name__=="__main__":
    app.run(debug=True)