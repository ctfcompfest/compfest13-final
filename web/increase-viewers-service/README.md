# Increase Viewers Service

by Bonceng

## Flag

```
COMPFEST13-bliNdne55_dOe5nT_KiLL_f3elInGs_2397a9a094
```

## Description
Do you want to increase viewers on your website? Give us your RSS link, and then we will send it to our customers.

For a free plan, you can get one promotion for one domain every 15 minutes. Try it now!

Flag regex: `COMPFEST13-[A-z0-9_-]+`

## Difficulty
Hard

## Hints
- Read redis configuration file carefully
- Make your XML valid or invalid based on something when system trying to process it.

## Tags
XXE, SSRF, Redis RCE

## Deployment
1. Ganti flag di `src/app/Dockerfile`. Pastikan juga **tidak ada** flag di `public/app/Dockerfile`.
2. Lakukan deployment `src/corsproxy` ke web publik (e.g heroku, netlify, dkk).
3. Ubah variable `CORS_PROXY` di file `src/app/web/static/custom.js` dan `public/app/web/static/custom.js` sesuai dengan alamat dari web `src/corsproxy`.
4. Install docker engine>=19.03.12 and docker-compose>=1.26.2.
5. Run the container using:
    ```
    docker-compose up --build --detach
    ```

## Notes
- Usahakan one user one service karena kalau ada user lain flush db bisa kacau dan harus ulang dari awal
- [ ] Pastikan container app bisa diakses dari luar tapi gak bisa melakukan request selain ke cache
- [ ] Pastikan container cache gak bisa diakses dari luar dan gak bisa akses apapun
- [ ] Pastikan bisa overwrite cronjob di container cache
- [X] Pastikan untuk hapus semua file xml dan dtd di semua container
- [X] Pastikan debug mode off
- [X] Jangan lupa ngeganti CORS Proxy yang ada di `src/app/web/static/custom.js` dan `public/app/web/static/custom.js`