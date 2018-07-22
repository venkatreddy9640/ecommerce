from flask import Flask, request, render_template, url_for, json
from flask_mongoengine import MongoEngine
from Users import User, UserOperations
from products import ProductOperations, Product
from orders import Order, OrderOperations
from logger import get_logger
import datetime, time

logger = get_logger('operations.log')

app = Flask(__name__)
db = MongoEngine()
app.config['MONGODB_SETTINGS']={'db':'amazon'}
db.init_app(app)

@app.route('/adduser', methods = ["POST",'GET'])
def AddUser():
    try:
        data = request.data
        data = json.loads(data)
        name = data['name']
        password = data['password']
        user_id = data['user_id']
        products_list = []
        street = data['street']
        city = data['city']
        state = data['state']
        location = {}
        location['state'] = state
        location['city'] = city
        location['street'] = street
        phone = data['phone']
        email = data['email']
        user = User(name=name, password = password, user_id = user_id, products_list = products_list, location = location, phone = phone, email = email)
        res = user.Save()
        return res, 200
    except Exception as e:
        logger.debug('Exception in adduser method')
        return str(e),500    

@app.route('/addproduct', methods = ["POST", "GET"])
def AddProduct():
    try:
        data = request.data
        data = json.loads(data)
        product_id = data['product_id']
        product_name = data['product_name']
        product_details = data['product_details']
        product_price = data['product_price']
        date = datetime.datetime.now()
        product_images = []
        product_category = data['product_category']
        product_keywords = data['product_keywords']
        product_quantity = data['product_quantity']
        product_rating = data['product_rating']
        product = Product(product_id = product_id, product_name = product_name, product_details = product_details, product_price = product_price, 
            date = date, product_images = product_images, product_category = product_category, product_keywords = product_keywords, product_quantity = 
            product_quantity, product_rating = product_rating)
        if product.Save():
            return 'Done',200
        return 'Failed', 400    
    except Exception as e:
        print e
        logger.debug('Exception in adding products')
        return str(e), 500  


@app.route('/viewusers')
def ViewUsers():
    useroperations = UserOperations()
    res = useroperations.ViewUsers()    
    return res, 200

@app.route('/finduser')
def FindUser():
    try:
        if not request.json:
            return 'Not a json request', 200
        data = request.data
        data = json.loads(data)
        user_id = data['user_id']
        useroperations = UserOperations()
        if useroperations.finduser(user_id):
            return user_id, 200
        return 'Failed ', 400
    except Exception as e:
        logger.debug('Exception occured in finding the user')
        return str(e), 500  
        
@app.route('/update')
def Update():
    try:
        if not request.json:
            return 'Not a json request', 400
        data = request.data
        data = json.loads(data)
        user_id = data['user_id']
        data.pop('user_id', None)
        useroperations = UserOperations()
        if useroperations.UpdateProductsList(user_id, data):
            return 'Done', 200
        return 'Failed', 400    
    except Exception as e:
        logger.debug('Exception occured while updating products'+ product_id)
        return str(e), 500


@app.route('/orderproducts')
def OrderProducts():
    try:
        if not request.json:
            return 'Not a json request ', 400
        data = request.data
        data = json.loads(data)
        product_id = data['product_id']
        quantity = data['quantity']
        user_id = data['user_id']
        billing_details = data['billing_details']
        productoperations = ProductOperations()
        if productoperations.OrderProduct(product_id, quantity, user_id, billing_details):
            return 'Done', 200
        return 'Failed ', 400   
    except Exception as e:
        print e
        logger.debug('Exception occured while ordering products')
        return str(e), 500

@app.route('/deleteproduct')
def Deleteproduct():
    try:
        if not request.json:
            return 'Not a json request ', 400
        data = request.data
        data = json.loads(request.data)
        product_id = data['product_id']
        productoperations = ProductOperations()
        if productoperations.Deleteproducts(product_id):
            return 'Done', 200
        return 'Failed', 400    
    except Exception as e:
        logger.debug('Exception in deleting product')
        return str(e), 500

@app.route('/addproductquantity')
def addproductquantity():
    try:
        if not request.json:
            return 'Not a json request', 400
        data = request.data
        data = json.loads(data)
        product_id = data['product_id']
        quantity = data['quantity']
        productoperations = ProductOperations()
        if productoperations.AddProductQuantity(product_id, quantity):
            return 'Done', 200
        return 'Failed', 400
    except Exception as e:
        logger.debug('Exception in addingproductquantity')
        return str(e), 500

@app.route('/finduserproducts')
def finduserproducts():
    try:
        if not request.json:
            return 'Not a json request', 400
        data = request.data
        data = json.loads(data)
        user_id = data['user_id']
        orderoperations = OrderOperations()
        res = orderoperations.FindUserOrders(user_id)
        if res:
            return res, 200
        return 'Failed', 400
    except Exception as e:
        logger.debug('Exception in finduserproducts method')
        return str(e), 500    
                      
        
if __name__ == '__main__':
    app.run(debug=True, port = 5000, host = '0.0.0.0')  
