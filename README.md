# Gem5 Array Cache

Analisis pengaruh konfigurasi cache dan pola akses memori terhadap performa
program array traversal menggunakan Gem5. Repository ini dibuat sebagai kode dan
dokumentasi pendukung project mata kuliah Organisasi dan Arsitektur Komputer
(OAK).

Link repository: <https://github.com/greyghstt/gem5-Array-Cache>

## Ringkasan Project

Project ini menggunakan Gem5 23.1.0.0 untuk menjalankan benchmark C sederhana
yang melakukan traversal array. Eksperimen membandingkan tiga pola akses memori
dan empat konfigurasi cache untuk melihat pengaruh locality dan hierarki cache
terhadap performa simulasi.

Gem5 dipilih karena mampu memodelkan komponen arsitektur komputer seperti CPU,
memori utama, dan cache. Pada project ini Gem5 digunakan untuk menjalankan
program dalam mode syscall emulation sehingga eksperimen dapat difokuskan pada
perilaku program dan konfigurasi cache.

## Tujuan

- Menjelaskan penggunaan Gem5 sebagai platform simulasi OAK.
- Menjalankan program array traversal pada Gem5.
- Membandingkan performa beberapa konfigurasi cache.
- Menganalisis dampak pola akses memori terhadap miss rate, `simTicks`, siklus,
  dan IPC.

## Struktur Repository

```text
.
|-- configs/              # Konfigurasi simulasi Gem5
|-- docs/                 # Dokumentasi desain eksperimen dan analisis
|-- results/              # Ringkasan dan output penting eksperimen
|-- scripts/              # Script otomasi eksperimen dan parsing hasil
|-- src/                  # Source benchmark C
|-- .gitignore
`-- README.md
```

Detail struktur tersedia di [docs/repository_structure.md](docs/repository_structure.md).

## Program Benchmark

Program utama berada di `src/array_access.c`. Program mengalokasikan array
integer, mengisi data secara deterministik, lalu menjumlahkan elemen array
berdasarkan mode akses yang dipilih.

Mode akses yang diuji:

- `seq`: akses berurutan, memiliki spatial locality tinggi.
- `stride`: akses dengan jarak tetap, dapat membuat sebagian isi cache line tidak
  termanfaatkan optimal.
- `random`: akses berdasarkan permutasi indeks, locality rendah karena alamat
  data tersebar.

## Konfigurasi Cache

Konfigurasi Gem5 berada di `configs/run_array_cache.py`.

| Konfigurasi | Deskripsi |
|---|---|
| `nocache` | CPU mengakses memori tanpa cache. |
| `l1_16k` | L1 instruction cache dan L1 data cache masing-masing 16 KiB. |
| `l1_32k` | L1 instruction cache dan L1 data cache masing-masing 32 KiB. |
| `l1_l2` | L1 32 KiB dan L2 256 KiB. |

## Desain Eksperimen

Eksperimen final menggunakan desain 3 x 4:

- 3 mode akses memori: `seq`, `stride`, `random`.
- 4 konfigurasi cache: `nocache`, `l1_16k`, `l1_32k`, `l1_l2`.
- Total: 12 simulasi.

Parameter final:

| Parameter | Nilai |
|---|---:|
| `SIZE` | 131072 |
| `REPEATS` | 8 |
| `STRIDE` | 16 |

Default pada `scripts/run_all.sh` dan `configs/run_array_cache.py` sudah
disesuaikan dengan parameter tersebut.

## Menjalankan Eksperimen

Prasyarat:

- Gem5 23.1.0.0 dengan build X86.
- GCC untuk mengompilasi benchmark C.
- Python 3 untuk parsing hasil.

Secara default, script mencari Gem5 pada `$HOME/gem5`. Jika Gem5 berada di
lokasi lain, gunakan variabel `GEM5_ROOT` atau `GEM5_BIN`.

```bash
cd ~/gem5-orkom
bash scripts/run_all.sh
```

Untuk menjalankan dengan parameter eksplisit:

```bash
SIZE=131072 REPEATS=8 STRIDE=16 bash scripts/run_all.sh
```

## Reproducibility

```bash
cd ~/gem5-orkom
bash scripts/run_all.sh
cat results/summary.md
```

Catatan: menjalankan ulang eksperimen akan memperbarui isi `results/raw/`,
`results/summary.csv`, dan `results/summary.md` sesuai hasil simulasi baru.

## Membaca Hasil

File hasil utama:

- `results/summary.csv`: ringkasan hasil dalam format CSV.
- `results/summary.md`: ringkasan hasil dalam format Markdown.
- `results/raw/`: output penting dari setiap simulasi, terutama `stats.txt` dan
  `terminal.log`.

Metrik utama:

- `simTicks`: total tick simulasi; semakin rendah umumnya semakin baik.
- `numCycles`: jumlah siklus CPU.
- `IPC`: instructions per cycle; semakin tinggi umumnya semakin baik.
- `L1D Miss Rate`: rasio miss pada data cache L1.

## Ringkasan Hasil

| Mode | Cache | simTicks | numCycles | IPC | L1D Miss Rate |
|---|---:|---:|---:|---:|---:|
| random | l1_16k | 79724258937 | 239412189 | 0.038932 | 0.407591 |
| random | l1_32k | 77170509909 | 231743273 | 0.040220 | 0.393253 |
| random | l1_l2 | 49444227612 | 148481164 | 0.062774 | 0.393133 |
| random | nocache | 592541413119 | 1779403643 | 0.005238 |  |
| seq | l1_16k | 13726143117 | 41219649 | 0.200681 | 0.086488 |
| seq | l1_32k | 13071351897 | 39253309 | 0.210733 | 0.080153 |
| seq | l1_l2 | 8047630980 | 24167060 | 0.342283 | 0.079514 |
| seq | nocache | 572040798588 | 1717840236 | 0.004815 |  |
| stride | l1_16k | 21337107534 | 64075398 | 0.129115 | 0.638531 |
| stride | l1_32k | 20684055906 | 62114282 | 0.133191 | 0.632207 |
| stride | l1_l2 | 22121678511 | 66431467 | 0.124535 | 0.398306 |
| stride | nocache | 478321702497 | 1436401509 | 0.005760 |  |

## Interpretasi Singkat

NoCache menjadi konfigurasi paling lambat pada semua mode karena tidak ada cache
antara CPU dan memori utama. L1 32 KiB umumnya sedikit lebih baik daripada L1 16
KiB karena kapasitas cache lebih besar.

L1 + L2 meningkatkan performa secara jelas pada sequential dan random. Pada
sequential, hasil ini didukung spatial locality yang tinggi. Pada random, L2
membantu mengurangi dampak akses memori utama meskipun locality tetap rendah.

Pada mode stride, L1 + L2 memiliki miss rate lebih rendah daripada L1 32 KiB,
tetapi `simTicks` sedikit lebih tinggi. Hal ini dapat terjadi karena tambahan
level cache tidak selalu langsung mempercepat pola stride, terutama jika overhead
akses dan pemanfaatan cache line tidak seimbang dengan manfaat L2.

Secara umum, sequential access paling efisien, random access paling berat karena
alamat data tersebar, dan stride access dapat memiliki miss rate tinggi karena
tidak semua data dalam cache line dimanfaatkan optimal.

## Dokumentasi Tambahan

- [docs/experiment_design.md](docs/experiment_design.md)
- [docs/result_analysis.md](docs/result_analysis.md)
- [docs/repository_structure.md](docs/repository_structure.md)

Repository ini hanya memuat kode benchmark, konfigurasi, script, hasil penting,
dan dokumentasi project. Source Gem5 tidak disertakan.
