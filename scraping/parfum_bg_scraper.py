# from bs4 import BeautifulSoup
# import requests
# from models import Product, PriceHistory, db, flag_suspicious_prices
#
#
# def scrape_parfum_bg(perfume_needed, limit):
#     base_url = 'https://www.parfum-bg.com/search/libre'
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
#     product_list = soup.find_all('article', class_='col-20 prod')
#     perfumes = []
#
#     for index, item in enumerate(product_list):
#         if index >= limit:
#             break
#
#         link_tag = item.find('a', href=True)
#         link = f"https://www.parfum-bg.com{link_tag['href']}" if link_tag else 'N/A'
#
#         image_tag = item.find('img')
#         image = image_tag['src'] if image_tag else 'N/A'
#
#         name_tag = item.find('a', title=True)
#         name = name_tag['title'].strip() if name_tag else 'N/A'
#
#         price_tag = item.find('div', class_='prod-price')
#         price = float(price_tag.text.strip().replace(',', '.').replace('лв', '')) if price_tag else 'N/A'
#
#         product = Product.query.filter_by(url=link).first()
#         if not product:
#             product = Product(name=name, current_price=price, url=link, image=image, source='Parfum BG')
#             db.session.add(product)
#         else:
#             product.current_price = price
#
#         price_history = PriceHistory(product_id=product.id, price=price)
#         db.session.add(price_history)
#         db.session.commit()
#
#         suspicious_prices = flag_suspicious_prices(product.id)
#         is_suspicious = price in suspicious_prices
#
#         perfumes.append({
#             'perfume_name': name,
#             'perfume_link': link,
#             'perfume_price': price,
#             'image': image,
#             'source': 'Parfum BG',
#             'is_suspicious': is_suspicious
#         })
#
#     return perfumes, None
