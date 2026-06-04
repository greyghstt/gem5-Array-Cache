# Analisis Pengaruh Konfigurasi Cache dan Pola Akses Memori terhadap Performa Program Array Traversal Menggunakan Gem5

Repository ini berisi project eksperimen Gem5 untuk tugas mata kuliah
Organisasi dan Arsitektur Komputer (OAK). Project menganalisis pengaruh
konfigurasi cache dan pola akses memori terhadap performa program array
traversal sederhana.

Platform utama yang digunakan adalah Gem5 versi 23.1.0.0 di WSL Ubuntu.
Path Gem5 pada lingkungan eksperimen adalah `/home/greyghst/gem5`, sedangkan
path project adalah `/home/greyghst/gem5-orkom`.

Link repository: <https://github.com/greyghstt/gem5-Array-Cache>

## Kesesuaian dengan Ketentuan Tugas

Repository ini disiapkan untuk memenuhi kebutuhan project mata kuliah OAK:

- Platform yang dipilih adalah Gem5.
- Program yang dijalankan adalah benchmark array traversal pada
  `src/array_access.c`.
- File konfigurasi Gem5 tersedia pada `configs/run_array_cache.py`.
- Langkah menjalankan eksperimen tersedia pada bagian
  [Cara Menjalankan Ulang Eksperimen](#cara-menjalankan-ulang-eksperimen).
- Hasil eksekusi tersedia pada `results/summary.csv`, `results/summary.md`, dan
  `results/raw/`.
- Analisis hasil dari sudut pandang organisasi dan arsitektur komputer tersedia
  pada bagian [Interpretasi Singkat](#interpretasi-singkat) dan
  `docs/result_analysis.md`.
- Source Gem5 di `/home/greyghst/gem5` tidak disertakan dan tidak dimodifikasi;
  repository hanya memuat kode, konfigurasi, hasil, dan dokumentasi project.

## Latar Belakang

Cache merupakan salah satu komponen penting dalam organisasi dan arsitektur
komputer karena menjembatani perbedaan kecepatan antara CPU dan memori utama.
Program yang mengakses data dengan locality tinggi cenderung memperoleh manfaat
besar dari cache, sedangkan program dengan pola akses tersebar dapat mengalami
banyak cache miss.

Array traversal dipilih karena pola akses memorinya mudah dikontrol. Dengan
membandingkan akses sequential, stride, dan random pada beberapa konfigurasi
cache, project ini menunjukkan hubungan antara locality, miss rate, dan metrik
performa simulasi seperti `simTicks`, `numCycles`, dan IPC.

## Tujuan Eksperimen

- Mengamati pengaruh keberadaan cache terhadap performa program array traversal.
- Membandingkan performa cache L1 16 KiB, L1 32 KiB, dan kombinasi L1 + L2.
- Menganalisis dampak pola akses sequential, stride, dan random terhadap cache
  miss rate dan waktu simulasi.
- Menyediakan hasil eksperimen yang dapat direproduksi untuk laporan OAK.

## Gem5 sebagai Platform Simulasi

Gem5 adalah simulator arsitektur komputer yang dapat digunakan untuk memodelkan
CPU, memori, dan hierarki cache. Dalam project ini, Gem5 digunakan dalam mode
syscall emulation (SE) untuk menjalankan binary benchmark `array_access` tanpa
mem-boot sistem operasi penuh. Pendekatan ini sesuai untuk eksperimen terkontrol
yang berfokus pada perilaku program dan konfigurasi mikroarsitektur.

Konfigurasi simulasi berada pada `configs/run_array_cache.py`. Script tersebut
menggunakan CPU `TIMING`, ISA `X86`, memori `SingleChannelDDR3_1600`, dan empat
variasi hierarki cache.

## Struktur Repository

```text
gem5-orkom/
|-- configs/
|   `-- run_array_cache.py
|-- docs/
|   |-- experiment_design.md
|   |-- repository_structure.md
|   `-- result_analysis.md
|-- results/
|   |-- raw/
|   |-- summary.csv
|   `-- summary.md
|-- scripts/
|   |-- parse_stats.py
|   `-- run_all.sh
|-- src/
|   `-- array_access.c
|-- .gitignore
`-- README.md
```

Penjelasan detail struktur repository tersedia di
[`docs/repository_structure.md`](docs/repository_structure.md).

## Program Array Traversal

Program utama berada di `src/array_access.c`. Program mengalokasikan array data
berisi integer, menginisialisasi data deterministik, lalu menghitung akumulasi
nilai array berdasarkan mode akses yang dipilih. Nilai hasil disimpan ke
`global_sink` bertipe `volatile` agar kompilator tidak menghapus loop utama
sebagai optimisasi.

Argumen program benchmark adalah:

```text
array_access <seq|stride|random> <size> <repeats> <stride>
```

## Mode Akses Memori

- `seq`: mengakses array dari indeks awal sampai akhir secara berurutan. Mode
  ini memiliki spatial locality tinggi karena elemen yang berdekatan berada pada
  cache line yang sama atau berdekatan.
- `stride`: mengakses array dengan jarak indeks tertentu. Pada eksperimen final,
  `STRIDE=16`. Mode ini dapat membuat banyak data dalam cache line tidak
  dimanfaatkan optimal.
- `random`: mengakses array berdasarkan permutasi indeks deterministik. Mode ini
  memiliki locality rendah karena alamat data tersebar.

## Konfigurasi Cache

- `nocache`: tidak menggunakan cache antara CPU dan memori utama.
- `l1_16k`: menggunakan private L1 instruction cache dan data cache masing-
  masing 16 KiB.
- `l1_32k`: menggunakan private L1 instruction cache dan data cache masing-
  masing 32 KiB.
- `l1_l2`: menggunakan L1 instruction cache dan data cache masing-masing 32 KiB
  serta L2 cache 256 KiB.

## Parameter Eksperimen Final

Eksperimen final yang berhasil dijalankan menggunakan parameter berikut:

| Parameter | Nilai |
|---|---:|
| `SIZE` | 131072 |
| `REPEATS` | 8 |
| `STRIDE` | 16 |
| Mode akses | `seq`, `stride`, `random` |
| Konfigurasi cache | `nocache`, `l1_16k`, `l1_32k`, `l1_l2` |
| Total simulasi | 12 |

Default parameter pada `scripts/run_all.sh` dan `configs/run_array_cache.py`
telah disamakan dengan parameter eksperimen final tersebut.

## Cara Menjalankan Ulang Eksperimen

Pastikan Gem5 versi 23.1.0.0 sudah tersedia di `/home/greyghst/gem5` atau set
variabel `GEM5_ROOT` dan `GEM5_BIN` sesuai lokasi Gem5 yang digunakan.

```bash
cd ~/gem5-orkom
bash scripts/run_all.sh
```

Script `scripts/run_all.sh` akan mengompilasi `src/array_access.c`, menjalankan
12 simulasi Gem5, menyimpan hasil raw ke `results/raw/`, lalu membuat ulang
`results/summary.csv` dan `results/summary.md` melalui `scripts/parse_stats.py`.

Untuk menjalankan dengan parameter berbeda:

```bash
SIZE=131072 REPEATS=8 STRIDE=16 bash scripts/run_all.sh
```

## Reproducibility

```bash
cd ~/gem5-orkom
bash scripts/run_all.sh
cat results/summary.md
```

Catatan: menjalankan ulang command tersebut akan menulis ulang isi
`results/raw/`, `results/summary.csv`, dan `results/summary.md` sesuai hasil
simulasi baru.

## Cara Membaca Hasil

Hasil ringkasan tersedia dalam dua format:

- `results/summary.csv`: format tabular untuk pengolahan lebih lanjut.
- `results/summary.md`: format Markdown yang mudah dibaca di repository atau
  laporan.

Kolom utama yang digunakan dalam analisis:

- `simTicks`: total tick simulasi. Semakin rendah umumnya semakin baik.
- `numCycles`: jumlah siklus CPU yang tercatat. Semakin rendah umumnya semakin
  baik.
- `IPC`: instructions per cycle. Semakin tinggi menunjukkan eksekusi instruksi
  lebih efisien.
- `L1D Miss Rate`: rasio miss pada data cache L1. Nilai kosong pada `nocache`
  muncul karena konfigurasi tersebut memang tidak memiliki L1 data cache.

## Ringkasan Hasil

Tabel berikut berasal dari `results/summary.md`.

| Mode | Cache | simTicks | simInsts | numCycles | IPC | L1D Miss Rate | L1D Misses | L1D Hits |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random | l1_16k | 79724258937 | 9320416 | 239412189 | 0.038932 | 0.407591 | 1177402 | 1711282 |
| random | l1_32k | 77170509909 | 9320416 | 231743273 | 0.040220 | 0.393253 | 1135985 | 1752699 |
| random | l1_l2 | 49444227612 | 9320416 | 148481164 | 0.062774 | 0.393133 | 1135638 | 1753046 |
| random | nocache | 592541413119 | 9320416 | 1779403643 | 0.005238 |  |  |  |
| seq | l1_16k | 13726143117 | 8271703 | 41219649 | 0.200681 | 0.086488 | 159144 | 1680932 |
| seq | l1_32k | 13071351897 | 8271703 | 39253309 | 0.210733 | 0.080153 | 147487 | 1692589 |
| seq | l1_l2 | 8047630980 | 8271703 | 24167060 | 0.342283 | 0.079514 | 146312 | 1693764 |
| seq | nocache | 572040798588 | 8271703 | 1717840236 | 0.004815 |  |  |  |
| stride | l1_16k | 21337107534 | 8272782 | 64075398 | 0.129115 | 0.638531 | 1174953 | 665136 |
| stride | l1_32k | 20684055906 | 8272782 | 62114282 | 0.133191 | 0.632207 | 1163318 | 676771 |
| stride | l1_l2 | 22121678511 | 8272782 | 66431467 | 0.124535 | 0.398306 | 732919 | 1107170 |
| stride | nocache | 478321702497 | 8272782 | 1436401509 | 0.005760 |  |  |  |

## Interpretasi Singkat

NoCache menjadi konfigurasi paling lambat pada semua mode karena tidak ada cache
di antara CPU dan memori utama. Akibatnya, akses data harus dilayani langsung
dari memori utama dengan latensi yang jauh lebih tinggi.

L1 32 KiB umumnya sedikit lebih baik daripada L1 16 KiB karena kapasitas cache
yang lebih besar dapat menampung lebih banyak data aktif. Hal ini terlihat pada
penurunan `simTicks` dan kenaikan IPC pada mode sequential, stride, dan random.

Konfigurasi L1 + L2 memberikan peningkatan performa yang jelas pada sequential
dan random. Pada sequential, `simTicks` turun dari 13071351897 pada `l1_32k`
menjadi 8047630980 pada `l1_l2`. Pada random, `simTicks` turun dari 77170509909
menjadi 49444227612.

Pada mode stride, `l1_l2` memiliki miss rate lebih rendah daripada `l1_32k`,
yaitu 0.398306 dibanding 0.632207, tetapi `simTicks` sedikit lebih tinggi.
Kondisi ini dapat terjadi karena tambahan level cache tidak selalu langsung
mempercepat pola akses stride, terutama ketika overhead akses dan pola
pemanfaatan cache line tidak seimbang dengan manfaat L2.

Secara umum, sequential access efisien karena spatial locality tinggi. Random
access lebih berat karena alamat data tersebar dan locality rendah. Stride
access dapat memiliki miss rate tinggi karena banyak data dalam satu cache line
tidak dimanfaatkan secara optimal.

## Dokumentasi Tambahan

- [`docs/experiment_design.md`](docs/experiment_design.md) menjelaskan desain
  eksperimen 3 x 4.
- [`docs/result_analysis.md`](docs/result_analysis.md) berisi analisis hasil per
  mode akses dan per konfigurasi cache.
- [`docs/repository_structure.md`](docs/repository_structure.md) menjelaskan
  fungsi folder dan file utama.

Repository ini disiapkan sebagai artefak pendukung laporan tugas mata kuliah
Organisasi dan Arsitektur Komputer.
