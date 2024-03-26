from flask import Flask,render_template,redirect,url_for,request
from form_classes import *
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def index():
    db = sql.connect("database3.db")
    c = db.cursor()
    c.execute("PRAGMA foreign_keys = ON")
    db.commit()
    db.close()

    return render_template("index.html")

@app.route("/error")
def error():
    return render_template("error.html")


########################### STUDENTS ##################################

@app.route("/students")
def students():
    with sql.connect("database3.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query=""" SELECT * FROM STUDENTS """

        cursor.execute(query)

        students = cursor.fetchall()

    return render_template("students/students.html",students=students) 

@app.route("/students/add_student", methods=["GET","POST"])
def add_student():
    form = StudentForm(request.form)

    if request.method == "POST" and form.validate(): 
        student_name = form.student_name.data

        con = sql.connect("database3.db") 

        try:
            
            cursor=con.cursor()
            query = "INSERT INTO STUDENTS (StuName) VALUES (?)"
            cursor.execute("PRAGMA foreign_keys = ON")
            
            cursor.execute(query,(student_name,))
            con.commit()  

            cursor.close() 

        except:
            con.rollback()
            return redirect(url_for("error"))

        return redirect(url_for("students"))
    
    else:

        return render_template("students/add_student.html", form=form) 
    
@app.route("/edit_student/<string:id>", methods=["GET","POST"])
def edit_student(id):

    if request.method == "GET":
        form = StudentForm()

        with sql.connect("database3.db") as con:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")

            query = "SELECT StuName FROM STUDENTS WHERE (stuId = ?)"
            cur.execute(query,(id,))
            stu = cur.fetchone()#matching element

            form.student_name.data = stu["StuName"]

        return render_template("students/edit_student.html", form=form)

    if request.method == "POST":
        form = StudentForm(request.form)
        new_name = form.student_name.data

        con = sql.connect("database3.db") 
        try:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "UPDATE STUDENTS SET StuName = ? WHERE stuId = ?"
            cur.execute(query,(new_name, id))
            con.commit()
        except:
            con.rollback()
            return redirect(url_for("error"))            
        
        return redirect(url_for("students"))


@app.route("/delete_student/<string:id>")
def delete_student(id):

    with sql.connect("database3.db") as con:
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query = "DELETE FROM STUDENTS WHERE StuId = ?" 

        cursor.execute(query,(id,))

        con.commit() 

    return redirect(url_for("students"))


########################### STUDENT-INFO ##################################

@app.route("/stu_info")
def stu_info():
    with sql.connect("database3.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query="""SELECT STUINFO.*, STUDENTS.StuName
                FROM STUINFO
                JOIN STUDENTS ON STUINFO.stu = STUDENTS.stuId;
                """

        cursor.execute(query)

        students = cursor.fetchall()

    return render_template("stu_info/stu_info.html",students=students)

@app.route("/delete_info/<string:id>")
def delete_info(id):

    with sql.connect("database3.db") as con:
       cursor=con.cursor()
       cursor.execute("PRAGMA foreign_keys = ON") 
       query = "DELETE FROM STUINFO WHERE id = ?" 

       cursor.execute(query,(id,))

       con.commit() 

    return redirect(url_for("stu_info"))

@app.route("/stu_info/add_info", methods=["GET","POST"])
def add_info():
    form = StudentInfoForm(request.form)

    if request.method == "POST" and form.validate(): 
        student_number= form.student_number.data
        student_grade = form.student_grade.data
        stuParentName = form.stuParentName.data
        stuParentPhone = form.stuParentPhone.data
        stuMail = form.stuMail.data
        stuGender = form.stuGender.data
        

        con = sql.connect("database3.db") 
        try:
            cursor=con.cursor()
            query = "INSERT INTO STUINFO (stu,stugrade,parentname,parentphone,stumail,stugender) VALUES (?,?,?,?,?,?)"
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(query,(student_number,student_grade,stuParentName,stuParentPhone,stuMail,stuGender))

            #if cursor.lastrowid == 0:
            #    return render_template("index.html")

            con.commit()  

            cursor.close() 

        except:
            con.rollback()
            return redirect(url_for("error"))

        return redirect(url_for("stu_info"))
    
    else:
        return render_template("stu_info/add_info.html", form=form) 
    


@app.route("/edit_info/<string:id>", methods=["GET","POST"])
def edit_info(id):

    if request.method == "GET":
        form = StudentInfoForm()

        with sql.connect("database3.db") as con:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "SELECT * FROM STUINFO WHERE (id = ?)"
            cur.execute(query,(id,))

            sinfo = cur.fetchone()#matching element

            form.student_number.data = sinfo["stu"]
            form.student_grade.data = sinfo["stugrade"]
            form.stuParentName.data = sinfo["parentname"]
            form.stuParentPhone.data = sinfo["parentphone"]
            form.stuMail.data = sinfo["stumail"]
            form.stuGender.data = sinfo["stugender"]


        return render_template("stu_info/edit_info.html", form=form)

    if request.method == "POST":
        form = StudentInfoForm(request.form)
        student_number = form.student_number.data
        student_grade = form.student_grade.data
        stuParentName = form.stuParentName.data
        stuParentPhone = form.stuParentPhone.data
        stuMail = form.stuMail.data
        stuGender = form.stuGender.data

        con = sql.connect("database3.db")

        try:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "UPDATE STUINFO SET stu = ?, stugrade = ?, parentname = ?, parentphone = ?, stumail = ?, stugender = ?  WHERE id = ?"
            cur.execute(query,(student_number,student_grade,stuParentName,stuParentPhone,stuMail,stuGender,  id))
            con.commit()
            cur.close()
        except:
            con.rollback()
            return redirect(url_for("error"))            
        
        
        return redirect(url_for("stu_info"))



########################################################################################

#############################EXAMS##########################
@app.route("/exams")
def exams():
    with sql.connect("database3.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query="""SELECT EXAMS.*, STUDENTS.StuName
                FROM EXAMS
                JOIN STUDENTS ON EXAMS.stu = STUDENTS.stuId;
                """

        cursor.execute(query)

        students = cursor.fetchall()

    return render_template("exams/exams.html",students=students)

@app.route("/delete_exams/<string:id>")
def delete_exams (id):

    with sql.connect("database3.db") as con:
       cursor=con.cursor()
       cursor.execute("PRAGMA foreign_keys = ON") 
       query = "DELETE FROM EXAMS WHERE id = ?" 

       cursor.execute(query,(id,))

       con.commit() 

    return redirect(url_for("exams"))

@app.route("/exams/add_exams", methods=["GET","POST"])
def add_exams():
    form = ExamsForm(request.form)

    if request.method == "POST" and form.validate(): 
        student_number= form.student_number.data
        math = form.math.data
        physics = form.physics.data
        biology = form.biology.data
        history= form.history.data
        sports=form.sports.data
        

        con = sql.connect("database3.db") 
        try:
            cursor=con.cursor()
            query = "INSERT INTO EXAMS (stu,math,physics,biology,history,sports) VALUES (?,?,?,?,?,?)"
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(query,(student_number,math,physics,biology,history,sports))

            #if cursor.lastrowid == 0:
            #    return render_template("index.html")

            con.commit()  

            cursor.close() 

        except:
            con.rollback()
            return redirect(url_for("error"))

        return redirect(url_for("exams"))
    
    else:
        return render_template("exams/add_exams.html", form=form) 
    


@app.route("/edit_exams/<string:id>", methods=["GET","POST"])
def edit_exams(id):

    if request.method == "GET":
        form = ExamsForm()

        with sql.connect("database3.db") as con:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "SELECT * FROM EXAMS WHERE (id = ?)"
            cur.execute(query,(id,))

            sinfo = cur.fetchone()#matching element

            form.student_number.data = sinfo["stu"]
            form.math.data = sinfo["math"]
            form.physics.data = sinfo["physics"]
            form.biology.data = sinfo["biology"]
            form.history.data = sinfo["history"]
            form.sports.data = sinfo["sports"]


        return render_template("exams/edit_exams.html", form=form)

    if request.method == "POST":
        form = ExamsForm(request.form)
        student_number = form.student_number.data
        math = form.math.data
        physics = form.physics.data
        biology = form.biology.data
        history = form.history.data
        sports= form.sports.data

        con = sql.connect("database3.db")

        try:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "UPDATE EXAMS SET stu = ?, math = ?, physics= ?, biology = ?, history = ?,sports = ?  WHERE id = ?"
            cur.execute(query,(student_number,math,physics,biology,history,sports,id))
            con.commit()
            cur.close()
        except:
            con.rollback()
            return redirect(url_for("error"))            
        
        
        return redirect(url_for("exams"))



############################################################
    
    
##########################ATTENDANCE########################
@app.route("/attendance")
def attendance():
    with sql.connect("database3.db") as con:
        con.row_factory = sql.Row
        cursor=con.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")

        query="""SELECT ATTENDANCE.*, STUDENTS.StuName
                FROM ATTENDANCE
                JOIN STUDENTS ON ATTENDANCE.stu = STUDENTS.stuId;
                """

        cursor.execute(query)

        students = cursor.fetchall()

    return render_template("attendance/attendance.html",students=students)

@app.route("/delete_attendance/<string:id>")
def delete_attendance (id):

    with sql.connect("database3.db") as con:
       cursor=con.cursor()
       cursor.execute("PRAGMA foreign_keys = ON") 
       query = "DELETE FROM ATTENDANCE WHERE id = ?" 

       cursor.execute(query,(id,))

       con.commit() 

    return redirect(url_for("attendance"))

@app.route("/attendance/add_attendance", methods=["GET","POST"])
def add_attendance():
    form = AttendanceForm(request.form)

    if request.method == "POST" and form.validate(): 
        student_number= form.student_number.data
        math_absent = form.math_absent.data
        physics_absent= form.physics_absent.data
        biology_absent = form.biology_absent.data
        history_absent= form.history_absent.data
        sports_absent=form.sports_absent.data
        

        con = sql.connect("database3.db") 
        try:
            cursor=con.cursor()
            query = "INSERT INTO ATTENDANCE (stu,math_absent,physics_absent,biology_absent,history_absent,sports_absent) VALUES (?,?,?,?,?,?)"
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute(query,(student_number,math_absent,physics_absent,biology_absent,history_absent,sports_absent))

            #if cursor.lastrowid == 0:
            #    return render_template("index.html")

            con.commit()  

            cursor.close() 

        except:
            con.rollback()
            return redirect(url_for("error"))

        return redirect(url_for("attendance"))
    
    else:
        return render_template("attendance/add_attendance.html", form=form) 
    


@app.route("/edit_attendance/<string:id>", methods=["GET","POST"])
def edit_attendance(id):

    if request.method == "GET":
        form = AttendanceForm()

        with sql.connect("database3.db") as con:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "SELECT * FROM ATTENDANCE WHERE (id = ?)"
            cur.execute(query,(id,))

            sinfo = cur.fetchone()#matching element

            form.student_number.data = sinfo["stu"]
            form.math_absent.data = sinfo["math_absent"]
            form.physics_absent.data = sinfo["physics_absent"]
            form.biology_absent.data = sinfo["biology_absent"]
            form.history_absent.data = sinfo["history_absent"]
            form.sports_absent.data = sinfo["sports_absent"]


        return render_template("attendance/edit_attendance.html", form=form)

    if request.method == "POST":
        form = AttendanceForm(request.form)
        student_number = form.student_number.data
        math_absent = form.math_absent.data
        physics_absent = form.physics_absent.data
        biology_absent = form.biology_absent.data
        history_absent = form.history_absent.data
        sports_absent= form.sports_absent.data

        con = sql.connect("database3.db")

        try:
            con.row_factory = sql.Row
            cur=con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            query = "UPDATE ATTENDANCE SET stu = ?, math_absent = ?, physics_absent= ?, biology_absent = ?, history_absent = ?,sports_absent = ?  WHERE id = ?"
            cur.execute(query,(student_number,math_absent,physics_absent,biology_absent,history_absent,sports_absent,id))
            con.commit()
            cur.close()
        except:
            con.rollback()
            return redirect(url_for("error"))            
        
        
        return redirect(url_for("attendance"))

############################################################
     
if __name__ == "__main__":
    app.run(debug=True)