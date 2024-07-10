from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


def scrape_douglas(perfume_needed, limit):
    base_url = 'https://douglas.bg/catalogsearch/result/?q='
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(f'{base_url}{perfume_needed}', headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        return [], str(e)

    soup = BeautifulSoup(r.content, 'lxml')

    product_list = soup.find_all('div', class_='product-item-info')
    perfumes = []

    for index, item in enumerate(product_list):
        if index >= limit:
            break

        link_tag = item.find('a', class_='product photo product-item-photo')
        link = link_tag['href'] if link_tag else 'N/A'

        image_tag = item.find('img', class_='product-image-photo')
        image = image_tag['src'] if image_tag else 'N/A'

        name_tag = item.find('a', class_='product-formed-name')
        brand = name_tag.find('span', class_='brand').text.strip() if name_tag else 'N/A'
        line = name_tag.find('span', class_='line').text.strip() if name_tag else 'N/A'
        type = name_tag.find('span', class_='type').text.strip() if name_tag else 'N/A'
        name = f"{brand} {line} {type}" if name_tag else 'N/A'

        price_tag = item.find('span', {'data-price-type': 'finalPrice'})
        price = price_tag.find('span', class_='price').text.strip() if price_tag else 'N/A'

        perfumes.append({
            'perfume_name': name,
            'perfume_link': link,
            'perfume_price': price,
            'image': image,
            'source': 'Douglas'
        })

    return perfumes, None


def scrape_parfum_bg(perfume_needed, limit):
    base_url = 'https://www.parfum-bg.com/search/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(f'{base_url}{perfume_needed}', headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        return [], str(e)

    soup = BeautifulSoup(r.content, 'lxml')

    product_list = soup.find_all('article', class_='col-20 prod')
    perfumes = []

    for index, item in enumerate(product_list):
        if index >= limit:
            break

        link_tag = item.find('a', href=True)
        link = f"https://www.parfum-bg.com{link_tag['href']}" if link_tag else 'N/A'

        image_tag = item.find('img')
        image = f"https://www.parfum-bg.com{image_tag['src']}" if image_tag else 'N/A'

        name_tag = item.find('a', title=True)
        name = name_tag['title'].strip() if name_tag else 'N/A'

        price_tag = item.find('div', class_='prod-price')
        price = price_tag.text.strip() if price_tag else 'N/A'

        perfumes.append({
            'perfume_name': name,
            'perfume_link': link,
            'perfume_price': price,
            'image': image,
            'source': 'Parfum BG'
        })

    return perfumes, None


@app.route('/search', methods=['GET'])
def search():
    perfume_needed = request.args.get('q')
    limit = int(request.args.get('limit', 5))

    perfumes_douglas, error_douglas = scrape_douglas(perfume_needed, limit)
    perfumes_parfum_bg, error_parfum_bg = scrape_parfum_bg(perfume_needed, limit)

    if error_douglas and error_parfum_bg:
        return jsonify({'error': f"Error from both sources: {error_douglas}, {error_parfum_bg}"}), 500

    perfumes = perfumes_douglas + perfumes_parfum_bg

    return jsonify(perfumes)


if __name__ == '__main__':
    app.run(debug=True)

