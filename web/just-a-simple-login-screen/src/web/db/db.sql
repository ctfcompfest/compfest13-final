CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) NOT NULL,
    pass VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO users (username, pass)
    VALUES ("SomeRamdomUnknownGuy", "ThisIsThisIsThisIsAReallyReallyLong4ndUnthinkablePassw0rd999112277");