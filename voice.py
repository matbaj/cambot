import pywapi
import subprocess
import string

class AIController:

	def __init__(self, previous_orders, anger_meter):
		self.previous_orders = previous_orders
		self.anger_meter = anger_meter


	def act(self, order):
                rep = []
		if "love you" in order:
			rep.append(self.relation(order))

		if "hello" in order: 
			self.greet(order)

		# check if there is do not before track 
		if "track faces" in order :
			self.track(order)

		# check between city : please
		if "check weather" in order:
			self.weather(order)

		if "turn off" in order:
			self.turn_off()

		if "hide console" in order:
			self.hide_console()

		if "show_console" in order:
			self.show_console()

                return(rep)

	def track(self, order):
		before = order.find('track')
		if "do not" in order[:before]:
			if self.previous_orders == 0:
				self.call ('"But I am not tracking you, master"')
				if self.anger_meter != 10:
					self.anger_meter += 1
			else:
				if self.anger_meter == 10:
					self.call ('"NO!"')
				else :
					self.call ('"As you wish sire, I will stop tracking your face"')
					#here we stop tracking
				self.previous_orders = 0
				if self.anger_meter != 0:
					self.anger_meter -= 1
		else :
			if self.previous_orders == 1:
				self.call('"I am already tracking you"')
				if self.anger_meter != 10:
					self.anger_meter += 1
			else:
				if self.anger_meter == 10:
					self.call ('"NO!"')
				else :
					self.call('"Yes master, I will track you"')
					#we begin tracking
				self.previous_orders = 1
				if self.anger_meter != 0:
					self.anger_meter -= 1

	def weather(self, order):
		start = order.find('city') + 5
		end = order.find('please', start)
		city = order[start:end]
		loc_id = pywapi.get_location_ids(city)
		city_id = self.get_city_id(loc_id)
		all_info = pywapi.get_weather_from_weather_com( city_id , units = 'metric' )
		weather = all_info['current_conditions']['temperature'] 
   		self.call('Temperature:')
		self.call(weather)
		self.call('"celsius degrees in"')
		self.call(city)

	def turn_off(self):
		self.call('"turning off"')
    	#turn off

	def show_console(self):
    	#we show console here
		self.call('"I will now show you console"')

	def hide_console(self):
    	#we hide console
		self.call('"I will now hide console"')

	def relation(self, order):
		end = order.find('love')
		if 'not' in order[:end]:
			if self.anger_meter > 7:
				return("hehehe")
			else:
				return("I am sad")
		else:
			if self.anger_meter > 7:
				return("NO")
			else:
				return("I too love myself")

	def get_city_id(self, d):
		for key in d:
			return key

	def greet(self, order):
		self.call ('"Hello!"')

class VoiceResponse:
	def call(self, text):
		subprocess.call('espeak '+text, shell=True)


#resp = response(0,0)
	
#resp.act("check weather in city Wroclaw")

