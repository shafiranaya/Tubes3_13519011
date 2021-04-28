# Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant
> Tubes 3 IF2111 Strategi Algoritma

## Table of contents
  - [General Info](#general-info)
  - [Requirements](#requirements)
  - [Setup](#setup)
  - [How To Use](#how-to-use)
  - [Screenshots](#screenshots)
  - [Features](#features)
  - [Status](#status)
  - [Contact](#contact)

## General Info
Chatbot yang dibangun adalah Deadline Reminder Assistant (asisten pengingat deadline). Chatbot sederhana ini berfungsi untuk membantu mengingat berbagai deadline, tanggal penting, dan task-task tertentu kepada user yang menggunakannya.
Chatbot dibangun dengan memanfaatkan algoritma String Matching yaitu Boyer Moore dan Regular Expression.

## Requirements
- Python3
- Flask
- Sqlite3
- Sastrawi

Requirements di atas dapat diinstall dengan mengetikkan ini pada terminal:
```
pip3 install python3
pip3 install flask
pip3 install sqlite3
pip3 install sastrawi
```

## Setup
1. Unzip folder
2. Buka terminal di directory penyimpanan yang sesuai
3. Masuk ke folder berisi source code dengan mengetikkan di terminal:
   ```
   cd src
   ```
4. Jalankan program dengan mengetikkan di terminal:
   ```
   python3 app.py
   ```
## How to Use
1. Untuk menambahkan task baru, pastikan pesanmu memiliki komponen sebagai berikut:
   - Tanggal (format: DD/MM/YYYY atau dalam bahasa Indonesia)
   - Kode matkul (format: XXYYYY, X:huruf kapital, Y:angka)
   - Jenis tugas
   - Topik tugas
   Agar pesanmu dapat terdeteksi, pastikan topik tugas berada diantara kode matkul dan tanggal (contoh:[kode matkul] [topik] pada [tanggal])
2. Kombinasikan keyword 'deadline' dalam pesanmu untuk melihat deadline dari task yang ada
3. Kombinasikan keyword 'kapan' dan 'deadline' untuk memperoleh tanggal deadline dari task dengan kode matkul tertentu
   
## Screenshots
![alt text](https://i.imgur.com/F4XjGaC.png)

## Features
1. Fitur 1 - Menambahkan task baru
2. Fitur 2 - Melihat daftar task yang harus dikerjakan
3. Fitur 3 - Menampilkan deadline dari suatu task tertentu
4. Fitur 4 - Memperbaharui task tertentu
5. Fitur 5 - Menandai bahwa suatu task sudah selesai dikerjakan
6. Fitur 6 - Menampilkan opsi help yang difasilitasi oleh assistant
7. Fitur 7 - Mendefinisikan list kata penting terkait apakah itu merupakan suatu task atau tidak
8. Fitur 8 - Menampilkan pesan error jika pesan tidak dikenali
9. Fitur 9 - Memberikan rekomendasi kata apabila terdapat typo (BONUS)

## Status
Project is belum selesai

## Contact
Created by: 
- Jesica - 13519011 - K-1 - ([@jestsee](https://www.github.com/jestsee))
- Shafira Naya Aprisadianti - 13519040 - K-1 - ([@shafiranaya](https://www.github.com/shafiranaya))
- Delisha Azza Naadira - 13519133 - K-3 -  ([@delishaandr](https://www.github.com/delishaandr))
