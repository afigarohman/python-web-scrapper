import pandas as pd
import matplotlib.pyplot as plt

# 1. LOAD DATA
try:
    df = pd.read_csv("hasil_buku.csv")
    
    # --- BAGIAN PERBAIKAN (DEBUGGING) ---
    print("Nama kolom asli:", df.columns.tolist())
    
    # Hapus spasi di awal/akhir nama kolom (misal: 'Harga ' jadi 'Harga')
    df.columns = df.columns.str.strip()
    
    print("Nama kolom setelah dibersihkan:", df.columns.tolist())
    # ------------------------------------

    print("\n--- Data Awal ---")
    print(df.head())

    # 2. DATA CLEANING (Pembersihan Isi Data)
    # Hapus '£' dan ubah jadi angka
    # Kita gunakan try-except agar kalau ada error di baris tertentu, kita tahu
    
    # Cek apakah kolom 'Harga' benar-benar ada sekarang
    if 'Harga' in df.columns:
        df['Harga'] = df['Harga'].str.replace('£', '')
        df['Harga'] = df['Harga'].astype(float)
        
        # 3. ANALISIS DATA
        rata_rata = df['Harga'].mean()
        termahal = df['Harga'].max()
        termurah = df['Harga'].min()

        print("\n--- Hasil Analisis ---")
        print(f"Rata-rata Harga Buku: £{rata_rata:.2f}")
        print(f"Buku Termahal: £{termahal}")
        print(f"Buku Termurah: £{termurah}")

        # Cari judul buku yang paling mahal
        buku_sultan = df[df['Harga'] == termahal]
        
        # Kita pakai .iloc[0] untuk mengambil baris pertama saja biar rapi
        judul_sultan = buku_sultan.iloc[0]['Judul Buku'] if 'Judul Buku' in df.columns else buku_sultan.iloc[0]['judul buku']
        
        print(f"Judul Buku Termahal: {judul_sultan}")

        # 4. VISUALISASI DATA
        plt.figure(figsize=(10, 6))
        plt.hist(df['Harga'], bins=10, color='skyblue', edgecolor='black')
        plt.title('Distribusi Harga Buku')
        plt.xlabel('Harga (£)')
        plt.ylabel('Jumlah Buku')
        plt.grid(axis='y', alpha=0.75)
        
        plt.savefig("grafik_harga.png")
        print("\nGrafik berhasil disimpan sebagai 'grafik_harga.png'")
        
    else:
        print("\nERROR: Kolom 'Harga' masih tidak ditemukan. Cek nama kolom di atas.")

except Exception as e:
    print(f"\nTerjadi Error: {e}")