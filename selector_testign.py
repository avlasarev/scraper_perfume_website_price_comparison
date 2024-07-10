import requests
from bs4 import BeautifulSoup

def search_perfumes(perfume_needed, limit=5):
    base_url = 'https://douglas.bg/catalogsearch/result/?q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(f'{base_url}{perfume_needed}', headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")
        return

    soup = BeautifulSoup(r.content, 'lxml')

    product_list = soup.find_all('div', class_='product-item-info')
    perfumes = []

    for index, item in enumerate(product_list):
        if index >= limit:
            break

        link_tag = item.find('a', class_='product photo product-item-photo')
        link = link_tag['href'] if link_tag else 'N/A'

        name_tag = item.find('a', class_='product-formed-name')
        brand = name_tag.find('span', class_='brand').text.strip() if name_tag else 'N/A'
        line = name_tag.find('span', class_='line').text.strip() if name_tag else 'N/A'
        type = name_tag.find('span', class_='type').text.strip() if name_tag else 'N/A'
        name = f"{brand} {line} {type}" if name_tag else 'N/A'

        price_tag = item.find('span', class_='price')
        price = price_tag.text.strip() if price_tag else 'N/A'

        perfumes.append({
            'perfume_name': name,
            'perfume_link': link,
            'perfume_price': price,
        })

    for perfume in perfumes:
        print(f"Name: {perfume['perfume_name']}")
        print(f"Link: {perfume['perfume_link']}")
        print(f"Price: {perfume['perfume_price']}")
        print('-' * 40)

if __name__ == '__main__':
    perfume_needed = input("Enter the perfume name: ")
    limit = int(input("Enter the number of results to fetch: "))
    search_perfumes(perfume_needed, limit)
