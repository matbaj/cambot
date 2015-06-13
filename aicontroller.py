import pywapi
import datetime

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

		if "check time" in order:
			rep.append(self.clock())

		if "turn off" in order:
			rep.append(self.turn_off())

		if "hide console" in order:
			rep.append(self.hide_console())

		if "show_console" in order:
			rep.append(self.show_console())

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
			add_anger()
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
			add_please()
			all_info = pywapi.get_weather_from_weather_com( city_id , units = 'metric' )
			weather = all_info['current_conditions']['temperature'] 
			weather_respone = ('Temperature: ' + weather + ' celsius degrees in ' + city)
			return(weather_respone)
		except:
			print "Weather occurs some problems"
			return("NO!")

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
				add_anger()
				return("I am sad")
		else:
			if self.anger_meter > 7:
				return("NO")
			else:
				add_please()
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
