import json

# open file json
file = open("dataset.json", "r") 
data = file.read()

# json to data
data = json.loads(data)

# tampilkan data item
print("Data Items: ")
for key in data['item']:
	print('%s 	= %s' % (key, data['item'][key]))
print()

# tampilkan data transaksi
print("Data Transaksi: ")
for key in data['transaksi']:
	print('%s 	= %s' % (key, ', '.join(data['transaksi'][key])))
print()

minimum = 4
semua_kombinasi = {}
semua_diambil = {}
semua_tidak_diambil = {}

print("Langkah ke-1: Menghitung jumlah transaksi masing-masing item")
for key in data['item']:
	temp = 0
	for t in data['transaksi']:
		if key in data['transaksi'][t]:
			temp = temp + 1
	print('%s 	= %d' % (key, temp))
	semua_kombinasi[key] = temp
	# memilih transaksi minimum
	if temp >= minimum:
		semua_diambil[key] = temp
	else:
		semua_tidak_diambil[key] = temp
print()

# diambil dari semua_diambil
print("Langkah ke-2: Memilih transaksi dengan minimum transaksi")
for key in semua_diambil:
	print('%s 	= %s' % (key, semua_diambil[key]))
print()

# mengecek apakah lit sama
def same_list(list1, list2):
	if len(list1) != len(list2):
		return False
	for x in list1:
		if x not in list2:
			return False
	for x in list2:
		if x not in list1:
			return False
	return True

# mengecek apakah list di dalam list berisi list
def list_in(data_list, list):
	for x in data_list:
		if same_list(x, list):
			return True
	return False

print("Langkah ke-3: Membuat pasangan item")
def combinate(arg):
	kombinasi = []
	result = []
	args = []
	for x in arg:
		if ',' in x:
			args += x.split(',')
		else:
			args.append([x])
	# print(args)

	for x in args:
		for y in args:
			if x != y:
				temp = list(x + y)
				if not list_in(kombinasi, temp):
					kombinasi.append(temp)
	for x in kombinasi:
		result.append(','.join(x))
	return result

data_kombinasi = combinate(semua_diambil)
for x in data_kombinasi:
	print(x)
print()

def in_transaction(transaksi, list_item):
	for x in list_item:
		if x not in transaksi:
			return False
	return True

jumlah_transaksi_kombinasi = {};
kombinasi_diambil = {};
kombinasi_tidak_diambil = {};
print("Langkah ke-4: Menghitung jumlah transaksi masing-masing kombinasi")
for x in data_kombinasi:
	temp_jumlah = 0
	for y in data['transaksi']:
		if in_transaction(data['transaksi'][y], x.split(',')):
			temp_jumlah += 1
	print('%s 	= %d' % (x, temp_jumlah))
	if temp_jumlah >= minimum:
		kombinasi_diambil[x] = temp_jumlah
	else:
		kombinasi_tidak_diambil[key] = temp_jumlah
print()

print("Langkah ke-5: Memilih transaksi dengan minimum transaksi")
for key in kombinasi_diambil:
	print('%s 	= %s' % (key, kombinasi_diambil[key]))
print()