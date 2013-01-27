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
import mgmtlib


tn = mgmtlib.connect()
status = mgmtlib.get_status(tn)
mgmtlib.quit(tn)
status = mgmtlib.parse_status(status)
print status['users']

for u in status['users']:
	if u[0] == "UNDEF":
		continue # not yet connected
	try:
		user = User.objects.get(username=u[0])
	except User.DoesNotExist:
		print "user does not exist"
		continue
	try:
		c = Connection.objects.get(user=user, time_end=None)
	except Connection.DoesNotExist:
		print "missing a waiting connection"
		continue

	c.vpn_ip = u[2]
	c.traffic_recv = u[3]
	c.traffic_sent = u[4]
	try:
		c.save()
		print "done with user %s" % user.username
	except:
		print "couldn't save connection"
		continue
	
	try:
		tn = TrafficNode.objects.filter(user=user, connection=c).order_by('-time')[:1]
		tn = tn[0]
		print "got trafficnode object %s (%d)" % (tn.time, tn.pk)
		old_sent = tn.traffic_sent_total
		old_recv = tn.traffic_recv_total
	except:
		old_sent = 0
		old_recv = 0
	
	try:
		new_tn = TrafficNode(user=user, connection=c, time=datetime.datetime.now(), traffic_sent_since=(int(c.traffic_sent)-old_sent), traffic_recv_since=(int(c.traffic_recv)-old_recv), traffic_sent_total=int(c.traffic_sent), traffic_recv_total=int(c.traffic_recv))
		new_tn.save()
	except Exception, e:
		print "failed to save new tn: %s" % e
	
	# check bandwidth limits
	if user.get_profile().used_traffic > user.get_profile().max_traffic and user.get_profile().max_traffic > -1:
		# gotcha!
		tn = mgmtlib.connect()
		mgmtlib.send(tn, "kill %s" % u[0])
		mgmtlib.quit(tn)
		print "killed user %s for bandwidth usage" % user
