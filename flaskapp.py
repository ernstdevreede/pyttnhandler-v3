import sys
import os
import StringIO
import signal
import json
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
    last=db.uplinks.find({"deveui":deveui},{"_id":0, "payload_fields":1, "metadata.time": { "$slice": 1}}).sort([("_id", -1)])
    if "payload_fields" in last[0]:
      print "[[",last[0]["payload_fields"], "]]"
      last=last[0]
      lastdata=None
      lastdata=last["payload_fields"]
#    try:
#      lastdata=json.loads(last["payload_fields"])
#    except ValueError:
#      pass
      try:
	lasttime=last["metadata"]["gateways"][0]["time"]
      except KeyError:
	lasttime="-"
      try:
	lastservertime=last["metadata"]["time"]
      except KeyError:
	lastservertime="-"
  
 
      print >>output, "<p/>";
      print >>output, "<table>"
      print >>output, "<tr>";
      print >>output, "<td>",deveui,"</td><td>",nr ,"</td>","<td>",lasttime,"</td>"
      print >>output, "<td>",lastservertime,"</td>"

      if lastdata:
	if "t" in lastdata:
	  print >>output,"<td>",lastdata["t"],"</td>"
	else:
	  print >>output, "</td>"
      print >>output, "</tr>";
      print >>output, "</table>"

  return output.getvalue()

def handler(signum, frame):
    print 'Here you go'


if __name__ == '__main__':
#    signal.signal(signal.SIGINT, handler)
    app.run()
#    print hello_world()
