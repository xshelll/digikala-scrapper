import re
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class Grabber:
    def __init__(self, url) -> None:
        self.links = []
        self.pages = []
        self.url = url
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    
    def url_to_api(self):
        pattern = r"/category-(.*?)/"
        match = re.search(pattern, self.url)
        pattern2 = r"main/(.*?)/"
        match2 = re.search(pattern2, self.url)
        pattern3 = r"digikala.com/(.*?)/"
        match3 = re.search(pattern3, self.url)
        if match:
            result = match.group(1)
            api = "https://api.digikala.com/v1/categories/" + result + "/search/?seo_url=&page=1"
            return api
        elif match2:
            result2 = match2.group(1)
            if 'dk-ds-' in result2:
                result2 = result2.replace('dk-ds-', '').replace('-', '')
                api = 'https://api.digikala.com/v1/dynamic-category-page/' + result2 + "/"
                return api
            else:
                api = 'https://api.digikala.com/v1/categories/' + result2 + '/'
                return api
        elif match3:
            result3 = match3.group(1)
            api = "https://api.digikala.com/v1/" + result3 + "/"
            return api
        
    
    def get_category_pages_details(self):
        if not self.url.startswith('https://www.digikala.com/search/category-'): return False
        api = self.url_to_api()
        response = requests.get(api,headers=self.headers)
        response = response.json()
        total_page = response['data']['pager']['total_pages']
        if total_page > 100: total_page = 100
        for page in range(1, total_page+1):
            self.pages.append(api.replace('page=1', f'page={page}'))
        return True

    def fetch_product_details(self, url):
        try:
            response = requests.get(url,headers=self.headers)
            response = response.json()
            products = response['data']['products']
            products_link = ['https://www.digikala.com'+x['url']['uri'] for x in products]
            for product_link in products_link: self.links.append(product_link)
        except Exception as e:
            print(f"Error in request to {url}: {e}")

    def run(self):
        
        if not self.get_category_pages_details(): 
            print("#=> Invalid category link !\n")
            return False

        time1 = datetime.now()
        with ThreadPoolExecutor(max_workers=25) as executor:
            executor.map(self.fetch_product_details, self.pages)
        time2 = datetime.now()

        links_as_text = ''

        for link in self.links:
            if link != self.links[-1]:
                links_as_text += link + '\n'
            else:
                links_as_text += link
        
        with open('links.txt', 'w', encoding='utf-8') as file:
            file.write(links_as_text)

        print(f"#=> {len(self.links)} links from {len(self.pages)} pages grabbed successfuly in {time2-time1}!\n")

        return True