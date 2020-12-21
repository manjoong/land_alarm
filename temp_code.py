# -*- coding: utf-8 -*-
import threading
import time
import requests
import json
import logging
import sys
from fake_useragent import UserAgent
from datetime import datetime
# from django.utils import timezone
from pytz import common_timezones, timezone


def check_connection_permit(que_file):
    f = open(str(que_file),'r')
    line = f.readlines()
    f.close()
    if len(line) != 0:
        last_line = line[-1]
        if last_line[-1] == '\n':
            last_line = last_line[:-1]
        print("맨마지막 열은")
        print(str(last_line))
	print("맨 마지막 열의 맨 마지막 원소는")
        print(last_line[-1])
        print("비교 할 코드는")
        print(str(str(sys.argv[1])+"_"+str(sys.argv[2])))
        if str(last_line) == str(str(sys.argv[1])+"_"+str(sys.argv[2])):
            print("같습니다")
            return True

check_connection_permit("/root/que.txt")
