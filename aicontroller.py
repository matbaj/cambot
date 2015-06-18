import pywapi
import sys
import datetime
import imaplib

import httplib2
import os
import code
from googleapiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import dateutil.parser
import re
try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'cambot'


class AIController:

	def __init__(self):
		self.previous_orders = 1
		self.anger_meter = 0

	def act(self, order):
		rep = []
		if "love you" in order:
			rep.append(self.relation(order))

		elif "hello" in order: 
			rep.append(self.greet(order))

		# check if there is do not before track 
		elif "track faces" in order :
			rep.append(self.track(order))

		# check between city : please
		elif "check weather" in order:
			rep.append(self.weather(order))

		elif "check time" in order:
			rep.append(self.clock())

		elif "turn off" in order:
			rep.append(self.turn_off())

		elif "check mail" in order:
			rep.append(self.check_mail())

		elif "check calendar" in order:
			rep.append(self.check_calendar())

		else:
			self.add_anger()
			camera.show_no()


		return(rep)

	def clock(self):
		now = datetime.datetime.now()
		now_str = ('hour: ' + str(now.hour) + ' minute: ' + str(now.minute))
		return(now_str)

	def track(self, order):
		before = order.find('track')
		if "do not" in order[:before]:
			if camera.face_tracking == 0:
				self.add_anger()
				return ('But I am not tracking you, master')
			else:
				camera.face_tracking = 0
				self.add_please()
				if self.anger_meter > 7:
					return ('NO!')
				else :
					camera.set_tracking(0)
					return ('As you wish sire, I will stop tracking your face')
		else :
			if camera.face_tracking == 1:
				self.add_anger()
				return('I am already tracking you')
			else:
				camera.face_tracking = 1
				self.add_please()
				if self.anger_meter == 10:
					return ('NO!')
				else :
					camera.set_tracking(1)
					return('Yes master, I will track you')

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
			weather_respone = ('It is ' + text + ', Temperature: ' + weather  + ' celsius degrees in ' + city)
			return(weather_respone)
		except:
			e = sys.exc_info()[0]
			print "Error: %s" % e 
			print "Weather occurs some problems"
			return("NO!")

	def check_mail(self):
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('gmail', 'v1', http=http)
		response =  service.users().messages().list(userId="me",maxResults=5,q="is:unread").execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])
		if (len(messages)) > 1 :
			result = "You have %d unreaded messages " % (len(messages))
		else :
			result = "You have %d unreaded message " % (len(messages))
		result_arr = []
		for m in messages:
			msg_txt= self.mail_get_detail(service, m.get('id')) 
			result_arr.append(msg_txt)
		return result+" ".join(result_arr)

	def mail_get_detail(self,service,msg_id):
		message = service.users().messages().get(userId='me', id=msg_id,format='raw').execute()
		snippet = message['snippet']
		p = re.compile(ur'\ \&lt;.*\&gt;')
		result =   re.sub(p,'',snippet)
		return result
			

	def check_calendar(self):
		credentials = self.get_credentials()
		http = credentials.authorize(httplib2.Http())
		service = discovery.build('calendar', 'v3', http=http)

		now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
		print 'Getting the upcoming 10 events'
		eventsResult = service.events().list(
			calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
			orderBy='startTime').execute()
		events = eventsResult.get('items', [])
		if not events:
			return 'You have no upcoming events.'
		result = []
				
		for event in events:
			start = event['start'].get('dateTime', event['start'].get('date'))
			dt = dateutil.parser.parse(start)
			dt_text =  dt.strftime('%A, %d %b %Y %l:%M %p')
			event_text = "%s at %s " % (event['summary'], dt_text)
			result.append(event_text)
		if (len(result)) > 1 :
			return "You have " + " - and after that ".join(result)
		return "You have " + result[0]


	def relation(self, order):
		end = order.find('love')
		if 'not' in order[:end]:
			if self.anger_meter > 7:
				return("So what?!")
			else:
				self.add_anger()
				return("You make me sad.")
		else:
			if self.anger_meter > 7:
				return("NO!")
			else:
				self.add_please()
				return("I too love myself.")

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
		credential_path = os.path.join(credential_dir, 'cambot-gapi.json')

		store = Storage(credential_path)
		credentials = store.get()
		if not credentials or credentials.invalid:
			flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
			flow.user_agent = APPLICATION_NAME
			if flags:
				credentials = tools.run_flow(flow, store, flags)
			else: 
				credentials = tools.run(flow, store)
		return credentials

