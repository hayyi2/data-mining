import random

class DBClustering:
    data = list()
    x_name = ''
    y_name = ''
    eps = 15
    min_pts = 3
    visited = list()
    data_cluster = list()

    def set_x_name(self, x_name):
        self.x_name = x_name

    def set_y_name(self, y_name):
        self.y_name = y_name

    def set_eps(self, eps):
        self.eps = eps

    def set_min_pts(self, min_pts):
        self.min_pts = min_pts

    def tambah_data(self, x, y):
        temp = {'x': x, 'y': y, 'cluster': 0}
        self.data.append(temp)

    def tampilkan_data(self):
        no = 1
        for item in self.data:
            print('Data %d, %s = %d, %s = %d' % (no, self.x_name, item['x'], self.y_name, item['y']))
            no += 1

    def hitung_jarak(self, dot1, dot2):
        return abs(dot1['x']-dot2['x'])+abs(dot1['y']-dot2['y'])

    def cari_tetangga(self, index):
        result = list()
        no = 0
        for item in self.data:
            if no != index:
                if self.eps >= self.hitung_jarak(self.data[index], item):
                    result.append(no)
            no += 1
        return result

    def run(self):
        cluster = 1
        iterasi = 1
        while len(self.visited) < len(self.data):

            print('Iterasi %d: ' % (iterasi))
            temp = -1;
            while True:
                temp = random.randint(0, len(self.data)-1)
                if temp not in self.visited:
                    break

            print('cp : %d' % (temp + 1))

            self.visited.append(temp)
            tetangga = self.cari_tetangga(temp)


            if len(tetangga) < self.min_pts:
                self.data[temp]['cluster'] = -1
            else:
                self.data[temp]['cluster'] = cluster
                for item in tetangga:
                    print('bp : %d' % (item + 1))
                    if item not in self.visited:
                        self.visited.append(item)
                        tetangga_tetangga = self.cari_tetangga(item)
                        if len(tetangga_tetangga) < self.min_pts:
                            self.data[item]['cluster'] = -1

                    if self.data[item]['cluster'] <= 0:
                        self.data[item]['cluster'] = cluster
                cluster += 1

            self.tampilkan_hasil()
            print('')
            iterasi += 1

        print('Hasil Akhir : ')
        self.tampilkan_hasil()
        
    def tampilkan_hasil(self):
        no = 1
        for item in self.data:
            print('Data %d, %s = %d, %s = %d, Cluster = %d' % (no, self.x_name, item['x'], self.y_name, item['y'], item['cluster']))
            no += 1


dbc = DBClustering()
dbc.set_x_name('T')
dbc.set_y_name('K')
dbc.tambah_data(85, 85)
dbc.tambah_data(80, 90)
dbc.tambah_data(65, 70)
dbc.tambah_data(72, 95)
dbc.tambah_data(83, 78)
dbc.tambah_data(60, 75)
dbc.tambah_data(78, 85)
dbc.tambah_data(64, 65)
dbc.tambah_data(69, 70)
dbc.tambah_data(75, 88)

print('Density Based Clustering')
print('')
dbc.tampilkan_data()
print('')

in_eps = int(input("Epsilon : "))
in_min_pts = int(input("Min Pts : "))
print('')

dbc.set_eps(in_eps)
dbc.set_min_pts(in_min_pts)

dbc.run()
print('')