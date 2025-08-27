import mysql.connector
import json
import re

import os
from dotenv import load_dotenv

load_dotenv()


# connection = mysql.connector.connect(
#    host=os.getenv("dbHost"),
#    user=os.getenv("dbUser"),
#    password=os.getenv("dbPassword"),
#     database = "nyc_streetart"
# )
# cursor=connection.cursor(dictionary=True)

# cursor.execute("select title, artist, address, latitude, longitude, img_url from street_art")
# rows = cursor.fetchall()

# with open("artworks.json", "w", encoding="utf-8") as f:
#     json.dump(rows,f,indent=2)

# print("json file generated with" , len(rows), "artworks.")

# cursor.close()
# connection.close()
