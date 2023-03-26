import  pymysql

def make_connection():
    cn=pymysql.connect(host="localhost",port=3306,user="root",passwd="",db="fee",autocommit=True)
    cur=cn.cursor()
    return cur

#To check photo of  accountant and admin
def check_photo(email):
    cur=make_connection()
    cur.execute("SELECT * FROM photodata where email='"+email+"'")
    n=cur.rowcount
    photo="no"
    if(n>0):
        row=cur.fetchone()
        photo=row[1]
    return photo

def get_admin_name(email):
    cur=make_connection()
    cur.execute("SELECT * FROM admindata where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if(n>0):
        row=cur.fetchone()
        name=row[0]
    return name

def get_accountant_name(email):
    cur=make_connection()
    cur.execute("SELECT * FROM accountant where email='"+email+"'")
    n=cur.rowcount
    name="no"
    if(n>0):
        row=cur.fetchone()
        name=row[1]
    return name

def get_student_name(reg):
    cur=make_connection()
    cur.execute("SELECT * FROM stdata where reg_no='"+reg+"'")
    n=cur.rowcount
    name="no"
    if(n>0):
        row=cur.fetchone()
        name=row[1]
    return name

#fetch photo of student
def check_pic(rno):
    cur=make_connection()
    cur.execute("SELECT * FROM stdata where reg_no='"+rno+"'")
    n=cur.rowcount
    photo="no"
    if(n>0):
        row=cur.fetchone()
        photo=row[5]
    return photo

#find course total of student
def total_fee(regno):
    cur = make_connection()
    cur.execute("SELECT * FROM stcourse where regno='" + regno + "'")
    n = cur.rowcount
    t=0
    if (n > 0):
        data=cur.fetchall()
        for d in data:
            t=t+d[3]
    return t

#find total of installments of one student
def total_installments(regno):
    cur = make_connection()
    cur.execute("SELECT * FROM stfee where reg_no='" + regno + "'")
    n = cur.rowcount
    t=0
    if (n > 0):
        data=cur.fetchall()
        for d in data:
            t=t+d[3]
    return t

#find total of installments of one course of student
def total_installments_course(regno,courseid):
    cur = make_connection()
    cur.execute("SELECT * FROM stfee where regno='" + regno + "' AND courseid="+courseid)
    n = cur.rowcount
    t=0
    if (n > 0):
        data=cur.fetchall()
        for d in data:
            t=t+d[3]
    return t