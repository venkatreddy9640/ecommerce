from flask_mongoengine import MongoEngine
from mongoengine.errors import NotUniqueError
from logger import get_logger
import json

db = MongoEngine()

logger = get_logger('users.log')

class User(db.Document):
	name = db.StringField()
	password = db.StringField()
	user_id = db.StringField()
	products_list = db.ListField()
	location = db.DictField()
	phone = db.StringField()
	email = db.StringField()
	meta = {
	    'indexes':[{'fields':['-user_id'],'unique':True }]
	}

	def Save(self):
		try:
			self.save()
			return 'Done'
		except NotUniqueError:
			return 'Duplicates'
		except Exception as e:
			return 'Failed'	

class UserOperations():

	def finduser(self, this_user_id):
		user = User.objects(user_id=this_user_id)
		if len(user) == 0:
			logger.debug('No user found with user_id '+this_user_id)
			return False
		elif len(user) == 1:
			logger.debug('User_id '+this_user_id+'Logged in')
			return True
		else:
			logger.debug('Multiple users with same user_id'+user_id)
			return None

	def Update(self, this_user_id, data):
		try:
			user = User.objects(user_id = this_user_id).first()
			print user.name
			for key in data:
				user[key]=data[key]
			user.Save()
			logger.debug('User '+user_id+'has updated details and details are '+str(data))
			return True
		except Exception as e:
			logger.debug('Exception occured while updating the user details of user '+ user_id)
			raise e
			return None	

	
	def RemoveUser(self, this_user_id):
		try:
			user = User.objects(user_id = this_user_id).first()
			user.delete()
			logger.debug('User '+user_id+' deleted Successfully')
			return True
		except Exception as e:
			logger.debug('Exception occured in removing user  '+user_id)
			raise e
			return None	

	def UpdateProductsList(self, this_user_id, products):
		try:
			user = User.objects(user_id = this_user_id).first()
			user.products_list.append(products)
			user.save()
			return True
		except Exception as e:
			print e
			logger.debug('Exception occured in updatingproducts method ')
			raise e
			return None	

	def ViewUsers(self):
		try:
			users = User.objects()
			user_ids = []
			for user in users:
				user_ids.append(user.user_id)
			user_ids = json.dumps(user_ids)
			logger.debug(user_ids)	
			return user_ids
			return True
		except Exception as e:
			logger.debug('Exception occured in view users method')
			raise e
			return None	

