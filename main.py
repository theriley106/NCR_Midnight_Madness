from datetime import *
import json
import threading
import time
from operator import itemgetter
openTimes = [["11-23"]] * 4 + [["11-24"], ["0-2", "11-24"], ["0-2", "11-21"]]

def convert_time(timeString):
	try:
		return datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S%fZ")
	except:
		timeString = timeString[:-1] + "0Z"
		return datetime.strptime(timeString, "%Y-%m-%dT%H:%M:%S%fZ")



def is_valid(array_of_orders):
	order_status = []
	for val in array_of_orders:
		pass

def is_open(datetimeVal):
	for val in openTimes[datetimeVal.weekday()]:
		if datetimeVal.hour in range(*[int(x) for x in val.split("-")]):
			return True
	return False

class Kitchen(object):
	def __init__(self):
		self.returnVal = []
		self.current_time = None
		self.active = 0
		self.orders = []
		self.pending_orders = []

	def is_valid_order(self, order, order_day):
		if order['numberOfBurgers'] + self.active <= 50:
			return True
		return False

	def update_orders(self, timeVal):
		self.active = 0
		for val in self.pending_orders:
			if timeVal >= val['start']:
				g = val
				self.pending_orders.remove(val)
				self.orders.append(g)
		for val in self.orders:
			if timeVal < val['pickup']:
				self.active -= val['orders']
				self.orders.remove(val)
			else:
				self.active += val['orders']
		print self.active


	def add_burger(self, order):
		self.update_orders(order['dateTime'])
		order_time = order['dateTime']
		order_day = order_time.strftime("%Y-%m-%d")
		if (self.is_valid_order(order, order_day) and is_open(order_time)) == False:
			self.returnVal.append({"orderId": order['orderId'], "wasAccepted": "false"})
		else:
			# This means it's an actual order
			if self.current_time == None:
				self.current_time = order['dateTime']
			if self.current_time < order['dateTime']:
				self.current_time = order['dateTime']
			self.pending_orders.append({"start": order['dateTime'] + timedelta(minutes=order['preparationLength']), "pickup": convert_time(order['pickUpTime']), "orders": order['numberOfBurgers']})
			self.returnVal.append({"orderId": order['orderId'], "wasAccepted": "true"})

if __name__ == '__main__':
	start = time.time()
	e = Kitchen()
	a = json.load(open("data.json"))
	for val in a:
		val['dateTime'] = convert_time(val['timeSubmitted'])
	a = sorted(a, key=itemgetter("dateTime"), reverse=False)
	for val in a:
		e.add_burger(val)
	print e.active
	for val in e.returnVal:
		print val
	end = time.time()
	print(end - start)
