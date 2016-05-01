import sys
import os

from flask import Flask
app = Flask(__name__)
from pymongo import MongoClient

mongo=None
db=None

@app.route('/')
def hello_world():
  global mongo
  global db
  if not db:
    mongo=MongoClient('ds011412.mlab.com',11412)
    mongo.lora.authenticate("lora_ingester", "lora")
    db=mongo["lora"]

  cnt=db.uplinks.find().count()
  return 'Hello World!'+" %d messages"%cnt

if __name__ == '__main__':
    app.run()
