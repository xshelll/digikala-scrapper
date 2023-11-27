import re
from concurrent.futures import ThreadPoolExecutor
import requests
import json
from grabber import Grabber
import subprocess

def generate_api_link(txt_file):

    links = open(txt_file, 'r', encoding='utf-8').readlines()
    links = [x for x in links if x != '\n']

    api_links = []

    for link in links:
        match = re.search(r'/dkp-(\d+)/', link)
        if match:
            product_id = match.group(1)
            api_links.append('https://api.digikala.com/v2/product/{}/'.format(product_id))
    
    return api_links


def fetch_product_details(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url,headers=headers)
        response = response.json()
        product = response['data']['product']
        product_url = 'https://digikala.com' + product['url']['uri']
        main_image = product['images']['main']['url'][0]
        list_image = product['images']['list']
        list_image = [x['url'][0] for x in list_image]
        responses.append({"product_url": product_url, "main_image": main_image, "list_image": list_image})
    except Exception as e:
        print(f"Error in request to {url}: {e}")

if __name__ == '__main__':
    
    category_url = input("Enter category url: ")

    print("#=> Start grabbing products links...\n")

    grabber = Grabber(category_url)
    if not grabber.run():
        exit()

    print("#=> Generating products api link...\n")
    responses = []
    urls = generate_api_link('links.txt')
    
    print("#=> Grabbin products details...\n")
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(fetch_product_details, urls)
    
    with open('products.json', 'w') as json_file:
        json.dump(responses, json_file)
    
    print(f"#=> The details of {len(responses)} product grabbed successfully !\n")

    print("#=> Running http server on: http://127.0.0.1:8000/index.html\n")

    subprocess.run(['python', '-m', 'http.server'])