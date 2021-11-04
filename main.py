from selenium import webdriver
import time
from urllib.parse import urlparse
from datetime import datetime

driver = webdriver.Chrome(executable_path=r"C:\Users\Marvin\Desktop\chromedriver.exe")  # r = raw String
gdpr_banner_keywords = ["Alle Akzeptieren", "Alle akzeptieren", "Auswahlmöglichkeiten anpassen",
                        "Weitere Informationen",
                        "Nur Essentielle Cookies akzeptieren", "Nur Essenzielle Cookies akzeptieren",
                        "Manage options", "Nicht-essentielle ablehnen"]
cookie_banner_keywords = ["Akzeptieren", "Verstanden", "Ablehnen"]
positive_cookie_banner_buttons = ["Alle Akzeptieren", "Alle akzeptieren", "Akzeptieren", "Verstanden"]
websites = ["https://www.unimals.de/", "https://www.evosportsfuel.de/", "https://www.ruehl24.de/de/",
            "https://www.saysorry.de/"]  # Note: Use www so that the website name can be shortened optimally
single_website = ["https://www.evosportsfuel.de/"]
short_website_name = ""
current_website_gdpr_compliant = False
current_website_cookie_use = False
current_website_unauthorized_use_of_cookies_at_beginning = False

# Analysis
a_cookies_before = []
a_cookies_after = []
cookie_difference = []



# Unauthorized third-party cookies:
# _fbp = Facebook Pixel
# _pin_unauth = Pinterest Tag
# _ga, _gat, _gid, _gcl_au = Google Analytics
third_party_cookies = ["_fbp", "_pin_unauth", "_ga", "_gat", "_gid", "_gcl_au"]


def initialize_website_file_and_check_cookie_banner():
    global current_website_cookie_use

    print("Überprüfe Cookie-Status für die Website: " + website + " (" + short_website_name + ")")
    for keyword in cookie_banner_keywords:
        if keyword in html_source:
            current_website_cookie_use = True

    if current_website_cookie_use:
        print("Es ist ein Cookie-Banner vorhanden!")
    else:
        print("Es ist KEIN Cookie-Banner vorhanden!")

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        dt_string = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        website_file.write("Website " + str((websites.index(website)) + 1) + ": " + website + " | Created: " + str(dt_string) + "\n")
        website_file.write("Website uses a cookie banner: " + str(current_website_cookie_use) + "\n")


def check_gdpr_cookie_status():
    global current_website_gdpr_compliant
    global current_website_cookie_use
    global short_website_name

    if current_website_cookie_use:
        print("Überprüfe GDPR-Cookie-Banner-Status...")
        for keyword in gdpr_banner_keywords:
            if keyword in html_source:
                print("Rechtskonformität (erneut) bestätigt!")
                print("Gefundenes Keyword: " + keyword)
                current_website_gdpr_compliant = True

        if current_website_gdpr_compliant:
            print("Fazit: Es handelt sich um einen rechtskonformen GDPR-Cookie-Banner")
        else:
            print("Keine passenden GDPR-Keywords gefunden!")
            print("Fazit: Es handelt sich NICHT um einen rechtskonformen GDPR-Cookie-Banner!")

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("Website uses a GDPR compliant cookie banner: " + str(current_website_gdpr_compliant) + "\n")


def check_cookies_at_start():
    global short_website_name

    cookies = driver.get_cookies()
    print("Anzahl der zu Beginn geladenen Cookies: " + str(cookies.__len__()))
    print(cookies)

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## Before accepting the Cookie-Banner ##############################" + "\n")
        website_file.write("[Before] Website-Cookie-Amount: " + str(cookies.__len__()) + "\n")
        website_file.write("[Before] Website-Cookies: " + str(cookies) + "\n")

        for cookie in cookies:
            print("Cookie-Name: " + cookie['name'])
            website_file.write("[Before] Cookie-Name " + str((cookies.index(cookie)) + 1) + ": " + cookie['name'] + "\n")


def check_cookies_after_banner_accept():
    cookies = driver.get_cookies()
    print("Anzahl der Cookies, nachdem der Cookie-Banner akzeptiert wurde: " + str(cookies.__len__()))
    print(cookies)

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## After accepting the Cookie-Banner ##############################" + "\n")
        website_file.write("[After] Website-Cookie-Amount: " + str(cookies.__len__()) + "\n")
        website_file.write("[After] Website-Cookies: " + str(cookies) + "\n")

        for cookie in cookies:
            print("Cookie-Name: " + cookie['name'])
            website_file.write("[After] Cookie-Name " + str((cookies.index(cookie)) + 1) + ": " + cookie['name'] + "\n")


def accept_cookie_banner():
    global current_website_cookie_use

    if current_website_cookie_use:
        for keyword in positive_cookie_banner_buttons:
            buttons = driver.find_elements_by_xpath("//*[contains(text(),'" + keyword + "')]")
            for btn in buttons:
                if btn.is_enabled() and btn.is_displayed():
                    btn.click()
                    print("Cookies Akzeptiert!")


def create_short_website_name():
    global short_website_name

    short_website_name_sub = urlparse(website).netloc
    short_website_name = '.'.join(short_website_name_sub.split('.')[1:])


def analyze_cookie_files():
    global current_website_unauthorized_use_of_cookies_at_beginning, cookie_difference

    with open("results/" + short_website_name + ".txt") as cookies_before:
        lines_before = cookies_before.readlines()

    for line in lines_before:
        if "[Before] Cookie-Name" in line:
            a_cookies_before.append(line.split(": ")[1])

        if "[After] Cookie-Name" in line:
            a_cookies_after.append(line.split(": ")[1])

    cookie_difference = set(a_cookies_before) ^ set(a_cookies_after)

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## Difference ##############################" + "\n")
        website_file.write("[New] Cookies added: " + str(cookie_difference.__len__()) + "\n")

        for cookie_dif in cookie_difference:
            website_file.write("[New] Cookie-Name: " + str((list(cookie_difference).index(cookie_dif)) + 1) + ": " + str(cookie_dif))




    # for line in lines_before:
    #     for t_p_c in third_party_cookies:
    #         if t_p_c in line:
    #             print("Es wurde ein third-party-cookie gefunden! " + "-> " + t_p_c)
    #             current_website_unauthorized_use_of_cookies_at_beginning = True  # MUSS SPÄTER IN EINE FINALE DATEI GESCHRIEBEN WERDEN!


    # 2. Wieviele Cookies hat eine Seite vor und danach gehabt?
    # Ist der Unterschied zwischen den beiden Werten nicht zu groß und der erste Wert ist größer als 5,
    # Speicher diese Information in einer neuen Variablen

if __name__ == '__main__':
    for website in websites:
        create_short_website_name()
        driver.get(website)
        current_website_gdpr_compliant = False
        current_website_cookie_use = False
        current_website_unauthorized_use_of_cookies_at_beginning = False
        a_cookies_before.clear()
        a_cookies_after.clear()
        cookie_difference.clear()
        time.sleep(3)  # Wait for the website to load

        html_source = driver.page_source  # Get HTML-source-code

        initialize_website_file_and_check_cookie_banner()  # Generiere eine Website-File. Ist überhaupt ein Cookie-Banner vorhanden?
        time.sleep(1)
        check_gdpr_cookie_status()  # Ist der vorhandene Cookie-Banner GDPR-Konform?
        time.sleep(1)
        check_cookies_at_start()  # Welche Cookies existieren bereits nach dem Laden der Seite?
        time.sleep(1)
        accept_cookie_banner()  # Akzeptiere den angezeigten Cookie-Banner
        time.sleep(1)
        check_cookies_after_banner_accept()  # Welche Cookies existieren auf der Seite, nachdem der entsprechende Cookie-Banner akzeptiert wurde?
        time.sleep(1)
        analyze_cookie_files()

    print("Durchlauf beendet, schließe driver...")
    driver.close()

    # facebook, instgram, pinterest cookies? Wann werden diese gesetzt? Bevor oder nach
    # Check: Setzt die website schon vor der Abfrage cookies?
    # Gibt es eine Möglichkeit abzulehnen?
    # Pre-selected boxes?
    # Cookies setzen obwohl abgelehnt

    # Den gesamten Log einer Seite in die Seiten-File dazu schreiben
