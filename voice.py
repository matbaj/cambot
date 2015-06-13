import pywapi
import subprocess
import string

class AIController:

	def __init__(self):
		self.previous_orders = 0
		self.anger_meter = 0


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

		if "turn off" in order:
			rep.append(self.turn_off())

		if "hide console" in order:
			rep.append(self.hide_console())

		if "show_console" in order:
			rep.append(self.show_console())

		return(rep)

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
					return ('"As you wish sire, I will stop tracking your face"')
					#here we stop tracking
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
					return('"Yes master, I will track you"')
					#we begin tracking

	def weather(self, order):
		words = order.split(" ")
		city_index = words.index("in") + 1
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
		all_info = pywapi.get_weather_from_weather_com( city_id , units = 'metric' )
		weather = all_info['current_conditions']['temperature'] 
		weather_respone = ('Temperature: ' + weather + ' celsius degrees in ' + city)
   		return(weather_respone)

	def turn_off(self):
		return('"turning off"')
    	#turn off

	def show_console(self):
    	#we show console here
		return('"I will now show you console"')

	def hide_console(self):
    	#we hide console
		return('"I will now hide console"')

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
		return ('"Hello!"')

	def add_please(self):
		if self.anger_meter != 0:
			self.anger_meter -= 1

	def add_anger(self):
		if self.anger_meter != 10:
			self.anger_meter += 1

class VoiceResponse:
	def say(self, text):
		subprocess.call("espeak \"%s\"" %(text), shell=True)



