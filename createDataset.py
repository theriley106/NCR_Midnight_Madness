import json



all_vals = open("all_data.txt").read().split("\n")


all_dicts = []

info = {}

print all_vals

while len(all_vals) > 0:
	try:
		if str(all_vals[0]) == '':
			all_dicts.append(info)
			info = {}
			if len(all_vals) > 0:
				all_vals.pop(0)
			else:
				break
		info['orderId'] = all_vals.pop(0)
		info['timeSubmitted'] = all_vals.pop(0)
		info['pickUpTime'] = all_vals.pop(0)
		info['numberOfBurgers'] = all_vals.pop(0)
		info['preparationLength'] = all_vals.pop(0)
	except:
		pass

with open('data.json', 'w') as outfile:
    json.dump(all_dicts, outfile)
