class Apriori:
	item = list()
	transaksi = list()

	minimum = 3

	def tambah_transaksi(self, transaksi):
		for x in transaksi:
			if x not in self.item:
				self.item.append(x)
		self.transaksi.append(transaksi)

	def tampilkan_item(self):
		no = 1
		for x in self.item:
			print('%s 	= %s' % (no, x))
			no += 1

	def tampilkan_transaksi(self):
		no = 1
		for x in self.transaksi:
			print('%d 	= %s' % (no, ', '.join(x)))
			no += 1

	def set_minimum(self, minimum):
		self.minimum = minimum

	def cek_di_transaksi(self, transaksi, list_item):
		for x in list_item:
			if x not in transaksi:
				return False
		return True

	def same_list(self, list1, list2):
		if len(list1) != len(list2):
			return False
		for x in list1:
			if x not in list2:
				return False
		for x in list2:
			if x not in list1:
				return False
		return True

	def list_in(self, data_list, list):
		for x in data_list:
			if self.same_list(x, list):
				return True
		return False

	def get_kombinasi_item(self, arg):
		kombinasi = []
		result = []
		args = []
		for x in arg:
			if ',' in x:
				args.append(x.split(', '))
			else:
				args.append([x])

		for x in args:
			for y in args:
				if x != y:
					temp = list(set(x) | set(y))
					if not self.list_in(kombinasi, temp):
						kombinasi.append(temp)
		for x in kombinasi:
			result.append(', '.join(x))
		return result

	def run(self, data_list = [], result = {}):
		if data_list == []:
			data_list = self.item
		else:
			data_list = self.get_kombinasi_item(data_list)
		transaksi_minimum = {}
		print("Menghitung jumlah transaksi")
		for x in data_list:
			temp_jumlah = 0
			for y in self.transaksi:
				if self.cek_di_transaksi(y, x.split(', ')):
					temp_jumlah += 1
			print('%s = %d' % (x, temp_jumlah))
			if temp_jumlah >= self.minimum:
				transaksi_minimum[x] = temp_jumlah
		print()

		if len(transaksi_minimum) > 0:
			print("Memilih transaksi dengan minimum")
			for x, y in transaksi_minimum.items():
				print('%s = %d' % (x, y))
		else:
			print("Tidak ada yang memenuhi minimum")
		print()

		if len(x.split(', ')) > 1:
			result = {**result, **transaksi_minimum}

		if len(transaksi_minimum) > 1: # iterasi
			self.run(transaksi_minimum, result)
		else: 
			print("Hasil akhir: ")
			for x, y in result.items():
				print('%s = %d' % (x, y))
			print()

			print("Hasil akhir yang diurutkan: ")
			sorted_data = sorted(result.items(), key=lambda kv: kv[1], reverse=True)
			for x, y in sorted_data:
				print('%s = %d' % (x, y))
			print()


apriori = Apriori()
apriori.tambah_transaksi(['Jahe', 'Kunyit', 'Laos', 'Garam', 'Merica'])
apriori.tambah_transaksi(['Cengkeh', 'Santan', 'Gula', 'Cabe', 'Kayu manis'])
apriori.tambah_transaksi(['Jahe', 'Laos', 'Santan', 'Gula', 'Merica'])
apriori.tambah_transaksi(['Kayu manis', 'Kunyit', 'Garam', 'Gula', 'Cengkeh'])
apriori.tambah_transaksi(['Garam', 'Gula', 'Cabe', 'Laos', 'Kayu manis'])
apriori.tambah_transaksi(['Merica', 'Jahe', 'Santan', 'Cabe', 'Kunyit'])
apriori.tambah_transaksi(['Laos', 'Jahe'])
apriori.tambah_transaksi(['Kayu manis', 'Cengkeh', 'Santan'])
apriori.tambah_transaksi(['Gula', 'Garam'])
apriori.tambah_transaksi(['Cengkeh', 'Kayu manis', 'Laos'])

print("Data Items :")
apriori.tampilkan_item()
print()

print("Data Transaksi :")
apriori.tampilkan_transaksi()
print()

try:
    minimum_input = input("Minimum : ")
    minimum = int(minimum_input)
    apriori.set_minimum(minimum)
except ValueError as ex:
    print("Input harus berupa angka")
    quit()

apriori.run()