import xbmc
import xbmcaddon
import json
from backports import ssl_match_hostname
import websocket
import time
import socket, os, sys
 
__addon__       = xbmcaddon.Addon(id='script.pushbullet')
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')

title = "PushBullet"
time = 5000  # ms

settings = xbmcaddon.Addon( id="script.pushbullet" )
userapikey = settings.getSetting("apikey")

def on_message(ws, message):
    data = json.loads(message)
    if data["type"] == "push":
	  xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(data["push"]["title"], data["push"]["body"], time, __icon__))

def on_error(ws, error):
	print error

def on_close(ws):
	print "### closed ###"

def on_open(ws):
	xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(title, "Websocket Open", time, __icon__))

if __name__ == "__main__":
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp("wss://stream.pushbullet.com/websocket/"+userapikey,
							  on_message = on_message,
							  on_error = on_error,
							  on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()