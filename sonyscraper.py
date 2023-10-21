import requests
import re
from bs4 import BeautifulSoup

show_names = []
url = input("enter base url: ")
season_num = input("enter season number: ")
from urllib.parse import urlparse

# Parse the URL
parsed_url = urlparse(url)

# Extract the path component
path = parsed_url.path

# Split the path by '/' and get the last part
parts = path.split('/')
showName = parts[-1]

# Print the extracted show name
print(showName)

match = re.search(r'\d+$', url)

# Send an HTTP GET request to the URL and retrieve the content
response = requests.get(url)
html_content = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all <span> elements with the class "episodeTitle"
episode_titles = soup.find_all("span", class_="episodeTitle")

# Extract and print the text content of the <span> elements
for episode_title in episode_titles:
    print(episode_title.text)
    show_names.append(episode_title.text)
    with open('show_names.txt', 'w') as file:
        for show_name in show_names:
            file.write(f"{show_name}\n")

if match:
    numeric_identifier = match.group()
    print(numeric_identifier)
else:
    print("Numeric identifier not found in the URL.")

content_ids = []
numeric_values = []
headers = {
    'authority': 'content.airtel.tv',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'if-none-match': '000a29d77aa485b7295349105496d5bb--gzip',
    'origin': 'https://www.airtelxstream.in',
    'referer': 'https://www.airtelxstream.in/',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'x-atv-ab': '96304:0|100390:1|76965:0|110385:1|70747:1|129832:0',
    'x-atv-did': 'cec8dbb5-0f40-42fe-9038-3f4409b0919d|BROWSER|WEBOS|10.0|56|56.0.0',
    'x-atv-traceid': '093193db-27d2-4aa7-9f43-b1482506b8e8',
    'x-atv-utkn': 'XV85j-g60i8Z4G02o0:RTV2UHeKjdF7Kbn8RTgPQxMIVIg=',
}
id = 'SONYLIV_VOD_TVSHOW_' + numeric_identifier + '_SEASON_' + season_num
print(id)
params = {
    'id': id ,
    'appId': 'WEB',
}
response = requests.get('https://content.airtel.tv/app/v4/content', params=params, headers=headers)
data = response.json()
items = data["episodeRefs"]
for item in items:
    content_id = item.get("refId")

    # Use a regular expression to extract the numeric value
    match = re.search(r'\d+', content_id)

    if match:
        numeric_value = match.group()
        print(numeric_value)
    else:
        print("Numeric value not found in the text.")
    episode_num = item.get("episodeNumber")
    content_ids.append(content_id)
    numeric_values.append(numeric_value)
    
    with open('numeric_value.txt', 'w') as file:
        for numeric_value in numeric_values:
            file.write(f"{numeric_value}\n")



