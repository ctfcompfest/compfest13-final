# Freshly Random

by sl0ck

---

## Flag

```
COMPFEST13{0K_m4yB_S0me_pRn6_4r3_N0t_f0R_r54_91ccc43458}
```

## Description
I own some random store across the street. We sell some homemade, freshly generated random numbers and RSA-encrypted messages... who knows, maybe you can even get something more out of them?

## Difficulty
Tingkat kesulitan soal: medium

## Hints
* how is the randomness achieved?
* idk about you but e seems quite small

## Tags
RSA, pseudorandom number generation, Mersenne Twister, Franklin-Reiter 

## Deployment
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

## Notes
* "Freshly Random" -> "FR" -> hint Franklin Reiter o_o
* Solusi intended butuh minimal 106 kali requests untuk ekstrak flag.