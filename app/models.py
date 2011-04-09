from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q, Count, Sum

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	banned = models.BooleanField(default=False)
	max_traffic = models.BigIntegerField(default=0)
	#used_traffic_sent = models.BigIntegerField(default=0)
	#used_traffic_recv = models.BigIntegerField(default=0)

	@property
	def used_traffic_sent(self):
		try:
			return Connection.objects.filter(user=self).aggregate(traffic_sent=Sum("traffic_sent"))["traffic_sent"]
		except:
			return -1
	
	@property
	def used_traffic_recv(self):
		try:
			return Connection.objects.filter(user=self).aggregate(traffic_recv=Sum("traffic_recv"))["traffic_recv"]
		except:
			return -1

	@property
	def used_traffic(self):
		try:
			return (self.used_traffic_sent + self.used_traffic_recv)
		except:
			return -1

	@property
	def may_connect(self):
		if self.banned or not self.user.is_active:
			return False
		if self.used_traffic > self.max_traffic and self.max_traffic > -1:
			self.user.email_user("VPN connection denied", "Hey,\n\nyou just tried to connect to zVPN. Sadly, you exceeded your traffic allowance. Try talking to Sven.", "'zVPN' <no-reply@vpn.zakx.de>")
			return False
		return True
	
	@property
	def session(self):
		try:
			session = Connection.objects.get(user=self.user, time_end=None)
			return session
		except Connection.DoesNotExist:
			return False
	
	def __unicode__(self):
		return "%s (%.2fM/%sM)" % (self.user.username, float(self.used_traffic)/1024/1024, self.max_traffic/1024/1024)

class Connection(models.Model):
	user = models.ForeignKey(User)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField(null=True, blank=True)
	traffic_sent = models.BigIntegerField(default=0)
	traffic_recv = models.BigIntegerField(default=0)
	remote_ip = models.IPAddressField()
	vpn_ip = models.IPAddressField(null=True, blank=True)

	@property
	def is_connected(self):
		if self.time_end:
			return False
		else:
			return True

#	def finish(self):
#		super(Connection, self).save()
#		self.user.get_profile().used_traffic_

class TrafficNode(models.Model):
	user = models.ForeignKey(User)
	connection = models.ForeignKey(Connection)
	time = models.DateTimeField()
	traffic_sent_since = models.BigIntegerField(default=0)
	traffic_recv_since = models.BigIntegerField(default=0)
	traffic_sent_total = models.BigIntegerField(default=0)
	traffic_recv_total = models.BigIntegerField(default=0)

