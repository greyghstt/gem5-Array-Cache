# Desain Eksperimen

Dokumen ini merangkum rancangan eksperimen cache pada benchmark array traversal
menggunakan Gem5.

## Platform

- Simulator: Gem5 23.1.0.0.
- Mode simulasi: syscall emulation.
- ISA: X86.
- CPU: `TIMING`.
- Memori: `SingleChannelDDR3_1600`.

Gem5 digunakan untuk memodelkan CPU, memori, dan hierarki cache sehingga dampak
konfigurasi cache terhadap performa program dapat diamati secara terukur.

## Benchmark

Benchmark berada di `src/array_access.c`. Program melakukan penjumlahan elemen
array dengan tiga mode akses:

| Mode | Karakteristik |
|---|---|
| `seq` | Akses berurutan dengan spatial locality tinggi. |
| `stride` | Akses berjarak tetap dengan `STRIDE=16`. |
| `random` | Akses acak deterministik dengan locality rendah. |

Parameter final:

| Parameter | Nilai |
|---|---:|
| `SIZE` | 131072 |
| `REPEATS` | 8 |
| `STRIDE` | 16 |

## Konfigurasi Cache

| Konfigurasi | Deskripsi |
|---|---|
| `nocache` | Tanpa cache antara CPU dan memori utama. |
| `l1_16k` | L1 instruction cache dan L1 data cache 16 KiB. |
| `l1_32k` | L1 instruction cache dan L1 data cache 32 KiB. |
| `l1_l2` | L1 32 KiB dan L2 256 KiB. |

## Matriks Eksperimen

Eksperimen menggunakan desain 3 x 4: tiga mode akses memori dan empat
konfigurasi cache. Total simulasi adalah 12 percobaan.

| Mode | nocache | l1_16k | l1_32k | l1_l2 |
|---|---|---|---|---|
| `seq` | Ya | Ya | Ya | Ya |
| `stride` | Ya | Ya | Ya | Ya |
| `random` | Ya | Ya | Ya | Ya |

## Alur Eksekusi

1. `scripts/run_all.sh` mengompilasi benchmark menjadi `build/array_access`.
2. Script menjalankan seluruh kombinasi mode akses dan cache pada Gem5.
3. Output setiap simulasi disimpan ke `results/raw/<mode>_<cache>/`.
4. `scripts/parse_stats.py` mengambil metrik penting dari `stats.txt`.
5. Ringkasan akhir ditulis ke `results/summary.csv` dan `results/summary.md`.

## Metrik

- `simTicks`: total tick simulasi.
- `simInsts`: jumlah instruksi yang disimulasikan.
- `numCycles`: jumlah siklus CPU.
- `IPC`: instruksi per siklus.
- `L1D Miss Rate`: rasio miss pada L1 data cache.

Pada `nocache`, metrik L1D kosong karena tidak ada data cache L1 yang dimodelkan.
