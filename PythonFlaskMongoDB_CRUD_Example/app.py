#Python | Flask | MongoDB Atlas | HTML/CSS 
#CRUD Example
#Paul Manriquez
#Date: May 2024

from flask import Flask, jsonify, render_template, request, redirect, url_for
from product import Product
import database as dbase

#   Make a connection to the data base 
db = dbase.dbConnection() 
#   ==================================


app = Flask(__name__)


#=========== Home =============
@app.route('/')
def home():
    #Get and display the data from the data base 
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html',products = productsReceived)

#=========== Save Data =================
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products'] #Create or connect to the database called 'products'

    #=== Get data from the Form
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    #Save the data if the 3 where satisfied 
    if name and price and quantity:
        #1) Create an object of the class product 
        NerwProduct = Product(name, price, quantity)
        #2) Insert in the data base 
        products.insert_one(NerwProduct.toDB_Collection())
        #the data is stored as what returns our function (dic/json)

        #3)
        response = jsonify({
            'name': name,
            'price': price,
            'quantity':quantity
        })
        return redirect(url_for('home'))
    else:
        return notFound()
    

#=========== Delete =================
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))


#=========== Edit (Put method) =================
@app.route('/edit/<string:product_name>',methods=['POST'] )
def edit(product_name):
    #1)Connect to the data base
    products = db['products']
    
    #2)Get the data from the form to modify
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
                            #Search the element to modify | Modify section 
        products.update_one({'name':product_name}, {'$set': {'name':name, 'price':price, 'quantity':quantity}})
        response = jsonify({'message': 'Producto' + product_name + ' has been updated'})
        return redirect(url_for('home'))
    else:
        return notFound()





#=========== Not found Page ========= 
@app.errorhandler(404)
def notFound(error=None):
    message = {
         'message': 'Not found ' + request.url,
         'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == "__main__":
    app.run(debug=True,port=4000)