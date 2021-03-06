#database.py
import sqlite3
class tugas():

    def __init__(self, tanggal, matkul, jenis, topik):
        self.tanggal = tanggal
        self.matkul = matkul
        self.jenis = jenis
        self.topik = topik

    def __str__(self):
        string = "(ID: {id}) {tanggal} - {kode} - {jenis} - {topik}".format(id="id",tanggal=str(self.tanggal), kode=self.matkul, jenis=self.jenis, topik=self.topik)
        return string

    # operator =
    def __eq__(self, other):
        if(self.tanggal == other.tanggal and self.matkul == other.matkul and self.jenis == other.jenis and self.topik == other.topik):
            return True
        else:
            return False

# create table
file_db = "../test/tugas.db"
conn = sqlite3.connect(file_db)
c = conn.cursor()



# tabel buat simpan daftar tugas
c.execute('''CREATE TABLE IF NOT EXISTS tugas
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             tanggal DATE, 
             matkul TEXT, 
             jenis TEXT,
             topik TEXT,
             UNIQUE(tanggal, matkul, jenis, topik))''')

# tabel yang simpan daftar id dari tugas yang sudah selesai
c.execute('''CREATE TABLE IF NOT EXISTS done
             (id_done INTEGER,
             FOREIGN KEY (id_done) REFERENCES tugas (id),
             UNIQUE (id_done))''')

def cursor():
    return sqlite3.connect(file_db).cursor()

# buat fitur 1 : nambahin tugas ke database 
def add_tugas(tugas):
    lastid = -99
    try: # kalo tugasnya belom ada baru ditambahin
        c = cursor()
        with c.connection:
            c.execute("INSERT INTO tugas (tanggal, matkul, jenis, topik) VALUES (?, ?, ?, ?)",(tugas.tanggal, tugas.matkul, tugas.jenis, tugas.topik))
        lastid = c.lastrowid
        c.connection.close()
    except sqlite3.Error as error:
        print("Tugas sudah tercatat di database")
    return lastid

# buat fitur 2 & 3 : menampilkan tugas berdasarkan kondisi tertentu
def showAllTugas():
    c = cursor()
    c.execute('''SELECT * FROM tugas 
                WHERE id NOT IN (SELECT id_done FROM done)''')
    return c.fetchall()
    # return dalam bentuk array of tuple 
    # [(1, '2021-04-14', 'IF2210', 'tubes', 'engimon')]

def showTugasFrom(date1, date2):
    # date1 < date2
    c = cursor()
    c.execute('''SELECT *
                 FROM tugas
                 WHERE tanggal >= date(?)
                 AND tanggal <=  date(?)
                 AND id NOT IN (SELECT id_done FROM done)''',(date1,date2))
    return c.fetchall()
    # return dalam bentuk array of tuple
    # [(1, '2021-04-14', 'IF2210', 'tubes', 'engimon')]

def showTugasbyDate(date):
    # date1 < date2
    c = cursor()
    c.execute('''SELECT *
                 FROM tugas
                 WHERE tanggal = date(?)
                 AND id NOT IN (SELECT id_done FROM done)''',(date,))
    return c.fetchall()
    # return dalam bentuk array of tuple 
    # [(1, '2021-04-14', 'IF2210', 'tubes', 'engimon')]

def showTugasbyJenis(jenis):
    c = cursor()
    c.execute('''SELECT *
                 FROM tugas
                 WHERE jenis like ?
                 AND id NOT IN (SELECT id_done FROM done)''',(jenis,))
    return c.fetchall()
    # return dalam bentuk array of tuple 
    # [(1, '2021-04-14', 'IF2210', 'tubes', 'engimon')]

def showTugasbyMatkul(matkul):
    c = cursor()
    c.execute('''SELECT *
                 FROM tugas
                 WHERE matkul like ?
                 AND id NOT IN (SELECT id_done FROM done)''',(matkul,))
    return c.fetchall()
    # return dalam bentuk array of tuple 
    # [(1, '2021-04-14', 'IF2210', 'tubes', 'engimon')]

def showTugasbyId(id):
    c = cursor()
    c.execute('''SELECT *
                 FROM tugas
                 WHERE id = ?
                 ''',(id,))
    return c.fetchall()

# fitur 4 : update tugas berdasarkan id
def isIdExist(id):
    c = cursor()
    temp = []
    with c.connection:
        c.execute('''
        SELECT * FROM tugas WHERE id = ? AND id NOT IN (SELECT * FROM done)''', (id,))
        temp = c.fetchall()

    if len(temp)!=0:
        return True
    else:
        print("id tugas tidak ditemukan")
        return False

def updateTanggal(id, tanggal):
    if isIdExist(id):
        try:
            file_db = "../test/tugas.db"
            sqliteConnection = sqlite3.connect(file_db)
            cursor = sqliteConnection.cursor()

            cursor.execute("""Update tugas set tanggal = ? where id = ?""", (tanggal,id))
            sqliteConnection.commit()
            cursor.close()

        except sqlite3.Error as error:
            print("gagal untuk melakukan update deadline tugas", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()

# fitur 5 : tandain suatu task sudah selesai dikerjakan
def tugasDone(id):
    try:
        c = cursor()
        with c.connection:
            c.execute("INSERT INTO done VALUES (?)", (id,))
        c.connection.close()
    except sqlite3.Error as error:
        print("tugas sudah pernah ditandai")

def showAllDoneTask():
    c = cursor()
    c.execute('''SELECT * FROM tugas 
                WHERE id IN (SELECT id_done FROM done)''')
    return c.fetchall()

# driver
# print("--------- database.py -------\n")
# tanggal1 = "2021-04-14"
# matkul1 = "IF2210"
# jenis1 = "tubes"
# topik1 = "engimon"
# tugas1 = tugas(tanggal1,matkul1,jenis1,topik1)
# tugas2 = tugas("2020-10-20",matkul1,jenis1,"asd")
# tugas3 = tugas("2077-10-20",matkul1,jenis1,"masa depan")
# print(str(tugas1))
# add_tugas(tugas1)
# add_tugas(tugas2)
# add_tugas(tugas3)
# print(str_data_tugas(showAllTugas()))

# c.execute("DROP TABLE done")
# c.execute("DROP TABLE tugas")