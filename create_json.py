#!/usr/bin/python

import json

habits = {}
habits["Exercise"] = 7
habits["Content"] = 15
json_dumps = json.dumps(habits)

obj = open("habits.json",'w+')
obj.write(json_dumps)
obj.close()
