import pymongo
import pprint
import time
import datetime
from pymongo import MongoClient


class history:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db_history_option = client['sdm_rule_bot']['history_option']
		self.db_history_question = client['sdm_rule_bot']['history_question']

	def current_month_timestamp(self):
		s = datetime.date.today().replace(day=1)
		s = datetime.datetime.strptime(str(s),"%Y-%m-%d")
		s = datetime.datetime.timestamp(s)
		return s

	def current_year_timestamp(self):
		s = datetime.date.today().replace(day=1,month=1)
		s = datetime.datetime.strptime(str(s),"%Y-%m-%d")
		s = datetime.datetime.timestamp(s)
		return s

	def insert_option(self, dari):
		ts = time.time()
		data = {
			'timestamp':ts,
			'dari':dari
		}
		oid = self.db_history_option.insert_one(data).inserted_id
		if oid != None:
			return True
		else:
			return False

	def insert_question(self,question,label):
		ts = time.time()
		data = {
			'timestamp':ts,
			'question':question,
			'label':label
		}
		oid = self.db_history_question.insert_one(data).inserted_id
		if oid != None:
			return True
		else:
			return False

	def count_option_by_month(self):
		month_timestamp = self.current_month_timestamp()
		ct = self.db_history_option.count_documents({'timestamp':{'$gt':month_timestamp}})
		return ct

	def count_option_by_year(self):
		year_timestamp = self.current_year_timestamp()
		ct = self.db_history_option.count_documents({'timestamp':{'$gt':year_timestamp}})
		return ct

	def count_question_by_month(self):
		month_timestamp = self.current_month_timestamp()
		ct = self.db_history_question.count_documents({'timestamp':{'$gt':month_timestamp}})
		return ct

	def count_question_by_year(self):
		year_timestamp = self.current_year_timestamp()
		ct = self.db_history_question.count_documents({'timestamp':{'$gt':year_timestamp}})
		return ct

	def get_question_limit(self,limit):
		document = self.db_history_question.find({},{'_id': False}).sort([('timestamp', 1)]).limit(limit) 
		result = []
		for item in document:
			result.append(item)
		return result

if __name__ == '__main__':
	history = history()
	print(history.get_question_limit(10))


