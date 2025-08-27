from bs4 import BeautifulSoup
import requests
import mysql.connector

#scrapping
# page_to_scrape = requests.get("https://quotes.toscrape.com/")
# soup = BeautifulSoup(page_to_scrape.text, "html.parser")

# quotes = soup.find_all("span", attrs={"class":"text"})
# authors = soup.find_all("small", attrs={"class":"author"})
#-----------------------------------------------------------------------------------------------------------
#fill database
# connection = mysql.connector.connect(

# )

# cursor = connection.cursor()

# for quote, author in zip(quotes, authors):
#     quote_text = quote.text
#     author_text = author.text
#     cursor.execute("INSERT INTO quotes (quote,author) VALUES (%s,%s)", (quote_text, author_text))

# connection.commit()
# cursor.close()
# connection.close()
#-----------------------------------------------------------------------------------------------------------
#print from sql database to console 
 
conn = mysql.connector.connect(

 )

cursor = conn.cursor()
cursor.execute("select * from quotes")

rows = cursor.fetchall()

for row in rows:
    print(row)
    

cursor.close()
conn.close()





