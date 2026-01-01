from bs4 import BeautifulSoup

# Read your HTML file
with open('aaa.htm', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all <option> tags with value containing "https://www.ncdex.com/products/"
option_tags = soup.find_all('option', value=True)
print(option_tags)
# Filter options that contain "https://www.ncdex.com/products/" in the value
filtered_options = [option.text.strip() for option in option_tags]

# Print the extracted option content (text inside the <option> tags)
for content in filtered_options:
    print(content)
