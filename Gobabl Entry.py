import requests
import time
import matplotlib.pyplot as plt
import datetime

#Loosely based on https://packetlife.net/blog/2019/aug/7/apis-real-life-snagging-global-entry-interview/ there are also several other repo's available


#Use a browsers network debugging tools to see the specific request from https://ttp.cbp.dhs.gov/schedulerui/schedule-interview/location?lang=en&vo=true&returnUrl=ttp-external&service=up 
#Click on your desired location, should look like https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=1&locationId=5200&minimum=1
LocationsDict = {
"Logan" : 5441,
"RI" 	: 9300,
# "JFK"	: 5140,
"NYC"	: 6480,
"CT"	: 14681,
# "Guam"	: 9140	#Test location, Guam is always open apparently

}

Verbose = 0

print("Retrieving locations...")
while (1):
	for Location in LocationsDict:
		#Build and ping the URL, pull it as JSON
		RequestURL = "https://ttp.cbp.dhs.gov/schedulerapi/slots?orderBy=soonest&limit=100&locationId=%d&minimum=1" % LocationsDict[Location]
		if (Verbose): print ("Checking %s, id %d, URL: %s" % (Location,LocationsDict[Location],RequestURL))
		Appts = requests.get(RequestURL).json()
	
		if (Verbose): print ("%d appointments found at %s" % (len(Appts),Location))
		
		#99% of the time these will be empty or we wouldn't be scripting this
		if (len(Appts) > 0):
			Now  = datetime.datetime.now()
			for Appt in Appts:
				#Check when the appointment is, work out how long until the appointment
				ApptTime = datetime.datetime.strptime(Appt["startTimestamp"], "%Y-%m-%dT%H:%M")
				Delta = ApptTime-Now
				
				#Any day if it's local, Friday-Monday if it isn't. Need a few days notice to travel
				if (Location == "Logan") or ((ApptTime.weekday() > 3) and Delta.days>2) or ((ApptTime.weekday() == 0) and Delta.days>2):
					
					if (Verbose):
						print ("%s Appt available." % Location)
						print (Appts)
					#Quick and dirty way to implement a pop up window so we can panic click our way through the website as fast as possible
					#Could add a timer to kill this since appointments last ~1 minute before they are snagged, but this is as simple as it gets
					ApptInfo = ApptTime.strftime ("%a %b %d %Y")
					plt.text (0.5,0.5,"%s - %s" % (Location,ApptInfo))
					plt.show()
		time.sleep(2)	#Don't agressively ping the server
	