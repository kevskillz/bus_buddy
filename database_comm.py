import serial
from datetime import datetime
import pymongo
from pymongo import MongoClient
f = open("pass.txt", "r")
passw = f.read().rstrip('\n')
cluster=MongoClient(f'mongodb+srv://kevskillz:{passw}@cluster0.ysqun.mongodb.net/bus_buddy?retryWrites=true&w=majority')
db = cluster['bus_buddy']
coll = db.time_logs



if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            line = str(line[1:])
            query = coll.find({'id':line})
            b = True
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M")
            if coll.count_documents({ 'id': line }, limit = 1) != 0:
               for log_poss in query:
                 if log_poss['off_time'] == "Null":
                    coll.update_one({"_id": log_poss["_id"]}, {"$set": {"off_time": dt_string}})
                    b = False

            if b:
                log = {
                    "id":line,
                    "off_time":"Null",
                    "on_time":str(dt_string)
                 }
                print("inserting")
                print(log)
                coll.insert_one(log)

