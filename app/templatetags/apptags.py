from django import template
import socket

register = template.Library()

@register.filter(name='rdns')
def rdns(value):
	try:
		hostname = socket.gethostbyaddr(value)[0]
	except:
		return "" # fail silently
	return hostname