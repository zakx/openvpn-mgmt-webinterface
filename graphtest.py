#!/usr/bin/env python
# coding=utf-8
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import connection
#from django.contrib.auth.models import User
from purple.app.models import *

import os
import sys
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

tn = TrafficNode.objects.filter(user=User.objects.get(), connection__pk=12)
hurr = []
durr = []
for node in tn:
	hurr.append(float(node.traffic_sent_since)/1024/1024)
	durr.append(float(node.traffic_recv_since)/1024/1024)

plt.plot(hurr)
plt.plot(durr)
plt.ylabel('some numbers')

plt.savefig('hurr.png')
