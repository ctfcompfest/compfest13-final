# Writeup - WaifuDroid Returns

Diberikan suatu bot Discord (lagi), setiap pesan yang dikirim kepada bot tersebut diproses pada suatu konteks VM baru. Tujuan kita adalah untuk menginput *justonemoresecret* tanpa menginput string tersebut karena setiap input disanitise secara rekursif. Selain itu, juga tidak bisa menginput angka dan `/[0-9\"'+]/` serta "``". Yang bisa dilakukan adalah dengan menurunkan string dari hasil return `typeof()`. Sebagai contoh, 
```
typeof([]) == `object`
typeof(typeof([])) == typeof(`object`) == `string`
typeof(x) == `undefined` // Karena tidak ada variabel x
(typeof(x)).search(typeof([])) == -1
```
Sehingga kita tinggal mencari nama tipe-tipe data yang memiliki karakter-karakter yang diinginkan dan mengginakan `search()` untuk mencapai indeks yang tepat. Sebagai contoh,
```
typeof(x) == `undefined`
(typeof(x)).search(typeof(x)) == 0
(typeof(x))[(typeof(x)).search(typeof(x))] == `undefined`[0] == `u`
```
yang dapat pula digunakan untuk mendapatkan karakter-karakter lainnya, lalu tinggal di*concat*.
Detail breakdown *payload* terdapat pada `payload_breakdown.txt`.

![img0](https://cdn.discordapp.com/attachments/815844122673938453/892843117303193671/unknown.png)

## Flag
```
COMPFEST13{I_sWe412_1_maD3_H3r_tH3_m05T_tRu57w0rThY_b07_3VeRrr_10fad5dc9c}
```