# Secret scraper on the hunt for hidden gems

import requests
from bs4 import BeautifulSoup

print("Enter the website that you want to search for secrets:")
website = input() # user input for the website

def secret_scraper(website): # parsing through the site to find all the links
    
    try:
        source_code = requests.get(website)
        soup = BeautifulSoup(source_code.text, 'html.parser')
    except requests.exceptions.RequestException as e: # just in case the site is down or dosen't exist
        print("Whoops! Something is screwy with the website.")
        print(e)
        

    links = []
    for line in soup.find_all("a"):
        links.append(line.get("href")) # adding the links to the list
    return links

results = secret_scraper(website)
for item in results:
    print(item) # printing out the links
    
    
    



