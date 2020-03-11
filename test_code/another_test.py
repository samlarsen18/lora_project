import sqlite3

sql_create_projects_table = """CREATE TABLE IF NOT EXISTS gps_coords (
                                    lat text NOT NULL,
                                    long text NOT NULL,
                                    time text NOT NULL,
                                    rssi integer NOT NULL,
                                    snr REAL NOT NULL 
                                )"""


my_conn = sqlite3.connect('gps_data.sqlite')
my_conn.close()
my_conn = sqlite3.connect('gps_data.sqlite')
cur = my_conn.cursor()
cur.execute(sql_create_projects_table)
my_conn.commit()
# 'INSERT INTO gps_coords (lat,long,time,rssi,snr) values ("{}","{}","{}",{},{})'.format(lat,lng,time,rssi,snr)
cur.execute('INSERT INTO gps_coords (lat,long,time,rssi,snr) values ("{}","{}","{}",{},{})'.format("lat","lng","time",1,0.0))
my_conn.commit()