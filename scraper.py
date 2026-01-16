import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# --- BAGIAN 1: FUNGSI KHUSUS PENGINTIP DETAIL ---
def get_book_detail(book_url):
    """
    Fungsi ini bertugas masuk ke link buku, mengambil deskripsi & stok,
    lalu kembali membawa data tersebut.
    """
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # 1. Ambil Deskripsi
            desc_header = soup.find("div", id="product_description")
            if desc_header:
                # .find_next_sibling() adalah perintah: "Ambil tetangga sebelah bawahmu"
                description = desc_header.find_next_sibling("p").text
            else:
                description = "Tidak ada deskripsi"
            
            # 2. Ambil Stok
            # Biasanya textnya: "In stock (22 available)"
            stock_element = soup.find("p", class_="instock availability")
            stock = stock_element.text.strip() if stock_element else "Unknown"
            
            # Kembalikan hasil dalam bentuk paket (Dictionary)
            return {
                "Deskripsi": description[:100] + "...", 
                "Stok": stock
            }
    except Exception as e:
        print(f"Error ambil detail: {e}")
    
    return {"Deskripsi": "-", "Stok": "-"}


# --- BAGIAN 2: PROGRAM UTAMA (MAIN LOOP) ---

data_lengkap = []
base_url_page = "http://books.toscrape.com/catalogue/page-{}.html"
base_url_book = "http://books.toscrape.com/catalogue/"

halaman_awal = 1
halaman_akhir = 1 

print(f"🕵️  Memulai DEEP SCRAPING (Halaman {halaman_awal} - {halaman_akhir})...")
print("Ini akan memakan waktu lebih lama karena kita masuk ke setiap buku.")

for halaman in range(halaman_awal, halaman_akhir + 1):
    url_page = base_url_page.format(halaman)
    print(f"\n📂 Membuka Daftar: Halaman {halaman}")
    
    response = requests.get(url_page)
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    counter = 1
    for book in books:
        # 1. Ambil Data Dasar (Judul & Harga)
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text
        
        # 2. Ambil Link Buku (URL Relative)
        relative_url = book.find("h3").find("a")["href"]
        
        if "catalogue/" in relative_url:
             full_book_url = "http://books.toscrape.com/" + relative_url
        else:
             full_book_url = base_url_book + relative_url
            
        print(f"   [{counter}/20] Mengintip: {title[:30]}...")
        
        # 3. PANGGIL FUNGSI DETAIL (Bagian Deep Scraping)
        detail_data = get_book_detail(full_book_url)
        
        # 4. Gabungkan semua data
        data_lengkap.append({
            "Judul": title,
            "Harga": price,
            "Stok": detail_data["Stok"],         
            "Deskripsi": detail_data["Deskripsi"], 
            "URL Link": full_book_url
        })
        
        counter += 1
        time.sleep(0.5)

# Simpan ke CSV
df = pd.DataFrame(data_lengkap)
df.to_csv("buku_detail_lengkap.csv", index=False)

print("\n" + "="*40)
print("✅ SELESAI!")
print("Cek file 'buku_detail_lengkap.csv' untuk melihat Stok dan Deskripsi.")