import time
import ttn
import base64
import sqlite3

sql_create_projects_table = """CREATE TABLE IF NOT EXISTS gps_coords (
                                    lat REAL NOT NULL,
                                    long REAL NOT NULL,
                                    time text NOT NULL,
                                    rssi integer NOT NULL,
                                    snr REAL NOT NULL 
                                )"""

app_id = "sams_first_app"
access_key = "ttn-account-v2.4iE2PtMMgBHla2mohYH-9iLidrw-sjsfz3ji789lso8"

def uplink_callback(msg, client):
  print("Received uplink from ", msg.dev_id)
  #print(msg)
  #print("gps cord: ",base64.b64decode(msg.payload_raw).decode())

  #Parse payload
  lat = base64.b64decode(msg.payload_raw).decode().split()[0][1:-1]
  lng =  base64.b64decode(msg.payload_raw).decode().split()[1][1:-1]
  time = msg.metadata.time
  rssi = msg.metadata.gateways[0].rssi
  snr = msg.metadata.gateways[0].snr
  
  #Establish Connection
  conn = sqlite3.connect("gps_data.sqlite")
  cur = conn.cursor()

  #Save data to DB
  cur.execute('INSERT INTO gps_coords (lat,long,time,rssi,snr) values ("{}","{}","{}",{},{})'.format(lat,lng,time,rssi,snr))
  conn.commit()
  conn.close()

def connect_callback(res, client):
  print("Connected with ", app_id)

def downlink_callback(mid, client):
  print("downlink from ", client)
  print("message id ", mid)

def set_up_db():
  try:
    conn = sqlite3.connect('gps_data.sqlite')
    # my_conn.close()
  except:
    print("Something went wrong")
  cur = conn.cursor()
  cur.execute(sql_create_projects_table)
  conn.commit()
  conn.close()


handler = ttn.HandlerClient(app_id, access_key)

# Set up table
set_up_db()

# using mqtt client
mqtt_client = handler.data()
mqtt_client.set_uplink_callback(uplink_callback)
mqtt_client.set_connect_callback(connect_callback)
mqtt_client.set_downlink_callback(downlink_callback)
mqtt_client.connect()

# time.sleep(180)
while True:
  time.sleep(10)
mqtt_client.close()

# using application manager client
app_client =  handler.application()
my_app = app_client.get()
print(my_app)
my_devices = app_client.devices()
print(my_devices)