import streamlit as st
import pandas as pd

# Setting Halaman Lebar
st.set_page_config(layout="wide", page_title="Madiun Digital Library", page_icon="📚")

# CSS HACK: Agar tampilan kotak-kotak rapi (Card Style)
st.markdown("""
<style>
    div[data-testid="column"] {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        transition: transform 0.2s;
    }
    div[data-testid="column"]:hover {
        transform: scale(1.02);
        background-color: #eef2f5;
    }
    img { border-radius: 5px; }
    h3 { text-align: center; }
</style>
""", unsafe_allow_html=True)

# LOAD DATA
try:
    # Membaca file CSV yang sudah ada gambarnya
    df = pd.read_csv("buku_dengan_gambar.csv")
except:
    st.error("⚠️ File data tidak ditemukan! Jalankan 'python scraper.py' dulu.")
    st.stop()

# JUDUL WEBSITE
st.title("📚 Madiun Digital Library")
st.write("Perpustakaan digital modern dengan teknologi Python.")
st.markdown("---")

# MENU FILTER (Pencarian & Harga)
col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("🔍 Cari Judul Buku...", placeholder="Ketikan sesuatu...")
with col2:
    max_price = st.slider("💰 Filter Harga (£)", 0, 100, 100)

# LOGIKA FILTER
if search:
    df = df[df['Judul'].str.contains(search, case=False)]

# Filter Harga (Bersihkan simbol £ dulu)
df['Harga_Num'] = df['Harga'].astype(str).str.replace('£','').astype(float)
df = df[df['Harga_Num'] <= max_price]

# TAMPILAN GRID (NETFLIX STYLE)
st.subheader(f"Menampilkan {len(df)} Buku")

# Kita bagi jadi 4 kolom per baris
cols = st.columns(4)

for index, row in df.iterrows():
    # Tentukan data ini masuk kolom ke berapa (0, 1, 2, atau 3)
    with cols[index % 4]:
        # Tampilkan Gambar
        if pd.notna(row['Gambar']):
            st.image(row['Gambar'], use_container_width=True)
        
        # Tampilkan Judul (Dipotong kalau kepanjangan)
        judul_pendek = row['Judul'][:25] + "..." if len(row['Judul']) > 25 else row['Judul']
        st.markdown(f"**{judul_pendek}**")
        
        # Harga & Stok
        st.caption(f"🏷️ {row['Harga']} | 📦 {row['Stok']}")
        
        # Tombol
        st.button("Pinjam", key=f"btn_{index}")
        st.markdown("---")