# import requests
# from bs4 import BeautifulSoup

# url = "https://www.digikala.com/product/dkp-10738143/"  # Replace with the actual URL of the web page you want to scrape
# headers = {
#             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
#         }
# # Send a GET request to the URL
# response = requests.get(url,headers=headers)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the HTML content of the page using BeautifulSoup
#     soup = BeautifulSoup(response.content, "html.parser")
#     print(response.content)

#     # Find all <a> tags
#     all_href_tags = soup.find_all("a")

#     # Extract and print the href attributes
#     for tag in all_href_tags:
#         print(tag.get("href"))
# else:
#     print(f"Failed to retrieve the page. Status code: {response.status_code}")

import re

url = "https://www.digikala.com/search/category-notebook-netbook-ultrabook/"
pattern = r"category-(.*?)/"

match = re.search(pattern, url)

if match:
    result = match.group(1)
    print(result)
else:
    print("Pattern not found in the URL.")