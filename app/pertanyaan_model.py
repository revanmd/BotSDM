import pymongo
import pprint
import time
import datetime
from datetime import timedelta
from pymongo import MongoClient
from bson import ObjectId


class pertanyaan:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db_pertanyaan = client['sdm_rule_bot']['history_question']
		self.db_label_question = client['sdm_rule_bot']['label_question']

	##LABEL PERTANYAAN

	def check_label(self,label):
		cek = self.db_label_question.find_one({'label':label})
		if cek == None:
			return True
		else:
			return False 

	def add_label(self,label):
		if self.check_label(label):
			data = {
				'label':label
			}
			oid = self.db_label_question.insert_one(data).inserted_id
			if oid != None:
				return True
			else:
				return False
		else:
			return False

	def get_label(self):
		document = self.db_label_question.find({},{'_id': False})
		return list(document)

	## END LABEL PERTANYAAN

	def add_label_pertanyaan(self,id_str,label):
		oid = ObjectId(id_str)
		doc = self.db_pertanyaan.find_one_and_update(
			{'_id':oid},
			{'$set':
				{'target':label}
			},upsert=True
		)
		if doc != None:
			return True
		else:
			return False
			


if __name__ == '__main__':
	model = pertanyaan()
	print(model.add_label('Asuransi Kesehatan'))
	print(model.add_label('BPJS'))
	print(model.add_label('Absensi'))
	pprint.pprint(model.add_label_pertanyaan('618a1d6bf8be92d88062a602','Reschedule Pesanan'))