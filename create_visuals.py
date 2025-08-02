import plotly.express as px
from data_loader import routes_only
import folium

hover_data = {
    'lat': False,
    'lng': False,
    'Type': True,
    'Status': False,
    'Address': True
}

def create_scatter_map(df):
    fig = px.scatter_map(
        data_frame=df, 
        lat=df.lat, 
        lon=df.lng, 
        hover_name='Terminal', 
        hover_data=hover_data, 
        color='Status',  
        color_discrete_sequence=px.colors.qualitative.Set1, 
        zoom=10
    )

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Rockwell",
            font=dict(color='black')
        ),
        legend=dict(
            x=0.35,   
            y=0.24,  
            xanchor='left',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.4)',  
            bordercolor='black',
            font=dict(color='black', size=12),
            borderwidth=1
        ),
        height=600,
        width=800
    )

    fig.update_traces(
        marker=dict(
            size=8,
            opacity=0.8
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )

    return fig


def create_folium_map(start_location):
    map_lagos = folium.Map(location=start_location, zoom_start=13)
    for row in routes_only.iterrows():
        point = row[1]
        icon = folium.Icon(icon='info-sign', 
                        color='red')
        marker = folium.Marker(
            location=(point['lat'], point['lng']),
            icon=icon, 
            # Get summary info on terminal point
            popup=folium.Popup(f"<b>Terminal Name</b>: {point['Terminal']} <br>" \
                + f"<b>Address</b>: {point['Address']} <br>" \
                + f"<b>Type</b>: {point['Type']} <br>" \
                + f"<b>Nature</b>: {point['Nature']} <br>" \
                + f"<b>Status</b>: {point['Status']} <br>", max_width=300
            )
        )

        line = folium.PolyLine(
            locations=[(point['lat'], point['lng']), 
                    (point['Ending Station Lat'], point['Ending Station Lng'])],
            # Display the Route ID to obtain schedule information upon click
            tooltip=f"{point['Route ID']}",
            weight=6,
            # Get summary info on route
            popup=folium.Popup(f"<b>{point['Terminal']} <-> {point['Ending Station']}</b> <br>" \
                + f"<b>Price</b>: ₦{point['Price']} <br>" \
                + f"<b>Duration (mins)</b>: {point['Duration (mins)']}",
                max_width=300
            )
        )

    
        marker.add_to(map_lagos)
        line.add_to(map_lagos)
        
    return map_lagos