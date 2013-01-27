#!/usr/bin/env python
# coding=utf-8
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import connection
from app.models import *

import os
import sys
import datetime

env_certuser = os.environ.get("common_name")
env_user = os.environ.get("username")
if not env_user:
	env_user = env_certuser
env_remote_ip = os.environ.get("trusted_ip")
env_vpn_ip = os.environ.get("ifconfig_pool_remote_ip")
env_traffic_recv = os.environ.get("bytes_received")
env_traffic_sent = os.environ.get("bytes_sent")

try:
	user = User.objects.get(username=env_user)
except User.DoesNotExist:
	print "user does not exist"
	sys.exit(1)

try:
	c = Connection.objects.get(user=user, remote_ip=env_remote_ip, vpn_ip=env_vpn_ip, time_end=None)
except Connection.DoesNotExist:
	print "missing a waiting connection"
	sys.exit(1)

c.time_end = datetime.datetime.now()
c.traffic_recv = env_traffic_recv
c.traffic_sent = env_traffic_sent
try:
	c.save()
except:
	print "couldn't save connection"
	#c.delete()
	sys.exit(1)
