from requests_html import HTMLSession


def get_autobuy(steam_listing):
    url='https://steamcommunity.com/market/listings/730/'+steam_listing
    session = HTMLSession()
    response = session.get(url)

    # Рендеринг JavaScript
    response.html.render(sleep=3)  # Подождите несколько секунд для завершения рендеринга JavaScript

    if item_type in ['weapon', 'agent']:
        price_xpath = '/html/body/div[1]/div[7]/div[4]/div[1]/div[4]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/span[2]/text()'
    else:
        price_xpath = '//*[@id="market_buyorder_info_details"]/div[1]/span[2]/text()'

    price = response.html.xpath(price_xpath, first=True)

    if price:
        return price
    else:
        print("Price not found on the page")
        return None


# Пример использования
url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Slate%20%28Field-Tested%29"
item_type = "weapon"  # или 'agent', или 'other' в зависимости от типа предмета
price = get_autobuy(url)
if price:
    print(f"Auto-buy price: {price}")
