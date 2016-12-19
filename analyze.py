import os
import StringIO
import signal
import json
from pymongo import MongoClient
from datetime import datetime,timedelta

mongo=None
db=None

def hello_world():
  global mongo
  global db
  if not db:
    mongo=MongoClient('ds011412.mlab.com',11412)
    mongo.lora.authenticate("lora_ingester", "lora")
    db=mongo["lora"]
    deveuis=db.uplinks.find({},{"_id": False, "deveui": True}).distinct("deveui")

  deveuis=db.uplinks.find({},{"_id": False, "deveui": True}).distinct("deveui")

  cnt=db.uplinks.find().count()
  print " %d messages"%cnt
  for deveui in deveuis:
    nr=db.uplinks.find({"deveui": deveui}, {"_id":False, "deveui": True}).count()
    cur=db.uplinks.find({"deveui":deveui},{"_id":0, "decoded":1, "metadata.gateway_time": { "$slice": 1}}).sort([("_id", 1)])
    prevdt=None
    for msg in cur:
      (dt, mSecs)=msg["metadata"][0]["gateway_time"].strip().split(".")
      dt=datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
      mSecs=mSecs.replace("Z", "")
      dt = dt + timedelta(microseconds=float("0."+mSecs)*1000000)
      if prevdt:
        print deveui,msg["metadata"][0]["gateway_time"],dt, dt-prevdt
      else:
        print deveui,msg["metadata"][0]["gateway_time"],dt, "-" 
      prevdt=dt



if __name__=="__main__":
  hello_world()

