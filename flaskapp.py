import sys
import os
import StringIO
import signal
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
  
  deveuis=db.uplinks.find({},{"_id": False, "deveui": True}).distinct("deveui")

  output = StringIO.StringIO()
  cnt=db.uplinks.find().count()
  print >>output,  'Hello World!'+" %d messages"%cnt
  for deveui in deveuis:
    nr=db.uplinks.find({"deveui": deveui}, {"_id":False, "deveui": True}).count()
    print >>output, "<p/>";
    print >>output, "<table>"
    print >>output, "<tr>";
    print >>output, "<td>",deveui,"</td><td>",nr ,"</td>"
    print >>output, "</tr>";
    print >>output, "</table>"

  return output.getvalue()

def handler(signum, frame):
    print 'Here you go'


if __name__ == '__main__':
#    signal.signal(signal.SIGINT, handler)
    app.run()
#    print hello_world()
