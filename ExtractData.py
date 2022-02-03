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

# Cookie-Amount-Difference
websites_use_less_than_10_c_difference = 0
websites_use_less_than_20_c_difference = 0
websites_use_less_than_30_c_difference = 0
websites_use_less_than_40_c_difference = 0
websites_use_less_than_50_c_difference = 0
websites_use_more_than_50_c_difference = 0

# Analysis
websites_no_use_of_decline_button = 0  # Exception: websites that are using a GDPR banner. These use a cookie selection mechanism
websites_use_of_cookies_at_beginning = 0
websites_use_unauthorized_third_party_c_at_beginning = 0
websites_respects_users_decision = 0

# Summary: GDPR-Compliant?
websites_that_are_gdpr_compliant = 0

# Variables/Directories
text_files = []
c_amount_before = 0
c_amount_after = 0
c_amount_difference = 0


def analyze_generated_files():
    global websites_use_cookie_banner
    global websites_use_gdpr_cookie_banner
    global websites_use_accept_button
    global websites_use_decline_button
    global websites_use_gdpr_decline_button
    global websites_use_facebook_pixel
    global websites_use_pinterest_tag
    global websites_use_google_service
    global websites_use_hotjar_tool
    global c_amount_before, c_amount_after, c_amount_difference
    global websites_use_less_than_10_c_before, websites_use_less_than_10_c_after, websites_use_less_than_10_c_difference
    global websites_use_less_than_20_c_before, websites_use_less_than_20_c_after, websites_use_less_than_20_c_difference
    global websites_use_less_than_30_c_before, websites_use_less_than_30_c_after, websites_use_less_than_30_c_difference
    global websites_use_less_than_40_c_before, websites_use_less_than_40_c_after, websites_use_less_than_40_c_difference
    global websites_use_less_than_50_c_before, websites_use_less_than_50_c_after, websites_use_less_than_50_c_difference
    global websites_use_more_than_50_c_before, websites_use_more_than_50_c_after, websites_use_more_than_50_c_difference

    print("Search files...")
    time.sleep(1)

    for file in glob.glob("*.txt"):
        text_files.append(file)

    print("Found " + str(text_files.__len__()) + " files!")
    print("Start Analysis...")
    time.sleep(1)

    # Loop through all files and all lines in that files
    for index, file in enumerate(text_files, start=1):
        with open("results/" + file) as website_file:  # TODO: fixen
            # results/360living.de.txt
            lines = website_file.readlines()

            print("[" + str(index) + "] " + "Analyze text file: " + file)
            # Ask for different sentences/words/phrases
            for line in lines:
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
                elif line.__eq__("[Used] Cookie-Name: _fbp (Facebook Pixel)"):
                    websites_use_facebook_pixel += 1
                elif line.__eq__("[Used] Cookie-Name: _pin_unauth (Pinterest Tag)"):
                    websites_use_pinterest_tag += 1
                elif line.__eq__("[Used] Cookie-Name: _gcl_au (Google Adsense)") or \
                        line.__eq__("[Used] Cookie-Name: _ga (Google Analytics)") or \
                        line.__eq__("[Used] Cookie-Name: _gat (Google Analytics)") or \
                        line.__eq__("[Used] Cookie-Name: _gid (Google Analytics)"):
                    websites_use_google_service += 1
                elif line.__eq__("[Used] Cookie-Name: _hjAbsoluteSessionInProgress (Hotjar (User experience tool))") or \
                        line.__eq__("[Used] Cookie-Name: _hjIncludedInSessionSample (Hotjar (User experience tool))") or \
                        line.__eq__("[Used] Cookie-Name: _hjFirstSeen (Hotjar (User experience tool))") or \
                        line.__eq__("[Used] Cookie-Name: _hjIncludedInPageviewSample (Hotjar (User experience tool))"):
                    websites_use_hotjar_tool += 1
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
    time.sleep(3)
    print("Analysis finished!")
    time.sleep(1)
    print("Results:")
    time.sleep(1)
    print("Webseiten, welche einen cookie banner verwenden: " + str(websites_use_cookie_banner))
    print("Webseiten, welche einen GDPR konformen cookie banner verwenden: " + str(websites_use_gdpr_cookie_banner))
    # TODO: Weiterführen...
    # TODO: Die Ergebnisse in eine Datei kurz schreiben lassen...


if __name__ == '__main__':
    analyze_generated_files()
