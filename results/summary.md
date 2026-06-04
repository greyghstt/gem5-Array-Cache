# Summary Hasil Eksperimen Gem5

Format ringkas untuk dibaca langsung dengan `cat`.
Detail lengkap tersedia di `results/summary.csv`.

## Mode: random

- l1_16k
  simTicks      : 79724258937
  IPC           : 0.038932
  L1D miss rate : 0.407591

- l1_32k
  simTicks      : 77170509909
  IPC           : 0.040220
  L1D miss rate : 0.393253

- l1_l2
  simTicks      : 49444227612
  IPC           : 0.062774
  L1D miss rate : 0.393133

- nocache
  simTicks      : 592541413119
  IPC           : 0.005238
  L1D miss rate : -

## Mode: seq

- l1_16k
  simTicks      : 13726143117
  IPC           : 0.200681
  L1D miss rate : 0.086488

- l1_32k
  simTicks      : 13071351897
  IPC           : 0.210733
  L1D miss rate : 0.080153

- l1_l2
  simTicks      : 8047630980
  IPC           : 0.342283
  L1D miss rate : 0.079514

- nocache
  simTicks      : 572040798588
  IPC           : 0.004815
  L1D miss rate : -

## Mode: stride

- l1_16k
  simTicks      : 21337107534
  IPC           : 0.129115
  L1D miss rate : 0.638531

- l1_32k
  simTicks      : 20684055906
  IPC           : 0.133191
  L1D miss rate : 0.632207

- l1_l2
  simTicks      : 22121678511
  IPC           : 0.124535
  L1D miss rate : 0.398306

- nocache
  simTicks      : 478321702497
  IPC           : 0.005760
  L1D miss rate : -
