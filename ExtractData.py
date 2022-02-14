import time
import glob
import os

# Counter
# Cookie-Use/Button-Use
websites_use_cookie_banner = 0
websites_use_gdpr_cookie_banner = 0
websites_use_accept_button = 0
websites_use_decline_button = 0
websites_use_gdpr_decline_button = 0

# Cookie-Amount-Before
websites_use_less_than_10_c_before = 0
websites_use_less_than_20_c_before = 0
websites_use_less_than_30_c_before = 0
websites_use_less_than_40_c_before = 0
websites_use_less_than_50_c_before = 0
websites_use_more_than_50_c_before = 0

# Cookie-Amount-After
websites_use_less_than_10_c_after = 0
websites_use_less_than_20_c_after = 0
websites_use_less_than_30_c_after = 0
websites_use_less_than_40_c_after = 0
websites_use_less_than_50_c_after = 0
websites_use_more_than_50_c_after = 0

# Third-Party-Cookie-Use
websites_use_facebook_pixel = 0
websites_use_pinterest_tag = 0
websites_use_google_service = 0
websites_use_hotjar_tool = 0
websites_use_hubspot_system = 0
websites_use_klaviyo_tool = 0
websites_use_leadfeeder_b2b_spytool = 0
websites_use_microsoft_clarity_tool = 0
websites_use_luckyorange_tool = 0

# Block-Variables
found_google = False
found_hotjar = False
found_hubspot = False
found_microsoft_clarity = False
found_lucky_orange = False

# Cookie-Amount-Difference
websites_use_less_than_10_c_difference = 0
websites_use_less_than_20_c_difference = 0
websites_use_less_than_30_c_difference = 0
websites_use_less_than_40_c_difference = 0
websites_use_less_than_50_c_difference = 0
websites_use_more_than_50_c_difference = 0

# Analysis
websites_special_characteristic = 0  # Special case
websites_use_of_decline_option = 0
websites_no_use_of_decline_option = 0  # Exception: websites that are using a GDPR banner. These use a cookie selection mechanism
websites_use_of_cookies_at_beginning = 0  # Debug
websites_use_unauthorized_third_party_c_at_beginning = 0
websites_respects_users_decision = 0

# Summary: GDPR-Compliant?
websites_that_are_gdpr_compliant = 0

# Variables/Directories
text_files = []
c_amount_before = 0
c_amount_after = 0
c_amount_difference = 0
german_language_output = True  # Choose language output: german = True, english = False


def calculate_other_values(base_value):
    global german_language_output

    if german_language_output:
        return " => [Prozentsatz: " + str(int((base_value / text_files.__len__()) * 100)) + "%]" + ", [" + str(text_files.__len__() - base_value) + \
               " Webseite(n) nicht" + "]"
    else:
        return " => [Percentage: " + str(int((base_value / text_files.__len__()) * 100)) + "%]" + ", [" + str(text_files.__len__() - base_value) + \
               " website(s) not" + "]"


def calculate_percentage_value(base_value):
    return " [" + str(int(base_value / text_files.__len__() * 100)) + "%" + "]"


def analyze_generated_files():
    global german_language_output
    global websites_use_cookie_banner
    global websites_use_gdpr_cookie_banner
    global websites_use_accept_button
    global websites_use_decline_button
    global websites_use_gdpr_decline_button
    global websites_use_facebook_pixel
    global websites_use_pinterest_tag
    global websites_use_google_service
    global websites_use_hotjar_tool
    global websites_use_hubspot_system
    global websites_use_klaviyo_tool
    global websites_use_leadfeeder_b2b_spytool
    global websites_use_microsoft_clarity_tool
    global websites_use_luckyorange_tool
    global websites_special_characteristic  # Analysis
    global websites_use_of_cookies_at_beginning  # Debug
    global websites_use_of_decline_option
    global websites_use_unauthorized_third_party_c_at_beginning
    global websites_respects_users_decision
    global websites_that_are_gdpr_compliant
    global c_amount_before, c_amount_after, c_amount_difference
    global websites_use_less_than_10_c_before, websites_use_less_than_10_c_after, websites_use_less_than_10_c_difference
    global websites_use_less_than_20_c_before, websites_use_less_than_20_c_after, websites_use_less_than_20_c_difference
    global websites_use_less_than_30_c_before, websites_use_less_than_30_c_after, websites_use_less_than_30_c_difference
    global websites_use_less_than_40_c_before, websites_use_less_than_40_c_after, websites_use_less_than_40_c_difference
    global websites_use_less_than_50_c_before, websites_use_less_than_50_c_after, websites_use_less_than_50_c_difference
    global websites_use_more_than_50_c_before, websites_use_more_than_50_c_after, websites_use_more_than_50_c_difference
    global found_google, found_hotjar, found_hubspot, found_microsoft_clarity, found_lucky_orange

    print("Search files...")
    time.sleep(1)

    for file in glob.glob("local_results/*.txt"):
        text_files.append(file)

    print("Found " + str(text_files.__len__()) + " files!")
    print("Start Analysis...")
    time.sleep(1)

    # Loop through all files and all lines in that files
    for index, file in enumerate(text_files, start=1):
        with open(file) as website_file:
            # local_results/360living.de.txt
            lines = website_file.readlines()

            print("[" + str(index) + "] " + "Analyze text file: " + file)
            # Ask for different sentences/words/phrases
            for line in lines:
                line = line.replace("\n", "")
                if line.__eq__("[Initial] Website uses a cookie banner: True"):
                    websites_use_cookie_banner += 1
                elif line.__eq__("[Initial] Website uses a GDPR compliant cookie banner: True"):
                    websites_use_gdpr_cookie_banner += 1
                elif line.__eq__("[Initial] Website uses a "'"Accept"'"-Button: True"):
                    websites_use_accept_button += 1
                elif line.__eq__("[Initial] Website uses a "'"Decline"'"-Button: True"):
                    websites_use_decline_button += 1
                elif line.__eq__("[Initial] Website uses a "'"Decline"'"-Button (GDPR-Banner): True"):
                    websites_use_gdpr_decline_button += 1
                elif line.__eq__("[Special] Website has characteristics for a cookie banner, but it is not displayed to the user"):
                    websites_special_characteristic += 1
                elif line.__eq__("[Analysis] Website offers the user, in addition to accepting the cookie-banner, the possibility to "
                                 "reject it: True"):
                    websites_use_of_decline_option += 1
                elif line.__eq__("[Analysis] Website generally uses cookies at the beginning (non-essential), although they are not authorized by "
                                 "the user: True"):
                    websites_use_of_cookies_at_beginning += 1  # Debug
                elif line.__eq__("[Analysis] Website uses unauthorized third-party cookies at the beginning: True"):
                    websites_use_unauthorized_third_party_c_at_beginning += 1
                elif line.__eq__("[Analysis] Website respects the user's decision and loads THIRD-PARTY-COOKIES only after approval: True"):
                    websites_respects_users_decision += 1
                elif line.__eq__("[Analysis] Website is GDPR compliant!"):
                    websites_that_are_gdpr_compliant += 1
                elif line.__eq__("[Used before] Cookie-Name: _fbp (Facebook Pixel)"):
                    websites_use_facebook_pixel += 1
                elif line.__eq__("[Used before] Cookie-Name: _pin_unauth (Pinterest Tag)"):
                    websites_use_pinterest_tag += 1
                elif line.__eq__("[Used before] Cookie-Name: _gcl_au (Google Adsense)") and not found_google or \
                        line.__eq__("[Used before] Cookie-Name: _ga (Google Analytics)") and not found_google or \
                        line.__eq__("[Used before] Cookie-Name: _gat (Google Analytics)") and not found_google or \
                        line.__eq__("[Used before] Cookie-Name: _gid (Google Analytics)") and not found_google:
                    websites_use_google_service += 1
                    found_google = True
                elif line.__eq__("[Used before] Cookie-Name: _hjAbsoluteSessionInProgress (Hotjar (User experience tool))") and not found_hotjar or \
                        line.__eq__("[Used before] Cookie-Name: _hjIncludedInSessionSample (Hotjar (User experience tool))") and not found_hotjar or \
                        line.__eq__("[Used before] Cookie-Name: _hjFirstSeen (Hotjar (User experience tool))") and not found_hotjar or \
                        line.__eq__("[Used before] Cookie-Name: _hjIncludedInPageviewSample (Hotjar (User experience tool))") and not found_hotjar:
                    websites_use_hotjar_tool += 1
                    found_hotjar = True
                elif line.__eq__("[Used before] Cookie-Name: __hssc (HubSpot (CRM-System))") and not found_hubspot or \
                        line.__eq__("[Used before] Cookie-Name: hubspotutk (HubSpot (CRM-System))") and not found_hubspot:
                    websites_use_hubspot_system += 1
                    found_hubspot = True
                elif line.__eq__("[Used before] Cookie-Name: __kla_id (Klaviyo (E-Mail-Marketing))"):
                    websites_use_klaviyo_tool += 1
                elif line.__eq__("[Used before] Cookie-Name: _lfa (Leadfeeder (B2B Spy-tool))"):
                    websites_use_leadfeeder_b2b_spytool += 1
                elif line.__eq__("[Used before] Cookie-Name: _clsk (Microsoft Clarity (User experience tool))") and not found_microsoft_clarity or \
                        line.__eq__("[Used before] Cookie-Name: _clck (Microsoft Clarity (User experience tool))") and not found_microsoft_clarity:
                    websites_use_microsoft_clarity_tool += 1
                    found_microsoft_clarity = True
                elif line.__eq__("[Used before] Cookie-Name: __lotl (Lucky Orange (User experience tool))") and not found_lucky_orange or \
                        line.__eq__("[Used before] Cookie-Name: _lo_v (Lucky Orange (User experience tool))") and not found_lucky_orange or \
                        line.__eq__("[Used before] Cookie-Name: _lorid (Lucky Orange (User experience tool))") and not found_lucky_orange or \
                        line.__eq__("[Used before] Cookie-Name: _lo_uid (Lucky Orange (User experience tool))") and not found_lucky_orange:
                    websites_use_luckyorange_tool += 1
                    found_lucky_orange = True
                elif "[Before] Website-Cookie-Amount:" in line:
                    c_amount_before = line.split(": ")[1]

                    if int(c_amount_before) < 10:
                        websites_use_less_than_10_c_before += 1
                    elif int(c_amount_before) < 20:
                        websites_use_less_than_20_c_before += 1
                    elif int(c_amount_before) < 30:
                        websites_use_less_than_30_c_before += 1
                    elif int(c_amount_before) < 40:
                        websites_use_less_than_40_c_before += 1
                    elif int(c_amount_before) < 50:
                        websites_use_less_than_50_c_before += 1
                    else:
                        websites_use_more_than_50_c_before += 1
                elif "[After] Website-Cookie-Amount:" in line:
                    c_amount_after = line.split(": ")[1]

                    if int(c_amount_after) < 10:
                        websites_use_less_than_10_c_after += 1
                    elif int(c_amount_after) < 20:
                        websites_use_less_than_20_c_after += 1
                    elif int(c_amount_after) < 30:
                        websites_use_less_than_30_c_after += 1
                    elif int(c_amount_after) < 40:
                        websites_use_less_than_40_c_after += 1
                    elif int(c_amount_after) < 50:
                        websites_use_less_than_50_c_after += 1
                    else:
                        websites_use_more_than_50_c_after += 1
                elif "[Difference] Cookies added:" in line:
                    c_amount_difference = line.split(": ")[1]

                    if int(c_amount_difference) < 10:
                        websites_use_less_than_10_c_difference += 1
                    elif int(c_amount_difference) < 20:
                        websites_use_less_than_20_c_difference += 1
                    elif int(c_amount_difference) < 30:
                        websites_use_less_than_30_c_difference += 1
                    elif int(c_amount_difference) < 40:
                        websites_use_less_than_40_c_difference += 1
                    elif int(c_amount_difference) < 50:
                        websites_use_less_than_50_c_difference += 1
                    else:
                        websites_use_more_than_50_c_difference += 1
        found_google = False
        found_hotjar = False
        found_hubspot = False
        found_microsoft_clarity = False
        found_lucky_orange = False

    time.sleep(3)
    print("Analysis finished!")
    time.sleep(1)
    print("Results:")
    time.sleep(1)

    if german_language_output:
        print("\n#################### Grundlegende Ergebnisse ####################")
        print("Anzahl der Webseiten, welche einen cookie banner verwenden (Merkmale besitzen): " +
              str(websites_use_cookie_banner) + calculate_other_values(websites_use_cookie_banner))
        print("Anzahl der Webseiten, welche einen GDPR konformen cookie banner verwenden: " +
              str(websites_use_gdpr_cookie_banner) + calculate_other_values(websites_use_gdpr_cookie_banner))
        print("Anzahl der Webseiten, welche einen "'"Akzeptieren"'"-Button (Merkmale davon) verwenden: " +
              str(websites_use_accept_button) + calculate_other_values(websites_use_accept_button))
        print("Anzahl der Webseiten, welche einen "'"Ablehnen"'"-Button (Merkmale davon) verwenden: " +
              str(websites_use_decline_button) + calculate_other_values(websites_use_decline_button))
        print("Anzahl der Webseiten, welche GDPR-konforme Auswahlmechanismen anbieten: " +
              str(websites_use_gdpr_decline_button) + calculate_other_values(websites_use_gdpr_decline_button))

        print("\n#################### Cookie-Amount-Ergebnisse ####################")
        print("---Before:")
        print("Anzahl der Webseiten, welche weniger als 10 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_10_c_before) + calculate_percentage_value(websites_use_less_than_10_c_before))
        print("Anzahl der Webseiten, welche zwischen 10 und 20 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_20_c_before) + calculate_percentage_value(websites_use_less_than_20_c_before))
        print("Anzahl der Webseiten, welche zwischen 20 und 30 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_30_c_before) + calculate_percentage_value(websites_use_less_than_30_c_before))
        print("Anzahl der Webseiten, welche zwischen 30 und 40 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_40_c_before) + calculate_percentage_value(websites_use_less_than_40_c_before))
        print("Anzahl der Webseiten, welche zwischen 40 und 50 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_50_c_before) + calculate_percentage_value(websites_use_less_than_50_c_before))
        print("Anzahl der Webseiten, welche mehr als 50 cookies vor der Akzeptierung verwendet haben: " +
              str(websites_use_more_than_50_c_before) + calculate_percentage_value(websites_use_more_than_50_c_before))

        print("---After:")
        print("Anzahl der Webseiten, welche weniger als 10 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_10_c_after) + calculate_percentage_value(websites_use_less_than_10_c_after))
        print("Anzahl der Webseiten, welche zwischen 10 und 20 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_20_c_after) + calculate_percentage_value(websites_use_less_than_20_c_after))
        print("Anzahl der Webseiten, welche zwischen 20 und 30 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_30_c_after) + calculate_percentage_value(websites_use_less_than_30_c_after))
        print("Anzahl der Webseiten, welche zwischen 30 und 40 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_40_c_after) + calculate_percentage_value(websites_use_less_than_40_c_after))
        print("Anzahl der Webseiten, welche zwischen 40 und 50 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_less_than_50_c_after) + calculate_percentage_value(websites_use_less_than_50_c_after))
        print("Anzahl der Webseiten, welche mehr als 50 cookies nach der Akzeptierung verwendet haben: " +
              str(websites_use_more_than_50_c_after) + calculate_percentage_value(websites_use_more_than_50_c_after))

        print("---Difference:")
        print("Unterschied cookie-anzahl (davor/danach), weniger als 10 cookies dazugekommen: " +
              str(websites_use_less_than_10_c_difference) + calculate_percentage_value(websites_use_less_than_10_c_difference))
        print("Unterschied cookie-anzahl (davor/danach), zwischen 10 und 20 cookies dazugekommen: " +
              str(websites_use_less_than_20_c_difference) + calculate_percentage_value(websites_use_less_than_20_c_difference))
        print("Unterschied cookie-anzahl (davor/danach), zwischen 20 und 30 cookies dazugekommen: " +
              str(websites_use_less_than_30_c_difference) + calculate_percentage_value(websites_use_less_than_30_c_difference))
        print("Unterschied cookie-anzahl (davor/danach), zwischen 30 und 40 cookies dazugekommen: " +
              str(websites_use_less_than_40_c_difference) + calculate_percentage_value(websites_use_less_than_40_c_difference))
        print("Unterschied cookie-anzahl (davor/danach), zwischen 40 und 50 cookies dazugekommen: " +
              str(websites_use_less_than_50_c_difference) + calculate_percentage_value(websites_use_less_than_50_c_difference))
        print("Unterschied cookie-anzahl (davor/danach), mehr als 50 cookies dazugekommen: " +
              str(websites_use_more_than_50_c_difference) + calculate_percentage_value(websites_use_more_than_50_c_difference))

        print("\n#################### Third-Party-Cookie-Ergebnisse ####################")
        print("Anzahl der Webseiten, welche den facebook-pixel als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_facebook_pixel) + calculate_other_values(websites_use_facebook_pixel))
        print("Anzahl der Webseiten, welche den pinterest-tag als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_pinterest_tag) + calculate_other_values(websites_use_pinterest_tag))
        print("Anzahl der Webseiten, welche einen google service unerlaubt als third-party-cookie verwendet haben: " +
              str(websites_use_google_service) + calculate_other_values(websites_use_google_service))
        print("Anzahl der Webseiten, welche hotjar als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_hotjar_tool) + calculate_other_values(websites_use_hotjar_tool))
        print("Anzahl der Webseiten, welche hubspot als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_hubspot_system) + calculate_other_values(websites_use_hubspot_system))
        print("Anzahl der Webseiten, welche klaviyo als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_klaviyo_tool) + calculate_other_values(websites_use_klaviyo_tool))
        print("Anzahl der Webseiten, welche leadfeeder als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_leadfeeder_b2b_spytool) + calculate_other_values(websites_use_leadfeeder_b2b_spytool))
        print("Anzahl der Webseiten, welche microsoft clarity als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_microsoft_clarity_tool) + calculate_other_values(websites_use_microsoft_clarity_tool))
        print("Anzahl der Webseiten, welche lucky orange als third-party-cookie unerlaubt verwendet haben: " +
              str(websites_use_luckyorange_tool) + calculate_other_values(websites_use_luckyorange_tool))

        print("\n#################### Finale Analyse ####################")
        print("Anzahl der Webseiten, welche cookie-merkmale besitzen aber dem Nutzer keinen cookie-banner anzeigen (Sondermerkmal): " +
              str(websites_special_characteristic) + calculate_other_values(websites_special_characteristic))
        print("Anzahl der Webseiten, welche dem Nutzer eine "'"Ablehn"'"-Option anbieten: " +
              str(websites_use_of_decline_option) + calculate_other_values(websites_use_of_decline_option))
        print("Anzahl der Webseiten, welche third-party-cookies am Anfang unerlaubt nutzen: " +
              str(websites_use_unauthorized_third_party_c_at_beginning) + calculate_other_values(websites_use_unauthorized_third_party_c_at_beginning))
        print("Anzahl der Webseiten, welche die Entscheidung des Nutzers respektieren und third-party-cookies nur dann laden, wenn dies ausdrücklich "
              "gewünscht ist: " + str(websites_respects_users_decision) + calculate_other_values(websites_respects_users_decision))
        print("\nAnzahl der Webseiten, welche GDPR-konform sind: " +
              str(websites_that_are_gdpr_compliant) + calculate_other_values(websites_that_are_gdpr_compliant))


if __name__ == '__main__':
    analyze_generated_files()
