# detect_fitur.py
import re
import copy
from datetime import date
from extract_info import *
from database import *
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# TODO daftar kata penting kita tuh apa aja sih sebenernya
# entar convert ke lowercase semua dulu
r = re.compile(".*tubes.*|.*tucil.*|.*kuis.*|.*quiz.*|.*ujian.*|.*praktikum.*|.*uts.*|.*uas.*")
# data kamus, yaitu semua keywords
all_keywords = load_text("help_keywords") + load_text("done") + load_text("update_keywords") + load_text("jenis_tugas") + load_text("waktu")
# print(all_keywords)

# membersihkan stopwords, return dalam bentuk array
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

def isFitur1(message): # untuk sementara udah aman kayaknya
    # harus punya : tanggal, kode matkul, jenis tugas, topik tugas
    dateList = allDates(message)
    courseList = find_course_id(message)
    taskList = detectTugas(message)
    topik = []
    string = ""

    if(len(courseList)!=0):
        topik = detectTopik(message, courseList[0])

    if(len(dateList)!=0 and len(courseList)!=0 and len(taskList)!=0 and len(topik)!=0):
        task = tugas(dateList[0],courseList[0],taskList[0],topik[2].strip())
        lastid = add_tugas(task)
        if(lastid!=-99):
            data = showTugasbyId(lastid)[0]
            #print("[TASK BERHASIL DICATAT]")
            string = "(ID : {}) {} - {} - {} - {}".format(data[0],data[1],data[2],data[3],data[4]) 
            # semoga nanti string-nya tinggal di pass ke kolom chat
            # print(string)
        return True, string
    else:
        return False, string

def isFitur2(message):
    yes = False
    string = ""
    taskId = find_task_id(message)
    keykpn = boyer_moore(message, "kapan")
    keydeadline = find_deadline_keyword(message)

    # cari jenis tugas
    taskList = detectTugas(message)

    # cari tanggal
    dateList = allDates(message)
    
    # cari durasi
    duration = find_duration(message)

    if taskId[0] == -99 and keykpn == -1 and (keydeadline != -1 or len(taskList)!=0 or len(duration)!=0):
        yes = True
    
    # if contains 'deadline'
    if(yes):

        # deadline semua tugas ...
        if(len(taskList)!=0 and len(dateList)==0 and len(duration)==0):
            # print("Menampilkan semua deadline dari",taskList[0])
            #printDeadline(showTugasbyJenis(taskList[0]))
            
            string = rawString(showTugasbyJenis(taskList[0]))

        # tugas ... pada tanggal ... (tanggalnya cuma 1)
        elif(len(taskList)!=0 and len(dateList)==1):
            # print("Menampilkan",taskList[0],"tanggal",dateList[0])
            tempjenis = showTugasbyJenis(taskList[0])
            temptanggal = showTugasbyDate(dateList[0])
            #printDeadline(intersection(tempjenis,temptanggal))

            string = rawString(intersection(tempjenis,temptanggal))
        
        # tugas ... pada tanggal .. sampai .. (tanggalnya ada 2)
        elif(len(taskList)!=0 and len(dateList)==2  and (boyer_moore(message, "sampai") != -1 or boyer_moore(message, "antara") != -1)): # TODO
            # print("Menampilkan",taskList[0],"antara",dateList[0],"sampai",dateList[1])
            tempjenis = showTugasbyJenis(taskList[0])
            temptanggal = showTugasFrom(dateList[0],dateList[1])
            #printDeadline(intersection(tempjenis,temptanggal))

            string = rawString(intersection(tempjenis,temptanggal))

        # tugas ... dengan durasi ...
        elif(len(taskList)!=0 and len(duration)!=0):
            # print("Menampilkan",taskList[0],duration[0],"kedepan")
            dateLast = incrementDate(date.today(),convert_duration_to_days(duration))

            tempjenis = showTugasbyJenis(taskList[0])
            temptanggal = showTugasFrom(date.today(),dateLast)
            #printDeadline(intersection(tempjenis,temptanggal))

            string = rawString(intersection(tempjenis,temptanggal))

        # semua tugas tanggal ...
        elif(len(dateList)==1):
            # print("Menampilkan semua tugas yang deadline-nya tanggal",dateList[0])
            #printDeadline(showTugasbyDate(dateList[0]))

            string = rawString(showTugasbyDate(dateList[0]))
        
        # deadline semua tugas dari tanggal .. sampai ..
        elif(len(dateList)==2 and ((boyer_moore(message, "sampai") != -1) or (boyer_moore(message, "antara") != -1))):
            # print("Menampilkan semua tugas dengan deadline dari tanggal",dateList[0],"sampai",dateList[1])
            #printDeadline(showTugasFrom(dateList[0],dateList[1]))

            string = rawString(showTugasFrom(dateList[0],dateList[1]))

        # terdapat durasi ...
        elif(len(duration)!=0):
            # print("Menampilkan tugas dengan deadline",duration[0],"kedepan ")
            dateLast = incrementDate(date.today(),convert_duration_to_days(duration))
            #printDeadline(showTugasFrom(date.today(),dateLast))

            string = rawString(showTugasFrom(date.today(),dateLast))

        # besok
        elif(boyer_moore(message,"besok")!=-1):
            string = rawString(showTugasbyDate(incrementDate(date.today(),1)))

        # lusa
        elif(boyer_moore(message,"lusa")!=-1):
            string = rawString(showTugasbyDate(incrementDate(date.today(),2)))

        # hari ini
        elif(boyer_moore(message,"hari ini")!=-1):
            string = rawString(showTugasbyDate(date.today()))

        # cetak semua tugas
        else:
            string = rawString(showAllTugas())

    return yes, string
    # case dari spek udah work semua, belum tau kalo misalkan masih ada bug

def isFitur3(message):
    yes = False
    string = ""
    temp = []

    key = (boyer_moore(message,"kapan") != -1) and (boyer_moore(message,"deadline") != -1)

    courseList = find_course_id(message)
    taskList = detectTugas(message)
    
    if(key and len(courseList)!=0) :
        yes = True
        if len(taskList)!=0:
            if(taskList[0]=="tucil" or taskList[0]=="tubes"):
                tempmatkul = showTugasbyMatkul(courseList[0])
                temptugas = showTugasbyJenis(taskList[0])
                temp = intersection(tempmatkul,temptugas)
            elif(taskList[0]=="kuis" or taskList[0]=="ujian" or taskList[0]=="praktikum" or taskList[0]=="uts" or taskList[0]=="tucil" or taskList[0]=="uas"):
                string = "Task tidak termasuk tugas"
        else:
            # print("menampilkan deadline dari tugas",courseList[0])
            temp = showTugasbyMatkul(courseList[0])
    
    if(len(temp)!=0):
        for i in range(len(temp)):
            string = string + temp[i][1] + " - "+ temp[i][3] + " - "+temp[i][4] + "\n"
    print(string)
    return yes, string

def isFitur4(message):
    string = ""
    yes = False
    taskID = find_task_id(message)
    dateList = allDates(message)
    
    key = find_update_keyword(message)

    if(key!=-1 and taskID[0]!=-99):

        # jika id valid
        if(isIdExist(taskID[0])):
            # lakukan update
            old = copy.deepcopy(showTugasbyId(taskID[0])[0][1])
            updateTanggal(taskID[0],dateList[0])
            new = showTugasbyId(taskID[0])[0][1]

            string = "Sukses memperbaharui deadline tugas dengan ID:{}\ndari tanggal {} menjadi {}".format(taskID[0], old, new)
        
        else:
            string = "Task ID tidak ditemukan"

        yes = True
    return yes, string

def isFitur5(message):
    yes = False
    string = ""
    key = find_done_keyword(message)

    taskID = find_task_id(message)

    if(key!=-1):
        # print("menandai tugas sudah selesai")
        if(isIdExist(taskID[0])):
            tugasDone(taskID[0])
            string = "Sukses menandai task {} selesai".format(taskID[0])
        else:
            string = "ID task tidak ditemukan"
        yes = True
    return yes, string

def isFitur6(message):
    yes = False
    string = ""
    key = find_help_keyword(message)

    if(key!=-1):
        # print("menampilkan apa saja yang bot bisa lakukan")
        #print("mendefinisikan list kata penting")
        yes = True
        header = "[FITUR]\n"
        fitur1 = "1. Menambahkan task baru\n"
        fitur2 = "2. Melihat daftar task yang harus dikerjakan\n"
        fitur3 = "3. Menampilkan deadline dari suatu task tertentu\n"
        fitur4 = "4. Memperbaharui task tertentu\n"
        fitur5 = "5. Menandai bahwa suatu task sudah selesai dikerjakan\n"
        fitur6 = "6. Menampilkan opsi help yang difasilitasi oleh assistant\n"
        fitur7 = "7. Mendefinisikan list kata penting terkait apakah itu merupakan suatu task atau tidak\n"
        fitur8 = "8. Menampilkan pesan error jika pesan tidak dikenali\n"
        fitur9 = "9. Memberikan rekomendasi kata apabila ada typo dari user\n"
        daftar_kata_penting = "[DAFTAR KATA PENTING]\n1. Kuis\n2. Ujian\n3. Tucil\n4. Tubes\n5. Praktikum"
        string = header+fitur1+fitur2+fitur3+fitur4+fitur5+fitur6+fitur7+fitur8+fitur9+daftar_kata_penting
    return yes, string

# input array of words, return array contains keywords
def detectTugas(message):
    mylist = cleanStopWord(message)
    newlist = list(filter(r.match, mylist)) 
    return newlist

def detectTopik(userMessage, key):
    # input str // diasumsiin topik selalu diantara :
    # 1) kode matkul ... pada
    # 2) kode matkul ... tanggal/tgl (ini kalo "pada" tidak ditemukan)
    # adalagi..?
    if (boyer_moore(userMessage,"pada") != -1): 
        part = userMessage.partition("pada")
        # print(part)
        part1 = part[0].partition(key) # asumsi
        return part1
    else:
        if (boyer_moore(userMessage,"tanggal") != -1):
            part = userMessage.partition("tanggal")
            # print(part)
            part1 = part[0].partition(key) # asumsi
            return part1
        elif (boyer_moore(userMessage,"tgl") != -1):
            part = userMessage.partition("tgl")
            # print(part)
            part1 = part[0].partition(key) # asumsi
            return part1

def rawString(arrtup):
    title = ""
    data = arrtup
    for i in range (len(data)):
        tgs = data[i]
        title = title + ("{}. (ID : {}) {} - {} - {} - {}".format(i+1,tgs[0],tgs[1],tgs[2],tgs[3],tgs[4])) + "\n"
    return title

def printDeadline(arrtup):
    print(rawString(arrtup))

def incrementDate(date, daysduration):
    date += datetime.timedelta(days=daysduration)
    return date

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def replace_all(text, array):
    for dic in array:
        text = text.replace(dic[0],dic[1])
    return text

def allDates(string_date):
    rawDate = find_date(string_date)
    # print("rawDate :",rawDate)
    alldates = []
    if(len(rawDate)==0):
        pass
    elif(len(rawDate)>1):
        angka = rawDate[0]
        huruf = rawDate[1]
        for a in angka:
            alldates.append(convert_to_date(a))
        for h in huruf:
            alldates.append(convert_string_to_date(h))
    else:
        # cuma 1 jenis tanggal
        for i in range (len(rawDate[0])):
            if(re.search("/",rawDate[0][0])):
                alldates.append(convert_to_date(rawDate[0][i]))
            else:
                alldates.append(convert_string_to_date(rawDate[0][i]))
    return alldates

# BOT RESPONSE: return string
def get_bot_response(userMessage):
    response = ""

    b1, r1 = isFitur1(userMessage)
    b2, r2 = isFitur2(userMessage)
    b3, r3 = isFitur3(userMessage)
    b4, r4 = isFitur4(userMessage)
    b5, r5 = isFitur5(userMessage)
    b6, r6 = isFitur6(userMessage)

    # fitur tambahan ngide hehe
    demot = find_demot_keyword(userMessage)

    if(b1):
        if(r1!=""):
            response = "[TASK BERHASIL DICATAT]\n" + r1
        else:
            response = "Tugas sudah tercatat di database"

    elif(b2):
        if(r2!=""):
            response = "[DAFTAR DEADLINE]\n"+ r2
        else:
            response = "Tidak terdapat deadline pada waktu tersebut"

    elif(b3):
        if(r3!=""):
            response = r3
        else:
            response = "Maaf, matkul atau jenis tugas tidak ditemukan"

    elif(b4):
        response = r4

    elif(b5):
        response = r5

    elif(b6):
        response = r6
    
    elif(demot != -1):
        response = "Semangat yaaa pasti bisa kok :D"

    else: # fitur 8 & fitur 9
        # typo / pesan tidak dikenali
        # print("masuk ke else!!!!!")
        list_suggestions = []
        message = cleanStopWord(userMessage)
        for word in message:
            recommended_word = word_recommendation(word,all_keywords+load_text("keywords"))
            if (recommended_word != ""):
                list_suggestions.append([word,recommended_word])
        # pesan tidak dikenali
        if (len(list_suggestions) == 0):
            response = pesan_operator()
        # ada typo
        else:
            # HARUSNYA UDAH BENER
            for pair in list_suggestions:
                new_user_message = replace_all(userMessage,list_suggestions)
                response = 'Mungkin maksudmu: "' + new_user_message + '"'
    if response is not None:
        response = "<br />".join(response.split("\n"))
        response = "&emsp;".join(response.split("\t"))
    else:
        response = pesan_operator()
    return response

def pesan_operator():
    string = '''Maaf, pesanmu ga bisa dikenali nih
    \t[TIPS]
    <ol style="line-height:80%">
    <li style="line-height:150%">Untuk menambahkan task baru, pastikan pesanmu memiliki komponen sebagai berikut:
    <ul style="line-height:80%">
    <li>Tanggal (format: DD/MM/YYYY atau dalam bahasa Indonesia) </li>
    <li>Kode matkul (format: XXYYYY, X:huruf, Y:angka)</li>
    <li>Jenis tugas</li>
    <li>Topik tugas</li>
    </ul>
    Agar pesanmu dapat terdeteksi, pastikan topik tugas berada diantara kode matkul dan tanggal (contoh:[kode matkul] [topik] pada [tanggal])
    </li>
    <li style="line-height:150%">Kombinasikan keyword 'deadline' dalam pesanmu untuk melihat deadline dari task yang ada</li>
    <li style="line-height:150%">Kombinasikan keyword 'kapan' dan 'deadline' untuk memperoleh tanggal deadline dari task dengan kode matkul tertentu</li>
    </ol>'''
    return string