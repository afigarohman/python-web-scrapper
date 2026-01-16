import pandas as pd
import matplotlib.pyplot as plt
import re  # Library Regex (Pencari Pola Teks)

def bersihkan_stok(teks_stok):
    """
    Mengubah 'In stock (22 available)' menjadi angka 22.
    """
    # Pola regex: \d+ artinya "cari angka apa saja"
    angka = re.findall(r'\d+', teks_stok)
    if angka:
        return int(angka[0]) # Ambil angka pertama yang ketemu
    return 0

# 1. LOAD DATA BARU
filename = "buku_detail_lengkap.csv"
try:
    df = pd.read_csv(filename)
    
# 2. DATA CLEANING

    # A. Bersihkan Harga
    df['Harga_Clean'] = df['Harga'].astype(str).str.replace('£', '').astype(float)
    
    # B. Bersihkan Stok (Pakai fungsi regex)
    # .apply() artinya: Terapkan fungsi ini ke SETIAP baris
    df['Stok_Clean'] = df['Stok'].apply(bersihkan_stok)
    
    # C. Hitung Nilai Aset (Harga x Stok)
    df['Total_Aset'] = df['Harga_Clean'] * df['Stok_Clean']

    # 3. ANALISIS BISNIS
    total_buku_fisik = df['Stok_Clean'].sum()
    rata_stok = df['Stok_Clean'].mean()
    total_nilai_tokopedia = df['Total_Aset'].sum()
    
    print(f"\n--- LAPORAN GUDANG ({len(df)} Jenis Buku) ---")
    print(f"Total Buku Fisik di Gudang : {total_buku_fisik} pcs")
    print(f"Rata-rata Stok per Judul   : {rata_stok:.0f} pcs")
    print(f"Total Nilai Aset (Omzet)   : £{total_nilai_tokopedia:,.2f}")
    
    print("\n--- TOP 5 BUKU DENGAN STOK TERBANYAK ---")
    top_stok = df.nlargest(5, 'Stok_Clean')
    print(top_stok[['Judul', 'Stok_Clean', 'Harga']])

    # 4. VISUALISASI (SCATTER PLOT)
    plt.figure(figsize=(10, 6))
    
    # Membuat Scatter Plot (Titik-titik penyebaran)
    plt.scatter(df['Harga_Clean'], df['Stok_Clean'], color='purple', alpha=0.7)
    
    plt.title('Hubungan Harga Buku vs Ketersediaan Stok')
    plt.xlabel('Harga Buku (£)')
    plt.ylabel('Jumlah Stok')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.savefig("grafik_stok_vs_harga.png")
    print("\nGrafik analisis disimpan sebagai 'grafik_stok_vs_harga.png'")

except FileNotFoundError:
    print(f"File {filename} tidak ditemukan. Jalankan scraper dulu!")