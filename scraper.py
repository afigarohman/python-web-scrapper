import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # Library wajib untuk mengatur jeda waktu

# 1. Persiapan
data_semua_buku = []
base_url = "http://books.toscrape.com/catalogue/page-{}.html"

# Kita akan mengambil data dari halaman 1 sampai 5
# range(1, 6) artinya: mulai dari 1, berhenti SEBELUM 6 (jadi 1,2,3,4,5)
halaman_awal = 1
halaman_akhir = 5

print(f"Memulai scraping dari halaman {halaman_awal} sampai {halaman_akhir}...")
print("-" * 40)

# 2. Proses Looping (Perulangan) per Halaman
for halaman in range(halaman_awal, halaman_akhir + 1):
    # Membuat URL dinamis: page-1.html, page-2.html, dst
    url_saat_ini = base_url.format(halaman)
    
    print(f"Sedang mengambil data dari: Halaman {halaman}")
    
    try:
        response = requests.get(url_saat_ini)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            books = soup.find_all("article", class_="product_pod")
            
            # Loop untuk setiap buku di halaman tersebut
            for book in books:
                # Ambil Judul
                title = book.find("h3").find("a")["title"]
                
                # Ambil Harga
                price = book.find("p", class_="price_color").text
                
                # Masukkan ke keranjang besar
                data_semua_buku.append({
                    "Judul Buku": title,
                    "Harga": price
                })
        else:
            print(f"--> Gagal membuka halaman {halaman}")
            
    except Exception as e:
        print(f"--> Terjadi error di halaman {halaman}: {e}")
    
    # PENTING: Tidur dulu 1 detik sebelum lanjut ke halaman berikutnya
    # Ini etika scraping agar tidak membebani server
    time.sleep(1)

# 3. Penyimpanan Data
print("-" * 40)
print("Proses Selesai!")

if len(data_semua_buku) > 0:
    # Simpan ke file CSV baru biar file lama tidak tertimpa (opsional)
    filename = "hasil_buku_banyak.csv"
    df = pd.DataFrame(data_semua_buku)
    df.to_csv(filename, index=False)
    
    print(f"Berhasil mendapatkan total {len(data_semua_buku)} buku.")
    print(f"Data disimpan ke file: {filename}")
else:
    print("Tidak ada data yang didapatkan.")