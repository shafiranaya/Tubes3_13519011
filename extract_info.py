import re
import datetime

today_date = datetime.date.today()
print(today_date)

kata_penting = ["kuis","ujian","tucil","tubes","praktikum"]
tambahtask1 = "Tubes IF2211 String Matching pada 14 November 2021"
tambahtask2 = "Halo bot, tolong ingetin kalau ada kuis IF3110 Bab 2 sampai 3 pada 22/04/2021"
tambahtask3 = "Halo bot, tolong ingetin kalau ada tugas TL2105 Litosfer pada 22/05/21" # tes format date lain, GAUSAH DEH
lihat1 = "Apa saja deadline yang dimiliki sejauh ini?"
lihat2 = "Ada deadline apa saja antara 03/04/2021 sampai 15/04/2021?"
lihat3 = "Deadline 2 minggu ke depan apa saja?"
lihat4 = "Deadline 13 hari ke depan apa saja?"
lihat5 = "Apa saja deadline hari ini?"
lihat6 = "5 minggu ke depan ada tubes apa saja?"
deadline1 = "Deadline tugas IF2211 itu kapan?"
update1 = "Deadline 4 diundur menjadi 28/04/2021"
done1 = "Saya sudah selesai mengerjakan task 3"

help1 = "Apa yang bisa assistant lakukan?"
error1 = "apakah mayones sebuah instrumen?"
error2 = "skdhfakjdfhak hfkj ahklskfa"
error3 = "halo, apa kabar?"
error4 = "mari kita coba"

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

def is_date1(string_date):
    return bool(re.match(r"([\d]{1,2}/[\d]{1,2}/[\d]{4})", string_date))
print(is_date1('13/11/2001'))

def is_date2(string_date):
    return bool(re.match(r"(\d{1,2} (?:januari|februari|maret|april|mei|juni|juli|agustus|september|oktober|november|desember) \d{4})", string_date))
print(is_date2('10 april 2021'))

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
print("hasil convert : ",convert_string_to_date("14 april 2021"))

# Fungsi untuk convert dari format "13/11/2001" ke date
def convert_to_date(string_date):
    d,m,y = [int(x) for x in string_date.split('/')]
    dates = datetime.date(y,m,d)
    return dates
print(convert_to_date('13/11/2001'))

# TODO bingung nge-extract task_title nya (sebelum 'pada'?) // mungkin iya, udah nyoba buat tp gatau bener apa ngga wkwk
# def find_task_title(text):
#     task_title = re.findall(r"([A-Z][A-Z]\d{4})", text)

# TODO pake KMP/Boyer Moore. Jenis task: tubes,tucil, dll // harus pake KMP/BM bukan regex?
# def find_task(text):
    # task = re.findall(r"([A-Z][A-Z]\d{4})", text.lower())

# TODO mungkin nanti bakal return idnya aja? gatau 
# return task_id nya aja
# masih bug???
def find_task_id(text):
    task_id = re.findall(r"((?:task) \d{1,2})", text.lower())
    # return task_id
    id = -99
    if(len(task_id)!=0):
        id = int(re.search(r'\d+', task_id[0]).group())
    t_id = []
    t_id.append(id)
    return t_id
print("ID = ",find_task_id(update1))

def find_course_id(text):
    course_id = re.findall(r"([A-Z][A-Z]\d{4})", text)
    return course_id

print(find_course_id(tambahtask2))
print(find_course_id(tambahtask3))

# return list of duration
def find_duration(text):
    duration = re.findall(r"(\d{1,2} (?:minggu|pekan|hari|bulan|hari ini))", text.lower()) 
    return duration

# return integer yaitu durasinya dalam hari
def convert_duration_to_days(duration_string):
    duration_list = duration_string[0].split()
    if (duration_list[1] == "hari"):
        days = int(duration_list[0]) * 1
    elif (duration_list[1] == "hari ini"):
        days = 1
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
    listkata = ['undur', 'ubah', 'maju', 'ganti', 'update']
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
    listkata = ['selesai', 'done', 'udah', 'kumpul']
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
    listkata = ['help', 'command', 'daftar', 'cara', 'fitur', 'assistant']
    idx = -1
    i = 0
    while (i < len(listkata)):
        idx = boyer_moore(text, listkata[i])
        if idx != -1:
            break
        else:
            i = i + 1
    return idx

# TODO gabungin semua method find, masukin ke satu list of keywords. return list_of_keywords
# def extract_info(user_text):

print(find_date(tambahtask1))
print(find_duration(lihat3))
print(convert_duration_to_days(find_duration(lihat3)))
print(find_duration(lihat4))
print("Update: " + str(find_update_keyword(update1)))
print("Done: " + str(find_done_keyword(done1)))
print("Help: " + str(find_help_keyword(help1)))

# def print_matrix(matrix):
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             print(matrix[i][j],end=" ")
#         print()

# COBA
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
# If the last characters of both strings are the same, 
# then the edit distance is equal to the edit distance of the same two strings, up to their second-to-last character.
# If the last character is different, 
# then the edit distance is equal to the minimum of the cost of inserting, deleting, or replacing the last character of string a.
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
print(levenshtein_distance("deadline","deadline"))
# print(similarity("deadline","deadline"))

# TODO masih belom fix
# BIKIN TXT ISI SEMUA WORDS YANG MUNGKIN selain keywords??
# Implementasi:
# Jadi pertama di extract kan terus dapet kata2. 
# trus untuk kata2 sisanya yg ga ke extract, cek apakah itu typo apa engga. 
# (pake word_recommendation(string, array))
# kalo recommended_words nya empty yaudah gak return apa2
# kalo gak empty kasih tau kalo typo, kasih kata2nya
# return satu saja recommended word nya
def word_recommendation(string, array):
    # TODO array-nya itu berisi semua keywords yang kita punya ?? atau kayak bahasa indonesia gatau
    # atau bisa juga buat txt yang isinya semua kata-kata yang mungkin gitu, jadinya iterate ke txt tsb bukan ke array
    recommended_words = []
    for word in array:
        if similarity(string, word) > 0.75:
            recommended_words.append([word,similarity(string,word)])
    # Karena nanti yang diambil cuma kata yang paling mirip (di kasus khusus misal ada lebih dari satu kata yang mirip)
    recommended_words = sorted(recommended_words, key=lambda x: x[1], reverse=True)
    return recommended_words[0][0]

# def check_typo(word, keywords):
#     recommended_words = word_recomendation(word, keywords)
#     if (len(recommended_words)) == 0:
#         return False, recommended_words[0]
#     else:
#         return True, ""

print(word_recommendation("dedline",["deadline","dedline","tugas","shafira","ngasal"]))

print("bm : ",find_update_keyword("ya halo diundur ya"))