#!/usr/bin/env python
# coding=utf-8
from django.core.management import setup_environ
import settings
setup_environ(settings)

from django.db import connection
from purple.app.models import *
from django.contrib.auth import authenticate

import os
import sys
import datetime

import mgmtlib

env_certuser = os.environ.get("common_name")
env_remote_ip = os.environ.get("untrusted_ip")

def report(error):
	f = open("/tmp/log", "a")
	f.write("%s\n" % error)
	f.close()
	#sys.exit(1)

f = open(sys.argv[1], "r")
challenge_user = f.readline().rstrip()
challenge_pass = f.readline().rstrip()
f.close()

user = authenticate(username=challenge_user, password=challenge_pass)
if user is None:
	report("login failed")
	sys.exit(1)

if not user.get_profile().may_connect:
	report("user may not connect")
	sys.exit(1)

# TODO right here: check for open existing connections and kill+finish them
try:
	c = Connection.objects.filter(user=user, time_end=None)
	for conn in c:
		try:
			report("finishing conn")
			conn.time_end = datetime.datetime.now()
			conn.save()
		except:
			pass
#	try:
#		report("killing connections")
		#tn = mgmtlib.connect()
		#mgmtlib.send(tn, "kill %s" % user.username)
		#mgmtlib.quit(tn)
		#sys.exit(1)
#	except Exception, e:
#		report("failed: %s" % e)
#	finally:
#		try:
#			mgmtlib.quit(tn)
#		except:
#			pass
except Connection.DoesNotExist:
	report("no abandoned connections")
	pass # this is a good thing

try:
	c = Connection(user=user, time_start=datetime.datetime.now(), remote_ip=env_remote_ip)
	c.save()
except Exception, e:
	report("connection could not be saved: %s" % e)
	sys.exit(1)

report("connection granted")
