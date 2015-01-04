#!/usr/bin/python

## Imports
import Shivtr
import BotActions
import sys
import Queue
import threading
import time
import re
import zmq
import json

## Vars
shout_refresh = 5 # Secs before we check for new shouts

## Functions
def watch_shouts(q, s):
  # Let's get the last shout first. We'll only deal with shouts newer than this one. 
  last_shout = s.get_last_shoutid()
  while True:
    time.sleep(shout_refresh)
    new_shouts = s.get_new_shouts()
    #print new_shouts
    # Add them to our queue (if any)
    for i in new_shouts:
      q.put(i)

def handle_shouts(q, s):
  # We get new shouts and Deal With Them.
  while True:
    # Let's see if we have any work to be done.
    new_shout = q.get()
    msg = new_shout[1]
    #author = Shivtr.get_nickname(new_shout[2])
    author = new_shout[3]
    # Anything for us?
    #if re.search(r'^mfxbot[,: ]', msg, re.IGNORECASE):
    #  question = re.sub(r'^[Mm][Ff][Xx][Bb][Oo][Tt][,: ]', '', msg)
    #  BotActions.find_answer(s, question)
    #  #s.post_shout('ok :D')

    #if re.search(r'^[%/]quote$', msg):
    #  BotActions.tell_quote(s)
    #if re.search(r'^[%/]cookie$', msg):
    #  BotActions.tell_fortune(s)
    if re.search(r'^[%/](fokmenol|rpmemory|reminiscence)$', msg):
      BotActions.rpg_quote(s)
    elif re.search(r'^[%/]drwho$', msg):
      BotActions.drwho_quote(s)
    elif re.search(r'[%/][dD]20$', msg):
      BotActions.roll_d20(s,author)
    elif re.search(r'[%/]status$', msg):
      BotActions.status(s)
    elif re.search(r'[%/]help$', msg):
      BotActions.help(s)
    elif re.search(r'tette', msg, re.IGNORECASE):
      BotActions.tetten(s)
    else:
      # Post on IRC
      shoutbox_client(new_shout)

    # This one is done, Sir.
    q.task_done()

def shoutbox_client(shout):
  # Connect to ircbot which is listening for messages
  context = zmq.Context()
  socket = context.socket(zmq.REQ)
  # todo: add exception
  socket.connect('tcp://127.0.0.1:6000')
  socket.send(json.dumps(shout).encode('utf-8'))
  socket.close()

## Main program

# Let's start up a session
s = Shivtr.Session()

# Now we spawn a thread which will watch the shoutbox,
# looking for new shouts with ids > last_shout.
# These new shouts will be put in a queue where we can
# handle them with multiple worker threads.
q = Queue.Queue()
watcher = threading.Thread(target=watch_shouts, args=(q,s))
watcher.deamon = True
watcher.start()

# Spawn our worker threads.
for _ in range(5):
  worker = threading.Thread(target=handle_shouts, args=(q,s))
  worker.daemon = True
  worker.start()

# Block until tasks are done (only when we kill the bot)
q.join()

## EOF
sys.exit(0)
