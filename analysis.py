import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD DATA BARU
filename = "hasil_buku_banyak.csv"  # <-- Kita ubah ke file yang datanya 100 biji
try:
    df = pd.read_csv(filename)
    
    # Bersihkan nama kolom (hapus spasi ekstra)
    df.columns = df.columns.str.strip()
    
    # 2. DATA CLEANING
    if 'Harga' in df.columns:
        # Hapus '£' dan ubah jadi angka float
        df['Harga'] = df['Harga'].str.replace('£', '')
        df['Harga'] = df['Harga'].astype(float)
        
        # 3. ANALISIS DATA
        rata_rata = df['Harga'].mean()
        print(f"\n--- HASIL ANALISIS ({len(df)} Buku) ---")
        print(f"Rata-rata Harga: £{rata_rata:.2f}")
        
        # Fitur Baru: Top 5 Buku Termahal
        print("\nTop 5 Buku Termahal:")
        top_5 = df.nlargest(5, 'Harga')
        for index, row in top_5.iterrows():
            print(f"- {row['Judul Buku']} (£{row['Harga']})")

        # 4. VISUALISASI DATA
        plt.figure(figsize=(10, 6))
        
        # Histogram
        plt.hist(df['Harga'], bins=20, color='#4CAF50', edgecolor='black')
        
        # Menambahkan garis rata-rata (garis merah putus-putus)
        plt.axvline(rata_rata, color='red', linestyle='dashed', linewidth=2, label=f'Rata-rata: £{rata_rata:.2f}')
        
        plt.title(f'Distribusi Harga {len(df)} Buku')
        plt.xlabel('Harga (£)')
        plt.ylabel('Jumlah Buku')
        plt.legend()
        plt.grid(axis='y', alpha=0.5)
        
        plt.savefig("grafik_harga.png")
        print("\nGrafik berhasil disimpan sebagai 'grafik_harga.png'")
        
    else:
        print("Kolom 'Harga' tidak ditemukan.")

except FileNotFoundError:
    print(f"File {filename} tidak ditemukan. Jalankan scraper.py dulu!")