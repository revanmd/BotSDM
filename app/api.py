from flask import Blueprint,request, jsonify, make_response, render_template, session
from flask import current_app as app
from flask_cors import cross_origin
from .model import model
from .history_model import history
import requests

api = Blueprint('api',__name__)
rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"
model = model()
history = history()

def rasa_handler(message):
	res = requests.post(rasa_endpoint,json={'message':stopwords_removal(message.lower())})
	out = ""
	if res.status_code == 200:
		for item in res.json():
			out += item['text']
	return out

def stopwords_removal(message):
	stopwords = ['ada', 'agak', 'aku', 'apa', 'bagaimana', 'bantu', 'berapa', 'cara', 'dapat', 'dari', 'dia', 'dimana', 'hal', 'harap', 'harus', 'ia', 'ini', 'itu', 'juga', 'kah', 'kami', 'kapan', 'kenapa', 'kita', 'lagi', 'masih', 'melalui', 'mengapa', 'menggunakan', 'mereka', 'minta', 'mohon', 'oleh', 'saja', 'saya', 'secara', 'sedang', 'siapa', 'terus', 'tolong', 'untuk', 'yang']
	temp = []
	for item in message.split(' '):
		if item not in stopwords:
			temp.append(item)
	return ' '.join(temp)

@api.route('',methods=['post'])
def main_handler():
	json_from_react = request.get_json()
	message = json_from_react['msg']
	output = {
		'message':rasa_handler(message)
	}

	#Simpan hasil sebagai history
	label = ""
	if output['message'] == "Maaf kami tidak mengerti apa maksud anda.!menu":
		label = "gagal"
	else:
		label = "berhasil"
	history.insert_question(message,label)

	return jsonify(output)

@api.route('option',methods=['get'])
def option_handler():
	kelas = request.args.get('kelas')
	level = request.args.get('level')
	dari = request.args.get('dari')
	label = request.args.get('label')
	data = []
	if None not in [kelas,level,dari,label]:
		if dari == ""	:
			path = dari+label
			path = path.replace("'",'')
		else:	
			path = dari+'-'+label
		
		if int(kelas) != 0:
			data = model.get_item(int(kelas),int(level),str(path))
		else:
			data = model.get_item(int(label),1,"")
	else:
		data = model.get_item(0,0,"")

	if len(data) == 1:
		history.insert_option(data[0]['dari'])

	return jsonify(data)

@api.route('masukan',methods =['GET','POST'])
def masukan_handler():
	output = {
		'message':rasa_handler('beri masukan dan kendala')
	}
	return jsonify(output)

@api.route('prototype',methods=['get'])
def admin_handler():
	return render_template('prototype.html')

@api.route('iam',methods=['get'])
def iam_handler():
	return render_template('iam.html')

@api.route('mobile',methods=['get'])
def mobile_handler():
	return render_template('mobile.html')