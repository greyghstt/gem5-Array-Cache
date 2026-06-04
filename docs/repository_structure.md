# Struktur Repository

Dokumen ini menjelaskan fungsi folder dan file utama pada repository
`gem5-orkom`.

## Ringkasan Struktur

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

## Folder dan File Utama

### `src/`

Folder ini berisi source code benchmark.

`src/array_access.c` adalah program C utama yang menjalankan traversal array
dengan mode `seq`, `stride`, dan `random`. Program ini dikompilasi secara statis
oleh `scripts/run_all.sh` sebelum simulasi Gem5 dijalankan.

### `configs/`

Folder ini berisi konfigurasi simulasi Gem5.

`configs/run_array_cache.py` mendefinisikan board Gem5, CPU, memori, workload,
dan variasi hierarki cache. File ini menerima argumen seperti `--binary`,
`--mode`, `--cache`, `--size`, `--repeats`, dan `--stride`.

### `scripts/`

Folder ini berisi script otomasi eksperimen dan parsing hasil.

`scripts/run_all.sh` adalah entry point eksperimen. Script ini memeriksa binary
Gem5, mengompilasi benchmark, menjalankan 12 kombinasi eksperimen, dan memanggil
parser hasil.

`scripts/parse_stats.py` membaca file `stats.txt` dari setiap folder raw result,
mengambil metrik penting, lalu menghasilkan `results/summary.csv` dan
`results/summary.md`.

### `results/`

Folder ini berisi hasil eksperimen.

`results/summary.csv` adalah hasil ringkasan dalam format CSV untuk analisis
tabular.

`results/summary.md` adalah hasil ringkasan dalam format Markdown untuk dibaca
langsung atau dimasukkan ke laporan.

`results/raw/` berisi output mentah dari Gem5 untuk setiap kombinasi eksperimen.
File `stats.txt` dan `terminal.log` pada setiap subfolder dipertahankan karena
berguna untuk audit hasil. Artefak lain seperti file konfigurasi visual atau
intermediate Gem5 dapat dibuat ulang saat simulasi dijalankan kembali.

### `docs/`

Folder ini berisi dokumentasi pendukung laporan.

`docs/experiment_design.md` menjelaskan desain eksperimen 3 x 4, parameter, dan
alur pelaksanaan eksperimen.

`docs/result_analysis.md` menyajikan tabel ringkasan hasil dan analisis per mode
akses serta per konfigurasi cache.

`docs/repository_structure.md` menjelaskan struktur repository dan fungsi file
utama.

### `README.md`

File ini menjadi halaman utama repository. Isinya mencakup latar belakang,
tujuan, platform Gem5, struktur repository, cara menjalankan ulang eksperimen,
ringkasan hasil, dan interpretasi singkat.

### `.gitignore`

File ini mengatur file yang tidak perlu diunggah ke GitHub, seperti hasil build,
cache Python, file editor, file sistem, dan artefak raw Gem5 yang dapat dibuat
ulang. File penting seperti `src/`, `configs/`, `scripts/`, `docs/`,
`results/summary.csv`, `results/summary.md`, serta `stats.txt` dan
`terminal.log` di `results/raw/` tetap diperbolehkan untuk dilacak.

## Catatan Penggunaan GitHub

Repository ini disiapkan agar siap diunggah ke GitHub sebagai artefak tugas OAK.
Sebelum commit, periksa kembali file yang akan dilacak dengan:

```bash
git status
```

Tidak perlu memasukkan source Gem5 dari `/home/greyghst/gem5` ke repository ini.
