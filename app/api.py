from flask import Blueprint,request, jsonify, make_response, render_template, session
from flask import current_app as app
from flask_cors import cross_origin
import re

# Import Model Here
from .models.model import model
from .models.history_model import history
from .models.dashboard_model import dashboard
from .models.pertanyaan_model import pertanyaan
from .models.feedback_model import feedback
# End Import Model

import requests
import html

api = Blueprint('api',__name__)
rasa_endpoint = "http://localhost:5005/webhooks/rest/webhook"
model = model()
history = history()
dashboard = dashboard()
pertanyaan = pertanyaan()
feedback = feedback()

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

@api.route('treeview',methods=['get'])
def treeview_handler():
	parent = model.get_item(1,1,'')
	tempo = []
	for item in parent:
		data = {
			'text':item['message'],
			'nodes':[]
		}
		tempo.append(data)
		model.recursive(item,2,tempo,data['nodes'])

	return render_template('bstreeview.html',rule= tempo)

@api.route('getrule',methods=['get'])
def getrule_handler():
	root = model.get_item(0,0,'')
	kelas = []
	tree_id = []
	result = {}
	for i in root:
		kelas.append(i['label'])
		parent = model.get_item(i['label'],1,'')
		tempo = []
		for item in parent:
			item['message'] = html.escape(item['message'])
			func_editmenu = "editSubMenu({},{},'{}',{},'{}')".format(item['kelas'],item['level'],item['dari'],item['label'],item['message'])
			func_deletemenu = "deleteSubMenu({},{},'{}',{},'{}')".format(item['kelas'],item['level'],item['dari'],item['label'],item['message'])
			func_addmenu = "addSubMenu({},{},'{}',{},'{}')".format(item['kelas'],item['level'],item['dari'],item['label'],item['message'])
			
			html_data = item['message']+"<button class='button-tree-edit' onclick='"+html.escape(func_editmenu)+"'> <i class='fa fa-pencil' aria-hidden='true'></i></button> <button class='button-tree-delete' onclick='"+html.escape(func_deletemenu)+"'> <i class='fa fa-trash-o' aria-hidden='true'></i></button><button class='button-tree-add' onclick='"+html.escape(func_addmenu)+"'> <i class='fa fa-plus' aria-hidden='true'></i></button>"
			data = {
				'text':html_data,
				'nodes':[]
			}
			tempo.append(data)
			model.recursive(item,2,tempo,data['nodes'])

		result['tree'+str(i['label'])] = tempo
		tree_id.append('tree'+str(i['label']))

	result['kelas'] = kelas
	result['root'] = root
	result['tree_id'] = tree_id

	return jsonify(result);

@api.route('editsubrule',methods=['post'])
def editsubrule_handler():
	json = request.get_json()
	kelas_parent = json['kelas_parent']
	level_parent = json['level_parent']
	dari_parent = json['dari_parent']
	label_parent = json['label_parent']
	new_message = json['new_message']
	status = model.edit_rule(kelas_parent,level_parent,dari_parent,label_parent,new_message)
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('deletesubrule',methods=['post'])
def deletesubrule_handler():
	json = request.get_json()
	kelas_parent = json['kelas_parent']
	level_parent = json['level_parent']
	dari_parent = json['dari_parent']
	label_parent = json['label_parent']

	status = model.delete_sub_rule(kelas_parent,level_parent,dari_parent,label_parent)
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('appendsubrule',methods=['post'])
def appendsubrule_handler():
	json = request.get_json()
	kelas_parent = json['kelas_parent']
	level_parent = json['level_parent']
	dari_parent = json['dari_parent']
	label_parent = json['label_parent']
	new_message = json['new_message']
	status = model.append_new_rule(kelas_parent,level_parent,dari_parent,label_parent,new_message)
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('appendmainrule',methods=['post'])
def appendmainrule_handler():
	json = request.get_json()
	new_message = json['new_message']
	status = model.append_main_rule(new_message)
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('deletemainrule',methods=['post'])
def deletemainrule_handler():
	json = request.get_json()
	label = int(json['del_label'])
	status = model.delete_sub_rule(0,0,'',label)
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('dashboard',methods=['get'])
def dashboard_handler():
	data = dashboard.data_dashboard()
	pesan = dashboard.latest_message(10)
	feedback = dashboard.latest_feedback(5)

	return jsonify({
		'data':data,
		'pesan':pesan,
		'feedback':feedback
	})

@api.route('daftarpertanyaan',methods=['get'])
def daftarpertanyaan_handler():
	total_rasa = dashboard.total_rasa()
	dikenali = dashboard.total_dikenali()
	gagal = dashboard.total_gagal_dikenali()
	pesan = dashboard.latest_message(200)

	return jsonify({
		'total_rasa':total_rasa,
		'dikenali':dikenali,
		'gagal':gagal,
		'pesan':pesan
	})
@api.route('daftarmasukan',methods=['get'])
def daftarmasukan_handler():
	total_masukan = dashboard.total_masukan()
	total_current_year = dashboard.total_masukan_by_year('current')
	total_prev_year = dashboard.total_masukan_by_year('prev')
	total_current_month = dashboard.total_masukan_by_month('current')
	total_prev_month = dashboard.total_masukan_by_month('prev')

	masukan = dashboard.latest_feedback(200)

	return jsonify({
		'total_masukan':total_masukan,
		'total_current_year':total_current_year,
		'total_prev_year':total_prev_year,
		'total_current_month':total_current_month,
		'total_prev_month':total_prev_month,
		'masukan':masukan
	})

@api.route('labeling_question',methods=['post'])
def labeling_question_handler():
	json = request.get_json()
	status = pertanyaan.add_label_pertanyaan(json['id'],json['label'])
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}

	return jsonify(data)

@api.route('labeling_feedback',methods=['post'])
def labeling_masukan_handler():
	json = request.get_json()
	status = feedback.add_label_feedback(json['id'],json['label'])
	data = {'status':'failed'}
	if status :
		data = {
			'status':'success'
		}
	return jsonify(data)

@api.route('getlabelpertanyaan',methods=['get'])
def getlabelpertanyaan_handler():
	label = pertanyaan.get_label()
	return jsonify(label)

@api.route('getlabelmasukan',methods=['get'])
def getlabelmasukan_handler():
	label = feedback.get_label()
	return jsonify(label)

@api.route('getchartfeedback',methods=['get'])
def getchartfeedback_handler():
	chart = dashboard.chart_feedback()
	return jsonify(chart)

@api.route('getclosedfeedback',methods=['get'])
def getclosedfeedback_handler():
	closed_feedback = feedback.get_closed_feedback(500);
	return jsonify(closed_feedback)

@api.route('filterfeedback',methods=['post'])
def filterfeedback_handler():
	json = request.get_json()
	filtered_data = feedback.filter_feedback(json['label'])
	return jsonify(filtered_data)

