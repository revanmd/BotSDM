import pymongo
import pprint
from pymongo import MongoClient
import time
import datetime

class model:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db = client['sdm_rule_bot']

	def insert_feedback(self,message):
		data = {
			'message':message,
			'timestamp':time.time()
		}
		oid = self.db['feedback_form'].insert_one(data).inserted_id
		if oid != None:
			return True
		else:
			return False