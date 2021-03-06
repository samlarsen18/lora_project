# Import the necessary libraries
import pandas as pd
import gmplot
# For improved table display in the notebook
from IPython.display import display

raw_data = pd.read_csv("coord_3.csv")

# Success! Display the first 5 rows of the dataset
display(raw_data.head(n=5))
display(raw_data.info())

# Let's limit the dataset to the first 15,000 records for this example
data = raw_data.head(n=400)

# Store our latitude and longitude
latitudes = data["lat"]
longitudes = data["long"]
print(longitudes)

# latitudes.remove("Done")

# Creating the location we would like to initialize the focus on.
# Parameters: Lattitude, Longitude, Zoom
gmap = gmplot.GoogleMapPlotter(40.24717, -111.6477, 16)
gmap.apikey = "NOT INCLUDED"
# Overlay our datapoints onto the map
ret = gmap.heatmap(latitudes, longitudes)
print(ret)
# Generate the heatmap into an HTML file
gmap.draw("my_heatmap.html")