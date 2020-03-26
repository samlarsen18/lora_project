import pandas as pd

# Read data from file 'filename.csv' 
# (in the same directory that your python process is based)
# Control delimiters, rows, column names with read_csv (see later) 
data = pd.read_csv("coord_1.csv") 
# Preview the first 5 lines of the loaded data 
data = pd.DataFrame(data)

for _, row in data.iterrows():
    rssi = row["rssi"]
    row["rssi"] = rssi * rssi * -1
data.to_csv("coord_1.csv")