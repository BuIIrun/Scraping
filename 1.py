import requests
import json
import tabulate
from bs4 import BeautifulSoup
class restcountries:


    def __init__(self):
        pass

    #Функція відправки запиту та отримання відповіді
    def get_all(self):
        uri = "https://restcountries.com/v3.1/all"
        response = requests.get(uri)
        if response.status_code == 200:
            result_list = []
            data = json.loads(response.text)
            if type(data) == list:
                for country_data in data:
                    name = country_data.get("name").get("official")
                    capital = str(country_data.get("capital")).replace("['", "").replace("']", "")
                    flag = country_data.get("flags").get("png")
                    result_list.append([name, capital, flag])
            return self.print_result(result_list)
        elif response.status_code == 404:
            raise requests.exceptions.InvalidURL
        else:
            raise requests.exceptions.RequestException

    # Функція відображення даних
    def print_result(self, result):
        columns = ["Назва країни", "Назва столиці", "Посилання на зображення прапору в форматі png"]
        #Використовую модуль tabulate для гарного відображення табличних даних
        results = tabulate.tabulate(result, headers=columns, tablefmt="grid")
        print(results)


class ebay_scraper:


    def __init__(self, url):
        self.url = url

    # Функція відправки запиту та скрапінгу
    def scrape_page(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, 'html.parser')
        name = soup.find(id='mainContent').find_next(class_='x-item-title__mainTitle').find_next('span', class_='ux-textspans ux-textspans--BOLD').text
        price = soup.find(id='mainContent').find_next(class_='x-price-primary').find_next('span', class_='ux-textspans').text
        seller = soup.find(id='mainContent').find_next(class_='x-sellercard-atf__info__about-seller').find_next('span', class_='ux-textspans ux-textspans--BOLD').text
        shipping_price = soup.find(id='mainContent').find_next(class_='ux-labels-values__values-content').find_next('span').text
        images = soup.find(class_='main-container').find_next(class_='vim x-photos').find_next('div', class_='ux-image-grid-container filmstrip filmstrip-x').find_all_next('img')
        for img in images:
            if img.has_attr('data-zoom-src'):
                images = img['data-zoom-src']
                break
        return self.print_result(name, price, seller, shipping_price, images)

    # Функція відображення даних
    def print_result(self, name, price, seller, shipping_price, images):
        # Конвертую отримані дані в json
        data_json = {'Назва товару': name, 'Ціна': price, 'Продавець': seller, 'Ціна доставки': shipping_price,
                     'Посилання на фото': images, 'Посилання на товар': self.url}
        print("json: ", data_json)
        columns = ["Назва товару", "Ціна", "Продавець", "Ціна доставки", "Посилання на фото", "Посилання на товар"]
        # Використовую модуль tabulate для гарного відображення табличних даних
        table = [(name, price, seller, shipping_price, images, self.url)]
        results = tabulate.tabulate(table, headers=columns, tablefmt="grid")
        print(results)

if __name__ == "__main__":
    restcountries().get_all()
    #Працює лише в такому форматі: https://www.ebay.com/itm/ХХХХХХХХХХ
    ebay_scraper(url="https://www.ebay.com/itm/235332399310").scrape_page()
    #По всім категоріям товарів не провіряв, тому можливі помилки