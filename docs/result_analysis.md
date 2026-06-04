# Analisis Hasil Eksperimen

Dokumen ini menganalisis hasil eksperimen Gem5 berdasarkan ringkasan pada
`results/summary.md`. Eksperimen menggunakan `SIZE=131072`, `REPEATS=8`, dan
`STRIDE=16`.

## Tabel Ringkasan Hasil

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

## Analisis Per Mode Akses

### Sequential

Mode sequential menunjukkan performa terbaik di antara pola akses yang memakai
cache. Hal ini sesuai dengan karakteristik spatial locality: setelah satu cache
line dimuat, beberapa elemen array berikutnya dapat dimanfaatkan tanpa harus
selalu mengambil data dari memori utama.

Pada mode ini, `nocache` memiliki `simTicks` 572040798588 dan IPC 0.004815,
jauh lebih buruk dibanding semua konfigurasi cache. L1 32 KiB sedikit lebih baik
daripada L1 16 KiB, dengan `simTicks` turun dari 13726143117 menjadi
13071351897. Konfigurasi `l1_l2` memberikan peningkatan paling jelas, dengan
`simTicks` 8047630980 dan IPC 0.342283.

### Stride

Mode stride memiliki miss rate tinggi pada konfigurasi L1 saja. Pada `l1_16k`,
L1D miss rate adalah 0.638531, sedangkan pada `l1_32k` nilainya 0.632207.
Kondisi ini terjadi karena akses dengan stride dapat melewati banyak elemen
dalam cache line, sehingga tidak semua data yang sudah dimuat dapat dimanfaatkan
secara optimal.

Konfigurasi `l1_l2` menurunkan L1D miss rate menjadi 0.398306, lebih rendah
daripada `l1_32k`. Namun, `simTicks` pada `l1_l2` adalah 22121678511, sedikit
lebih tinggi daripada `l1_32k` yang bernilai 20684055906. Hal ini menunjukkan
bahwa tambahan level cache tidak selalu langsung mempercepat pola akses stride,
terutama jika overhead akses dan pola pemanfaatan cache line tidak seimbang
dengan manfaat L2.

### Random

Mode random merupakan pola akses yang berat karena alamat data tersebar dan
locality rendah. Pada konfigurasi L1 saja, miss rate berada di sekitar 0.39
sampai 0.41. L1 32 KiB sedikit lebih baik daripada L1 16 KiB, dengan `simTicks`
turun dari 79724258937 menjadi 77170509909.

Konfigurasi `l1_l2` memberikan peningkatan performa yang jelas pada mode random.
`simTicks` turun menjadi 49444227612 dan IPC naik menjadi 0.062774. Walaupun
akses random tetap sulit diprediksi, L2 dapat membantu menahan sebagian data
yang tidak tertampung efektif di L1.

## Analisis Per Konfigurasi Cache

### NoCache

NoCache adalah konfigurasi paling lambat pada semua mode. Tanpa cache di antara
CPU dan memori utama, akses data harus dilayani langsung dari memori utama.
Akibatnya, `simTicks` dan `numCycles` menjadi sangat tinggi, sedangkan IPC sangat
rendah.

### L1 16 KiB

Konfigurasi L1 16 KiB sudah jauh lebih baik daripada `nocache`, terutama pada
mode sequential. Namun, kapasitasnya lebih terbatas dibanding L1 32 KiB,
sehingga jumlah miss umumnya lebih tinggi.

### L1 32 KiB

L1 32 KiB umumnya sedikit lebih baik daripada L1 16 KiB karena kapasitas cache
lebih besar. Perbaikan ini terlihat konsisten pada sequential, stride, dan
random melalui penurunan `simTicks` dan peningkatan IPC.

### L1 + L2

Konfigurasi L1 + L2 meningkatkan performa secara jelas pada sequential dan
random. Pada sequential, performa meningkat karena locality tinggi dapat
dimanfaatkan oleh hierarki cache. Pada random, L2 membantu mengurangi dampak
akses memori utama yang mahal.

Pada stride, L1 + L2 menurunkan miss rate tetapi tidak menghasilkan `simTicks`
lebih rendah daripada L1 32 KiB. Hasil ini perlu dibaca hati-hati: miss rate yang
lebih rendah tidak selalu berarti waktu total lebih rendah, karena ada overhead
tambahan untuk level cache dan pola akses stride belum tentu memanfaatkan cache
line secara efisien.

## Kesimpulan Analisis

Hasil eksperimen menunjukkan bahwa cache sangat berpengaruh terhadap performa
program array traversal. Sequential access paling efisien karena spatial locality
tinggi. Random access lebih berat karena locality rendah. Stride access dapat
menimbulkan miss rate tinggi karena banyak data dalam cache line tidak
dimanfaatkan optimal.

Secara keseluruhan, konfigurasi cache yang lebih lengkap cenderung meningkatkan
performa, tetapi hasil mode stride menunjukkan bahwa hubungan antara miss rate,
overhead hierarki cache, dan performa total tidak selalu linear.
