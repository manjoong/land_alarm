# -*- coding: utf-8 -*-
import threading
import time
import datetime
import requests
import json
import logging


with open('./station.json') as json_file:
    data = json.load(json_file)

result=data["subways"]["subway"]



print(len(result))
print(json.dumps(result, indent = 1, ensure_ascii = False)) 