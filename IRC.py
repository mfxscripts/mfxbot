#!/usr/bin/python
##

## Imports.
import socket
import ssl
import ConfigParser

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
    self.channel = c.get('IRC', 'channel'))
    self.botnick = c.get('IRC', 'botnick'))
    self.nickserv = c.get('IRC', 'nickserv'))

  def connect_to_irc(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    ircsock = ssl.wrap_socket(s)
    ircsock.send("USER "+ self.botnick +" "+ self.botnick + \
                 " "+ self.botnick +" :I am a bot.\n")
    ircsock.send("NICK "+ botnick +"\n")

## Functions

## EOF.
