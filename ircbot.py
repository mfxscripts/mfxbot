#!/usr/bin/python

## Imports
import sys
import IRC
import time
import Queue
import threading
import re

## Vars
version = '0.02a'

## Functions

## Main program
def parse_irc_msgs(irc):
  while True:
    msg = irc.queue.get()
    #print msg
    if re.search(':Hello '+ irc.botnick, msg):
      irc.sendmsg(irc.channel, 'Hello!')
    # ..
    irc.queue.task_done()

# Connect to IRC
irc = IRC.Session()

# Join default channel
irc.join_channel(irc.channel)

# Say something in default channel
irc.sendmsg(irc.channel, 'EvilDroid version ' + version + ' now operational.')
irc.sendmsg(irc.channel, 'Greetings, earthlings.') 

# Now start workers
for _ in range(5):
  worker = threading.Thread(target=parse_irc_msgs, args=(irc,))
  worker.daemon = True
  worker.start()

# Block until all tasks are done (never)
irc.queue.join()

## EOF
sys.exit(0)
