#!/usr/bin/env sh
echo -e "\nStart mysqld"
/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &
sleep 5

php-fpm7
nginx -g 'daemon off;'