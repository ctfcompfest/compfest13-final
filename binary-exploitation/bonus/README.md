# Bonus

by prajnapras19

---

## Flag

```
COMPFEST13{simpl3_FILE__4nd_O0ov3RfLow_5ae447a38e}
```

## Description
Since You are our shop manager, and we have working so hard these days, why don't you give us a bonus?

## Difficulty
easy-medium

## Hints
* Angelboy can make a file great again

## Tags
FILE struct, ROP

## Deployment
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

## Notes
- How to compile:
    ```
    gcc -no-pie -o chall chall.c
    ```