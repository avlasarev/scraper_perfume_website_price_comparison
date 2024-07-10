# from bs4 import BeautifulSoup
# import requests
# from models import Product, PriceHistory, db, flag_suspicious_prices
# import re
#
# def scrape_douglas(perfume_needed, limit):
#     base_url = 'https://douglas.bg/catalogsearch/result/?q='
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
#     }
#
#     try:
#         r = requests.get(f'{base_url}{perfume_needed}', headers=headers)
#         r.raise_for_status()
#     except requests.RequestException as e:
#         return [], str(e)
#
#     soup = BeautifulSoup(r.content, 'lxml')
#
#     product_list = soup.find_all('div', class_='product-item-info')
#     perfumes = []
#
#     for index, item in enumerate(product_list):
#         if index >= limit:
#             break
#
#         link_tag = item.find('a', class_='product photo product-item-photo')
#         link = link_tag['href'] if link_tag else 'N/A'
#
#         image_tag = item.find('img', class_='product-image-photo')
#         image = image_tag['src'] if image_tag else 'N/A'
#
#         name_tag = item.find('a', class_='product-formed-name')
#         brand = name_tag.find('span', class_='brand').text.strip() if name_tag else 'N/A'
#         line = name_tag.find('span', class_='line').text.strip() if name_tag else 'N/A'
#         type = name_tag.find('span', class_='type').text.strip() if name_tag else 'N/A'
#         name = f"{brand} {line} {type}" if name_tag else 'N/A'
#
#         price_tag = item.find('span', {'class': 'price-wrapper', 'data-price-type': 'finalPrice'})
#         if price_tag:
#             price_text = price_tag.text.strip().replace(',', '.')
#             price_text = re.sub(r'[^\d.]', '', price_text)  # Remove non-numeric characters
#             try:
#                 price = float(price_text)
#             except ValueError:
#                 price = None
#         else:
#             price = None
#
#         product = Product.query.filter_by(url=link).first()
#         if not product:
#             product = Product(name=name, current_price=price, url=link, image=image, source='Douglas')
#             db.session.add(product)
#             db.session.commit()
#         else:
#             product.current_price = price
#
#         if price is not None:
#             price_history = PriceHistory(product_id=product.id, price=price)
#             db.session.add(price_history)
#             db.session.commit()
#
#             suspicious_prices = flag_suspicious_prices(product.id)
#             is_suspicious = price in suspicious_prices
#         else:
#             is_suspicious = False
#
#         perfumes.append({
#             'perfume_name': name,
#             'perfume_link': link,
#             'perfume_price': price,
#             'image': image,
#             'source': 'Douglas',
#             'is_suspicious': is_suspicious
#         })
#
#     return perfumes, None
