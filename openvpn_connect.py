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


def report(error):
        f = open("/tmp/log", "a")
        f.write("%s\n" % error)
	print error
        f.close()
env_certuser = os.environ.get("common_name")
env_user = os.environ.get("username")
if not env_user:
	env_user = env_certuser
env_remote_ip = os.environ.get("trusted_ip")
env_vpn_ip = os.environ.get("ifconfig_pool_remote_ip")
try:
	user = User.objects.get(username=env_user)
except User.DoesNotExist:
	report("user does not exist: %s" % env_user)
	sys.exit(1)
try:
	c = Connection.objects.filter(user=user, remote_ip=env_remote_ip, vpn_ip=None)[0]
except Connection.DoesNotExist:
	report("missing a waiting connection: %s" % user)
	sys.exit(1)
c.vpn_ip = env_vpn_ip
try:
	c.save()
except:
	report("couldn't save connection: %s" % user)
	c.delete()
	sys.exit(1)
try:
	tn = TrafficNode(user=user, connection=c, time=datetime.datetime.now())
	tn.save()
except Exception, e:
	report("tn failed: %s (for %s)" % (e, user))

report("user may connect: %s" % user)
