# Writeup - LZ21
Diberikan 3 file, ketiganya tampak sangat berantakan. Dari membukanya melalui text editor, terlihat bahwa `main` dan `func` kemungkinan merupakan *source files*, sementara `lorem` merupakan teks lorem ipsum biasa. Maka, teks `lorem` dapat digunakan untuk mempelajari apa yang telah terjadi pada file-file tersebut. Apabila `lorem` dibuka dengan *hex editor*, maka akan terlihat bahwa setiap karakter alfabet didahului oleh 2 byte.

![img1](https://cdn.discordapp.com/attachments/815844122673938453/834358227377455154/unknown.png)

Terlihat pula bahwa karakter yang sudah tertulis tidak terulang lagi, menunjuk pada kemungkinan bahwa terdapat suatu skema kompresi yang dilakukan terhadap teks tersebut. Tiadanya *dictionary* yang dideklarasikan secara eksplisit di awal file dan dua byte yang mendahului tiap karakter alfabet mengindikasikan bahwa kompresi yang digunakan adalah suatu jenis [LZ77](https://en.wikipedia.org/wiki/LZ77_and_LZ78). Pada LZ77, tiap karakter yang tidak ditemukan pada dictionary akan diawali dengan dua byte 0, sementara jika ditemukan, maka byte pertama akan diisi oleh jarak menuju kemunculan terakhir dan byte kedua adalah panjang dari *match* yang terpanjang.

![img2](https://www.researchgate.net/publication/322296027/figure/fig4/AS:579960579346433@1515284785811/An-example-of-LZ77-encoding.png)

Dari teks `lorem`, terlihat bahwa substring pertama yang hilang adalah `"m "`pada `"ipsum "`mengingat `"m "` telah ditemukan sebelumnya pada `"Lorem "`. Dapat dicek bahwa hipotesis berlaku dengan menghitung jarak dari kemunculan `"m "` ke kemunculan sebelumnya yaitu 6 karakter. Sementara, 2 byte yang mengisi kehilangan substring tersebut adalah `06 20`, dan benar bahwa byte pertama merupakan offset dari kemunculan terakhir hingga buffer.
```
...
00 00 65 -> 'e' 
00 00 6D -> 'm' // i - 6
00 00 20 -> ' ' // i - 5
00 00 69 -> 'i' // i - 4
00 00 70 -> 'p' // i - 3
00 00 73 -> 's' // i - 2
00 00 75 -> 'u' // i - 1
06 20 64 -> 'd' // i
...
```
Namun, tampaknya terdapat sesuatu yang salah. Byte kedua yang seharusnya merupakan panjang bernilai `0x20`, padahal substirng `"m "` hanya memiliki panjang 2. Perlu diperhatikan bahwa kita menggunakan little endian, sehingga nilai biner dari kedua byte tersebut adalah
```
Expected:
0110 0000 0100 0000 (06 02)
Actual:
0110 0000 0000 0100 (06 20)
```
Mengingat panjang substring tersebut adalah 2, maka pasti hanya `0100` yang merupakan panjang dari substring. Hal ini menunjukkan bahwa salah satu varian LZ77 yang menggunakan offset sebesar 12 bit dan informasi panjang sebesar 4 bit digunakan. (Untuk lebih detailnya [di sini](https://en.wikibooks.org/wiki/Data_Compression/Dictionary_compression))
Sehingga, dapat diilustrasikan bahwa pembagian dua byte tersebut adalah
```
0110 0000 0000 (6) => offset ke kemunculan terakhir (12 bit)
0100 (2) => panjang substring (4 bit)
```
Maka, kita dapat memulai proses dekompresi dengan membaca file dan menginspeksi tiap chunk yang terdiri atas 3 bytes.
```python
with  open("lorem", "rb")  as file:
	content = file.read()
	out =  ''
	for i in  range(0, len(content), 3):
		triplet =  content[i:i+3]
```
Pastikan bahwa tiap kali 2 bytes pertama bernilai 0, maka karakter (elemen ketiga dalam triplet) langsung dikonkatenasi ke string output.
```python
if(triplet[0]  ==  0  and  triplet[1]  ==  0):
	out +=  chr(triplet[2])
	continue
```
Sebaliknya, jika tidak, maka kita dapat menggunakan offset dan panjang yang terkandung dalam 2 bytes pertama tiap chunk untuk menemukan substring yang dihapus. Mengingat di sini kita menggunakan LZ77 dengan variasi (12 bit, 4 bit), maka kita perlu mengambil 4 bit pertama dari byte panjang dan melakukan konkatenasi dengan byte offset, agar membentuk bit string 12 bit. Lalu, untuk byte panjang, perlu dihapus 4 bit pertamanya, dapat dilakukan dengan bit shifting ke kanan sebanyak 4 kali. Pada akhirnya, kita dapat mengambil substring dari string yang telah terbentuk berdasarkan informasi dari 2 byte pertama tersebut (mulai dari `buffer - offset` sebanyak `length `kali), kemudian melakukan konkatenasi sekali lagi dengan karakter pada byte terakhir pada chunk tersebut.
```python
offset = (triplet[1]  &  0b1111) <<  8  |  triplet[0]
length =  triplet[1]  >>  4
absolute_pos =  len(out)  - offset
out +=  out[absolute_pos:absolute_pos + length]  +  chr(triplet[2])
```
Maka, kita dapat mencoba untuk melakukan *decompression* pada file tersebut, dan berhasil. 

![img3](https://cdn.discordapp.com/attachments/815844122673938453/834367880229289984/unknown.png)

Selanjutnya, kita tinggal melakukan *decompression* pada `main` dan `func`. Terlihat bahwa keduanya merupakan program Python sangat sederhana yang menerima input password dan melakukan verifikasi. 
File `main`:

![img4](https://cdn.discordapp.com/attachments/815844122673938453/834368488821882921/unknown.png)

File `funcs`:

![img5](https://cdn.discordapp.com/attachments/815844122673938453/834368769118830592/unknown.png)

dst.
Password diverifikasi dengan suatu sistem persamaan (total terdapat 32 persamaan), kita tinggal memasukkan semuanya ke Z3 untuk mendapatkan *pass key*nya.

![img6](https://cdn.discordapp.com/attachments/815844122673938453/834369496734760960/unknown.png)

Maka, kita dapatkan pass key:

![img7](https://cdn.discordapp.com/attachments/815844122673938453/834369705199403008/unknown.png)

Lalu, memasukkannya pada `main`:

![img8](https://cdn.discordapp.com/attachments/815844122673938453/834369924327145472/unknown.png)

## Flag
```
COMPFEST13{Sm0l1n_wuvz_Lz1_bb622fbc0c}
```