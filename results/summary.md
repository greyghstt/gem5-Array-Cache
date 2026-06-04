# Summary Hasil Eksperimen Gem5

Parameter: SIZE=131072, REPEATS=8, STRIDE=16
Catatan: simTicks lebih rendah lebih baik; IPC lebih tinggi lebih baik.
Detail lengkap: results/summary.csv

Mode    Cache     simTicks    IPC     L1D_miss
------  --------  ----------  ------  --------
random  l1_16k        79.72B  0.0389    0.4076
random  l1_32k        77.17B  0.0402    0.3933
random  l1_l2         49.44B  0.0628    0.3931
random  nocache      592.54B  0.0052         -
seq     l1_16k        13.73B  0.2007    0.0865
seq     l1_32k        13.07B  0.2107    0.0802
seq     l1_l2          8.05B  0.3423    0.0795
seq     nocache      572.04B  0.0048         -
stride  l1_16k        21.34B  0.1291    0.6385
stride  l1_32k        20.68B  0.1332    0.6322
stride  l1_l2         22.12B  0.1245    0.3983
stride  nocache      478.32B  0.0058         -
