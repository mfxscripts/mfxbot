#!/usr/bin/python

## Imports
import sys
import IRC
import time
import Queue
import threading
import re
import NMBS
import zmq
import json

## Vars
version = '0.03'

## Functions
def shoutbox_server(irc,tcp_port):
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind('tcp://127.0.0.1:' + tcp_port)
  while True:
    shout = socket.recv()
    if shout:
      j = json.loads(shout)
      author = j[3].encode('utf-8')
      msg = j[1].encode('utf-8')
      irc.sendmsg(irc.channel, '[MFX] <' + author + '> ' + msg)
      socket.send('OK')

def parse_irc_msgs(irc):
  while True:
    msg = irc.queue.get()
    #print msg
    if re.search(':Hello '+ irc.botnick, msg):
      irc.sendmsg(irc.channel, 'Hello!')

    # Check NMBS info
    m = re.search(r':.nmbs ([a-zA-Z\-]+) ([a-zA-Z\-]+)', msg)
    if m:
      nmbs_info = NMBS.get_next_trains(m.group(1), m.group(2))
      if len(nmbs_info) > 0:
        r = nmbs_info.split('\n')
        irc.sendmsg(irc.channel, '[NMBS] ' + ' | '.join(r))
      else:
        irc.sendmsg(irc.channel, '[NMBS] No results found.')

    # The work is done, Master.
    irc.queue.task_done()

## Main program

# Connect to IRC
irc = IRC.Session()

# Wait 2 secs and identify
time.sleep(2)
irc.identify_nickserv()
time.sleep(1)

# Join default channel
irc.join_channel(irc.channel)

# Say something in default channel
#irc.sendmsg(irc.channel, 'EvilDroid version ' + version + ' now operational.')
#irc.sendmsg(irc.channel, 'Greetings, earthlings.') 

# Now start workers
for _ in range(5):
  worker = threading.Thread(target=parse_irc_msgs, args=(irc,))
  worker.daemon = True
  worker.start()

# We also need a socket to send shoutbox messages to
tcp_port = '6000'
worker = threading.Thread(target=shoutbox_server, args=(irc,tcp_port))
worker.daemon = True
worker.start()

# Block until all tasks are done (never)
irc.queue.join()

## EOF
sys.exit(0)
