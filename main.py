from selenium import webdriver
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from random import randrange
import time
import re
import os

# Driver settings / Headless-mode settings
# Headless-mode: Should the scanning process be displayed visually? Performance is being saved by this mode.
use_headless_mode = False
if use_headless_mode:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1200")
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(options=options)
else:
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)

# Keywords and phrases
# Typical keywords for GDPR compliant cookie banner
gdpr_banner_keywords = ["Alle Akzeptieren", "Alle akzeptieren", "Auswahlmöglichkeiten anpassen",
                        "Weitere Informationen", "Nur Essentielle Cookies akzeptieren", "Nur Essenzielle Cookies akzeptieren",
                        "Manage options", "Nicht-essentielle ablehnen", "Cookie Richtlinien", "Alle zulassen", "Alle Zulassen",
                        "Meine Auswahl bestätigen", "Meine Auswahl Bestätigen", "Einstellungen", "Preferences", "Auswahl", "Cookie-Einstellungen",
                        "Präferenzen", "Alle Cookies zulassen", "Alle cookies zulassen", "Einstellungen verwalten"]

# General Keywords to confirm cookie banner
positive_cookie_banner_buttons = ["Alle Akzeptieren", "Alles akzeptieren", "Alles Akzeptieren", "Alle akzeptieren", "Akzeptieren", "Verstanden",
                                  "Verstanden!", "ZUSTIMMEN", "Zustimmen", "Alles klar!", "Alles klar", "I accept", "Accept", "Ich habe verstanden.",
                                  "Einverstanden", "Got it", "Alle Cookies akzeptieren", "Alle Cookies Akzeptieren", "Alle Cookies akzeptieren",
                                  "Zustimmen!", "Got it!", "Annehmen", "Ich stimme zu", "Ich stimme zu.", "Geht klar", "Geht klar!", "Geht klar."
                                  "Akzeptiere alle", "Akzeptiere Alle", "Alle Cookies zulassen", "Alle cookies zulassen", "Accept all", "Accept All",
                                  "Alle cookies erlauben", "Alle Cookies erlauben", "Stimme zu", "Ich stimme zu", "Got it !", "Alle akzeptieren!",
                                  "Agree to cookies", "Alle zulassen", "Cookies zulassen", "Stimme zu.", "Stimme Zu", "Ja, ich stimme zu",
                                  "Alle akzeptieren !", "Bestätigen", "Bitte bestätigen", "Alles klar", "Einverstanden!", "Voll.", "Ich verstehe",
                                  "Ich habs!", "Okay", "OKAY", "Cookies Zulassen", "Akzeptieren & weiter", "Akzeptiere cookies", "Alles Klar!",
                                  "Ok, Ich stimme zu.", "Ok, ich stimme zu", "Akzeptieren und schließen", "Akzeptieren & schließen", "Ermöglichen",
                                  "Fortsetzen", "Ich akzeptiere", "Ok, verstanden", "Allow all cookies", "Akzeptieren Sie", "Alles klar.",
                                  "I agree to use cookies.", "I agree to use cookies", "Accept all cookies", "Ok", "OK", "ok", " ok "," Ok ", " OK ",
                                  "ok!", "Ok!", "OK!", "ja", "Ja", "JA", " ja ", " Ja ", " JA "]

# General Keywords to decline cookie banner
negative_cookie_banner_buttons = ["Ablehnen", "Alle ablehnen", "Nur Essentielle Cookies akzeptieren", "No Thanks", "Nur notwendige Cookies",
                                  "Nur notwendige cookies", "Nur notwendige Cookies akzeptieren", "Nur notwendige Cookies Akzeptieren"]

# Sources
# Note: Use www so that the website name can be shortened optimally
all_websites = "src/backup/websites.txt"  # Debug
# Use different files with max 400 websites to avoid crashing
all_websites_f1 = "src/websites_1.txt"  # 400 websites
all_websites_f2 = "src/websites_2.txt"  # 400 websites
all_websites_f3 = "src/websites_3.txt"  # 400 websites
all_websites_f4 = "src/websites_4.txt"  # 400 websites
all_websites_f5 = "src/websites_5.txt"  # 400 websites
all_websites_f6 = "src/websites_6.txt"  # 400 websites
all_websites_f7 = "src/websites_7.txt"  # 400 websites
all_websites_f8 = "src/websites_8.txt"  # 278 websites

# Debug (For test purposes, use custom websites)
single_website = ["http://www.google.de/"]
websites = ["http://www.google.de/", "http://www.youtube.de/", "http://www.facebook.de/"]

# Warnings (Captured in a German browser)
website_warning = "Only one step left!"
website_warning_2 = "is currently unavailable."
website_warning_3 = "Dies ist keine sichere Verbindung"
website_warning_4 = "Domain erwerben"
website_warning_5 = "Be the first to know when we launch"

# Essential Variables
short_website_name = ""
website_index = 0
screen_shot_index_randomly = 1
screen_shot_index_no_banner = 1
offline_websites_amount = 0
able_to_accept_cookies = False
current_website_gdpr_compliant = False
current_website_cookie_use = False
current_website_accept_button_use = False
current_website_decline_button_use = False
current_website_unauthorized_use_of_cookies_at_beginning = False
current_website_unauthorized_use_of_third_party_cookies_at_beginning = False
current_website_authorized_use_of_third_party_cookies_after = False

# Analysis
a_cookies_before = []
a_cookies_after = []
cookie_difference = []
t_p_c_name = ""

# Keywords: Unauthorized third-party-cookies:
# _fbp = Facebook Pixel
# _pin_unauth = Pinterest Tag
# _ga, _gat, _gid = Google Analytics
# _gcl_au = Google Adsense
# _hjAbsoluteSessionInProgress, _hjFirstSeen, _hjIncludedInSessionSample = Hotjar
third_party_cookies = ["_fbp", "_pin_unauth", "_ga", "_gat", "_gid", "_gcl_au",
                       "_hjAbsoluteSessionInProgress", "_hjFirstSeen", "_hjIncludedInSessionSample"]
t_p_c_pairs = [("_fbp", "Facebook Pixel"), ("_pin_unauth", "Pinterest Tag"), ("_ga", "Google Analytics"),
               ("_gat", "Google Analytics"), ("_gid", "Google Analytics"), ("_gcl_au", "Google Adsense"),
               ("_hjAbsoluteSessionInProgress", "Hotjar"), ("_hjFirstSeen", "Hotjar"), ("_hjIncludedInSessionSample", "Hotjar")]


def initialize_website_file_and_check_cookie_banner():
    global current_website_cookie_use
    global website_index
    global short_website_name
    global current_website_accept_button_use
    global current_website_decline_button_use

    # Check if a cookie-banner is present at all
    print("Check cookie status for the website: " + website + " (" + short_website_name + ")")
    for keyword in positive_cookie_banner_buttons:
        # Special case for "ok" buttons: These can be confusing with normal text, e.g: "look" -> ok
        if re.search(r"\b" + keyword + r"\b", html_source):
            current_website_cookie_use = True

    if current_website_cookie_use:
        print("There is a cookie banner available!")

        # Check if accept button exists
        for keyword in positive_cookie_banner_buttons:
            buttons = driver.find_elements_by_xpath("//*[contains(text(),'" + keyword + "')]")

            if buttons.__len__() > 0:
                print("Keyword is identical with an existing "'"Accept"'"-Button!")
                current_website_accept_button_use = True
            else:
                print("Keyword is not identical with an existing "'"Accept"'"-Button!")

        # Check if decline button exists
        for keyword in negative_cookie_banner_buttons:
            buttons = driver.find_elements_by_xpath("//*[contains(text(),'" + keyword + "')]")

            if buttons.__len__() > 0:
                print("Keyword is identical with an existing "'"Reject"'"-Button!")
                current_website_decline_button_use = True
            else:
                print("Keyword is not identical with an existing "'"Reject"'"-Button!")
    else:
        print("There is NO cookie banner available!")
        generate_screenshot("no_banner")

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        dt_string = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        if use_headless_mode:
            website_file.write("Website " + str(website_index) + ": " + website + " | Created: " + str(dt_string) + " | HEADLESS-MODE: ON" + "\n")
        else:
            website_file.write("Website " + str(website_index) + ": " + website + " | Created: " + str(dt_string) + " | HEADLESS-MODE: OFF" + "\n")

        website_file.write("[Initial] Website uses a cookie banner: " + str(current_website_cookie_use) + "\n")


def check_gdpr_cookie_status():
    global current_website_gdpr_compliant
    global current_website_cookie_use
    global short_website_name
    global current_website_accept_button_use
    global current_website_decline_button_use

    if current_website_cookie_use:
        print("Check GDPR cookie banner status...")
        for keyword in gdpr_banner_keywords:
            if re.search(r'\b' + keyword + r'\b', html_source):
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
        website_file.write("[Initial] Website uses a "'"Accept"'"-Button: " + str(current_website_accept_button_use) + "\n")

        if current_website_gdpr_compliant:
            website_file.write("[Initial] Website uses a "'"Decline"'"-Button (GDPR-Banner): " + str(current_website_decline_button_use) + "\n")
            website_file.write("[Initial] -> GDPR-Banner often use settings buttons. " + "\n")

        else:
            website_file.write("[Initial] Website uses a "'"Decline"'"-Button: " + str(current_website_decline_button_use) + "\n")


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
    global current_website_cookie_use

    cookies = driver.get_cookies()

    print("Number of cookies after the cookie banner has been accepted: " + str(cookies.__len__()))
    print(cookies)

    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## After accepting the Cookie-Banner (or not) ##############################" + "\n")
        website_file.write("[After] Website-Cookie-Amount: " + str(cookies.__len__()) + "\n")
        website_file.write("[After] Website-Cookies: " + str(cookies) + "\n")

        for cookie in cookies:
            print("Cookie-Name: " + cookie['name'])
            website_file.write("[After] Cookie-Name " + str((cookies.index(cookie)) + 1) + ": " + cookie['name'] + "\n")


def generate_screenshot(reason):
    global screen_shot_index_randomly
    global screen_shot_index_no_banner
    global short_website_name

    if reason == "no_banner":
        body_part = driver.find_element_by_tag_name('body')
        body_part.screenshot("screenshots/no_banner/image_" + str(screen_shot_index_no_banner) + "_" + str(short_website_name) + ".png")
        screen_shot_index_no_banner += 1

        print("A screenshot was created! Reason: No Banner available")
    elif reason == "randomly":
        if randrange(10) == 4:
            body_part = driver.find_element_by_tag_name('body')
            body_part.screenshot("screenshots/randomly/image_" + str(screen_shot_index_randomly) + "_" + str(short_website_name) + ".png")
            screen_shot_index_randomly += 1

            print("A screenshot was created! Reason: Randomly selected")


def accept_cookie_banner():
    global current_website_cookie_use
    global able_to_accept_cookies

    if current_website_cookie_use:
        for keyword in positive_cookie_banner_buttons:
            buttons = driver.find_elements_by_xpath("//*[contains(text(),'" + keyword + "')]")
            for btn in buttons:
                if btn.text.casefold() == keyword.casefold():  # For multiple buttons: only click the real button to avoid misbehaviour
                    if btn.is_enabled() and btn.is_displayed():
                        btn.click()
                        print("Cookies Accepted! " + "(With keyword: " + keyword + ")")
                        able_to_accept_cookies = True
                        break  # After accepting the cookies, cancel the search for more buttons to accept cookies
                else:
                    continue  # Only executed if the inner loop did NOT break
                break  # Only executed if the inner loop DID break

        if not able_to_accept_cookies:
            print("This website has characteristics for a cookie banner, but it is not displayed to the user")


def create_short_website_name():
    global short_website_name

    short_website_name_sub = urlparse(website).netloc
    short_website_name = '.'.join(short_website_name_sub.split('.')[1:])


def analyze_cookie_files():
    global current_website_unauthorized_use_of_cookies_at_beginning
    global current_website_unauthorized_use_of_third_party_cookies_at_beginning
    global current_website_authorized_use_of_third_party_cookies_after
    global cookie_difference
    global t_p_c_name
    global current_website_cookie_use
    global current_website_accept_button_use
    global current_website_decline_button_use
    global able_to_accept_cookies

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
    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## Third party cookies used before acceptance ##############################" + "\n")

    # cookie_b = cookie before
    for a_cookie_b in a_cookies_before:
        updated_cookie_b = str(a_cookie_b).replace("\n", "")
        if updated_cookie_b in third_party_cookies:
            current_website_unauthorized_use_of_third_party_cookies_at_beginning = True

            with open("results/" + short_website_name + ".txt", "a") as website_file:
                t_p_c_name = [y for (x, y) in t_p_c_pairs if x == updated_cookie_b]
                website_file.write("[Used] Cookie-Name: " + updated_cookie_b + " (" + str(t_p_c_name[0]) + ")" + "\n")

    # Rate the new amount of cookies
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
        # For Problem: If no third-party cookies are present after cookie-button click, the website must still be presented as GDPR compliant
        elif not current_website_unauthorized_use_of_cookies_at_beginning and not current_website_unauthorized_use_of_third_party_cookies_at_beginning:
            current_website_authorized_use_of_third_party_cookies_after = True

    # Write the information of the analysis into the respective website files
    with open("results/" + short_website_name + ".txt", "a") as website_file:
        website_file.write("\n" + "############################## Difference (Before/After) ##############################" + "\n")
        website_file.write("[Difference] Cookies added: " + str(cookie_difference.__len__()) + "\n")

        for cookie_dif in cookie_difference:
            website_file.write("[Difference] Cookie-Name: " + str((list(cookie_difference).index(cookie_dif)) + 1) + ": " + str(cookie_dif))

        if current_website_cookie_use and not able_to_accept_cookies:
            website_file.write("\n" + "############################## Special Characteristics ##############################" + "\n")

            website_file.write("[Special] Website has characteristics for a cookie banner, but it is not displayed to the user" + "\n")

        website_file.write("\n" + "############################## Analysis ##############################" + "\n")

        if able_to_accept_cookies:
            if current_website_accept_button_use and current_website_decline_button_use:
                website_file.write("[Analysis] Website offers the user, in addition to accepting the cookie-banner, the possibility to reject it: "
                                   + "True" + "\n")
            else:
                if current_website_gdpr_compliant:
                    website_file.write("[Analysis] Website offers the user, in addition to accepting the cookie-banner, the possibility to reject it "
                                       "(GDPR): " + "False" + "\n")
                else:
                    website_file.write("[Analysis] Website offers the user, in addition to accepting the cookie-banner, the possibility to "
                                       "reject it: " + "False" + "\n")
        else:
            website_file.write("[Analysis] No corresponding buttons available, because cookie banner is not displayed" + "\n")

        website_file.write("[Analysis] Website generally uses cookies at the beginning (non-essential), although they are not authorized by the "
                           "user: " + str(current_website_unauthorized_use_of_cookies_at_beginning) + "\n")
        website_file.write("[Analysis] Website uses unauthorized third-party cookies at the beginning: "
                           + str(current_website_unauthorized_use_of_third_party_cookies_at_beginning) + "\n")
        website_file.write("[Analysis] Website respects the user's decision and loads THIRD-PARTY-COOKIES only after approval: "
                           + str(current_website_authorized_use_of_third_party_cookies_after) + "\n")

        # GDPR-compliant:
        # 1. Use of a GDPR-compliant banner
        # 2. Respecting third party cookie choice of user
        # 3. "Accept" and "Decline"-Button must be available
        if current_website_gdpr_compliant and current_website_authorized_use_of_third_party_cookies_after:
            website_file.write("\n" + "[Analysis] Website is GDPR compliant!" + "\n")
        elif not current_website_gdpr_compliant and current_website_authorized_use_of_third_party_cookies_after:
            if current_website_accept_button_use and current_website_decline_button_use:
                website_file.write("\n" + "[Analysis] Website is GDPR compliant!" + "\n")
            else:
                website_file.write("\n" + "[Analysis] Website is NOT GDPR compliant!" + "\n")
        elif not current_website_gdpr_compliant and not current_website_authorized_use_of_third_party_cookies_after:
            website_file.write("\n" + "[Analysis] Website is NOT GDPR compliant!" + "\n")
        elif current_website_gdpr_compliant and not current_website_authorized_use_of_third_party_cookies_after:
            website_file.write("\n" + "[Analysis] Website is NOT GDPR compliant!" + "\n")


if __name__ == '__main__':
    with open(all_websites_f1) as websites_all:  # File-options: all_websites_f[1-8]
        lines_websites = websites_all.readlines()

    for website in lines_websites:  # lines_websites
        try:
            website = str(website).replace("\n", "")
            create_short_website_name()
            driver.get(website)
            able_to_accept_cookies = False
            current_website_gdpr_compliant = False
            current_website_cookie_use = False
            current_website_unauthorized_use_of_cookies_at_beginning = False
            current_website_unauthorized_use_of_third_party_cookies_at_beginning = False
            current_website_authorized_use_of_third_party_cookies_after = False
            current_website_accept_button_use = False
            current_website_decline_button_use = False
            website_index += 1
            a_cookies_before.clear()
            a_cookies_after.clear()
            cookie_difference.clear()
            time.sleep(1)  # Wait for the website to load 15

            html_source = driver.page_source  # Get HTML-source-code

            # Check if website is still available
            if website_warning in html_source or \
                    website_warning_2 in html_source or \
                    website_warning_3 in html_source or \
                    website_warning_4 in html_source or \
                    website_warning_5 in html_source:
                print("Website not available!")
                print("Skip website...")
                offline_websites_amount += 1
                continue

            initialize_website_file_and_check_cookie_banner()  # Generate a website file. Is there a cookie banner at all?
            time.sleep(1)
            check_gdpr_cookie_status()  # Is the existing cookie banner GDPR compliant?
            time.sleep(1)
            check_cookies_at_start()  # Which cookies already exist after loading the page?
            time.sleep(1)
            generate_screenshot("randomly")  # Randomly generate a screenshot showing the cookie-banner status of the current page
            time.sleep(2)
            accept_cookie_banner()  # Accept the cookie banner displayed
            time.sleep(1)
            check_cookies_after_banner_accept()  # What cookies exist on the site after accepting the corresponding cookie banner?
            time.sleep(1)
            analyze_cookie_files()  # Analyze the generated website files
            driver.delete_all_cookies()  # Remove loaded cookies after each iteration to increase performance
        except WebDriverException:
            print("\nException: Page most likely unavailable or offline!")
            os.remove("results/" + short_website_name + ".txt")
            print("Skip website...")
            continue

    print("\nAmount of offline websites: " + str(offline_websites_amount))
    print("Analysis finished, close driver...")
    driver.close()
