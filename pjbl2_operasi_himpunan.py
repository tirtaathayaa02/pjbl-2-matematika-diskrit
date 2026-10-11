"""
PJBL-2 Sesi 2 Pertemuan 6
Implementasi Operasi Himpunan, Visualisasi Diagram Venn,
dan Prinsip Inklusi-Eksklusi

Fitur:
1. Operasi himpunan: gabungan, irisan, selisih, selisih simetris, komplemen
2. Diagram Venn otomatis (2 atau 3 himpunan)
3. Prinsip Inklusi-Eksklusi (hitung manual + verifikasi dengan gabungan langsung)
4. Pengujian dengan 2 dataset contoh

Kebutuhan: pip install matplotlib matplotlib-venn
"""

from itertools import combinations

import matplotlib
matplotlib.use("Agg")  # hapus baris ini jika ingin jendela plot tampil
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3


# ---------------------------------------------------------------
# 1. OPERASI HIMPUNAN
# ---------------------------------------------------------------
def gabungan(*himpunan):
    hasil = set()
    for h in himpunan:
        hasil |= h
    return hasil


def irisan(*himpunan):
    hasil = set(himpunan[0])
    for h in himpunan[1:]:
        hasil &= h
    return hasil


def selisih(a, b):
    return a - b


def selisih_simetris(a, b):
    return a ^ b


def komplemen(a, semesta):
    return semesta - a


def tampilkan_operasi(nama, data, semesta):
    """Cetak semua operasi himpunan untuk dataset (dict nama -> set)."""
    print(f"\n{'=' * 60}\nDATASET: {nama}\n{'=' * 60}")
    for k, v in data.items():
        print(f"{k} = {sorted(v)}  (n = {len(v)})")
    print(f"Semesta S = {sorted(semesta)}  (n = {len(semesta)})")

    kunci = list(data.keys())
    print("\n--- Operasi antar dua himpunan ---")
    for x, y in combinations(kunci, 2):
        A, B = data[x], data[y]
        print(f"{x} U {y}  = {sorted(gabungan(A, B))}")
        print(f"{x} ∩ {y}  = {sorted(irisan(A, B))}")
        print(f"{x} - {y}  = {sorted(selisih(A, B))}")
        print(f"{y} - {x}  = {sorted(selisih(B, A))}")
        print(f"{x} Δ {y}  = {sorted(selisih_simetris(A, B))}")
        print()

    print("--- Komplemen ---")
    for k in kunci:
        print(f"{k}' = {sorted(komplemen(data[k], semesta))}")

    if len(kunci) >= 3:
        print(f"\nIrisan semua himpunan = {sorted(irisan(*data.values()))}")
        print(f"Gabungan semua himpunan = {sorted(gabungan(*data.values()))}")


# ---------------------------------------------------------------
# 2. PRINSIP INKLUSI-EKSKLUSI
# ---------------------------------------------------------------
def inklusi_eksklusi(data):
    """
    |A1 U A2 U ... U An| =
        sum|Ai| - sum|Ai ∩ Aj| + sum|Ai ∩ Aj ∩ Ak| - ... + (-1)^(n+1)|A1 ∩ ... ∩ An|
    Mengembalikan (total, rincian langkah).
    """
    nama = list(data.keys())
    n = len(nama)
    total = 0
    rincian = []
    for r in range(1, n + 1):
        tanda = 1 if r % 2 == 1 else -1
        jumlah_r = 0
        for kombinasi in combinations(nama, r):
            ukuran = len(irisan(*[data[k] for k in kombinasi]))
            jumlah_r += ukuran
            simbol = " ∩ ".join(kombinasi)
            rincian.append(f"  |{simbol}| = {ukuran}")
        total += tanda * jumlah_r
        rincian.append(
            f"  >> Suku ke-{r}: {'+' if tanda > 0 else '-'} {jumlah_r}"
        )
    return total, rincian


def tampilkan_inklusi_eksklusi(data):
    print("\n--- Prinsip Inklusi-Eksklusi ---")
    total, rincian = inklusi_eksklusi(data)
    print("\n".join(rincian))
    langsung = len(gabungan(*data.values()))
    print(f"\nHasil Inklusi-Eksklusi : {total}")
    print(f"Hitung langsung |U|    : {langsung}")
    status = "COCOK ✔" if total == langsung else "TIDAK COCOK ✘"
    print(f"Verifikasi             : {status}")
    assert total == langsung, "Inklusi-Eksklusi tidak sesuai!"


# ---------------------------------------------------------------
# 3. VISUALISASI DIAGRAM VENN OTOMATIS
# ---------------------------------------------------------------
def gambar_venn(nama, data, nama_file):
    kunci = list(data.keys())
    himpunan = [data[k] for k in kunci]
    plt.figure(figsize=(7, 6))

    if len(kunci) == 2:
        venn2(himpunan, set_labels=kunci)
    elif len(kunci) == 3:
        venn3(himpunan, set_labels=kunci)
    else:
        raise ValueError("Diagram Venn otomatis hanya mendukung 2 atau 3 himpunan.")

    plt.title(f"Diagram Venn - {nama}")
    plt.tight_layout()
    plt.savefig(nama_file, dpi=150)
    plt.close()
    print(f"\nDiagram Venn disimpan: {nama_file}")


# ---------------------------------------------------------------
# 4. PROSES UTAMA + DATASET CONTOH
# ---------------------------------------------------------------
def proses(nama, data, nama_file):
    semesta = gabungan(*data.values())
    tampilkan_operasi(nama, data, semesta)
    tampilkan_inklusi_eksklusi(data)
    gambar_venn(nama, data, nama_file)


def main():
    # Dataset 1: Peserta kegiatan mahasiswa (3 himpunan)
    dataset1 = {
        "Basket": {"Andi", "Budi", "Citra", "Dewi", "Eko", "Fajar"},
        "Paduan Suara": {"Citra", "Dewi", "Gita", "Hana", "Indra"},
        "Programming": {"Budi", "Dewi", "Hana", "Joko", "Kiki", "Eko"},
    }

    # Dataset 2: Pelanggan toko online berdasarkan produk yang dibeli (2 himpunan)
    dataset2 = {
        "Beli Laptop": {"P01", "P02", "P03", "P04", "P05", "P06", "P07"},
        "Beli Mouse": {"P04", "P05", "P08", "P09", "P10"},
    }

    # Dataset 3 (opsional): ganti dengan dataset proyek kelompok Anda
    proses("Peserta Kegiatan Mahasiswa", dataset1, "venn_dataset1.png")
    proses("Pelanggan Toko Online", dataset2, "venn_dataset2.png")


if __name__ == "__main__":
    main()