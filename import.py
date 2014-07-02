#!/usr/bin/python

import Shivtr
import time

s = Shivtr.Session()

for i in reversed(range(3460)):
  insert_data = []
  j = s.get_shouts(i)
  for m in j['shouts']:
    insert_data.append((m['id'], m['message'], m['created_on'], m['member']['id']))

  print insert_data
  c = s.db.cursor()
  c.executemany('INSERT INTO shouts VALUES (?,?,?,?)', insert_data)
  s.db.commit()
  time.sleep(5)

s.db.close()
