from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError
from logger import get_logger
import json

db = MongoEngine()

logger = get_logger('orders.log')

class Order(db.Document):
	order_id = db.IntField()
	date = db.DateTimeField()
	product_id = db.StringField()
	user_id = db.StringField()
	billing_id = db.IntField()
	meta = {
	    'indexes':[{'fields':['-order_id'],'unique':True }]
	}

	def Save(self):
		try:
			self.save()
			return True	
		except Exception as e:
			logger.debug('Exception in Saving the orders'+str(e))
			return False		

class OrderOperations():
	
	def FindOrderDetails(self, order_id):
		try:
			order = Order.objects(order_id = order_id)
			if len(order) == 1:
				order = order.first()
				order_details = {}
				order_details['order_id'] = order_id
				order_details['product_id'] = order.product_id
				order_details['user_id'] = order.user_id
				order_details['date'] = order.date
				order_details = json.dumps(order_details)
				return order_details
			logger.debug('Not a valid order id')	
			return False
		except Exception as e:
			logger.debug('Excpetion in FIndorderDetails method')
			raise e
			return False

	def FindUserOrders(self,user_id):
		try:
			orders = Order.objects(user_id = user_id)
			if len(orders) == 0:
				logger.debug('Not a valid user_id or not orders with this user_id')
				return False	
			result = []
			for	order in orders:
				order_details = {}
				order_details['order_id'] = order.order_id
				order_details['product_id'] = order.product_id
				order_details['user_id'] = order.user_id
				order_details['date'] = str(order.date)
				result.append(order_details)
			result = json.dumps(result)
			return result
		except Exception as e:
			logger.debug('Exception in findingallorders')
			raise e
			return False					


