import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_book_detail(book_url):
    try:
        response = requests.get(book_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Ambil Stok
            stock_element = soup.find("p", class_="instock availability")
            stock = stock_element.text.strip() if stock_element else "Unknown"
            
            # Ambil GAMBAR (Link Gambar Sampul)
            img_tag = soup.find("div", class_="item active").find("img")
            raw_img = img_tag["src"].replace("../../", "")
            full_img_url = "http://books.toscrape.com/" + raw_img
            
            return {"Stok": stock, "Gambar": full_img_url}
    except:
        pass
    return {"Stok": "-", "Gambar": "https://via.placeholder.com/150"}

# --- MAIN PROGRAM ---
data_lengkap = []
base_url_page = "http://books.toscrape.com/catalogue/page-{}.html"
base_url_book = "http://books.toscrape.com/catalogue/"

# Kita ambil 1 halaman saja (20 buku) biar cepat untuk demo
for halaman in range(1, 2): 
    print(f"Sedang mengambil data Halaman {halaman}...")
    response = requests.get(base_url_page.format(halaman))
    soup = BeautifulSoup(response.content, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    
    for book in books:
        title = book.find("h3").find("a")["title"]
        price = book.find("p", class_="price_color").text
        
        # Susun Link Detail
        relative_url = book.find("h3").find("a")["href"]
        if "catalogue/" in relative_url:
             full_book_url = "http://books.toscrape.com/" + relative_url
        else:
             full_book_url = base_url_book + relative_url
            
        # Ambil Detail Gambar & Stok
        detail = get_book_detail(full_book_url)
        
        data_lengkap.append({
            "Judul": title,
            "Harga": price,
            "Stok": detail["Stok"],
            "Gambar": detail["Gambar"] # Kolom baru!
        })

# Simpan CSV baru
df = pd.DataFrame(data_lengkap)
df.to_csv("buku_dengan_gambar.csv", index=False)
print("✅ Selesai! Data gambar tersimpan.")