import serial
import pymongo
from pymongo import MongoClient
f = open("pass.txt", "r")
passw = f.read().rstrip('\n')
cluster=MongoClient(f'mongodb+srv://kevskillz:{passw}@cluster0.ysqun.mongodb.net/bus_buddy?retryWrites=true&w=majority')
db = cluster['bus_buddy']
coll = db['user_data']



if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            line = line[1:]
            query = coll.find({'id':line})
            for user in query:
               print(user['name'])

