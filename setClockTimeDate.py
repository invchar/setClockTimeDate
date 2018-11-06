#!/usr/bin/python3
import os
import time
import mechanicalsoup
from syslog import syslog, LOG_INFO, LOG_ERR

user = os.getenv("clocks_user")
password = os.getenv("clocks_password")
clocks_string = os.getenv("clocks_ips")
clocks = clocks_string.split(":")

def log(log_level=LOG_INFO, message="No message provided"):
	syslog(log_level, message)

def updateClock(clock):
	try:
		browser = mechanicalsoup.StatefulBrowser()
		browser.open('http://{}/termsup.htm'.format(clock), auth=(user,password))
		browser.select_form()
		browser["FDateString"] = time.strftime("%y%m%d")
		browser["FTimeString"] = time.strftime("%H%M%S")
		browser.submit_selected()
		log(message="setClockTimeDate.py: Clock {} has been updated".format(clock))
		return 0
	except Exception as e:
		log(LOG_ERR, "setClockTimeDate.py: Failed to update clock")
		log(LOG_ERR, str(e))
		return 1

def main():
	if (not user or not password or not clocks):
		log(LOG_ERR,"setClockTimeDate.py: Not all environment variables are set")
		sys.exit(1)
	for clock in clocks:
		if (updateClock(clock)):
			log(LOG_ERR, "seClockTimeDate.py: {} was not updated".format(clock))

if __name__ == "__main__":
	main()
