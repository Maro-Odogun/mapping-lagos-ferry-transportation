import pandas as pd
import geopandas as gpd

# Get Ferry Data
ferry_data = pd.read_excel('data/Ferry Data.xlsx', sheet_name=[0, 1, 2, 3])

# Split into individual dataframes
terminals = ferry_data[0]
routes = ferry_data[1]
schedules = ferry_data[2]
boats = ferry_data[3]

# Extract the Latitudes and Longitudes from the 'Location' column
location_data = terminals['Location'].str.split(',').values.reshape(-1, 1)
latitudes = [float(row[0][0]) for row in location_data]
longitudes = [float(row[0][1].strip()) for row in location_data]

# Create latitude and longitude columns in the terminals dataframe
terminals['lat'] = latitudes
terminals['lng'] = longitudes
terminals.drop('Location', axis=1, inplace=True)

# Create point geometries from the data
terminals['geometry'] = gpd.points_from_xy(x=terminals['lng'], y=terminals['lat'], crs='epsg:4326')
geo_terminals = gpd.GeoDataFrame(terminals, crs='epsg:4326', geometry=terminals.geometry)


# Merge Terminal, Routes, Schedules, and Boat data on corresponding columns
routes_and_schedules = routes.merge(schedules, on='Route ID', how='inner')
routes_schedules_boats = routes_and_schedules.merge(boats, on='Boat ID', how='inner')
all_data = geo_terminals.merge(routes_schedules_boats, left_on='Terminal ID', right_on='Start Station ID', how='left')
all_data = all_data.rename(columns={'Name': 'Boat Name'})

# Get the names of the starting and ending stations based on ID
terminals_dict = geo_terminals[['Terminal ID', 'Terminal']].set_index('Terminal ID')['Terminal'].to_dict()
all_data['Starting Station'] = all_data['Start Station ID'].map(terminals_dict)
all_data['Ending Station'] = all_data['End Station ID'].map(terminals_dict)

# Get the latitudes and longitudes of the ending stations
terminal_lats = geo_terminals[['Terminal', 'lat']].set_index('Terminal')['lat'].to_dict()
terminal_lngs = geo_terminals[['Terminal', 'lng']].set_index('Terminal')['lng'].to_dict()
all_data['Ending Station Lat'] = all_data['Ending Station'].map(terminal_lats)
all_data['Ending Station Lng'] = all_data['Ending Station'].map(terminal_lngs)

# Simplify the data by removing middle stations and dropping terminals that do not start any route
all_data_simplified = all_data.drop('Middle Station ID', axis=1)
all_data_simplified = all_data_simplified.dropna(subset='Start Station ID')

#Get unique routes
routes_only = all_data_simplified.drop_duplicates(subset='Route ID')

# Get trip schedules for routes
trip_scheduled_info = all_data_simplified[['Route ID', 'Starting Station', 'Ending Station', 'Departure', 'Arrival', 'Boat Name']]
