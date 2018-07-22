from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError
from logger import get_logger
from Users import User, UserOperations
from orders import Order, OrderOperations
from billing import Billing
import json, datetime, time

db = MongoEngine()

logger = get_logger('products.log')

class Product(db.Document):
	product_id = db.StringField()
	product_name = db.StringField()
	product_details = db.DictField()
	product_price = db.IntField()
	date = db.DateTimeField()
	product_images = db.ListField()
	product_category = db.StringField()
	product_keywords = db.ListField()
	product_quantity = db.IntField()
	product_rating = db.StringField()
	meta ={
		'indexes':[{'fields':['-product_id'],'unique':True }]
	}

	def Save(self):
		try:
			self.save()
			return 'Saved Successfully'
		except NotUniqueError as e:
			print e
			logger.debug('unique excetption in product_id ')
			return None
		except Exception as e:
			print e
			logger.debug('Exception in saving the product')
			return None

class ProductOperations():
	
	def GetProducts(self, keyword):
		result = []
		products = Product.objects().first()
		for product in products:
			if keyword in product.product_keywords and product.quantity > 0:
				result.append(product)
		return result		

	def DeleteProducts(self, this_product_id):
		try:
			product = Product.objects(product_id = this_product_id).first()
			product.delete()
			return True
		except Exception as e:
			logger.debug('Exception in deletion of product')
			raise e
			return None

	def AddProductQuantity(self, this_product_id, new_qantity):
		try:
			product = Product.objects(product_id = this_product_id).first()
			product.product_quantity += new_qantity
			product.save()
			return True
		except Exception as e:
			logger.debug('Exception in adding product quantity' + product_id)
			raise e
			return None
	
	def OrderProduct(self, this_product_id, quantity, user_id, billing_details):
		try:
			logger.debug('Trying to decrease the product_quantity by '+ str(quantity))
			product = Product.objects(product_id = this_product_id).first()
			product.product_quantity -= quantity
			useroperations = UserOperations()
			useroperations.UpdateProductsList(user_id, product.product_category)
			orderoperations = OrderOperations()
			date = datetime.datetime.now()
			billing_id = int(time.time())
			billing_price = quantity*product.product_price
			billing = Billing(billing_id = billing_id, billing_price = billing_price, billing_date = date, billing_details = billing_details)
			print billing_price, billing_details
			order_id = int(time.time())
			order = Order(user_id = user_id, date = date, order_id = order_id, product_id = this_product_id)
			billing.Save()
			order.Save()
			product.Save()
			return True
		except Exception as e:
			print e
			logger.debug('Exception in Order Product method')
			logger.debug('Exception occured while trying to decrease product quantity of product '+ product.product_id +' by quantity '+ quantity)
			raise e
			return None







