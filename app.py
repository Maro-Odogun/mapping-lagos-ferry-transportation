import streamlit as st
from create_visuals import create_scatter_map, create_folium_map
from data_loader import geo_terminals, trip_scheduled_info
from streamlit_folium import st_folium

app_title = 'Lagos Ferry Transportation'
app_h1 = 'Terminals/Jettys across the State'
app_h2 = 'Available Routes'

st.title(app_title)
st.header(app_h1)


# Display Plotly Scatter Map
scatter_map = create_scatter_map(geo_terminals)
st.plotly_chart(scatter_map, use_container_width=True)


# Display Folium Map for routes
start_location = (6.445737749170641, 3.415135796913002)   #Keffi Street
map_lagos = create_folium_map(start_location)
st.header(app_h2)
st.caption('Click on the route lines for trip schedule information')
routes_map = st_folium(map_lagos, height=500, use_container_width=True)


# Get schedule for route with Route ID
route_id = ''
if routes_map["last_object_clicked_tooltip"]:
    st.subheader('Schedules')
    route_id = float(routes_map["last_object_clicked_tooltip"])
    st.write(trip_scheduled_info[trip_scheduled_info['Route ID'] == route_id].reset_index(drop=True))
