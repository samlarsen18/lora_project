# Import the necessary libraries
import pandas as pd
import gmplot
import sqlite3
import gmaps
from ipywidgets.embed import embed_minimal_html
# For improved table display in the notebook
from IPython.display import display

sql_create_projects_table = """CREATE TABLE IF NOT EXISTS gps_coords (
                                    lat REAL NOT NULL,
                                    long REAL NOT NULL,
                                    time text NOT NULL,
                                    rssi integer NOT NULL,
                                    snr REAL NOT NULL 
                                )"""


def set_up_db():
    try:
        conn = sqlite3.connect('../lora_server/gps_data.sqlite')
        # my_conn.close()
    except:
        print("Something went wrong")
    cur = conn.cursor()
    cur.execute(sql_create_projects_table)
    conn.commit()
    conn.close()


def adjust_by_120(x):
    return x + 120


def make_negative(x):
    return x * (-1)


# Establish Connection
conn = sqlite3.connect("../lora_server/gps_data.sqlite")
cur = conn.cursor()
sql_data = pd.read_sql_query("SELECT * FROM gps_coords WHERE lat != 'None'", conn)

# Close Connection
conn.commit()
conn.close()

# Format Data
sql_data["long"] = sql_data["long"].apply(make_negative)
latitudes = sql_data["lat"]
longitudes = sql_data["long"]
print(longitudes)
locations = sql_data[['lat', 'long']]
sql_data["rssi"] = sql_data["rssi"].apply(adjust_by_120)
rssi = sql_data["rssi"]
print(rssi)
figure_layout = {
    'width': '100%',
    'height': '840px'
}

byu_coordinates = (40.247118312166805, -111.6482334121247)
fig = gmaps.figure(map_type='SATELLITE',
                   layout=figure_layout,
                   center=byu_coordinates,
                   zoom_level=16.5)

heatmap_layer = gmaps.heatmap_layer(
    locations, weights=rssi,
    max_intensity=100, point_radius=10.0
)
fig.add_layer(heatmap_layer)

embed_minimal_html('weighted_heatmap.html', views=[fig])
# print(latitudes)
# print(longitudes)
"""
# Let's limit the dataset to the first 15,000 records for this example
data = raw_data.head(n=15000)

# Store our latitude and longitude
latitudes = data["LAT"]
longitudes = data["LON"]

# Creating the location we would like to initialize the focus on.
# Parameters: Lattitude, Longitude, Zoom
gmap = gmplot.GoogleMapPlotter(34.0522, -118.2437, 10)

# Overlay our datapoints onto the map
gmap.heatmap(latitudes, longitudes)

# Generate the heatmap into an HTML file
gmap.draw("my_heatmap.html")

"""

"""raw_data = pd.read_csv("Addresses_in_the_City_of_Los_Angeles.csv")

# Success! Display the first 5 rows of the dataset
display(raw_data.head(n=5))
display(raw_data.info())

# Let's limit the dataset to the first 15,000 records for this example
data = raw_data.head(n=15000)

# Store our latitude and longitude
latitudes = data["LAT"]
longitudes = data["LON"]

# Creating the location we would like to initialize the focus on.
# Parameters: Lattitude, Longitude, Zoom
gmap = gmplot.GoogleMapPlotter(34.0522, -118.2437, 10)

# Overlay our datapoints onto the map
gmap.heatmap(latitudes, longitudes)

# Generate the heatmap into an HTML file
gmap.draw("my_heatmap.html")"""
