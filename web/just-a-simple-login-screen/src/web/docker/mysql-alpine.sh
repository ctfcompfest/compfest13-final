#!/usr/bin/env sh
MYSQL_ROOT_PASSWORD=SecretPassword
MYSQL_DATABASE=challenge
MYSQL_USER=hanyabaca
MYSQL_PASSWORD=Bacaajajangandidrop

echo "Installing mysql"
apk update && apk add --no-cache mysql mysql-client

echo -e "\nCreate directory to run the mysqld bg process"
mkdir -p /run/mysqld
chown -R mysql:mysql /run/mysqld

echo -e "\nLoad the database file"
chown -R mysql:mysql /var/lib/mysql
mysql_install_db --user=mysql --ldata=/var/lib/mysql

echo -e "\nStart mysqld"
/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &
sleep 5

echo -e "\nSet root password"
mysqladmin -u root password "${MYSQL_ROOT_PASSWORD}"

echo -e "\nCreate database ${MYSQL_DATABASE}"
echo "CREATE DATABASE ${MYSQL_DATABASE};" | mysql -u root -p="${MYSQL_ROOT_PASSWORD}"

echo -e "\nCreate user ${MYSQL_USER}"
echo "CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';" | mysql -u root -p="${MYSQL_ROOT_PASSWORD}"

echo -e "\nGrant select privileges on all database for ${MYSQL_USER}"
echo "GRANT SELECT ON *.* TO '${MYSQL_USER}'@'localhost';" | mysql -u root -p="${MYSQL_ROOT_PASSWORD}"
echo "FLUSH PRIVILEGES;" | mysql -u root -p="${MYSQL_ROOT_PASSWORD}"

for FILE in /db/*.sql; do
    echo -e "\nBackup ${FILE} to ${MYSQL_DATABASE}"
    mysql -u root -p="${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE} < $FILE
done

echo -e "\nStop mysqld"
mysqladmin -u root -p="${MYSQL_ROOT_PASSWORD}" shutdown