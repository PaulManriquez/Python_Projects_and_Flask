#Programmer: Paul Manriquez
#Date: May 2024
from flask import Flask, render_template, request , redirect, url_for
import os 
import database as db 

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src', 'templates')

app = Flask(__name__,template_folder=template_dir)

#======================= Routes ======================================
#def home: will execute a query to show all the data in the root of the page 
@app.route('/')
def home():
    cursor = db.database.cursor()#Make the connection to the data base 
    cursor.execute("SELECT * FROM register_table")
    myresult = cursor.fetchall()#Get a list of tuples of the data stored 
    #Convertt the data to a dictionary 
    insertObject = []
    print("**** Root QUERY ****")
    columnNames = [column [0] for column in cursor.description]#Get the name of the columns in the table
    
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
        #zip process
        #1) (ID,UserName,Name,Password),(1,user1@gmail.com,user1,1234) 
        #2) zip()
        #3) ( (ID,1) (UserName,user1@gmail.com) (Name,user1) (Password,1234) )
        #4) Convert to a dictionary
        #5) Store in the list, this will become in a list of dictionaries  
    #print(insertObject)
    cursor.close()
    return render_template('index.html',data=insertObject)

#def addUser: save the users to the data base ENDPOINT
#The petition will be satisfied if at the moment of pressing the button
#Will be performed  this action through the use of this route 
@app.route('/user',methods=['POST'])
def addUser():
    username = request.form['username']
    name = request.form['Name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "INSERT INTO register_table (UserName,Name,Password) VALUES (%s,%s,%s)"
        data = (username,name,password)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home'))    

#Delete section ENDPOINT
#This will be executed according with the parameter (id) that will be retrieved 
#in the id from the html code. 
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM register_table WHERE ID=%s"
    data = (id,)#It need the "," to be able to identify it as a tuple  
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

#Update section ENDPOINT
#From the html file when press edit , it prompts another window
#that have the button name "Save Changes", this send the rquest to this route and pass
#The parameter (id) to execute the change 
@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['Name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = "UPDATE register_table SET UserName = %s, Name = %s, Password = %s WHERE ID = %s"
        data = (username,name,password, id)
        cursor.execute(sql,data)
        db.database.commit()
    return redirect(url_for('home')) 



if __name__ == '__main__':
    app.run(debug=True,port=4000)