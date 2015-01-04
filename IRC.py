#!/usr/bin/python
##

## Imports.
import socket
import ssl
import ConfigParser
import Queue
import threading
import re
import time

## Vars.
config_file = '/home/p/etc/bot.conf'

## Classes.
#class AuthError( Exception ): pass

class Session:
  ' session to IRC using ssl '

  def __init__(self):
    # Read values from config file.
    c = ConfigParser.ConfigParser()
    c.read(config_file)
    self.server = c.get('IRC', 'server')
    self.port = int(c.get('IRC', 'port'))
    self.channel = c.get('IRC', 'channel')
    self.botnick = c.get('IRC', 'botnick')
    self.nickserv = c.get('IRC', 'nickserv')
    # Open a socket
    self.ircsock = self.connect_to_irc()
    # Start a background process to watch IRC messages
    self.queue = Queue.Queue()
    watcher = threading.Thread(target=self.watch_irc)
    watcher.deamon = True
    watcher.start()

  def connect_to_irc(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((self.server, self.port))
    ircsock = ssl.wrap_socket(s)
    ircsock.send("USER ev ev ev" + \
                 " :I am a bot.\n")
    ircsock.send("NICK "+ self.botnick +"\n")
    return ircsock

  def watch_irc(self):
    # Lets get data from IRC server
    while True:
      ircmsg = self.ircsock.recv(2048)
      ircmsg = ircmsg.strip('\n\r')
      #if ircmsg.find("PING :") != -1:
      if re.search(r'^PING :', ircmsg):
        # We handle PING replies here automatically
        self.pong()
      else:
        # Everything else we put in the queue
        self.queue.put(ircmsg)

  def join_channel(self,channel):
    self.ircsock.send("JOIN "+ channel +"\n")

  def pong(self):
    self.ircsock.send("PONG :pingis\n")

  def identify_nickserv(self):
    self.ircsock.send("PRIVMSG NickServ : IDENTIFY " + self.nickserv + "\n")

  def sendmsg(self,channel,msg):
    self.ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n")

  def quit(self,msg):
    self.ircsock.send("QUIT :"+ msg + "\n")
    time.sleep(1) # Deal with lag
    self.ircsock.close()

## Functions

## EOF.
