from selenium import webdriver
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import time
# Driver settings
driver = webdriver.Chrome(executable_path=r"C:\Users\Marvin\Desktop\chromedriver.exe")

# Keywords and phrases
gdpr_banner_keywords = ["Alle Akzeptieren", "Alle akzeptieren", "Auswahlmöglichkeiten anpassen",
                        "Weitere Informationen",
                        "Nur Essentielle Cookies akzeptieren", "Nur Essenzielle Cookies akzeptieren",
                        "Manage options", "Nicht-essentielle ablehnen", "Cookie Richtlinien", "Alle zulassen", "Alle Zulassen",
                        "Meine Auswahl bestätigen", "Meine Auswahl Bestätigen"]
cookie_banner_keywords = ["Akzeptieren", "Verstanden", "Ablehnen", "Zustimmen", "Alle akzeptieren", "ok", "Ok", "OK", "Alles klar", "Alles klar!",
                          "I accept", "Accept", "Ich habe verstanden.", "Einverstanden", "Alle Cookies akzeptieren", "Alle Cookies Akzeptieren",
                          "Zustimmen!", "Got it!", "Annehmen", "Ich stimme zu"]
positive_cookie_banner_buttons = ["Alle Akzeptieren", "Alle akzeptieren", "Akzeptieren", "Verstanden"]
websites = ["https://www.unimals.de/", "https://www.evosportsfuel.de/", "http://www.kilenzo.de/", "https://www.ruehl24.de/de/",
            "https://www.saysorry.de/"]  # Note: Use www so that the website name can be shortened optimally
single_website = ["https://www.unimals.de/"]
all_websites = "src/websites.txt"
website_warning = "Only one step left!"
website_warning_2 = "is currently unavailable."

# Essential Variables
short_website_name = ""
website_index = 0
current_website_gdpr_compliant = False
current_website_cookie_use = False
current_website_unauthorized_use_of_cookies_at_beginning = False
current_website_unauthorized_use_of_third_party_cookies_at_beginning = False
current_website_authorized_use_of_third_party_cookies_after = False

# Analysis
a_cookies_before = []
a_cookies_after = []
cookie_difference = []

# Keywords: Unauthorized third-party-cookies:
# _fbp = Facebook Pixel
# _pin_unauth = Pinterest Tag
# _ga, _gat, _gid, _gcl_au = Google Analytics
third_party_cookies = ["_fbp", "_pin_unauth", "_ga", "_gat", "_gid", "_gcl_au"]


def initialize_website_file_and_check_cookie_banner():
    global current_website_cookie_use
    global website_index

    print("Check cookie status for the website: " + website + " (" + short_website_name + ")")
    for keyword in cookie_banner_keywords:
        if keyword in html_source:
            current_website_cookie_use = True

    if current_website_cookie_use:
        print("There is a cookie banner available!")
    else:
        print("There is NO cookie banner available!")

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        dt_string = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        website_file.write("Website " + str(website_index) + ": " + website + " | Created: " + str(dt_string) + "\n")
        website_file.write("[Initial] Website uses a cookie banner: " + str(current_website_cookie_use) + "\n")


def check_gdpr_cookie_status():
    global current_website_gdpr_compliant
    global current_website_cookie_use
    global short_website_name

    if current_website_cookie_use:
        print("Check GDPR cookie banner status...")
        for keyword in gdpr_banner_keywords:
            if keyword in html_source:
                print("Legal conformity confirmed (again)!")
                print("Found Keyword: " + keyword)
                current_website_gdpr_compliant = True

        if current_website_gdpr_compliant:
            print("Conclusion: It is a legally compliant GDPR cookie banner")
        else:
            print("No matching GDPR keywords found!")
            print("Conclusion: This is NOT a legally compliant GDPR cookie banner!")

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("[Initial] Website uses a GDPR compliant cookie banner: " + str(current_website_gdpr_compliant) + "\n")


def check_cookies_at_start():
    global short_website_name

    cookies = driver.get_cookies()
    print("Number of cookies loaded at the beginning: " + str(cookies.__len__()))
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
    print("Number of cookies after the cookie banner has been accepted: " + str(cookies.__len__()))
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
                    print("Cookies Accepted!")


def create_short_website_name():
    global short_website_name

    short_website_name_sub = urlparse(website).netloc
    short_website_name = '.'.join(short_website_name_sub.split('.')[1:])


def analyze_cookie_files():
    global current_website_unauthorized_use_of_cookies_at_beginning
    global current_website_unauthorized_use_of_third_party_cookies_at_beginning
    global current_website_authorized_use_of_third_party_cookies_after
    global cookie_difference

    # Calculate the difference between the cookies that existed before and after the cookie-banner
    with open("results/" + short_website_name + ".txt") as website_files:
        lines = website_files.readlines()

    for line in lines:
        if "[Before] Cookie-Name" in line:
            a_cookies_before.append(line.split(": ")[1])

        if "[After] Cookie-Name" in line:
            a_cookies_after.append(line.split(": ")[1])

    cookie_difference = set(a_cookies_before) ^ set(a_cookies_after)

    # Are there already disallowed cookies in the cookie list at the beginning?
    for a_cookie_b in a_cookies_before:
        updated_cookie_b = str(a_cookie_b).replace("\n", "")
        if updated_cookie_b in third_party_cookies:
            current_website_unauthorized_use_of_third_party_cookies_at_beginning = True

    # Rate the new amount of cookies TODO: Kann man hier noch etwas verbessern?
    if a_cookies_after.__len__() % a_cookies_before.__len__() > 10 or current_website_unauthorized_use_of_third_party_cookies_at_beginning:
        current_website_unauthorized_use_of_cookies_at_beginning = True
    else:
        current_website_unauthorized_use_of_cookies_at_beginning = False

    # Are third-party-cookies loaded after acceptance?
    for a_cookie_a in a_cookies_after:
        updated_cookie_a = str(a_cookie_a).replace("\n", "")
        if updated_cookie_a in third_party_cookies and not current_website_unauthorized_use_of_cookies_at_beginning \
                and not current_website_unauthorized_use_of_third_party_cookies_at_beginning:
            current_website_authorized_use_of_third_party_cookies_after = True

    # Write the information of the analysis into the respective website files
    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## Difference ##############################" + "\n")
        website_file.write("[Difference] Cookies added: " + str(cookie_difference.__len__()) + "\n")

        for cookie_dif in cookie_difference:
            website_file.write("[Difference] Cookie-Name: " + str((list(cookie_difference).index(cookie_dif)) + 1) + ": " + str(cookie_dif))

        website_file.write("\n" + "############################## Analysis ##############################" + "\n")
        website_file.write("[Analysis] Website generally uses cookies at the beginning (non-essential), although they are not authorized by the "
                           "user: " + str(current_website_unauthorized_use_of_cookies_at_beginning) + "\n")
        website_file.write("[Analysis] Website uses unauthorized third-party cookies at the beginning: "
                           + str(current_website_unauthorized_use_of_third_party_cookies_at_beginning) + "\n")
        website_file.write("[Analysis] Website respects the user's decision and loads THIRD-PARTY-COOKIES only after approval: "
                           + str(current_website_authorized_use_of_third_party_cookies_after) + "\n")

        if current_website_gdpr_compliant and current_website_authorized_use_of_third_party_cookies_after:
            website_file.write("\n" + "[Analysis] Website is GDPR compliant!" + "\n")
        else:
            website_file.write("\n" + "[Analysis] Website is NOT GDPR compliant!" + "\n")


if __name__ == '__main__':
    with open(all_websites) as websites_all:
        lines_websites = websites_all.readlines()

    for website in lines_websites:
        try:
            website = str(website).replace("\n", "")
            create_short_website_name()
            driver.get(website)
            current_website_gdpr_compliant = False
            current_website_cookie_use = False
            current_website_unauthorized_use_of_cookies_at_beginning = False
            current_website_unauthorized_use_of_third_party_cookies_at_beginning = False
            current_website_authorized_use_of_third_party_cookies_after = False
            website_index += 1
            a_cookies_before.clear()
            a_cookies_after.clear()
            cookie_difference.clear()
            time.sleep(3)  # Wait for the website to load

            html_source = driver.page_source  # Get HTML-source-code

            # Check if website is still available
            if website_warning in html_source or website_warning_2 in html_source:
                print("Website not available! Skip website...")
                continue

            initialize_website_file_and_check_cookie_banner()  # Generate a website file. Is there a cookie banner at all?
            time.sleep(1)
            check_gdpr_cookie_status()  # Is the existing cookie banner GDPR compliant?
            time.sleep(1)
            check_cookies_at_start()  # Which cookies already exist after loading the page?
            time.sleep(1)
            accept_cookie_banner()  # Accept the cookie banner displayed
            time.sleep(1)
            check_cookies_after_banner_accept()  # What cookies exist on the site after accepting the corresponding cookie banner?
            time.sleep(1)
            analyze_cookie_files()  # Analyze the generated website files
        except WebDriverException:
            print("Exception: Page most likely unavailable or offline!")

    print("Analysis finished, close driver...")
    driver.close()
