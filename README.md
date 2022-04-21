# GDPR-Cookie-Crawler
A python-selenium crawler which checks the GDPR compliance regarding cookies in Shopify stores. The tool also analyzes the existing cookies (before and after cookie-banner-decision). I developed this tool for my master-thesis.

## Results (Console-log)
#################### Basic results ####################<br>
Number of websites that use a cookie banner (have characteristics): 2399 => [Percentage: 99.05%], [23 website(s) not]<br>
Number of websites that use a GDPR compliant cookie banner: 1578 => [Percentage: 65.15%], [844 website(s) not]<br>
Number of websites that use an "Accept" button (characteristics of it): 2399 => [Percentage: 99.05%], [23 website(s) not]<br>
Number of websites that use an "Decline" button (characteristics of it): 29 => [Percentage: 1.2%], [2393 website(s) not]<br>
Number of websites that offer GDPR-compliant selection mechanisms: 528 => [Percentage: 21.8%], [1894 website(s) not]<br>

#################### Cookie-Amount-Results ####################<br>
---Before:<br>
Number of websites that have used less than 10 cookies before acceptance: 473 [19.53%]<br>
Number of websites that have used between 10 and 20 cookies before acceptance: 1071 [44.22%]<br>
Number of websites that have used between 20 and 30 cookies before acceptance: 761 [31.42%]<br>
Number of websites that have used between 30 and 40 cookies before acceptance: 100 [4.13%]<br>
Number of websites that have used between 40 and 50 cookies before acceptance: 17 [0.7%]<br>
Number of websites that have used more than 50 cookies before acceptance: 0 [0.0%]<br>
---After:<br>
Number of websites that have used less than 10 cookies after acceptance: 99 [4.09%]<br>
Number of websites that have used between 10 and 20 cookies after acceptance: 945 [39.02%]<br>
Number of websites that have used between 20 and 30 cookies after acceptance: 932 [38.48%]<br>
Number of websites that have used between 30 and 40 cookies after acceptance: 387 [15.98%]<br>
Number of websites that have used between 40 and 50 cookies after acceptance: 58 [2.39%]<br>
Number of websites that have used more than 50 cookies after acceptance: 1 [0.04%]<br>
---Difference:<br>
Difference cookie count (before/after), less than 10 cookies added: 1978 [81.67%]<br>
Difference cookie count (before/after), between 10 and 20 cookies added: 319 [13.17%]<br>
Difference cookie count (before/after), between 20 and 30 cookies added: 119 [4.91%]<br>
Difference cookie count (before/after), between 30 and 40 cookies added: 6 [0.25%]<br>
Difference cookie count (before/after), between 40 and 50 cookies added: 0 [0.0%]<br>
Difference cookie count (before/after), more than 50 cookies added: 0 [0.0%]<br>

#################### Third-party-cookie-results ####################<br>
Number of websites that have used the facebook pixel as a third-party cookie without permission: 913 => [Percentage: 37.7%], [1509 website(s) not]<br>
Number of websites that have used the pinterest tag as a third-party cookie without permission: 294 => [Percentage: 12.14%], [2128 website(s) not]<br>
Number of websites that have used a google service as a third-party cookie without permission: 1194 => [Percentage: 49.3%], [1228 website(s) not]<br>
Number of websites that have used hotjar as a third-party cookie without permission: 175 => [Percentage: 7.23%], [2247 website(s) not]<br>
Number of websites that have used hubspot as a third-party cookie without permission: 25 => [Percentage: 1.03%], [2397 website(s) not]<br>
Number of websites that have used klaviyo as a third-party cookie without permission: 477 => [Percentage: 19.69%], [1945 website(s) not]<br>
Number of websites that have used leadfeeder as a third-party cookie without permission: 2 => [Percentage: 0.08%], [2420 website(s) not]<br>
Number of websites that have used microsoft clarity as a third-party cookie without permission: 80 => [Percentage: 3.3%], [2342 website(s) not]<br>
Number of websites that have used lucky orange as a third-party cookie without permission: 14 => [Percentage: 0.58%], [2408 website(s) not]<br>

#################### Final analysis ####################<br>
Number of websites that have cookie characteristics but do not display a cookie banner to the user (special characteristic): 953 => [Percentage: 39.35%], [1469 website(s) not]<br>
Number of websites that offer the user a "Decline" option: 521 => [Percentage: 21.51%], [1901 website(s) not]<br>
Number of websites that use third-party cookies without permission at the beginning: 1417 => [Percentage: 58.51%], [1005 website(s) not]<br>
Number of websites that respect the user's decision and only load third-party cookies if this is explicitly permitted: 973 => [Percentage: 40.17%], [1449 website(s) not]<br>

Number of websites which are GDPR compliant: 743 => [Percentage: 30.68%], [1679 website(s) not]

## Diagrams
soon...
