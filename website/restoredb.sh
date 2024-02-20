DBNAME=RESERVATION
DATE=`date +"%Y%m%d"`
SQLFILE=$DBNAME-${DATE}.sql
mysqldump -u sanpepelone -pbigdaddy  $DBNAME
