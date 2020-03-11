# Import the necessary libraries
import pandas as pd
import gmplot
# For improved table display in the notebook
from IPython.display import display

raw_data = pd.read_csv("Addresses_in_the_City_of_Los_Angeles.csv")

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
gmap.draw("my_heatmap.html")