from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path=r"C:\Users\Marvin\Desktop\chromedriver.exe")  # r = raw String
gdpr_banner_keywords = ["Alle Akzeptieren", "Alle akzeptieren", "Auswahlmöglichkeiten anpassen",
                        "Weitere Informationen",
                        "Nur Essentielle Cookies akzeptieren", "Nur Essenzielle Cookies akzeptieren",
                        "Manage options", "Nicht-essentielle ablehnen"]
cookie_banner_keywords = ["Akzeptieren", "Verstanden", "Ablehnen"]
positive_cookie_banner_buttons = ["Alle Akzeptieren", "Alle akzeptieren", "Akzeptieren", "Verstanden"]
websites = ["https://unimals.de/", "https://evosportsfuel.de/", "https://www.ruehl24.de/de/", "https://saysorry.de/"]
single_website = ["https://unimals.de/"]
current_website_gdpr_conform = False
current_website_cookie_use = False


def check_cookie_status():
    global current_website_cookie_use
    # Überprüfe, ob überhaupt ein Cookie-Banner vorhanden ist
    print("Überprüfe Cookie-Status für die Website: " + website)
    for keyword in cookie_banner_keywords:
        if keyword in html_source:
            current_website_cookie_use = True
    if current_website_cookie_use:
        print("Es ist ein Cookie-Banner vorhanden!")
    else:
        print("Es ist KEIN Cookie-Banner vorhanden!")


def check_gdpr_cookie_status():
    global current_website_gdpr_conform
    global current_website_cookie_use

    if current_website_cookie_use:
        # Unterscheide, ob es sich um einen normalen oder um einen GDPR Cookie-Banner handelt
        print("Überprüfe GDPR-Cookie-Banner-Status...")
        for keyword in gdpr_banner_keywords:
            if keyword in html_source:
                print("Rechtskonformität (erneut) bestätigt!")
                print("Gefundenes Keyword: " + keyword)
                current_website_gdpr_conform = True
        if current_website_gdpr_conform:
            print("Fazit: Es handelt sich um einen rechtskonformen GDPR-Cookie-Banner")
        else:
            print("Keine passenden GDPR-Keywords gefunden!")
            print("Fazit: Es handelt sich NICHT um einen rechtskonformen GDPR-Cookie-Banner!")


def check_cookies_at_start():
    cookies = driver.get_cookies()
    print("Anzahl der zu Beginn geladenen Cookies: " + str(cookies.__len__()))
    print(cookies)
    for cookie in cookies:
        print("Cookie-Name: " + cookie['name'])

    with open("data/cookies_at_start.txt", "a") as cookies_start:
        cookies_start.write(website + "$>" + str(cookies) + "\n")


def accept_cookie_banner():
    global current_website_cookie_use

    if current_website_cookie_use:
        for keyword in positive_cookie_banner_buttons:
            buttons = driver.find_elements_by_xpath("//*[contains(text(),'" + keyword + "')]")
            print("Anzahl gefundener Keywörter: " + str(buttons.__len__()))
            for btn in buttons:
                if btn.is_enabled() and btn.is_displayed():
                    btn.click()
                    print("Cookies Akzeptiert!")


if __name__ == '__main__':
    for website in websites:
        driver.get(website)
        current_website_gdpr_conform = False
        current_website_cookie_use = False
        time.sleep(3)  # Wait for the website to load

        html_source = driver.page_source  # Get HTML-source-code

        check_cookie_status()  # Ist überhaupt ein Cookie-Banner vorhanden?
        time.sleep(1)
        check_gdpr_cookie_status()  # Ist der vorhandene Cookie-Banner GDPR-Konform?
        time.sleep(1)
        check_cookies_at_start()  # Welche Cookies existieren bereits nach dem Laden der Seite? In .txt abspeichern
        time.sleep(1)
        accept_cookie_banner()  # Akzeptiere den angezeigten Cookie-Banner
        time.sleep(2)

    print("Durchlauf beendet, schließe driver...")
    driver.close()

    # facebook, instgram, pinterest cookies? Wann werden diese gesetzt? Bevor oder nach
    # Check: Setzt die website schon vor der Abfrage cookies?
    # Gibt es eine Möglichkeit abzulehnen?
    # Pre-selected boxes?
    # Cookies setzen obwohl abgelehnt
