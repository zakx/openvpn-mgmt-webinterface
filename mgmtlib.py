import sys
import telnetlib
import socket
import settings

class ConnectionError(Exception):
	pass

class OpenVPNManager():
	connection = False
	logged_in = False

	def connection_required(func):
		def wrapped():
			if self.connection and self.logged_in:
				return func()
			else:
				return
		return wrapped

	def __init__(self):
		self.connection = False
		self.logged_in = False

	def _connect(self):
		try:
			self.connection = telnetlib.Telnet("localhost", 7505, timeout=3)
		except socket.error, socket.timeout:
			self.connection = False
			raise ConnectionError("Cannot connect to OpenVPN management console.")

	def _login(self, password):
		if not self.connection:
			raise ConnectionError("Tried to login without connection.")
		if self.logged_in:
			return
		prompt = self.connection.read_until("ENTER PASSWORD:", timeout=5)
		if not prompt:
			self.quit()
			raise ConnectionError("Login to OpenVPN management console timed out.")
		self.connection.write(password+"\n")
		try:
			result = self.connection.read_some()
		except socket.timeout:
			self.quit()
			raise ConnectionError("Login to OpenVPN management console timed out.")
		if result[:7] != "SUCCESS":
			self.quit()
			raise ConnectionError("Login to OpenVPN management console failed. Check OPENVPN_PASSWORD.")
		self.connection.read_until("info\r\n", 3)
		self.logged_in = True

	def connect(self, password=settings.OPENVPN_PASSWORD):
		if self.connection or self.logged_in:
			return
		self._connect()
		self._login(password=password)
		return self.logged_in

	@connection_required
	def get_status(self):
		self.send("status 2")
		status = self.connection.read_until("END", 2)
		return status

	@connection_required
	def send(self, command):
		self.connection.write("%s\n" % command)

	def quit(self):
		if not self.connection:
			return
		self.connection.write("quit\n")
		self.connection.close()
		self.connection = False
		self.logged_in = False

	@connection_required
	def parse_status(self, status):
		stati = status.split("\r\n")
		users = []
		routes = []
		for i,line in enumerate(stati[3:]):
			if line[:6] == "HEADER":
				break
			users.append(line.split(",")[1:])
		for j,line in enumerate(stati[(4+i):]):
			if line[:6] == "GLOBAL":
				break
			routes.append(line.split(",")[1:])
		return {'users': users, 'routes': routes}
