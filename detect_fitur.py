# detect_fitur.py
import re
import string
from extract_info import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# entar convert ke lowercase semua dulu
r = re.compile(".*tubes.*|.*tucil.*|.*kuis.*|.*quiz.*|.*ujian.*|.*praktikum.*|.*uts.*|.*uas.*")

# membersihkan stopwords, return dalam bentuk kalimat
# dibuat return dalam bentuk kalimat karena diasumsikan
# proses pencocokan string menggunakan kalimat bukan array
def cleanStopWord(sentence):
    factory = StopWordRemoverFactory()
    ignore = ['lah','eh','ini','itu','loh'] # stop words tambahan 
    stopword = factory.create_stop_word_remover()

    # bersihin stop words, tanda baca dan ubah jadi lowercase semua
    stop = stopword.remove(sentence) 
    words = re.sub("[^\w]", " ",  stop).split() #bersihin tanda baca
    cleaned_text = [w.lower() for w in words if w not in ignore] #jadiin huruf kecil
    # final_string = ' '.join(cleaned_text)
    return cleaned_text

# TODO : untuk bagian2 kode yang if kata in kalimat mungkin nanti diganti pake KMP/BM
# karena di spek ditulis tidak dilakukan secara exact matching tp pake KMP/BM
# untuk menentukan kemiripan kata di perintah.

def isFitur1(message):
    # harus punya : tanggal, kode matkul, jenis tugas, topik tugas
    dateList = find_date(message)
    courseList = find_course_id(message)
    taskList = detectTugas(cleanStopWord(message))
    topik = []
    if(len(courseList)!=0):
        topik = detectTopik(message, courseList[0])

    if(len(dateList)!=0 and len(courseList)!=0 and len(taskList)!=0 and len(topik)!=0):
        # buat ngetes
        print("tanggal\t\t: ",dateList[0][0])
        print("kode matkul\t: ",courseList[0])
        print("tugas\t\t: ",taskList[0])
        print("topik\t\t: ",topik[2].strip())
        return True
    else:
        return False

def isFitur2(message):
    yes = False
    # cari kata deadline / apa saja / apa aja
    if "kapan" not in message and ("deadline" in message or "dedlen" in message) :
        yes = True

    # cari jenis tugas
    taskList = detectTugas(cleanStopWord(message))
    
    # cari tanggal
    dateList = find_date(message)
    
    # cari durasi
    duration = find_duration(message)
    
    # if contains 'deadline'
    if(yes):
        print(taskList)
        print(dateList)
        print(duration)

        # deadline semua task tertentu
        if(len(taskList)!=0 and len(dateList)==0 and len(duration)==0):
            print("menampilkan semua deadline dari")
            for task in taskList:
                print(task)

        # tugas tertentu pada tanggal tertentu
        elif(len(taskList)!=0 and len(dateList)==1):
            print("menampilkan ",taskList[0]," tanggal ",dateList[0][0])
        
        # tugas tertentu pada tanggal .. sampai ..
        elif(len(taskList)!=0 and len(dateList)!=0 and len(dateList[0])>1 and ("sampai" in message or "antara" in message)):
            print("menampilkan ",taskList[0]," antara ",dateList[0][0]," sampai ",dateList[0][1])

        elif(len(taskList)!=0 and len(duration)!=0):
            print("menampilkan ",taskList[0]," ",duration[0]," kedepan ")

        # deadline semua tugas di tanggal tsb
        elif(len(dateList)!=0 and len(dateList[0])==1):
            print("menampilkan semua tugas yang deadline-nya tanggal ",dateList[0][0])
        
        # deadline semua tugas dari tanggal .. sampai ..
        elif(len(dateList)!=0 and len(dateList[0])>1 and ("sampai" in message or "antara" in message)):
            print("menampilkan semua tugas dengan deadline dari tanggal ",dateList[0][0]," sampai ",dateList[0][1])
        
        # terdapat durasi
        elif(len(duration)!=0):
            print("menampilkan tugas dengan deadline ",duration[0]," kedepan ")
        
        # cetak semua tugas
        else:
            print("menampilkan semua deadline tugas yang ada")
    return yes
    # case dari spek udah work semua, belum tau kalo misalkan masih ada bug

def isFitur3(message):
    yes = False
    
    if("kapan" in message):
        print("masuk fitur 3")

    courseList = find_course_id(message)
    print(courseList)
    taskList = detectTugas(cleanStopWord(message))
    print(taskList)

    if("deadline" in message and "kapan" in message and len(courseList)!=0) :
        yes = True
        if len(taskList)!=0:
            print("menampilkan deadline dari",taskList[0],courseList[0])
        else:
            print("menampilkan deadline dari tugas",courseList[0])
        
    return yes
    # kode matkul harus huruf kapital baru kebaca

def isFitur4(message):
    yes = False
    taskID = find_task_id(message)
    dateList = find_date(message)

    keywords = re.compile(".*undur.*|.*maju.*|.*ubah.*|.*ganti.*")
    keyList = list(filter(keywords.match, cleanStopWord(message)))

    # TODO : nanti mesti dicek ke database id nya valid ato engga
    if(len(keyList)!=0):
        print("memperbarui tugas menjadi tanggal",dateList[0][0])
        yes = True
    return yes

def isFitur5(message):
    yes = False

    keywords = re.compile(".*umpul.*|.*selesai.*|.*kelar.*|.*done.*|.*beres.*")
    keyList = list(filter(keywords.match, cleanStopWord(message)))

    taskID = find_task_id(message)
    # TODO : nanti mesti dicek ke database id nya valid ato engga
    if(len(keyList)!=0):
        print("menandai tugas sudah selesai")
        yes = True
    return yes

def isFitur6(message):
    yes = False

    keywords = re.compile(".*help.*|.*command.*|.*cara.*|.*fitur.*|.*assistant.*")
    keyList = list(filter(keywords.match, cleanStopWord(message)))

    if(len(keyList)!=0):
        print("menampilkan apa saja yang bot bisa lakukan")
        print("mendefinisikan list kata penting")
        yes = True
    return yes

# input array of words, return array contains keywords
def detectTugas(message):
    mylist = cleanStopWord(userMessage)
    newlist = list(filter(r.match, mylist)) # Read Note
    return newlist

# input str // diasumsiin topik selalu diantara :
# 1) kode matkul ... pada
# 2) kode matkul ... tanggal/tgl (ini kalo "pada" tidak ditemukan)
# adalagi..?
def detectTopik(userMessage, key):
    if "pada" in userMessage:
        part = userMessage.partition("pada")
        print(part)
        part1 = part[0].partition(key) # asumsi
        return part1
    else:
        if "tanggal" in userMessage:
            part = userMessage.partition("tanggal")
            print(part)
            part1 = part[0].partition(key) # asumsi
            return part1
        elif "tgl" in userMessage:
            part = userMessage.partition("tgl")
            print(part)
            part1 = part[0].partition(key) # asumsi
            return part1

def incrementDate(date, daysduration):
    date += datetime.timedelta(days=daysduration)
    return date

# buat ngetes
userMessage = input("Masukan pesan : ")
# print(cleanStopWord(userMessage))

if(isFitur1(userMessage)):
    print("fitur 1")
elif(isFitur2(userMessage)):
    print("fitur 2")
elif(isFitur3(userMessage)):
    print("fitur 3")
elif(isFitur4(userMessage)):
    print("fitur 4")
elif(isFitur5(userMessage)):
    print("fitur 5")
elif(isFitur6(userMessage)):
    print("fitur 6")
else:
    print("maaf, pesan tidak bisa dikenali")

# test increment date
d1 = convert_string_to_date("14 april 2021")
print(incrementDate(d1,17))
