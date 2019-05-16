import math
import json

class DecisionTree:
    data = list()
    attr = list()
    class_attr = ''
    class_data = list()
    iterasi = 0
    kamus = {}
    hasil = {}

    def tambah_data(self, data):
        self.data.append(data)

    def tampilkan_data(self):
        no = 1
        for item in self.data:
            print('Data %d' % (no), end='')
            for x in item.keys():
                print(', %s = %s' % (x, item[x]), end='')
            print()
            no += 1

    def spilt_data(self):
        first_data = self.data[0]
        key_class = list(first_data.keys())[-1]
        for x in self.attr:
            if isinstance(first_data[x], int) or isinstance(first_data[x], float):
                self.split_row(x)

    def split_row(self, key_column):
        data_column = {}
        no = 0;
        for x in self.data:
            data_column[no] = x[key_column]
            no += 1

        data_column = sorted(data_column.items(), key=lambda kv: kv[1])
        spliter = {}
        total_data = len(data_column)
        for x in range(0, total_data - 1):
            spliter[(data_column[x][1] + data_column[x + 1][1])/2] = {}

        frequensi = {}
        total_frekuensi = len(self.data)
        for item in self.data:
            if item[self.class_attr] in frequensi.keys():
                frequensi[item[self.class_attr]] += 1
            else:
                frequensi[item[self.class_attr]] = 1

        total_entropy = 0
        for x in frequensi:
            p = frequensi[x]/total_frekuensi
            if p > 0:
                total_entropy += (p)*math.log(p,2)*-1

        temp_frekuensi = {}
        for x in spliter:
            temp_frekuensi[x] = {}
            for item in self.data:
                temp_class = 'no'
                if item[key_column] >= x:
                    temp_class = 'yes'

                if temp_class not in temp_frekuensi[x].keys():
                    temp_frekuensi[x][temp_class] = {'total': 0}

                if item[self.class_attr] not in temp_frekuensi[x][temp_class].keys():
                    temp_frekuensi[x][temp_class][item[self.class_attr]] = 1
                else:
                    temp_frekuensi[x][temp_class][item[self.class_attr]] += 1

                temp_frekuensi[x][temp_class]['total'] += 1

            for temp in ['yes', 'no']:
                if temp not in temp_frekuensi[x].keys():
                    temp_frekuensi[x][temp] = {'total':0}
                    for temp_class in self.class_data:
                        temp_frekuensi[x][temp][temp_class] = 0
                
                for temp_class in self.class_data:
                    if temp_class not in temp_frekuensi[x][temp].keys():
                        temp_frekuensi[x][temp][temp_class] = 0

                # cari entropy
                temp_frekuensi[x][temp]['entropy'] = 0
                for temp_class in self.class_data:
                    if temp_frekuensi[x][temp]['total'] > 0:
                        p = temp_frekuensi[x][temp][temp_class]/temp_frekuensi[x][temp]['total']
                        if p > 0:
                            temp_frekuensi[x][temp]['entropy'] += (p)*math.log(p,2)*-1

        # for x in temp_frekuensi:
        #     print(x, end="")
        #     print(temp_frekuensi[x])
        # print()
        
        gain = {}
        for key_item in temp_frekuensi:
            gain[key_item] = total_entropy
            for key_attr in temp_frekuensi[key_item]:
                gain[key_item] -= (abs(temp_frekuensi[key_item][key_attr]['total']/abs(total_frekuensi))*temp_frekuensi[key_item][key_attr]['entropy'])

        # for x in gain:
        #     print(x, end=" => ")
        #     print(gain[x], end="")
        #     print()
        # print()
        
        gain_orders = sorted(gain.items(), key=lambda kv: kv[1])
        
        # for x in gain_orders:
        #     print(x[0], end=" => ")
        #     print(x[1], end="")
        #     print()
        # print()
        
        current_spliter = gain_orders[-1][0]
        # print(current_spliter)
        self.kamus[key_column] = {
            'no': key_column + ' < ' + str(current_spliter),
            'yes': key_column + ' >= ' + str(current_spliter)
        }
        # print(self.kamus)
        no = 0
        for item in self.data:
            if item[key_column] < current_spliter:
                self.data[no][key_column] = 'no'
            else:
                self.data[no][key_column] = 'yes'
            no += 1

    def tampilkan_kamus(self):
        print("Split data")
        for key in self.kamus:
            print(key)
            for x in self.kamus[key]:
                print('%s = %s' % (x, self.kamus[key][x]))

    def prepar(self):
        self.attr = list(self.data[0].keys())
        self.class_attr = self.attr.pop()
        for item in self.data:
            temp = list(item.values())
            if temp[-1] not in self.class_data:
                self.class_data.append(temp[-1])
        print("Atribut = ", end="")
        no = 1
        for x in self.attr:
            if no > 1:
                print(', ', end="")
            print(x, end="")
            no += 1
        print()
        print("Class atribut = %s" % (self.class_attr))
        print("Class = ", end="")
        no = 1
        for x in self.class_data:
            if no > 1:
                print(', ', end="")
            print(x, end="")
            no += 1
        print()
        self.spilt_data()

    def run(self):
        self.hasil = self.run_proccess()
        print(self.hasil)
        print()
        self.tampilkan_rules()
    
    def run_proccess(self, rules={}):
        self.iterasi += 1
        print("Iterasi %s" % (self.iterasi))
        print()
        temp_data = self.data
        temp_attr = self.attr
        if rules != {}:
            data_filter = list()
            for item in temp_data:
                is_valid = True
                for key_rules in rules:
                    if key_rules in item:
                        if item[key_rules] != rules[key_rules]:
                            is_valid = False
                            break

                if is_valid == True:
                    del item[key_rules]
                    data_filter.append(item)

            for key_rules in rules:
                if key_rules in temp_attr:
                    temp_attr.remove(key_rules)

            temp_data = data_filter
        frequensi = {}
        total_frekuensi = len(temp_data)
        for item in temp_data:
            if item[self.class_attr] in frequensi.keys():
                frequensi[item[self.class_attr]] += 1
            else:
                frequensi[item[self.class_attr]] = 1

        total_entropy = 0
        for x in frequensi:
            p = frequensi[x]/total_frekuensi
            if p > 0:
                total_entropy += (p)*math.log(p,2)*-1

        for x in frequensi:
            print('Frekuensi %s = %d' % (x, frequensi[x]))
        print('Frekuensi Total = %d' % (total_frekuensi))
        print('Entropy(S) = %s' % (total_entropy))
        print()

        frekuensi_attr = {}
        for item in temp_data:
            for item_attr in temp_attr:
                if item_attr not in frekuensi_attr.keys():
                    frekuensi_attr[item_attr] = {}
                if item[item_attr] not in frekuensi_attr[item_attr].keys():
                    frekuensi_attr[item_attr][item[item_attr]] = {'total' : 0}

                if item[self.class_attr] in frekuensi_attr[item_attr][item[item_attr]].keys():
                    frekuensi_attr[item_attr][item[item_attr]][item[self.class_attr]] += 1
                else:
                    frekuensi_attr[item_attr][item[item_attr]][item[self.class_attr]] = 1
                frekuensi_attr[item_attr][item[item_attr]]['total'] += 1

        for key_item in frekuensi_attr:
            for key_attr in frekuensi_attr[key_item]:
                for item_class_data in self.class_data:
                    if item_class_data not in frekuensi_attr[key_item][key_attr]:
                        frekuensi_attr[key_item][key_attr][item_class_data] = 0

                frekuensi_attr[key_item][key_attr]['entropy'] = 0
                for item_class_data in self.class_data:
                    p = frekuensi_attr[key_item][key_attr][item_class_data]/frekuensi_attr[key_item][key_attr]['total']
                    if p > 0:
                        frekuensi_attr[key_item][key_attr]['entropy'] += (p)*math.log(p,2)*-1

        print("Entropy")
        for key_item in frekuensi_attr:
            print(key_item)
            for key_attr in frekuensi_attr[key_item]:
                print("%s => " % (key_attr), end="")
                print("total = %s" % (frekuensi_attr[key_item][key_attr]['total']), end="")
                for item_class_data in self.class_data:
                    print(", %s = %s" % (item_class_data, frekuensi_attr[key_item][key_attr][item_class_data]), end="")
                print(", entropy = %s" % (frekuensi_attr[key_item][key_attr]['entropy']))
        print()

        print("Gain")
        gain = {}
        for key_item in frekuensi_attr:
            gain[key_item] = total_entropy
            for key_attr in frekuensi_attr[key_item]:
                gain[key_item] -= (abs(frekuensi_attr[key_item][key_attr]['total']/abs(total_frekuensi))*frekuensi_attr[key_item][key_attr]['entropy'])

        for x in gain:
            print('%s = %s' % (x, gain[x]))

        print()
        gain_orders = sorted(gain.items(), key=lambda kv: kv[1])
        gain_terbesar = gain_orders[-1][0]
        print("Gain terbesar = %s" % (gain_terbesar))
        temp_rules = {}
        if len(temp_attr) == 1:
            temp_keys = list(frekuensi_attr[gain_terbesar].keys())
            temp_paling_besar = 0
            temp_class = False
            for item_class in self.class_data:
                if temp_paling_besar < frekuensi_attr[gain_terbesar][temp_keys[0]][item_class]:
                    temp_paling_besar = frekuensi_attr[gain_terbesar][temp_keys[0]][item_class]
                    temp_class = item_class
            temp_rules[temp_keys[0]] = temp_class
        else:
            for item in frekuensi_attr[gain_terbesar]:
                temp_rules[item] = False
                for item_class in self.class_data:
                    if frekuensi_attr[gain_terbesar][item]['total'] == frekuensi_attr[gain_terbesar][item][item_class]:
                        temp_rules[item] = item_class

        print("Rules")
        for item in temp_rules:
            if temp_rules[item] != False:
                print("%s = %s => %s" % (gain_terbesar, item, temp_rules[item]))
        print()

        if len(temp_attr) > 1:
            for item in temp_rules:
                if temp_rules[item] == False:
                    rules[gain_terbesar] = item
                    temp_rules[item] = self.run_proccess(rules)
        result = [gain_terbesar, temp_rules]
        return result

    def tampilkan_rules(self):
        print('Rules')
        print(json.dumps(self.hasil, sort_keys=True,indent=4, separators=(',', ': ')))

    # def rules_to_str(self, rules, level = 1):
    #     result = ""
    #     for item in rules[1]:
    #         if level == 1:
    #             result += "IF "
    #         if isinstance(rules[1][item], str):
    #             result += rules[0] + " = " + item + " THEN " + self.class_attr + " = " + rules[1][item] + "\n"
    #         else:
    #             result += rules[0] + " = " + item + " AND " + self.rules_to_str(rules[1][item], level + 1)
    #     return result


# main proses
dt = DecisionTree()
dt.tambah_data({'penghasilan': 3.5, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.2, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 10, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 3.7, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 3, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 5, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 2, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 3.8, 'pernikahan': 'sudah', 'tanggungan': 1, 'dp': 2, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 4.2, 'pernikahan': 'sudah', 'tanggungan': 3, 'dp': 0.5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.7, 'pernikahan': 'sudah', 'tanggungan': 2, 'dp': 7.5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.9, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.3, 'pernikahan': 'sudah', 'tanggungan': 0, 'dp': 9, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 8, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.2, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 0.5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.1, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 0.5, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.8, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 1, 'resiko': 'rendah'})
dt.tambah_data({'penghasilan': 2.9, 'pernikahan': 'sudah', 'tanggungan': 0, 'dp': 2, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 1.7, 'pernikahan': 'sudah', 'tanggungan': 3, 'dp': 0.5, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 1.2, 'pernikahan': 'sudah', 'tanggungan': 2, 'dp': 1, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 2.2, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 2, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 2.4, 'pernikahan': 'sudah', 'tanggungan': 4, 'dp': 2.5, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 2.6, 'pernikahan': 'sudah', 'tanggungan': 4, 'dp': 1.2, 'resiko': 'tinggi'})
dt.tambah_data({'penghasilan': 2.6, 'pernikahan': 'belum', 'tanggungan': 0, 'dp': 1.7, 'resiko': 'tinggi'})

print('Decision Tree')
print('')
dt.tampilkan_data()
print('')

dt.prepar()
print('')
dt.tampilkan_data()
print('')
dt.tampilkan_kamus()
print('')

dt.run()
print('')