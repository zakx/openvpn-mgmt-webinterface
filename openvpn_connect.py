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

env_certuser = os.environ.get("common_name")
env_user = os.environ.get("username")
if not env_user:
	env_user = env_certuser
env_remote_ip = os.environ.get("trusted_ip")
env_vpn_ip = os.environ.get("ifconfig_pool_remote_ip")

try:
	user = User.objects.get(username=env_user)
except User.DoesNotExist:
	print "user does not exist"
	sys.exit(1)

try:
	c = Connection.objects.get(user=user, remote_ip=env_remote_ip, vpn_ip=None)
except Connection.DoesNotExist:
	print "missing a waiting connection"
	sys.exit(1)

c.vpn_ip = env_vpn_ip
try:
	c.save()
except:
	print "couldn't save connection"
	c.delete()
	sys.exit(1)

try:
	tn = TrafficNode(user=user, connection=c, time=datetime.datetime.now())
	tn.save()
except Exception, e:
	print "tn failed: %s" % e

print "user may connect"
