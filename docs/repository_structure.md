# Struktur Repository

Repository ini memisahkan kode benchmark, konfigurasi Gem5, script eksperimen,
hasil, dan dokumentasi agar mudah dibaca di GitHub maupun dirujuk dalam laporan.

```text
.
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

## Folder Utama

- `src/`: source benchmark C. File utama adalah `array_access.c`.
- `configs/`: konfigurasi Gem5 untuk menjalankan benchmark dengan beberapa
  hierarki cache.
- `scripts/`: otomasi eksperimen dan parsing statistik Gem5.
- `results/`: hasil eksperimen final dan output raw penting.
- `docs/`: dokumentasi desain eksperimen, struktur repository, dan analisis
  hasil.

## File Penting

- `scripts/run_all.sh`: mengompilasi benchmark, menjalankan 12 simulasi, dan
  memanggil parser hasil.
- `scripts/parse_stats.py`: membaca `stats.txt` dan membuat ringkasan CSV serta
  Markdown.
- `results/summary.csv`: ringkasan hasil untuk pengolahan data.
- `results/summary.md`: ringkasan hasil yang mudah dibaca.
- `results/raw/*/stats.txt`: statistik detail dari Gem5.
- `results/raw/*/terminal.log`: log terminal setiap simulasi.

## Catatan GitHub

File build, cache editor, cache Python, dan artefak Gem5 yang besar atau dapat
dibuat ulang diabaikan melalui `.gitignore`. File yang tetap disimpan adalah
source, konfigurasi, script, dokumentasi, ringkasan hasil, serta `stats.txt` dan
`terminal.log` dari eksperimen final.

Source Gem5 tidak disertakan dalam repository ini. Repository hanya berisi
artefak project yang diperlukan untuk laporan OAK dan reproduksi eksperimen.
