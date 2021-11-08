import pymongo
import pprint
from pymongo import MongoClient

class model:
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.db = client['sdm_rule_bot']['rule_table']


	def rule_template(self,kelas,level,dari,label,message):
		data = {
			'kelas':kelas,
			'level':level,
			'dari':dari,
			'label':label,
			'message':message
		}
		return data

	def get_all(self):
		data = self.db.find({},{'_id':0})
		temp = []
		for item in data:
			temp.append(item)
		return temp

	def add_rule(self,kelas,level,dari,label,message):
		data = self.db.find_one({'kelas':kelas,'level':level,'label':label,'dari':dari})
		if data == None:
			data = self.rule_template(kelas,level,dari,label,message)
			oid = self.db.insert_one(data).inserted_id

			if oid != None:
				return True
			else:
				return False
		else:
			return False

	def clear_rule(self):
		return self.db.delete_many({})

	def seed_rule_hotel(self):
		self.add_rule(1,1,'',1,"Pengajuan Dinas")
		self.add_rule(1,1,'',2,"Laporan Dinas")
		self.add_rule(1,1,'',3,"Transportasi Dinas")
		self.add_rule(1,1,'',4,"Hotel Dinas")

		self.add_rule(1,2,'1',1,"Menu ini masih dalam pengembangan")
		self.add_rule(1,2,'2',1,"Menu ini masih dalam pengembangan")
		self.add_rule(1,2,'3',1,"Menu ini masih dalam pengembangan")

		self.add_rule(1,2,'4',1,"Cara Pesan Hotel")
		self.add_rule(1,2,'4',2,"Cek Budget Hotel")
		self.add_rule(1,2,'4',3,"Reschedule / Pembatalan Pemesanan")
		self.add_rule(1,2,'4',4,"Pertanyaan Lain")

		self.add_rule(1,3,'4-1',1,"Dipesankan Perusahaan")
		self.add_rule(1,3,'4-1',2,"Pesan Sendiri")

		self.add_rule(1,4,'4-1-1',1,"Cek Hotel Kerja Sama")
		self.add_rule(1,4,'4-1-1',2,"Cara Pesan Hotel")

		temp = """
		1. 	Buka web https://v2.corporateroomdeal.com.
		2. 	Login dengan : 
	     	Corporate ID : pusri
	     	username : pusri1
	     	password : Pusri2021 
		3. 	Setelah berhasil login, lalu ketik nama hotel yang dipesan, pilih tanggal check in dan tanggal check out. pilih grade karyawan lalu pilih CARI
		"""
		self.add_rule(1,5,'4-1-1-1',1,temp)

		temp = """
		1.	Pemesanan melalui email ke email ke   reservation3@corporateroomdeal.com dan cc ke adminhotel@pusri.co.id. 
		2.	Format emailnya sebagai berikut :

			Kepada :Tim Reservasi CRD. 
			Untuk dibantu pesankan hotel dengan rincian sbb :
			Nama hotel:
			Nama Tamu :
			Tgl Check in :
			Tgl Check out:
			Grade :
			Cost Center : 

		3.  Tunggu email konfirmasi pemesanan (bukan voucher hotel) dr email corporateroomdeal, lalu pastikan detail pemesanan sudah sesuai. 
		4. 	Jika sudah ok, lalu silahkan membalas email tersebut dengan keterangan 'Pemesanan sudah sesuai, agar dapat diterbitkan vouchernya'.
		5. 	Setelah ada konfirmasi ok voucher untuk diterbikan, tim CRD akan mengirimkan voucher hotelnya. 
		6. 	Harap untuk tidak melakukan check in/datang ke hotel jika voucher belum terima. 

		No. WA reservasi CRD : 0812 9288 8282
		"""
		self.add_rule(1,5,'4-1-1-2',2,temp)

		temp = """
		1.	Tiap karyawan yang dinas dapat melakukan pemesanan sendiri, dengan memperhatikan budgetnya.
		2.	Pembayarannya diproses pada saat laporan dinas (reiumburse) atau pada saat pengajuan travel request jika ada pemesanan lainnya
		3. 	Cek Budget Hotel
		"""
		self.add_rule(1,4,'4-1-2',1,temp)

		#Badge
		self.add_rule(1,3,'4-2',1,"Fitur ini masih dalam pengembangan")

		self.add_rule(1,3,'4-3',1,"Jadwal kegiatan dinas batal")
		self.add_rule(1,3,'4-3',2,"Kegiatan dinas lebih cepat selesai")
		self.add_rule(1,3,'4-3',3,"Kegiatan dinas diperpanjang")

		self.add_rule(1,4,'4-3-1',1,"Pemesanan Perusahaan")
		self.add_rule(1,4,'4-3-1',2,"Pemesanan Sendiri")

		self.add_rule(1,5,'4-3-1-1',1,"Pembatalan")	
		self.add_rule(1,5,'4-3-1-1',2,"Reschedule")

		temp = """
		1. 	Pembatalan melalui email  ke reservation3@corporateroomdeal.com dan cc ke adminhotel@pusri.co.id. Dengan melampirkan voucher hotelnya
		2. 	Format email sebagai berikut :

			Untuk dibantu pembatalan hotel dengan rincian sbb :    
			Nama hotel:
			Nama Tamu :
			Tgl Pemesanan :
			Alasan Pembatalan :

		3.	Jika pembatalan berhasil tanpa dikenakan biaya maka tidak perlu membuat surat pembatalan
		4.	Jika voucher tidak dibatalkan seluruh/sebagian maka perlu membuat surat pembatalan ke VP Ketenagekerjaan dengan menjelaskan alasan pembatalan serta cost center pembebanan pembatalan
		"""
		self.add_rule(1,6,'4-3-1-1-1',1,temp)

		temp = """
		1. 	Reschedule melalui email  ke reservation3@corporateroomdeal.com dan cc ke adminhotel@pusri.co.id. Dengan melampirkan voucher hotelnya
		2. 	Format email sebagai berikut :

			Untuk dibantu pembatalan hotel dengan rincian sbb :    
			Nama hotel:
			Nama Tamu :
			Tgl Pemesanan Awal :
			Tgl Perubahan :
			Alasan Reschedule :

		3. 	Jika Reschedule berhasil tanpa dikenakan biaya maka tidak perlu membuat surat reschedulu
		4. 	Jika voucher tidak dapat direschedulu maka perlu membuat surat pembatalan ke VP Ketenagekerjaan dengan menjelaskan alasan reschedule serta cost center pembebanan reschedule
		"""
		self.add_rule(1,6,'4-3-1-1-2',1,temp)

		temp = """
		1.	Silahkan melalukan pembatalan/reschedule mandiri
		2.	Jika terdapat biaya pembatalan/reschedule maka silahkan membuatkan surat kronologis terkait pembatalan/reschedule dengan menjelaskan alasan dan cost center pembebananya
		"""
		self.add_rule(1,5,'4-3-1-2',1,temp)

		temp = """
		1.	Jika kegiatan dinas lebih cepat selesai voucher tidak bisa dibatalkan, maka dapat dibuatkan surat kronologis pembatalan voucher hotel yang menjelaskan alasan pembatalan serta disebutkan cost center pembebanan voucher hotel yang tidak dapat dibatalkan
		2.	Surat tersebut ditujukan ke VP Ketenagakerjaan
		3.	Surat tersebut juga harus dilampirkan pada laporan dinas yang dikirim ke Dep. Naker
		"""
		self.add_rule(1,4,'4-3-2',1,temp)

		temp = """
		1.	Silahkan melakukan pemesanan lanjutan sesuai dengan hari perpanjangannya
		2.	Misal kegiatan dari tgl 1 Januari s.d 05 Januari 2021, lalu diperpanjang sampai tanggal 07 Januari 2021
		3.	Maka hotel dapat dipesan dari tanggal 05 - 07 Januari 2021
		4.	Pada laporan dinas harus melampirkan surat keterangan perpanjangan dinas ke Dep. Keternagakerjaan
		"""
		self.add_rule(1,4,'4-3-3',1,temp)


	def seed_2(self):
		self.add_rule(0,0,'',1,'Dinas / SPPD')
		self.add_rule(0,0,'',2,'Layanan Kesehatan')

		#tambahan pengembangan masukan dan kendala
		self.add_rule(0,0,'',3,'Masukan dan Kendala')
		self.add_rule(0,0,'3',1,'!masukan')

		self.add_rule(2,1,'',1,'Asuransi Kesehatan')
		self.add_rule(2,1,'',2,'BPJS Kesehatan')
		self.add_rule(2,1,'',3,'Klaim Kacamata')
		self.add_rule(2,1,'',4,'Klaim Autism')
		self.add_rule(2,1,'',5,'Ketentuan Telemedicine')
		self.add_rule(2,1,'',6,'Pendaftaran Keluarga')
		self.add_rule(2,1,'',7,'Kartu BPJS / Asuransi Hilang')

		#bagian anak dari asuransi kesehatan
		self.add_rule(2,2,'1',1,'Rincian Prosedur Asuransi Ramayana')
		self.add_rule(2,2,'1',2,'Daftar Provider Asuransi Ramayana')
		self.add_rule(2,2,'1',3,'Biaya Kesehatan Yang di-Reimburse')
		self.add_rule(2,2,'1',4,'Tata Cara Reimburse ke Asuransi Ramayana')
		self.add_rule(2,2,'1',5,'Kartu Berobat Ramayana Hilang')
		self.add_rule(2,2,'1',6,'Informasi Lainnya')

		self.add_rule(2,3,'1-1',1,'!download https://iam.pusri.co.id/faqkesehatan/download/faq1')
		self.add_rule(2,3,'1-2',1,'!download https://iam.pusri.co.id/faqkesehatan/download/faq2')
		self.add_rule(2,2,'3',1,'!download https://iam.pusri.co.id/faqkesehatan/download/faq11_12')
		self.add_rule(2,2,'4',1,'!download https://iam.pusri.co.id/faqkesehatan/download/faq11_12')

		temp ="""
		1. Jika peserta berobat di luar provider Ramayana tetapi tetap mengikuti prosedur berobat Asuransi Ramayana. Jika tidak sesuai prosedur, tidak dapat direimburse
		   contoh : Misal,karyawan langsung berobat ke dokter spesialis penyakit dalam tanpa ada rujukan dari dokter umum terlebih dahulu, maka biaya tidak dapat direimburse ke Ramayana. 
		   \n
		2. Jika ada obat atau pemeriksaan penunjang yang masuk dalam tanggungan Asuransi Ramayana tapi tidak tersedia di provider Asuransi Ramayana, peserta dapat mengajukan klaim reimburse penggantian ke Asuransi Ramayana.
		   contoh : Misal, vaksinasi anak masuk dalam tanggungan asuransi Ramayana, tapi ketika vaksinasi dilakukan di RS Bunda Palembang, RS tersebut tidak menyediakan vaksinasi untuk provider Ramayana, maka dapat di klaim reimburse \n
		3. Jika peserta rawat inap atau melahirkan dengan jaminan BPJS Kesehatan atau asuransi lain,dapat mengajukan reimburse selisih biaya atau hospital cash plan ke Asuransi Ramayana (silahkan baca kembali Rincian Benefit Prosedur Berobat Asuransi Ramayana) \n
		4. Di luar rincian benefit yang ditanggung Asuransi Ramayana, tidak dapat di-reimburse. 
		"""
		self.add_rule(2,3,'1-3',1,temp)

		#bagian anak dari tata cara reimburse
		self.add_rule(2,3,'1-4',1,'Rawat Jalan')
		self.add_rule(2,3,'1-4',2,'Rawat Inap')
		self.add_rule(2,3,'1-4',3,'Batas Waktu Klaim / Reimburse')
		self.add_rule(2,3,'1-4',4,'Penyerahan Dokumen Pengajuan Reimburse')

		temp = """
		1. Form/lembar keterangan diagnosis dokter atas penyakit dan rekomendasi terapi/pemeriksaan penunjang/tindakan yg dilakukan. Form atau lembar diagnosis ini harus ditanda-tangani dokter ygmerawat. Form diaganosis dapat menggunakan form dari Ramayana. (silahkan download disini) atau dapat menggunakan form yang tersedia di RS atau praktek dokter.
		   \n
		2. Surat rujukan dari dokter umum jika berobat kedokter spesialis , kecuali  5 dokter spesialis (Mata, THT,Obgyn, Anak, Gigi Spesialis) tidak perlu surat rujukan 
		   \n
		3. Kwitansi biaya dokter, jika berobat diluar provider Asuransi Ramayana.
		   \n
		4. Kwitansi biaya pemeriksaan penunjang (lab, rontgen, dll) dan copyhasil dari pemeriksaan penunjang, jika dilakukan diluar provider Asuransi Ramayana. 
		   \n
		5. Copy resep dan kuitansi pembelian obat (jika ada biaya obat yang akan di-reimburse)
		   \n
		6. Copy kartu Asuransi Ramayana
		   \n
		7. Keterangan badge, nomor rekening, nomor Handphone dan email karyawan. 
		"""
		self.add_rule(2,4,'1-4-1',1,temp)
		temp="""
		Dokumen pendukung klaim reimbursement untuk rawat inap, hospital cash plan, dan jenis rincian reimbursement lainnya dapat di-download disini.  
		"""
		self.add_rule(2,4,'1-4-2',1,temp)
		temp = """
		Masa berlaku klaim reimbursement adalah 90 (Sembilan puluh) hari kalender sejak tanggal Kwitansi.
		"""
		self.add_rule(2,4,'1-4-3',1,temp)

		temp ="""
		Dokumen reimbursement dapat dikumpulkan ke loket Departemen Ketenagakerjaan & Hubungan Industrial Atau dikirimkan ke PT. Asuransi Ramayana, Tbk (Unit Askes Ramayana, Jl. Kebon Sirih No. 49, Jakarta 10340)
		"""
		self.add_rule(2,4,'1-4-4',1,temp)

		#bagian anak dari kartu berobat ramayana hilang

		temp = """
		Jika kartu Asuransi Kesehatan hilang, peserta agar melapor ke Departemen Ketenagakerjaan dan Hubungan Industrial dengan membawa surat keterangan hilang darikepolisian dan selanjutnya akan diurus oleh SDM pencetakan kartu baru ke Asuransi
		\n
		 Pusri tidak bertanggung jawab atas tidak dibayarnya klaim reimbursement oleh Asuransi Ramayana akibat benefit yang tidak masuk dalam cakupan perjanjian dan polis, atau pengobatan yang tidak sesuai prosedur asuransi, atau akibat kekurangan dokumen klaim, atau klaim yang sudah melebihi masa berlaku klaim reimburse. 
		"""
		self.add_rule(2,3,'1-5',1,temp)
		temp = """
		 Pusri tidak bertanggung jawab atas tidak dibayarnya klaim reimbursement oleh Asuransi Ramayana akibat benefit yang tidak masuk dalam cakupan perjanjian dan polis, atau pengobatan yang tidak sesuai prosedur asuransi, atau akibat kekurangan dokumen klaim, atau klaim yang sudah melebihi masa berlaku klaim reimburse. 

		"""
		self.add_rule(2,3,'1-6',1,temp)

		#bagian anak dari BPJS
		self.add_rule(2,2,'2',1,'Tata Cara Mengubah Faskes 1')
		self.add_rule(2,2,'2',2,'Kartu BPJS Kesehatan Hilang')

		temp = """
		Download aplikasi JKN Mobile dan daftar sesuai dengan data kepesertaan Anda di BPJS Kesehatan. 
		\n Peserta dapat mengubah Faskes 1 yang diinginkan melalui aplikasi tersebut.
		"""
		self.add_rule(2,3,'2-1',1,temp)

		temp = """
		Jika kartu BPJS Kesehatan hilang, peserta dapat mencetak sendirie-card melalui aplikasi JKN Mobile atau dapat meminta untuk dicetak ulang oleh Departemen Ketenagakerjaan dan Hubungan Industrial dengan membawa surat keterangan kehilangan kartu BPJS Kesehatan dari kepolisian. 
		"""
		self.add_rule(2,3,'2-2',1,temp)

		self.add_rule(2,2,'3',1,'Plafon')
		self.add_rule(2,2,'3',2,'Jangka Waktu')
		self.add_rule(2,2,'3',3,'Tata Cara')

		temp = """
		Biaya penggantian kacamata maksimal sebesar Rp. 500.000,- (Frame Rp. 200.000,- Lensa Rp. 300.000,-)
		"""
		self.add_rule(2,3,'3-1',1,temp)

		temp = """
		Untuk pekerja diberikan 2 tahun sekali dan untuk keluarga pekerja diberikan 3 tahun sekali dari pengajuan klaim sebelumnya (sesuai data klaim di sistem ESS)
		"""
		self.add_rule(2,3,'3-2',1,temp)

		temp = """
		Untuk pekerja diberikan 2 tahun sekali dan untuk keluarga pekerja diberikan 3 tahun sekali dari pengajuan klaim sebelumnya (sesuai data klaim di sistem ESS)

		"""
		self.add_rule(2,3,'3-3',1,temp)

		#Bagian klaim autism belum ada

		#Bagian ketentuan telemedicine
		self.add_rule(2,2,'5',1,'Ketentuan')
		self.add_rule(2,2,'5',2,'Dokumen yang dibutuhkan')

		temp = """
		1. Metode klaim adalah dengan cara reimbursement dengan biaya pengobatan telemedicine maksimal Rp. 1.000.000,- (satujuta rupiah).
		2. Hanya bisa untuk pengobatan di Rumah Sakit yang menyelenggarakan telemedicine. 
		3. Prosedur pengobatan adalah berjenjang (melalui dokter umum terlebih dahulu, kecuali 5 dokter spesialis tanpa rujukan : Anak, Mata, THT, Obgyn dan Gigi Spesialis)
		4. Jika pengobatan langsung ke dokter spesialis, maka biaya dokter akan diganti sesuai dengan biaya dokter umum. 
		"""
		self.add_rule(2,3,'5-1',1,temp)
		temp = """
		• Bukti SMS/WA pendaftaran (registrasi) ke RumahSakit yang resmi menyelenggarakan layanan berbasis digital. 
		• Bukti SMS/WA Konsultasi dan pemberian resep oleh dokter dan tercantum Nomor Medical Record (nomor pendaftaran) Peserta.
		• Copy kartu Peserta
		• Keterangan badge, nomor rekening, nomor HP dan email karyawan
		\n
		Dokumen reimbursement dapat dikumpulkan keloket Departemen Ketenagakerjaan &Hubungan Industrial Atau dikirimkan ke PT. Asuransi Ramayana, Tbk(Unit Askes Ramayana, Jl. Kebon Sirih No. 49, Jakarta 10340

		"""
		self.add_rule(2,3,'5-2',1,temp)

		#Bagian pendaftaran anggota keluarga
		self.add_rule(2,2,'6',1,'Suami atau Istri')
		self.add_rule(2,2,'6',2,'Anak')
		self.add_rule(2,2,'6',3,'Pengumpulan Dokumen')
		self.add_rule(2,2,'6',4,'Aktivasi Kepesertaan')


		self.add_rule(2,3,'6-1',1,'Cara Pendaftaran')
		self.add_rule(2,3,'6-1',2,'Ketentuan Pendaftar')
		temp = """
		Daftar istri/suami melalui ESS (Employee Self Service – Life Events – Anggota Keluarga) attach dokumen pendaftaran pernikahan.  (DOWLOAD FORMULIR PENDAFTARAN PERNIKAHAN DISINI)

		"""
		self.add_rule(2,4,'6-1-1',1,temp)

		temp = """
		1. Jika istri/suami sudah terdaftar sebagai peserta BPJS Kesehatan Badan Usaha lain (di tempat suami/istri bekerja), 
		Mohon agar dapat menyertakan informasi tersebut saat mengumpulkan KK dan menyampaikan copy kartu BPJS Kesehatan istri/suami. 
		\n
		2. Jika istri/suami sudah terdaftar di BPJS Kesehatan sebagai peserta mandiri agar dapat dialihkan menjadi tanggungan Pusri, 
		Maka terlebih dahulu harus membayar lunas iuran BPJS Kesehatannya. Copy kartu BPJS Kesehatan dan Bukti pelunasaniuran BPJS Kesehatan agar disertakan saat mengumpulkan KK.  
		\n
		3. Jika istri/suami berhenti dari tempat kerjanya agar dapat dialihkan menjadi tanggungan Pusri, 
		Mengumpulkan KK Gabung, Copy BPJS Istri/suami dan Surat Keterangan Berhenti Kerja ke Bag. PRK &PascaKerja atau dapat melalui email sekdepnaker@pusri.co.id. Beri keterangan data badge, nama karyawan, alamat email dan nomor handphone karyawan saat mengumpulkan dokumen. 
		"""
		self.add_rule(2,4,'6-1-2',1,temp)

		self.add_rule(2,3,'6-2',1,'Cara Pendaftaran')
		self.add_rule(2,3,'6-2',2,'Ketentuan Pendaftar')

		temp = """
		Daftar anak yang baru lahir melalui ESS (Employee Self Service – Life Events – Anggota Keluarga) dan attach Surat Keterangan Lahir di ESS.
		"""
		self.add_rule(2,4,'6-2-1',1,temp)

		temp = """
		Anak dengan usia< 30 hari jika mau berobat/ imunisasi dan belum mendapatkan kartu Ramayana, maka dapat menggunakan kartu ibunya. Jika berumur> 30 hari agar mengkonfirmasi ke PIC Ramayana setiap kali akan berobat/imunisasi untuk dibuka kan akses ke Rumah Sakit secara manual.      
		"""
		self.add_rule(2,4,'6-2-2',1,temp)

		temp = """
		1. Dokumen asli (hard copy) pendukung pendaftaran agar dikirimkan ke Departemen Ketenagakerjaan. 
		2. Data istri/suami/anak yang dimasukkanke ESS akan di-approve setelah dokumen asli (hard copy)pendaftaran pernikahan diterima oleh SDM
		"""
		self.add_rule(2,3,'6-3',1,temp)

		temp = """
		1. Aktivasi kepesertaan istri/suami/anak di Asuransi adalah 1 hari kerja sejak data di ESS di-approve oleh SDM. Download atau refresh aplikasi askes Ramayana untuk memastikan bahwa istri/suami sudah terdaftar di Ramayana.
		2. Setelah diaktivasi,walaupun belum mendapat kartu asuransi, istri/suami/anak sudah dapat mengakses benefit asuransi kesehatan dengan terlebih dahulu menghubungi PIC Ramayana (PIC Ramayana: 081290373429) jika ingin berobat.
		3. Secara paralel, mohon untuk mengurus penambahan data di Kartu Keluarga (KK) dan mengumpulkan copy KK ke Bag. PRK &Pasca Kerja atau dapat dikirim ke email sekdepnaker@pusri.co.id untuk didaftarkan ke BPJS Kesehatan. Beri keterangan data badge, nama karyawan, alamat email dan nomor handphone karyawan saat mengumpulkan KK. 
		4. Pastikan KK sudah online di Dukcapil. Apabila belum online, maka anak tidak bias didaftarkan ke BPJS Kesehatan. 
		5. Apabila dalam 3 bulan peserta belum mengumpulkan KK, SDM berhak untuk menonaktifkan kepesertaan anak di Asuransi Kesehatan.  
		6. Untuk anak ke 4 dst tetap didaftar ke ESS, tetapi tidak mendapatkan tanggungan kepesertaan di BPJS Kesehatan dan Asuransi Kesehatan.
		"""
		self.add_rule(2,3,'6-4',1,temp)

		self.add_rule(3,1,'',1,'!masukan')



	def get_item(self,kelas,level,dari):
		data = self.db.find({'kelas':kelas,'level':level,'dari':dari},{'_id':0})
		out = []
		for item in data:
			out.append(item)
		return out

if __name__ == '__main__':
	model = model()
	model.clear_rule()
	model.seed_rule_hotel()	
	model.seed_2()