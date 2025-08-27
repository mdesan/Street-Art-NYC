from bs4 import BeautifulSoup
import requests
import time
import mysql.connector
import re
import os
from dotenv import load_dotenv

load_dotenv()


connection = mysql.connector.connect(
    host=os.getenv("dbHost"),
    user=os.getenv("dbUser"),
    password=os.getenv("dbPassword"),
    database = "nyc_streetart"
)
cursor=connection.cursor()


base_url = "https://streetartcities.com/"
list_url = "https://streetartcities.com/cities/newyork/artworks?status=active"
headers={"User-Agent": "Mozilla/5.0"}

#get the main page with all artwork "cards"
response=requests.get(list_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

grid = soup.find("div", class_="grid mt-4 grid-cols-2 md:grid-cols-3 gap-3")


artwork_cards = grid.find_all("div", class_="absolute bottom-0 left-0 right-0 px-3 py-2 text-sm text-white")


#-----------------------------------------------------------------------------------------------------------------------
#get all titles and artists

# id_counter=1
# for div in artwork_cards:
#     inner_divs = div.find_all("div")

#     artist = "Unknown"
#     title = "Untitled"

#     if len(inner_divs)==2:
#         artist = inner_divs[0].text.strip()
#         title =  inner_divs[1].text.strip()
#     elif (len(inner_divs) ==1) and (len(inner_divs[0].text.strip())!=0):
#         artist = inner_divs[0].text.strip()
#     elif (len(inner_divs) ==1) and (len(inner_divs[0].text.strip())==0):
#         artist = "Unknown"
#         title = "Untitled"
    
#     print(title + " by " + artist)
#     print(id_counter)

#     id_counter+=1

#     # add titles and artists to database
#     cursor.execute(
#         "insert into street_art (title, artist) values (%s, %s)",
#         (title, artist)
#     )
#-----------------------------------------------------------------------------------------------------------------------

#get the addresses

# pathways_to_addresses = grid.find_all("a", class_="h-24 sm:h-48 rounded-lg shadow-l relative")

# id_counter =1
# for pathway_to_address in pathways_to_addresses:
#     href = pathway_to_address.get("href")

#     artwork_url = base_url + href

#     artwork_response = requests.get(artwork_url, headers=headers)
#     artwork_soup = BeautifulSoup(artwork_response.text, "html.parser")

#     address_section = artwork_soup.find("div", class_="flex-3")
   
#     inner_divs = address_section.find_all("div")
   
#     address = inner_divs[1].text.strip()

#     cursor.execute(
#         "update street_art set address = %s where id = %s",
#         (address, id_counter)
#     )

#     id_counter+=1


#     print("Address:", address)
    
#     print(id_counter)
#-----------------------------------------------------------------------------------------------------------------------

#get the image urls 

# pathways_to_addresses = grid.find_all("a", class_="h-24 sm:h-48 rounded-lg shadow-l relative")

# img_url_list  =[]

# id_counter =1
# for pathway_to_address in pathways_to_addresses:
#     href = pathway_to_address.get("href")

#     artwork_url = base_url + href

#     artwork_response = requests.get(artwork_url, headers=headers)
#     artwork_soup = BeautifulSoup(artwork_response.text, "html.parser")

#     style = artwork_soup.find("header", style=re.compile(r'background-image')).get("style")
#     img_url = re.search(r'url\(["\']?(.*?)["\']?\)', style).group(1)

#     img_url_list.append(img_url)

#     cursor.execute(
#         "update street_art set img_url = %s where id = %s",
#         (img_url, id_counter)
#     )
#     id_counter+=1


# for url in img_url_list:
#     print(url)




connection.commit()
cursor.close()
connection.close()
 
time.sleep(1)