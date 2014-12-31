#!/usr/bin/env python

# Import some necessary libraries.
import socket, ssl, sys

# Some basic variables used to configure the bot        
server  = 'irc.rizon.net'
port    = 9999
channel = '#home-boyz'
botnick = 'EvilDroid'

def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :pingis\n")  

def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n") 

def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")

def hello(): # This function responds to a user that inputs "Hello Mybot"
  ircsock.send("PRIVMSG "+ channel +" :Hello!\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port)) # Here we connect to the server
ircsock = ssl.wrap_socket(s)
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :I am a bot.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined

while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  print(ircmsg) # Here we print what's coming from the server

  if ircmsg.find(":Hello "+ botnick) != -1: # If we can find "Hello Mybot" it will call the function hello()
    hello()

  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()

## EOF
sys.exit(0)