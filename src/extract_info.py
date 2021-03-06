import re
import datetime

# kata_penting = ["kuis","ujian","tucil","tubes","praktikum"]
# tambahtask1 = "Tubes IF2211 String Matching pada 14 November 2021" # TODO FIX. harusnya kl udah ada di database, jgn task berhasil dicatat
# tambahtask2 = "Halo bot, tolong ingetin kalau ada kuis IF3110 Bab 2 sampai 3 pada 22/04/2021" # TODO FIX. harusnya kl udah ada di database, jgn task berhasil dicatat
# lihat1 = "Apa saja deadline yang dimiliki sejauh ini?"
# lihat2 = "Ada deadline apa saja antara 03/04/2021 sampai 15/04/2021?"
# lihat3 = "Deadline 2 minggu ke depan apa saja?" # TODO FIX
# lihat4 = "Deadline 13 hari ke depan apa saja?" # TODO FIX
# lihat5 = "Apa saja deadline hari ini?" # TODO fix
# lihat6 = "5 minggu ke depan ada tubes apa saja?" # TODO fix
# deadline1 = "Deadline tugas IF2211 itu kapan?"
# update1 = "Deadline 4 diundur menjadi 28/04/2021"
# done1 = "Saya sudah selesai mengerjakan task 3" 

# help1 = "Apa yang bisa assistant lakukan?"
# error1 = "apakah mayones sebuah instrumen?"
# error2 = "skdhfakjdfhak hfkj ahklskfa"
# error3 = "halo, apa kabar?"
# error4 = "mari kita coba"

def load_text(file_name):
    file_to_open = file_name + ".txt"
    f = open("../test/" + file_to_open, "r")
    array_of_words = f.read().splitlines()
    return array_of_words
# load_text("keywords")

# find date dengan format date yang diterima: "13 November 2001", "13/11/2001"
def find_date(text):
    date_list = []
    date1 = re.findall(r"([\d]{1,2}/[\d]{1,2}/[\d]{4})", text.lower())
    date2 = re.findall(r"(\d{1,2} (?:januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember) \d{4})",text.lower())
    if (len(date1) != 0):
        date_list.append(date1)
    if (len(date2) != 0):
        date_list.append(date2)
    return date_list
print(find_date("aku lahir 13/11/2001 di jakarta, 12 maret 2021 blabla"))

#  fungsi buat convert "14 april 2021" ke format yang bisa dicompute sama library datetime
def convert_string_to_date(string_date):
    list_date = string_date.split()
    d = int(list_date[0])
    m = list_date[1]
    y = int(list_date[2])
    list_of_month = ['januari','februari','maret','april','mei','juni','juli','agustus','september','oktober','november','desember']
    for i in range(len(list_of_month)):
        if (m == list_of_month[i]):
            m = int(i+1)
    dates = datetime.date(y,m,d)
    return dates
# print("hasil convert : ",convert_string_to_date("14 april 2021"))

# Fungsi untuk convert dari format "13/11/2001" ke date
def convert_to_date(string_date):
    d,m,y = [int(x) for x in string_date.split('/')]
    dates = datetime.date(y,m,d)
    return dates
# print(convert_to_date('13/11/2001'))

# return task_id nya aja, list of integer dan harusnya cuman satu sih.
def find_task_id(text):
    task_id = re.findall(r"((?:task) \d{1,2})", text.lower())
    # return task_id
    id = -99
    if(len(task_id)!=0):
        id = int(re.search(r'\d+', task_id[0]).group())
    t_id = []
    t_id.append(id)
    return t_id
# print("ID = ",find_task_id(update1))

# return list of kode matkul
def find_course_id(text):
    course_id = re.findall(r"([a-zA-Z][a-zA-Z]\d{4})", text)
    return course_id

# return list of duration
def find_duration(text):
    duration = re.findall(r"(\d{1,2} (?:minggu|pekan|hari|bulan))", text.lower()) 
    return duration

# return integer yaitu durasinya dalam hari
def convert_duration_to_days(duration_string):
    duration_list = duration_string[0].split()
    if (duration_list[1] == "hari"):
        days = int(duration_list[0]) * 1
    elif (duration_list[1] == "minggu" or duration_list[1] == "pekan"):
        days = int(duration_list[0]) * 7
    else: # bulan
        days = int(duration_list[0]) * 30
    return days

# return list of last occurence of every letter
def build_last(pattern):
    last = [-1 for i in range(128)]
    for i in range (len(pattern)):
        last[ord(pattern[i])] = i
    return last

# return index of start pattern (-1 if no match)
def boyer_moore(text, pattern):
    last = build_last(pattern)
    m = len(pattern)
    n = len(text)
    i = m - 1
    if i > n - 1:
        return -1
    
    j = m - 1
    while (i <= n - 1):
        if pattern[j] == text[i]:
            if j == 0:
                return i
            else:
                i = i - 1
                j = j - 1
        else:
            lo = last[ord(text[i])]
            i = i + m - min(j, i + lo)
            j = m - 1
    return -1

# cari keyword update dari teks
def find_update_keyword(text):
    # listkata = ['undur', 'ubah', 'maju', 'ganti', 'update']
    listkata = load_text("update_keywords")
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# cari keyword done dari teks
def find_done_keyword(text):
    listkata = load_text("done")
    # listkata = load_text("done_keywords")
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# cari keyword help dari teks
def find_help_keyword(text):
    listkata = load_text("help_keywords")
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# cari keyword deadline dari teks
def find_deadline_keyword(text):
    listkata = load_text("deadline")
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# cari keyword demot dari teks
def find_demot_keyword(text):
    listkata = load_text("demot")
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# return distance (int)
def levenshtein_distance(string1, string2):
    # Membuat matrix
    D = [[0 for i in range(len(string2) + 1)] for j in range(len(string1) + 1)]
    for i in range(len(string1) + 1):
        D[i][0] = i
    for j in range(len(string2) + 1):
        D[0][j] = j
    # Menghitung distance lalu diassign ke tiap cell dalam matrix
    for i in range(1, len(string1) + 1):
        for j in range(1, len(string2) + 1):
            # Jika last char nya sama
            if string1[i - 1] == string2[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            # Jika last char berbeda
            else:
                insertion = D[i][j-1] + 1
                deletion = D[i-1][j] + 1
                replacement = D[i-1][j-1] + 1
                D[i][j] = min(insertion, deletion, replacement)
    # distance adalah cell pojok kanan bawah
    return D[len(string1)][len(string2)]

def similarity(string1, string2):
    similarity = 1 - levenshtein_distance(string1, string2)/ max(len(string1), len(string2))
    return similarity

def word_recommendation(string, array):
    recommended_words = []
    for word in array:
        if (0.75 <= similarity(string, word) < 1):
            recommended_words.append([word,similarity(string,word)])
    # Karena nanti yang diambil cuma kata yang paling mirip (di kasus khusus misal ada lebih dari satu kata yang mirip)
    recommended_words = sorted(recommended_words, key=lambda x: x[1], reverse=True)
    if (len(recommended_words) != 0):
        recommended_word = recommended_words[0][0]
    else:
        recommended_word = ""
    return recommended_word