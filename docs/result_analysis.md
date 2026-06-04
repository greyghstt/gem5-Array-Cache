# Analisis Hasil Eksperimen

Analisis ini menggunakan hasil final pada `results/summary.md` dengan parameter
`SIZE=131072`, `REPEATS=8`, dan `STRIDE=16`.

## Tabel Ringkas

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

## Analisis Per Mode

### Sequential

Sequential access paling efisien karena spatial locality tinggi. Elemen array
yang berdekatan cenderung berada pada cache line yang sama, sehingga cache dapat
dimanfaatkan dengan baik.

Pada mode ini, `nocache` jauh lebih lambat daripada semua konfigurasi cache. L1
32 KiB sedikit lebih baik daripada L1 16 KiB. Konfigurasi `l1_l2` memberi hasil
terbaik dengan `simTicks` 8047630980 dan IPC 0.342283.

### Stride

Stride access memiliki miss rate tinggi pada konfigurasi L1 saja. Penyebabnya,
akses berjarak tetap dapat membuat banyak data dalam satu cache line tidak
terpakai optimal.

`l1_l2` menurunkan L1D miss rate dari 0.632207 pada `l1_32k` menjadi 0.398306.
Namun, `simTicks` naik dari 20684055906 menjadi 22121678511. Hasil ini
menunjukkan bahwa miss rate yang lebih rendah tidak selalu menghasilkan waktu
simulasi lebih rendah. Tambahan level cache memiliki overhead, dan pola stride
belum tentu memanfaatkan cache line secara seimbang dengan manfaat L2.

### Random

Random access berat karena alamat data tersebar dan locality rendah. L1 32 KiB
tetap sedikit lebih baik daripada L1 16 KiB, tetapi peningkatan terbesar muncul
pada `l1_l2`. Pada mode random, `simTicks` turun dari 77170509909 pada `l1_32k`
menjadi 49444227612 pada `l1_l2`.

## Analisis Per Konfigurasi

- `nocache` paling lambat pada semua mode karena CPU harus mengakses memori
  utama tanpa perantara cache.
- `l1_16k` sudah memberi peningkatan besar dibanding `nocache`, tetapi
  kapasitasnya lebih terbatas.
- `l1_32k` umumnya sedikit lebih baik daripada `l1_16k` karena kapasitas cache
  lebih besar.
- `l1_l2` meningkatkan performa secara jelas pada sequential dan random, tetapi
  pada stride hasilnya perlu dibaca hati-hati karena overhead hierarki cache
  dapat mengurangi manfaat penurunan miss rate.

## Kesimpulan

Hasil eksperimen menunjukkan bahwa cache sangat memengaruhi performa program
array traversal. Sequential access paling menguntungkan bagi cache, random
access paling sulit karena locality rendah, dan stride access dapat menghasilkan
miss rate tinggi akibat pemanfaatan cache line yang kurang optimal.
