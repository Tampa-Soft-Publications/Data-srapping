import requests
from bs4 import BeautifulSoup

# Replace this with the URL of the site you're targeting
url = 'https://catalog.usf.edu/content.php?catoid=23&navoid=3958'

# Fetch the content of the page
response = requests.get(url)
html = response.text

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find all <li> elements with the specified style
list_items = soup.find_all('li', style="list-style-type: none")

# Print or process the items
f = open("links-of-programs.txt", 'w')
g = open("names-of-programs.txt", 'w')
for li in list_items:
    s = "https://catalog.usf.edu"
    a_tag = li.find('a')
    if a_tag and 'href' in a_tag.attrs:
        f.write(s+str(a_tag["href"]))
        g.write(a_tag.text)


f.close()
g.close()
