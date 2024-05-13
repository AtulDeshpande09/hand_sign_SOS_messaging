import requests
import folium

# But its not accurate!!!!
# I suggest using GPS or anything else to obtain accurate location.
# In this code i have used IP address for getting location.
# You can also directly pass the cordinates into display_map() function.

def get_computer_location():
    try:
        # Request the IP-API service for location information
        response = requests.get('http://ip-api.com/json/')
        data = response.json()

        if response.status_code == 200 and data['status'] == 'success':
            latitude = data['lat']
            longitude = data['lon']
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print("Error occurred:", e)
        return None, None

latitude, longitude = get_computer_location()

if latitude is not None and longitude is not None:
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Unable to retrieve computer location.")


def display_map(latitude, longitude):
    """Takes latitude and longitude of location and marks the location in the map"""
    
    # Create a map centered around the provided coordinates
    map_object = folium.Map(location=[latitude, longitude], zoom_start=20)

    # Add a marker for the provided coordinates
    folium.Marker(location=[latitude, longitude], popup='Location').add_to(map_object)

    # Save the map to an HTML file
    map_object.save('templates/map.html')


# Here you can also pass actual cordinates. you can get codinates from google maps with GPS location.
#display_map(latitude, longitude)
