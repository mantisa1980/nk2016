mongo Question --eval "printjson(db.dropDatabase())"
mongo User --eval "printjson(db.dropDatabase())"
mongoimport -d Question -c General doc/question/question.json
