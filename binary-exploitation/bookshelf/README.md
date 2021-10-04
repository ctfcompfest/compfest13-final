# Bookshelf

by prajnapras19

---

## Flag

```
COMPFEST13{00B_U4F__doUbL3_frrreee__7c2af20f46}
```

## Description
Keep your books tidy with our bookshelf. `nc <HOST> <PORT>`

## Difficulty
medium

## Hints
* If no solves until 2 hours after released, give the [source code](./src/chall.c).
* Free and free
* Don't think have any gadget? There is a thing that called one gadget.

## Tags
UAF, OOB, double free

## Deployment
- How to compile:
    ```
    gcc -o chall chall.c
    ```
- Jalankan:
    ```
    ./chall
    ```
- Workdir di `/home/nobody`
- libc 2.27, ubuntu 18.04
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

## Notes
- http://eternal.red/2018/children_tcache-writeup-and-tcache-overview/
- https://faraz.faith/2019-10-20-secconctf-2019-one/
- https://tc.gts3.org/cs6265/2019/tut/tut09-02-advheap.html
- https://heap-exploitation.dhavalkapil.com/diving_into_glibc_heap/security_checks
- https://sensepost.com/blog/2017/linux-heap-exploitation-intro-series-riding-free-on-the-heap-double-free-attacks/
- https://github.com/Mithreindeir/ctf-writeups/blob/master/pico-ctf2018/contacts/ReadMe.md
