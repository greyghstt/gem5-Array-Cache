# Summary Hasil Eksperimen Gem5

Tabel compact untuk dibaca cepat di terminal. Detail lengkap tersedia di `summary.csv`.

| Mode | Cache | simTicks | IPC | L1D Miss Rate |
|---|---:|---:|---:|---:|
| random | l1_16k | 79724258937 | 0.038932 | 0.407591 |
| random | l1_32k | 77170509909 | 0.040220 | 0.393253 |
| random | l1_l2 | 49444227612 | 0.062774 | 0.393133 |
| random | nocache | 592541413119 | 0.005238 |  |
| seq | l1_16k | 13726143117 | 0.200681 | 0.086488 |
| seq | l1_32k | 13071351897 | 0.210733 | 0.080153 |
| seq | l1_l2 | 8047630980 | 0.342283 | 0.079514 |
| seq | nocache | 572040798588 | 0.004815 |  |
| stride | l1_16k | 21337107534 | 0.129115 | 0.638531 |
| stride | l1_32k | 20684055906 | 0.133191 | 0.632207 |
| stride | l1_l2 | 22121678511 | 0.124535 | 0.398306 |
| stride | nocache | 478321702497 | 0.005760 |  |
