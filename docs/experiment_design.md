# Desain Eksperimen

Dokumen ini menjelaskan desain eksperimen project "Analisis Pengaruh
Konfigurasi Cache dan Pola Akses Memori terhadap Performa Program Array
Traversal Menggunakan Gem5".

## Tujuan

Eksperimen dirancang untuk mengamati bagaimana pola akses memori dan konfigurasi
cache memengaruhi performa program array traversal. Performa diamati melalui
metrik Gem5 seperti `simTicks`, `numCycles`, IPC, dan L1D miss rate.

## Platform

- Simulator: Gem5 23.1.0.0
- Lingkungan: WSL Ubuntu
- Path Gem5: `/home/greyghst/gem5`
- Path project: `/home/greyghst/gem5-orkom`
- ISA: X86
- CPU model: `TIMING`
- Memori: `SingleChannelDDR3_1600`

## Benchmark

Benchmark utama adalah `src/array_access.c`. Program mengalokasikan array
integer, mengisi data secara deterministik, lalu melakukan traversal berdasarkan
mode akses yang diberikan melalui argumen command line.

Parameter final benchmark:

| Parameter | Nilai |
|---|---:|
| `SIZE` | 131072 |
| `REPEATS` | 8 |
| `STRIDE` | 16 |

## Faktor Eksperimen

Desain eksperimen menggunakan kombinasi 3 mode akses memori dan 4 konfigurasi
cache. Total simulasi adalah 3 x 4 = 12 percobaan.

### Mode Akses Memori

| Mode | Penjelasan |
|---|---|
| `seq` | Akses array secara berurutan dari indeks awal sampai akhir. |
| `stride` | Akses array dengan jarak indeks tetap, yaitu `STRIDE=16`. |
| `random` | Akses array menggunakan urutan indeks acak deterministik. |

### Konfigurasi Cache

| Cache | Penjelasan |
|---|---|
| `nocache` | Tidak ada cache antara CPU dan memori utama. |
| `l1_16k` | L1 instruction cache 16 KiB dan L1 data cache 16 KiB. |
| `l1_32k` | L1 instruction cache 32 KiB dan L1 data cache 32 KiB. |
| `l1_l2` | L1 instruction/data cache 32 KiB dan L2 cache 256 KiB. |

## Matriks Percobaan

| Mode | nocache | l1_16k | l1_32k | l1_l2 |
|---|---|---|---|---|
| `seq` | Ya | Ya | Ya | Ya |
| `stride` | Ya | Ya | Ya | Ya |
| `random` | Ya | Ya | Ya | Ya |

## Alur Eksperimen

1. `scripts/run_all.sh` memeriksa keberadaan binary Gem5.
2. Script mengompilasi `src/array_access.c` menjadi `build/array_access`.
3. Script menjalankan simulasi untuk seluruh kombinasi mode dan cache.
4. Gem5 menulis output raw ke `results/raw/<mode>_<cache>/`.
5. `scripts/parse_stats.py` membaca `stats.txt` dari setiap percobaan.
6. Parser membuat `results/summary.csv` dan `results/summary.md`.

## Metrik yang Diamati

- `simTicks`: total waktu simulasi dalam tick Gem5.
- `simInsts`: jumlah instruksi yang disimulasikan.
- `numCycles`: jumlah siklus CPU.
- `IPC`: instruksi per siklus.
- `L1D Miss Rate`: rasio miss pada L1 data cache.
- `L1D Misses` dan `L1D Hits`: jumlah miss dan hit pada L1 data cache.

Pada konfigurasi `nocache`, metrik L1D kosong karena tidak ada L1 data cache
yang dimodelkan.

## Catatan Reproduksi

Eksperimen dapat dijalankan ulang dengan command berikut:

```bash
cd ~/gem5-orkom
bash scripts/run_all.sh
cat results/summary.md
```

Menjalankan ulang eksperimen akan memperbarui file hasil di `results/`.
