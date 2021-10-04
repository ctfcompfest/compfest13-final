# Writeup QuiccReader

Diberikan suatu *web app* yang membaca files pada sistem. Ternyata kita dapat melakukan injeksi Bash. Dengan menginject `ls` dapat kita lihat struktur direktori tersebut.

![img0](https://cdn.discordapp.com/attachments/815844122673938453/892844074007146516/unknown.png)
Terlihat bahwa terdapat file `flag.txt` yang hanya dapat dibaca oleh `root`, dan juga binary `admin_reader` yang di`setuid` dan dapat membaca files. Yang perlu dilakukan adalah membuat file baru yang cukup panjang, memanggil `admin_reader` untuk membaca file tersebut, dan ketika file sedang dibaca, ubah file menjadi *symbolic link* ke `flag.txt`. Lakukan ini berkali-kali hingga akhirnya *race condition* berupa *time-of-check time-of-use* (TOCTOU) dapat timbul dan `admin_reader` mencetak `flag.txt`.

![exp](https://cdn.discordapp.com/attachments/815844122673938453/890639231079313468/unknown.png)

## Flag
```
COMPFEST13{I_sWe412_1_maD3_H3r_tH3_m05T_tRu57w0rThY_b07_3VeRrr_10fad5dc9c}
```