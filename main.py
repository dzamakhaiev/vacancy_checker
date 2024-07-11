from urls_to_check import URLS_TO_CHECK


def main_loop():

    for website_name, data in URLS_TO_CHECK.items():
        url = data.get('url')
        locators_class = data.get('locators')
        page_class = data.get('page')
        driver_class = data.get('driver')

        page = page_class(driver=driver_class)
        page.go_to(url)
        vacancies = page.find_elements(locator=locators_class.VACANCIES)
        print(len(vacancies))


if __name__ == '__main__':
    main_loop()
