from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import Http404, HttpResponseServerError, HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.urlresolvers import reverse
import datetime
import os
import socket
from app.models import *
import mgmtlib

@login_required
def welcome_view(request):
	used = float(request.user.get_profile().used_traffic)/1024/1024
	if request.user.get_profile().max_traffic == -1:
		quota = "unlimited"
		used_percentage = False
	else:
		quota = float(request.user.get_profile().max_traffic)/1024/1024
		if quota == 0:
			used_percentage = 0
		else:
			used_percentage = round(used/quota*100)
	connection_count = Connection.objects.filter(user=request.user).count()
	return render_to_response("welcome.html", locals(), context_instance=RequestContext(request))

@login_required
def status_view(request):
	if not request.user.is_staff:
		raise Http404()
	mgmt = mgmtlib.OpenVPNManager()
	mgmt.connect()
	status = mgmt.get_status()
	mgmt.quit()
	users = status['users']
	sessions = Connection.objects.filter(time_end=None)
	userlist = User.objects.all()
	return render_to_response("status.html", locals(), context_instance=RequestContext(request))

def kill_action(request):
	pass

def ban_action(request):
	pass
