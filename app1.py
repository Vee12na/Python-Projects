from flask import Flask, render_template, url_for, request,redirect,session
import pandas as pd 
import numpy as np 
import joblib

import sqlite3 as sql


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predict', methods=["POST"])

def analyze():
    if request.method == 'POST':
        
        data = pd.read_csv("Iris.csv")

        
        # Check if 'Id' column exists and drop it
        if 'Id' in data.columns:
            data.drop('Id', axis=1, inplace=True)

        # Split data into features and target
        X = data.drop("Species", axis=1)  # Exclude the species feature
        y = data["Species"]

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize and train the Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Make predictions on the test set
        predictions = model.predict(X_test)

        # Evaluate accuracy
        accuracy = accuracy_score(y_test, predictions)
        print("Accuracy:", accuracy)
        
        # Save the model to disk
        joblib.dump(model, "iris_model.joblib")


        petal_length = request.form['petal_length']
        sepal_length = request.form['sepal_length']
        petal_width = request.form['petal_width']
        sepal_width = request.form['sepal_width']

       
        # Create a numpy array with the input data
        input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])

        # Load the trained model
        loaded_model = joblib.load("iris_model.joblib")

        # Define feature names
        feature_names = X.columns.tolist()

        # Create a DataFrame with the input data and feature names
        input_df = pd.DataFrame(input_data, columns=feature_names)

        # Make prediction
        result_prediction = loaded_model.predict(input_df)

        print(result_prediction)
        
        with sql.connect("iris.db") as con:
             c=con.cursor()
             c.execute("INSERT INTO predict (petallength,petalwidth,sepallength,sepalwidth,result) values(?,?,?,?,?)",(petal_length,petal_width,sepal_length,sepal_width,result_prediction)) 
             con.commit()

      

    
    return render_template('predict.html', petal_width=petal_width, petal_length=petal_length, sepal_length=sepal_length, sepal_width=sepal_width,result_prediction=result_prediction)
    #return render_template('predict.html')
    
@app.route("/signup", methods = ["GET","POST"])
def signup():
    msg=None
    if(request.method=="POST"):
        if (request.form["uname"]!="" and request.form["uphone"]!="" and request.form["username"]!="" and request.form["upassword"]!=""):
            username=request.form["username"]
            upassword=request.form["upassword"]
            uname=request.form["uname"]
            uphone=request.form["uphone"]


            with sql.connect("iris.db") as con:
                c=con.cursor()
                c.execute("INSERT INTO  signup VALUES('"+uname+"','"+uphone+"','"+username+"','"+upassword+"')")
                msg = "Your account is created"

                con.commit()
        else:
            msg="Something went wrong"


    return render_template("signup.html", msg=msg)

@app.route('/userlogin')
def userlogin():
    return render_template('userlogin.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/userloginNext',methods=['GET','POST'])
def userloginNext():
    msg=None
    if (request.method == "POST"):
        username = request.form['username']
      
        upassword = request.form['upassword']
        
        with sql.connect("iris.db") as con:
            c=con.cursor()
            c.execute("SELECT username,upassword  FROM signup WHERE username = '"+username+"' and upassword ='"+upassword+"'")
            r=c.fetchall()
            for i in r:
                if(username==i[0] and upassword==i[1]):
                    session["logedin"]=True
                    session["fusername"]=username
                    return redirect(url_for("userhome"))
                else:
                    msg= "please enter valid username and password"
    
    return render_template("userlogin.html",msg=msg)


@app.route('/userhome')
def userhome():
    return render_template("userhome.html")

@app.route('/usergallery')
def usergallery():
    return render_template('usergallery.html')

@app.route('/userviewfaq')
def userviewfaq():

    con=sql.connect("iris.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from addfaq")
    rows=cur.fetchall()
    print(rows)
    return render_template("userviewfaq.html",rows=rows)

@app.route('/viewprediction')
def viewprediction():
    con=sql.connect("iris.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select petallength,petalwidth,sepallength,sepalwidth from predict")
    rows=cur.fetchall()
    print(rows)
    return render_template("adminviewpredictions.html",rows=rows)

@app.route('/adminloginNext',methods=['GET','POST'])
def adminloginNext():
    msg=None
    if (request.method == "POST"):
        amail = request.form['amail']
      
        apassword = request.form['apassword']
        
        with sql.connect("iris.db") as con:
            c=con.cursor()
            c.execute("SELECT amail,apassword  FROM diginadmin WHERE amail = '"+amail+"' and apassword ='"+apassword+"'")
            r=c.fetchall()
            for i in r:
                if(amail==i[0] and apassword==i[1]):
                    session["logedin"]=True
                    session["fusername"]=amail
                    return redirect(url_for("adminhome1"))
                else:
                    msg= "please enter valid username and password"
    
    return render_template("adminlogin.html",msg=msg)



@app.route('/adminviewfaq')
def adminviewfaq():

    con=sql.connect("iris.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from addfaq")
    rows=cur.fetchall()
    print(rows)
    return render_template("adminviewfaq.html",rows=rows)


@app.route('/userpredict')
def userpredict():
    return render_template('userpredict.html')

@app.route('/userviewdataset')
def userviewdataset():
    df = pd.read_csv('data/iris.csv')
    return render_template('userviewdataset.html', df_view=df)

@app.route('/useraddfaq', methods=['POST','GET'])
def useraddfaq():
    #if request.method =='GET':
       

    if request.method == 'POST':
        try:
            question=request.form['question']
            answer=request.form['answer']
            

            with sql.connect("iris.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO addfaq(question,answer) VALUES(?,?)",(question,answer))
                con.commit
                msg="Record successfully added"
        
        except:
            con.rollback()
            msg="error in insert operation"

        finally:
            return render_template("useraddfaq.html",msg=msg)
            #return redirect(url_for('adminviewfaq'))

            con.close()	
    else:
        return render_template("useraddfaq.html")

@app.route('/userlogout')
def userlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('index'))



@app.route('/adminhome1',methods=['GET','POST'])
def adminhome1():
    return render_template('adminhome.html')

@app.route('/adminlogout')
def adminlogout():
	# Remove the session variable if present
	session.clear()
	return redirect(url_for('index'))

@app.route('/viewusers')
def viewusers():
    con=sql.connect("iris.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select uname,uphone,username from signup")
    rows=cur.fetchall()
    print(rows)
    return render_template("adminviewusers.html",rows=rows)

if __name__ == '__main__':
   app.run(debug=True)