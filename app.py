import streamlit as st
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

# Set Konfigurasi Halaman Web
st.set_page_config(
    page_title="Sistem Klasifikasi Data Himpunan - LogicFive_F",
    layout="wide"
)

# Title & Header
st.title("📊 Sistem Klasifikasi Data dengan Teori Himpunan")
st.subheader("Kelompok: LogicFive_F | Pertemuan 7 - PJBL-2 Final")
st.markdown("---")

# Data Dummy untuk Web
DATASET_1 = {
    "Basket": {"Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar"},
    "Paduan Suara": {"Citra", "Dewi", "Gita", "Hana", "Indra"},
    "Programming": {"Budi", "Dewi", "Hana", "Joko", "Kiki", "Eko"}
}

DATASET_2 = {
    "Beli Laptop": {"P01", "P02", "P03", "P04", "P05", "P06", "P07"},
    "Beli Mouse": {"P04", "P05", "P08", "P09", "P10"}
}

# Sidebar untuk Pilih Dataset & Operasi
st.sidebar.header("⚙️ Panel Kontrol")
pilihan_dataset = st.sidebar.selectbox("Pilih Dataset:", ["Dataset 1: Peserta Mahasiswa (3 Himpunan)", "Dataset 2: Pelanggan Toko (2 Himpunan)"])

if "Dataset 1" in pilihan_dataset:
    data_aktif = DATASET_1
else:
    data_aktif = DATASET_2

nama_himpunan = list(data_aktif.keys())

# --- BAGIAN 1: TAMPILAN DATASET ---
st.header("1. Himpunan Data")
cols = st.columns(len(data_aktif))
for idx, (nama, isi) in enumerate(data_aktif.items()):
    with cols[idx]:
        st.write(f"**{nama}** (Total: {len(isi)})")
        st.code(", ".join(sorted(list(isi))))

st.markdown("---")

# --- BAGIAN 2: OPERASI HIMPUNAN INTERAKTIF ---
st.header("2. Operasi Himpunan")

col_op1, col_op2 = st.columns(2)

with col_op1:
    himp_A = st.selectbox("Pilih Himpunan A:", nama_himpunan, index=0)
with col_op2:
    himp_B = st.selectbox("Pilih Himpunan B:", nama_himpunan, index=1 if len(nama_himpunan) > 1 else 0)

set_A = data_aktif[himp_A]
set_B = data_aktif[himp_B]

# Kalkulasi
gabungan = set_A | set_B
irisan = set_A & set_B
selisih_AB = set_A - set_B
selisih_BA = set_B - set_A
sym_diff = set_A ^ set_B

# Tampilan Hasil Operasi
res_col1, res_col2 = st.columns(2)
with res_col1:
    st.success(f"**Union ({himp_A} ∪ {himp_B}):**\n\n{sorted(list(gabungan))} (Total: {len(gabungan)})")
    st.info(f"**Intersection ({himp_A} ∩ {himp_B}):**\n\n{sorted(list(irisan))} (Total: {len(irisan)})")
    st.warning(f"**Symmetric Difference ({himp_A} Δ {himp_B}):**\n\n{sorted(list(sym_diff))} (Total: {len(sym_diff)})")

with res_col2:
    st.error(f"**Difference ({himp_A} - {himp_B}):**\n\n{sorted(list(selisih_AB))} (Total: {len(selisih_AB)})")
    st.error(f"**Difference ({himp_B} - {himp_A}):**\n\n{sorted(list(selisih_BA))} (Total: {len(selisih_BA)})")

st.markdown("---")

# --- BAGIAN 3: PRINSIP INKLUSI-EKSKLUSI (PIE) & DIAGRAM VENN ---
st.header("3. Prinsip Inklusi-EksKLusi (PIE) & Diagram Venn")

col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("Verifikasi PIE")
    if len(data_aktif) == 2:
        nA = len(set_A)
        nB = len(set_B)
        nAB = len(irisan)
        pie_calc = nA + nB - nAB
        st.write(f"- |{himp_A}| = {nA}")
        st.write(f"- |{himp_B}| = {nB}")
        st.write(f"- |{himp_A} ∩ {himp_B}| = {nAB}")
        st.latex(r"|A \cup B| = |A| + |B| - |A \cap B|")
        st.write(f"**Hasil Perhitungan Rumus PIE:** `{nA} + {nB} - {nAB} = {pie_calc}`")
        st.write(f"**Jumlah Unik Aktual:** `{len(gabungan)}`")
        if pie_calc == len(gabungan):
            st.success("✅ **STATUS VERIFIKASI: VALID (COCOK)**")

    elif len(data_aktif) == 3:
        A, B, C = list(data_aktif.values())
        pie_3 = (len(A) + len(B) + len(C)) - (len(A & B) + len(A & C) + len(B & C)) + len(A & B & C)
        st.latex(r"|A \cup B \cup C| = (|A|+|B|+|C|) - (|A \cap B|+|A \cap C|+|B \cap C|) + |A \cap B \cap C|")
        st.write(f"**Hasil Rumus PIE (3 Himpunan):** `{pie_3}`")
        st.write(f"**Jumlah Unik Aktual:** `{len(A | B | C)}`")
        if pie_3 == len(A | B | C):
            st.success("✅ **STATUS VERIFIKASI: VALID (COCOK)**")

with col_right:
    st.subheader("Visualisasi Diagram Venn")
    fig, ax = plt.subplots(figsize=(6, 4))
    himp_list = list(data_aktif.values())
    if len(data_aktif) == 2:
        venn2(himp_list, set_labels=nama_himpunan, ax=ax)
    elif len(data_aktif) == 3:
        venn3(himp_list, set_labels=nama_himpunan, ax=ax)
    st.pyplot(fig)