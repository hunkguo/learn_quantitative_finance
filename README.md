学习量化金融之路



运行mongo
mongod --config /usr/local/etc/mongod.conf
mongo查询
db.getCollection("trade_data_daily").find().sort({_id:-1}).limit(10)

ssh -i zbq.pem root@ctyun.listenvideo.club