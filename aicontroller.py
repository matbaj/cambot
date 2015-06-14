import pywapi
import sys
import datetime
import imaplib

import httplib2
import os

from googleapiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Quickstart'


class AIController:

	def __init__(self):
		self.previous_orders = 0
		self.anger_meter = 0

	def initMail(self, mail, password):
		self.mail = mail
		self.password = password

	def act(self, order):
		rep = []
		if "love you" in order:
			rep.append(self.relation(order))

		if "hello" in order: 
			rep.append(self.greet(order))

		# check if there is do not before track 
		if "track faces" in order :
			rep.append(self.track(order))

		# check between city : please
		if "check weather" in order:
			rep.append(self.weather(order))

		if "check time" in order:
			rep.append(self.clock())

		if "turn off" in order:
			rep.append(self.turn_off())

		if "check mail" in order:
			rep.append(self.check_mail())

		if "check calendar" in order:
			rep.append(self.check_calendar())
		return(rep)

	def clock(self):
		now = datetime.datetime.now()
		now_str = ('hour: ' + str(now.hour) + ' minute: ' + str(now.minute))
		return(now_str)

	def track(self, order):
		before = order.find('track')
		if "do not" in order[:before]:
			if self.previous_orders == 0:
				self.add_anger()
				return ('"But I am not tracking you, master"')
			else:
				self.previous_orders = 0
				self.add_please()
				if self.anger_meter > 7:
					return ('"NO!"')
				else :
					camera.set_tracking(0)
					return ('"As you wish sire, I will stop tracking your face"')
		else :
			if self.previous_orders == 1:
				self.add_anger()
				return('"I am already tracking you"')
			else:
				self.previous_orders = 1
				self.add_please()
				if self.anger_meter == 10:
					return ('"NO!"')
				else :
					camera.set_tracking(1)
					return('"Yes master, I will track you"')

	def weather(self, order):
		words = order.split(" ")
		try:
			city_index = words.index("in") + 1
		except ValueError:
			self.add_anger()
			print "Wrong syntax"
			return("No!")
		if words[city_index] == "city":
			city_index+=1
		if words[-1] == "please":
			city_arr = words[city_index:-1]
			self.add_please()
		else:
			city_arr = words[city_index:]
		city = " ".join(city_arr)
		loc_id = pywapi.get_location_ids(city)
		city_id = self.get_city_id(loc_id)
		try:
			self.add_please()
			all_info = pywapi.get_weather_from_weather_com( city_id , units = 'metric' )
			weather = all_info['current_conditions']['temperature'] 
			text = all_info['current_conditions']['text']
			weather_respone = ('It is ' + text + ', Temperature: ' + weather + ' celsius degrees in ' + city)
			return(weather_respone)
		except:
			e = sys.exc_info()[0]
			print "Error: %s" % e 
			print "Weather occurs some problems"
			return("NO!")

	def check_mail(self):
		obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
		print self.mail
		try:
			obj.login(self.mail,self.password)
		except:
			print "Wrong email"
			return ("No!")
		obj.select('INBOX')
		status, response = imap.search('INBOX', '(UNSEEN)')
		unread_messages = response[0].split()

		mails = []

		for email_id in unread_messages:
			_, response = imap.fetch(email_id, '(UID BODY[TEXT])')
			mails.append(response[0][1])

		return mails

	def check_calendar(self):
		credentials = get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('calendar', 'v3', http=http)

		now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
		print 'Getting the upcoming 10 events'
		eventsResult = service.events().list(
			calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
			orderBy='startTime').execute()
		events = eventsResult.get('items', [])

		result = []

		if not events:
			print 'No upcoming events found.'
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			result.append(start + event['summary'])
		return result

	def turn_off(self):
		return('"turning off"')
		#turn off

	def relation(self, order):
		end = order.find('love')
		if 'not' in order[:end]:
			if self.anger_meter > 7:
				return("hehehe")
			else:
				self.add_anger()
				return("I am sad")
		else:
			if self.anger_meter > 7:
				return("NO")
			else:
				self.add_please()
				return("I too love myself")

	def get_city_id(self, d):
		for key in d:
			return key

	def greet(self, order):
		return ('"Hello!"')

	def add_please(self):
		if self.anger_meter != 0:
			self.anger_meter -= 1

	def add_anger(self):
		if self.anger_meter != 10:
			self.anger_meter += 1

	def get_credentials(self):
		home_dir = os.path.expanduser('~')
		credential_dir = os.path.join(home_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		credential_path = os.path.join(credential_dir, 'calendar-quickstart.json')

		store = oauth2client.file.Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: 
				credentials = tools.run(flow, store)
		return credentials

