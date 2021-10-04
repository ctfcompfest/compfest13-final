# QuiccReader

by sl0ck

---

## Flag

```
COMPFEST13{R34deR_b3_n1Mbl3_12eAd3R_Be_qu1Cc_bu7_n0T_45_qU1cK_as_M3_a2b1c5313c}
```

## Description
My colleague Mr. Frink Zippy surfs the web a lot.. he never leaves his web browser! He even made a web app to read local files so he never has to leave his browser. He claims that his app is secure enough so that people still won't be able to read things they're not supposed to. I hope he's right.

## Difficulty
easy-medium

## Hints
* i start to doubt if the site can read as quickly as claimed...

## Tags
bash injection, race condition, TOCTOU

## Deployment
- ./src/files jadi files pada home directory di container
- `flag.txt` perlu di `chown` jadi root (`$ sudo chown root:root ./flag.txt`) hanya readable oleh root (`$ sudo chmod 400 ./flag.txt`)
- Executable `admin_reader` perlu di `chown` jadi root (`$ sudo chown root:root ./admin_reader`) dan di `setuid` (`$ sudo chmod 755 ./admin_reader ; sudo chmod u+s ./admin_reader`).
- Python terinstall di container

## Notes
> Intentionally left empty
