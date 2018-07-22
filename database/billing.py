from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError
from logger import get_logger
import json

db = MongoEngine()

logger = get_logger('billing.log')

class Billing(db.Document):
	billing_id = db.IntField()
	billing_price = db.IntField()
	billing_date = db.DateTimeField()
	billing_details = db.DictField()

	def Save(self):
		try:
			print 'reached here'
			self.save()
			return True
		except Exception as e:
			print e
			logger.debug('Failed in generatig field')
			return False





