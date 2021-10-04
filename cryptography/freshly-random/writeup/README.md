# Writeup - Freshly Random

Diketahui program memiliki dua fungsionalitas (selain exit), yaitu men-*generate* suatu angka acak sebesar 192 bit, dan mencetak flag yang telah dienkripsi. 
Fungsi pertama, yaitu membuat angka acak:

![imgRandom](https://cdn.discordapp.com/attachments/815844122673938453/846601835036934154/unknown.png)

Fungsi kedua, mencetak flag yang dienkripsi:

![imgEncryptedFlag](https://cdn.discordapp.com/attachments/815844122673938453/846602043158167592/unknown.png)

Maka, kita dapat menginspeksi *source code* dari soal ini. Bagian generasi angka acak adalah sebagai berikut:

![imgRandomCode](https://cdn.discordapp.com/attachments/815844122673938453/846602752172097556/unknown.png)

Tampaknya, angka acak dibuat melalui fungsi `getrandbits()` yang terdapat pada modul `random` di library Python. Fungsi `getrandbits()` dipanggil sebanyak 6 kali, lalu hasil setiap pemanggilan dikonkatenasi dengan hasil pemanggilan fungsi pada iterasi pertama yang menjadi *most significant bits* hingga hasil terakhir menjadi *least significant bits*.
Kita mengetahui bahwa modul `random` pada Python pada intinya menggunakan *pseudo-random number generator* yaitu [Mersenne-Twister](https://en.wikipedia.org/wiki/Mersenne_Twister)  (persisnya implementasi MT19937) yang tidak bersifat *cryptographically secure*. Oleh karena itu, terdapat *exploit* yang dapat digunakan untuk mengekstrak *internal state* dari generator tersebut. Mengingat pada kasus ini generator menyimpan seluruh 32-bit outputnya (tidak di*shift* ke kanan sebanyak *32 - n* kali sebagaimana apabila jika jumlah bit sebesar *n* dengan *32 > n*), maka kita dapat menggunakan extractor seperti [ini](https://github.com/eboda/mersenne-twister-recover/blob/master/MTRecover.py). Kita hanya perlu untuk membagi angka yang diberikan menjadi 6 angka 32-bit.
Untuk MT19937, ekstraksi *internal state* memerlukan 624 output dari PRNG tersebut. Pada kasus ini, karena PRNG dipanggil sebanyak 6 kali untuk setiap *request* yang kita berikan, maka kita hanya perlu membuat *request* sebanyak *624 / 6 = 104* kali untuk mendapatkan *internal state*nya. 

![imgRandomExtract](https://cdn.discordapp.com/attachments/815844122673938453/846607406569226280/unknown.png)

Setelah dapat mereplikasi generator yang digunakan, kita tinggal berfokus kepada *attack* terhadap enkripsi yang digunakan. Implementasi enkripsi adalah sebagai berikut: 

![imgPubKey](https://cdn.discordapp.com/attachments/815844122673938453/846607969587298304/unknown.png)

Terlihat bahwa modulus *N* merupakan hasil kali dua bilangan prima 1024 bit, dan eksponen *e* telah di*hard-coded* bernilai `0x17`. Sementara itu, skema enkripsi adalah:

![imgEncrypt](https://cdn.discordapp.com/attachments/815844122673938453/846608488947384370/unknown.png)

Ternyata flag dienkripsi menggunakan RSA dengan *padding* yaitu hash SHA-256 dari *random bytes* yang dibuat menggunakan fungsionalitas `rand()` yang sebelumnya telah diperiksa. Mengingat eksponen *e* kecil (`0x17`), maka kita dapat menggunakan *Franklin-Reiter related messages attack* untuk permasalahan ini. Kita perlu untuk mencari GCD dari dua polinomial yaitu selisih `(X + pad) ^ e` dengan *ciphertext* terkait pada *ring* `Z mod N`. Implementasinya adalah sebagai berikut:

![imgFR](https://cdn.discordapp.com/attachments/815844122673938453/846609391046230086/unknown.png)

Dengan semua informasi tersebut kita dapat mengekstrak *flag* minimal dalam 106 kali request (104 untuk ekstraksi *internal state* MT19937 dan 2 untuk *attack* Franklin-Reiter).

![imgSolve](https://cdn.discordapp.com/attachments/815844122673938453/846600132866080798/unknown.png)

## Flag
```
COMPFEST13{0K_m4yB_S0me_pRn6_4r3_N0t_f0R_r54_91ccc43458}
```