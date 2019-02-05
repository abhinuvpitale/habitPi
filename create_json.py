#!/usr/bin/python

import json

habits = {}
habits["Exercise"] = [15,'X-XX---']
habits["Content"] = [7,'X------']
json_dumps = json.dumps(habits)

obj = open("habits.json",'w+')
obj.write(json_dumps)
obj.close()
