import sys
import telnetlib
import settings

def connect():
	tn = telnetlib.Telnet("localhost", 7505, 3)
	print "hello there"
	tn.read_until("ENTER PASSWORD:")
	tn.write(settings.OPENVPN_PASSWORD+"\n") # YAY HARDCODED PASSWORDS
	print "login sent"
	hurr = tn.read_some()
	print "result there"
	if hurr[:7] != "SUCCESS":
		raise Exception("login failed")
	print "Login ok"
	tn.read_until("info\r\n", 3)
	return tn

def get_status(tn):
	tn.write("status 2\n")
	status = tn.read_until("END", 2)
	return status

def send(tn, command):
	tn.write("%s\n" % command)

def quit(tn):
	tn.write("quit\n")
	print "done"
	tn.close() # free it

def parse_status(status):
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
