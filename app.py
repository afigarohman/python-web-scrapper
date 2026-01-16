import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# KONFIGURASI HALAMAN (Judul Tab Browser & Icon)
st.set_page_config(
    page_title="Dashboard Analisa Buku",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------------------------
# JUDUL DAN DESKRIPSI
st.title("📚 Dashboard Analisa Pasar Buku")
st.markdown("Aplikasi ini menampilkan hasil scraping data dari **Books to Scrape** secara interaktif.")
st.markdown("---") # Garis pemisah

# ---------------------------------------------------------
# FUNGSI LOAD DATA (Supaya tidak reload ulang terus)
@st.cache_data
def load_data():
    # Load CSV
    df = pd.read_csv("buku_detail_lengkap.csv")
    
    # Cleaning Data (Sama seperti logic sebelumnya)
    # 1. Bersihkan Harga
    if 'Harga' in df.columns:
        df['Harga_Num'] = df['Harga'].astype(str).str.replace('£', '').astype(float)
    
    # 2. Bersihkan Stok (Ambil angkanya saja)
    # Kita pakai regex sederhana langsung di sini
    df['Stok_Num'] = df['Stok'].str.extract('(\d+)').astype(float)
    
    # 3. Total Aset
    df['Total_Aset'] = df['Harga_Num'] * df['Stok_Num']
    
    return df

# Memanggil fungsi load data
try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'buku_detail_lengkap.csv' tidak ditemukan. Harap jalankan scraper.py terlebih dahulu!")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR (FILTERING)
st.sidebar.header("🎛️ Filter Data")

# Filter 1: Rentang Harga (Slider)
min_price = float(df['Harga_Num'].min())
max_price = float(df['Harga_Num'].max())

selected_price = st.sidebar.slider(
    "Maksimal Harga (£):", 
    min_value=min_price, 
    max_value=max_price, 
    value=max_price # Defaultnya mentok kanan
)

# Filter 2: Ketersediaan Stok (Radio Button)
stok_option = st.sidebar.radio(
    "Filter Stok:",
    ("Semua Buku", "Stok Banyak (>15)", "Stok Sedikit (<=15)")
)

# ---------------------------------------------------------
# LOGIC FILTERING (Menerapkan pilihan user ke Tabel)
filtered_df = df[df['Harga_Num'] <= selected_price]

if stok_option == "Stok Banyak (>15)":
    filtered_df = filtered_df[filtered_df['Stok_Num'] > 15]
elif stok_option == "Stok Sedikit (<=15)":
    filtered_df = filtered_df[filtered_df['Stok_Num'] <= 15]

# ---------------------------------------------------------
# MENAMPILKAN METRIK UTAMA (KOTAK ANGKA)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Buku", f"{len(filtered_df)} Judul")
with col2:
    avg_price = filtered_df['Harga_Num'].mean()
    st.metric("Rata-rata Harga", f"£{avg_price:.2f}")
with col3:
    total_asset = filtered_df['Total_Aset'].sum()
    st.metric("Potensi Omzet", f"£{total_asset:,.0f}")

st.markdown("---")

# ---------------------------------------------------------
# VISUALISASI & TABEL
col_kiri, col_kanan = st.columns([2, 1]) # Kiri lebih lebar

with col_kiri:
    st.subheader("📊 Distribusi Harga Buku")
    
    # Membuat Grafik dengan Matplotlib di dalam Streamlit
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_df['Harga_Num'], bins=20, kde=True, color='skyblue', ax=ax)
    ax.set_xlabel("Harga (£)")
    ax.set_ylabel("Jumlah Buku")
    
    # Menampilkan grafik ke web
    st.pyplot(fig)

with col_kanan:
    st.subheader("🏆 Top 5 Termahal")
    # Menampilkan tabel kecil (Top 5) tanpa index
    top_5 = filtered_df.nlargest(5, 'Harga_Num')[['Judul', 'Harga']]
    st.table(top_5)

# Menampilkan Tabel Lengkap di Bawah
st.subheader("📋 Database Lengkap")
st.dataframe(filtered_df[['Judul', 'Harga', 'Stok', 'Deskripsi']])