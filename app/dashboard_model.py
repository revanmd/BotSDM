import pymongo
import pprint
import time
import datetime
from datetime import timedelta
from pymongo import MongoClient


class dashboard:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db_history_option = client['sdm_rule_bot']['history_option']
		self.db_history_question = client['sdm_rule_bot']['history_question']
		self.db_feedback_form = client['sdm_rule_bot']['feedback_form']

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

	def prev_month_timestamp(self):
		s = datetime.date.today().replace(day=1)
		s = s - timedelta(days=1)
		s = s.replace(day=1)
		s = datetime.datetime.strptime(str(s),"%Y-%m-%d")
		s = datetime.datetime.timestamp(s)
		return s

	def prev_year_timestamp(self):
		s = datetime.date.today().replace(day=1,month=1)
		s = s - timedelta(days=1)
		s = s.replace(day=1,month=1)
		s = datetime.datetime.strptime(str(s),"%Y-%m-%d")
		s = datetime.datetime.timestamp(s)
		return s

	def total_faq_by_month(self,flag='current'):
		month_timestamp = 0
		ct = 0
		if flag == 'current':
			month_timestamp = self.current_month_timestamp()
			ct = self.db_history_option.count_documents({'timestamp':{'$gt':month_timestamp}})
		elif flag == 'prev':
			current_month = self.current_month_timestamp()
			prev_month = self.prev_month_timestamp()
			ct = self.db_history_option.count_documents({'timestamp':{'$gt':current_month,'$lt':prev_month}})
		return ct

	def total_faq_by_year(self,flag='current'):
		month_timestamp = 0
		ct = 0
		if flag == 'current':
			month_timestamp = self.current_year_timestamp()
			ct = self.db_history_option.count_documents({'timestamp':{'$gt':month_timestamp}})
		elif flag == 'prev':
			current_month = self.current_year_timestamp()
			prev_month = self.prev_year_timestamp()
			ct = self.db_history_option.count_documents({'timestamp':{'$gt':current_month,'$lt':prev_month}})
		return ct

	def total_rasa_by_month(self,flag='current'):
		month_timestamp = 0
		ct = 0
		if flag == 'current':
			month_timestamp = self.current_month_timestamp()
			ct = self.db_history_question.count_documents({'timestamp':{'$gt':month_timestamp}})
		elif flag == 'prev':
			current_month = self.current_month_timestamp()
			prev_month = self.prev_month_timestamp()
			ct = self.db_history_question.count_documents({'timestamp':{'$gt':current_month,'$lt':prev_month}})
		return ct

	def total_rasa_by_year(self, flag='current'):
		month_timestamp = 0
		ct = 0
		if flag == 'current':
			month_timestamp = self.current_year_timestamp()
			ct = self.db_history_question.count_documents({'timestamp':{'$gt':month_timestamp}})
		elif flag == 'prev':
			current_month = self.current_year_timestamp()
			prev_month = self.prev_year_timestamp()
			ct = self.db_history_question.count_documents({'timestamp':{'$gt':current_month,'$lt':prev_month}})
		return ct

	def percent_faq(self):
		current = self.total_faq_by_month('current')
		prev = self.total_faq_by_month('prev')

		if prev == 0:
			return 100
		else:
			selisih = current - prev
			kenaikan = selisih / prev
			kenaikan *= 100
			return kenaikan

	def percent_rasa(self):
		current = self.total_rasa_by_month('current')
		prev = self.total_rasa_by_month('prev')

		if prev == 0:
			return 100
		else:
			selisih = current - prev
			kenaikan = selisih / prev
			kenaikan *= 100
			return kenaikan

	def total(self, flag='all'):
		if flag == 'all':
			faq = self.db_history_option.count_documents({})
			rasa = self.db_history_question.count_documents({})
			return rasa + faq

		elif flag == 'current':
			current_year = self.current_year_timestamp()
			faq = self.db_history_option.count_documents({'timestamp':{'$gt':current_year}})
			rasa = self.db_history_question.count_documents({'timestamp':{'$gt':current_year}})
			return rasa + faq

		elif flag == 'prev':
			current_year = self.current_year_timestamp()
			prev_year = self.prev_year_timestamp()
			faq = self.db_history_option.count_documents({'timestamp':{'$gt':current_year,'$lt':prev_year}})
			rasa = self.db_history_question.count_documents({'timestamp':{'$gt':current_year,'$lt':prev_year}})
			return rasa + faq

	def total_dikenali(self):
		dikenali = self.db_history_question.count_documents({'label':'berhasil'})
		return dikenali

	def total_gagal_dikenali(self):
		gagal = self.db_history_question.count_documents({'label':'gagal'})
		return gagal

	def latest_message(self,limit):
		document = self.db_history_question.find({},{'_id': False}).sort([('timestamp', 1)]).limit(limit) 
		result = []
		for item in document:
			item['timestamp'] = datetime.datetime.fromtimestamp(item['timestamp'])
			result.append(item)
		return result

	def latest_feedback(self,limit):
		document = self.db_feedback_form.find({},{'_id': False}).sort([('timestamp', 1)]).limit(limit) 
		result = []
		for item in document:
			item['timestamp'] = datetime.datetime.fromtimestamp(item['timestamp'])
			result.append(item)
		return result

	def data_dashboard(self):
		return {
			'total_faq_month': self.total_faq_by_month('current'),
			'total_rasa_month': self.total_rasa_by_month('current'),
			'total_faq_prevmonth': self.total_faq_by_month('prev'),
			'total_rasa_prevmonth': self.total_rasa_by_month('prev'),
			'percent_faq':self.percent_faq(),
			'percent_rasa':self.percent_rasa(),
			'total_all':self.total('all'),
			'total_current':self.total('current'),
			'total_prev':self.total('prev'),
			'total_dikenali':self.total_dikenali(),
			'total_gagal':self.total_gagal_dikenali()
		}




if __name__ == '__main__':
	mod = dashboard()

	pprint.pprint(mod.latest_message(5))

	"""
	TEST Data Dashboard
	print("FAQ by month",mod.total_faq_by_month('current'))
	print("FAQ by year",mod.total_faq_by_year('current'))
	print("Rasa by month",mod.total_rasa_by_month('current'))
	print("Rasa by year",mod.total_rasa_by_year('current'))
	print("Presentase kenaikan FAQ",mod.percent_faq())
	print("Presentase kenaikan RASA",mod.percent_rasa())
	print("total",mod.total('all'))
	print("total tahun ini",mod.total('current'))
	print("total tahun kemarin",mod.total('prev'))
	print("jumlah dikenali",mod.total_dikenali())
	print("jumlah gagal dikenali",mod.total_gagal_dikenali())
	"""




