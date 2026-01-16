import requests
from bs4 import BeautifulSoup  # Kita panggil alat bedahnya
import pandas as pd

url = "http://books.toscrape.com/"
response = requests.get(url)

if response.status_code == 200:
    # 1. Ubah data mentah (HTML) menjadi objek 'soup' agar bisa dibaca Python
    soup = BeautifulSoup(response.content, "html.parser")
    # 2. Cari semua wadah buku.
    # Di website ini, setiap buku dibungkus dalam tag <article> dengan class "product_pod"
    books = soup.find_all("article", class_="product_pod")
    data_buku = []

    
    # 3. Looping (perulangan) untuk membongkar setiap buku satu per satu
    for book in books:
        # Mengambil Judul
        # Judul ada di dalam tag <h3>, lalu di dalam tag <a>, atribut 'title'
        title_element = book.find("h3").find("a")
        title = title_element["title"] # Kita ambil isi atribut 'title' biar lengkap
        
        # Mengambil Harga
        # Harga ada di tag <p> dengan class "price_color"
        price_element = book.find("p", class_="price_color")
        price = price_element.text # Kita ambil teksnya saja (misal: £51.77)
        
        data_buku.append({
            "judul buku": title,
            "Harga": price
        })

        df = pd.DataFrame(data_buku)
        df.to_csv("hasil_buku.csv", index=False)

        print("berhasil, data telah disimpan ke 'hasil_buku.csv")
        print("Total data: {len(data_buku)} buku")
else:
    print("Gagal terhubung.")