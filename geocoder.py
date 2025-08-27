import mysql.connector
import googlemaps
import time
import os
from dotenv import load_dotenv

load_dotenv()

gmaps = googlemaps.Client(os.getenv("geocoderAPIKey"))

connection = mysql.connector.connect(
    host=os.getenv("dbHost"),
    user=os.getenv("dbUser"),
    password=os.getenv("dbPassword"),
    database="nyc_streetart"
)

cursor = connection.cursor()

cursor.execute("select address from street_art")
tuples = cursor.fetchall()
addresses = []

for tuple in tuples:
    addresses.append(tuple[0])


# fill coordinates 
coordinates = []

for addy in addresses:  
    result = gmaps.geocode(addy)
    location = result[0]['geometry']['location']
    coordinates.append([location['lat'], location['lng']])
    time.sleep(0.1)

# fill database with coordinates

id_counter = 1;
for coords in coordinates:
    lat =  coords[0]
    lng = coords[1]
    print(lat)
    print(lng)

    
    cursor.execute(
        "UPDATE street_art SET latitude = %s, longitude = %s WHERE id = %s", 
        (lat,lng,id_counter)           
    )
    id_counter += 1;
    





cursor.close()
connection.commit()
connection.close()