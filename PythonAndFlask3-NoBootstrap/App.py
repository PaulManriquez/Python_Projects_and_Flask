from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__) #Flask instance 

#========= Data base connection ===========
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'flaskcontacts'

mysql = MySQL(app) #Send the configurations
                   #To MySQL/Flask Module
#==========================================

#==================Enable messages with flask
app.secret_key = 'mysecretkey'#Make a session
#============================================

#============ Routes EndPoints ============

#Root
@app.route('/')
def Index():
    #===Show current data in data base
    #1) Connect to the data base
    cur = mysql.connection.cursor()
    #2) Write the query
    cur.execute('SELECT * FROM contacts')
    #3) Execute the query
    data = cur.fetchall()
    #=================================
    return render_template('index.html', contacts = data)
    # contacts = data: Pass by reference the data retrieved
    # by cur.fetchall(), (like a pointer pointing to data), to index.html

#Add a new contact
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        #========Get the data from the form 
        fullname = request.form['FullName']
        phone = request.form['Phone']
        email = request.form['Email']
        #==================================
        #Execute SQL
        #1) Connection
        cur = mysql.connection.cursor() 
        #2) Write the query
        sql_query = 'INSERT INTO contacts (FullName, Phone, Email) VALUES (%s, %s, %s)'
        values = (fullname,phone,email)
        cur.execute(sql_query,values) 
        #3) Message
        flash('Contact added successfully')
        #4) Execute the query
        mysql.connection.commit()
        #==============================================================================

        return redirect(url_for('Index')) # url_for('Index'): Name of the function 


        
#============================== Edit contact ========================================
@app.route('/edit/<string:ID>')
def get_contact(ID):
    #=========================== First, SHOW THE DATA TO THE USER TO EDIT THE CONTENT
    #===================== Send this data to the new html window to edit  the content  
    #Execute SQL
    #1) Connection
    cur = mysql.connection.cursor() 
    #2) Write the query
    sql_query = 'SELECT * FROM contacts WHERE ID = {0}'.format(ID)
    cur.execute(sql_query)
    data = cur.fetchall() 
    #3) Execute the query
    mysql.connection.commit()
    #=================================================================================
    return render_template('edit-contact.html', contact = data[0])
    #[0] you are passing the tuple and specifying to the first tuple in the list, (normally is the unique first element)
    #Redirect to the html template where show the data to the specific contact to edit 
    #its content 

@app.route('/update/<string:ID>',  methods = ['POST'])
def update_contact(ID):
    if request.method == 'POST':
        FullName = request.form['FullName']
        Phone = request.form['Phone']
        Email = request.form['Email']

        #Execute SQL
        #1) Connection
        cur = mysql.connection.cursor() 
        #2) Write the query
        sql_query = 'UPDATE contacts SET FullName = %s, Email = %s, Phone = %s WHERE ID = %s'
        data = (FullName,Phone,Email,ID)
        cur.execute(sql_query,data)
        #3) Execute the query
        flash('The contact has been edited successfully')
        mysql.connection.commit() 
        return redirect(url_for('Index'))   
    



#========================== END Edit contact ========================================

#Delete contact
@app.route('/delete/<string:ID>')
def delete_contact(ID):
    #Connect to the MySQL to execute the Query
    #Execute SQL
    #1) Connection
    cur = mysql.connection.cursor() 
    #2) Write the query
    sql_query = 'DELETE FROM contacts WHERE ID = {0}'.format(ID)
    cur.execute(sql_query) 
    #3) Execute query
    flash('Contact removed successfully')
    mysql.connection.commit()
    #Return/Update index
    return redirect(url_for('Index'))



#============= Main ================
if __name__ == '__main__':
    app.run(port=3000, debug = True)