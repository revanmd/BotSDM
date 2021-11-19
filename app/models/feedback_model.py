import pymongo
import pprint
import time
import datetime
from datetime import timedelta
from pymongo import MongoClient
from bson import ObjectId


class feedback:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db_feedback = client['sdm_rule_bot']['feedback_form']
		self.db_label_feedback = client['sdm_rule_bot']['label_feedback']

	##LABEL feedback

	def check_label(self,label):
		cek = self.db_label_feedback.find_one({'label':label})
		if cek == None:
			return True
		else:
			return False 

	def add_label(self,label):
		if self.check_label(label):
			data = {
				'label':label
			}
			oid = self.db_label_feedback.insert_one(data).inserted_id
			if oid != None:
				return True
			else:
				return False
		else:
			return False

	def get_label(self):
		document = self.db_label_feedback.find({},{'_id': False})
		return list(document)

	## END LABEL feedback

	def add_label_feedback(self,id_str,label):
		oid = ObjectId(id_str)
		doc = self.db_feedback.find_one_and_update(
			{'_id':oid},
			{'$set':
				{'target':label}
			},upsert=True
		)
		if doc != None:
			return True
		else:
			return False

	def get_closed_feedback(self,limit):
		document = self.db_feedback.find({'target':{'$exists':True}},{'_id': False}).sort([('timestamp', 1)]).limit(limit)
		return list(document)

	def filter_feedback(self,label):
		document = self.db_feedback.find({'target':label},{'_id': False}).sort([('timestamp', 1)])
		return list(document)
