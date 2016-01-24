# laughing-chainsaw
Simple Web Scraper

# laughing-chainsaw
Simple Web Scraper

This is a python script to scrape printer's configuration pages for MAC addresse
s. It accepts a csv file with a list of ip addresses, checks if port 80 is open 
on said addresses, and if it is attempts to pull a string from the page.

It should be noted that this script is for a very specific purpose on a very spe
cific set of ip addresses. For example: I know that when I grab the 21st string
element from the html it's becaus I already know that the information I'm lookin
g for (in this case the MAC address) is located at that location.

My intention is to take this functional, yet narrow use case, script and general
ize it as much as I can.


