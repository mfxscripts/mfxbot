#!/usr/bin/python

import Shivtr
import time

s = Shivtr.Session()
#print s.get_last_shoutid()
#print s.db_get_last_shoutid()
last_shout = s.get_last_shoutid()

while True:
  time.sleep(5)
  new_shouts = s.get_new_shouts(last_shout)
  print len(new_shouts)
  if len(new_shouts) == 20:
    last_shout = new_shouts[0][0] # Set it the newest shout we grabbed
  else:
    # Add them to our queue (if any)
    print new_shouts
    for i in new_shouts:
      print i[2]
      print s.memberid
      print i
      last_shout = i[0] # Store the new shout id
