import numpy
import csv
import sys
import pycurl
import requests
import json

with open('config.json') as json_data_file:
	data = json.load(json_data_file)

from bs4 import BeautifulSoup

from StringIO import StringIO

#Change stdout to write results to file instead of print to screen
orig_stdout = sys.stdout
f = file('rls_output.csv', 'w')
sys.stdout = f

#Open the pre-formatted csv as input
fp = open('rls_only2.csv')

#Create array for the ip addresses
data_list = []

#Populate the array with the ip addresses
for line in fp:
	data_list.append(tuple(line.strip().split(',')))

#Find out how many ip addresses there are to use in the while loop
print len(data_list[0])

#Assign the nubmer of ip addresses as max
count = len(data_list[0])

#Start the counter to zero
i = 0

#Main loop
while (i < count):

	ip_address = data_list[0][i]

  	storage = StringIO()

#Use pycurl to authenticate to the printer's Network Settings Page
       	c = pycurl.Curl()
       	c.setopt(pycurl.URL, "%s/bio/main.html" % ip_address)
       	c.setopt(c.WRITEFUNCTION, storage.write)
       	c.setopt(pycurl.FOLLOWLOCATION, 1)
       	c.setopt(pycurl.USERPWD, 'admin:access')
	c.setopt(pycurl.CONNECTTIMEOUT, 15)
	c.setopt(pycurl.TIMEOUT, 15)

#This block checks if port 80 is actually open at the ip address
	try:

       		c.perform()

#If the port is open and the HTTP_CODE returns 200 (OK)...
		if c.getinfo(pycurl.HTTP_CODE) == 200:
#Print the current ip address. Comma at the end to remove newline
			print "%s," % ip_address,
#Create variable to store the html_doc
			html_doc = storage.getvalue()
#Use the BeatifulSoup library to parse the html
			soup = BeautifulSoup(html_doc, 'html.parser')
#Create an array to hold the strings
			list_of_strings = []
#Populate the array with all of the strings in the scraped Network Settings Page
			for string in soup.stripped_strings:
				list_of_strings.append(repr(string))
#I already know that any devices with more than 21 string elemnts are printers
#This tests to see if the device is a printer or something else
			if len(list_of_strings) > 21:
#If the device is a printer than store element 21 (The MAC Address) into a variable
				myList = list_of_strings[21]
				print "%s," % myList
			else:
#Else print a nonsense character
				print "X,"
#If pycurl returns anything besides a code 200 then print a nonsense character
		elif c.getinfo(pycurl.HTTP_CODE) == 301:
			print "%s, X," % ip_address
		else:
			print "%s, X," % ip_address
#If port 80 is not even open then simply print the ip along with nonsense character
	except pycurl.error, error:
		errno, errstr = error
		#print 'An error occurred: ', errstr
		print "%s, X," % ip_address

#Increment loop counter
	i = i + 1

#Change the stdout back to normal
sys.stdout = orig_stdout
f.close()
