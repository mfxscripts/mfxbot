#!/usr/bin/python
##

## Imports.
import json
import requests
import ConfigParser
import time
import sqlite3

## Vars.
headers          = {'Content-type': 'application/json', 'Accept': 'text/plain'}
config_file      = '/home/p/etc/bot.conf'
token_max_age    = 10 # Mins before we need to reauthenticate
login_attempts   = 10 # Max attempts to login before giving up
login_retry_time = 30 # Seconds between login attempts
database_path    = '/home/p/var/db/mfx.db' # sqlite3 file

## Classes.
class AuthError( Exception ): pass

class Session:
  ' session to shivtr for authentication and shoutbox interaction '

  def __init__(self):
    # Read values from config file.
    c = ConfigParser.ConfigParser()
    c.read(config_file)
    self.email = c.get('Authentication', 'email')
    self.password = c.get('Authentication', 'password')
    self.memberid = int(c.get('Authentication', 'memberid'))
    self.auth_token = ''
    self.auth_time = 0
    self.last_shout = 0
    self.refresh_token()
    # Open DB connection
    self.db = open_db()

  def refresh_token(self):
    # Token empty?
    if ((len(self.auth_token) == 0) or
        (int(time.time()) - self.auth_time >= token_max_age*60)):
      try:
        self.signin() # Proceed to login our user
      except AuthError, ex:
        print ex, ex.sc # If login failed, print status code

  def signin(self):
    # Exception
    ex = AuthError("Failed to login.")
    # Sign in via JSON, get authentication_token as result.
    url = 'http://mfx.shivtr.com/users/sign_in.json';
    data = {'user': { 'email': self.email, 'password': self.password } }

    for _ in range(login_attempts):
      r = requests.post(url, data=json.dumps(data), headers=headers)
      ex.sc = r.status_code
      if ex.sc == 200:
        break
      time.sleep(login_retry_time) # Wait x sec between attempts.

    if ex.sc == 200:
      j = r.json()
      self.auth_token = j ['user_session']['authentication_token']
      self.auth_time = int(time.time())
    else:
      raise ex

  def get_shouts(self, page=1):
    # Always first check if we are still authenticated
    self.refresh_token()
    # Then get a page of shouts
    url = "http://mfx.shivtr.com/shouts.json?auth_token=" + self.auth_token + '&page=' + str(page)
    r = requests.get(url)
    #print url
    try:
      return r.json()
    except ValueError, ex:
      print ex
      return {}

  def post_shout(self, msg):
    # Always first check if we are still authenticated
    self.refresh_token()
    # Then send the message
    url = "http://mfx.shivtr.com/shouts.json?auth_token=" + self.auth_token;
    data = {'shout': { 'message': msg } }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.status_code

  def get_last_shoutid(self):
    j = self.get_shouts(1)
    return j['shouts'][0]['id']

  def db_get_last_shoutid(self):
    c = self.db.cursor()
    c.execute("select id from shouts order by id desc limit 1;")
    return c.fetchone()

  def get_new_shouts(self):
    # We get the first page, loop over it, add it to a 2D array.
    # We stop looping once we found the last_shout.
    new_shouts = []
    j = self.get_shouts(1) # Get last 20 shouts
    #print j
    for s in j['shouts']:
      if s['id'] == self.last_shout:
        break # exit for loop right away if no new shouts.
      #if s['member']['id'] != self.memberid:
      if s['member_id'] != self.memberid:
        #print s['message']
        member_id = s['member_id']
        member_name = self.get_member_name(j, member_id) # API change 05/01/2015
        new_shouts.append((s['id'], s['message'], member_id, member_name))
    else:
      # 20 new shouts, something is wrong (probably deleted messages or first page grab since startup)
      new_shouts = []

    self.last_shout = j['shouts'][0]['id'] # Update with last found shout
    return new_shouts

  def get_member_name(self, json, member_id):
    for m in json['members']:
      if m['id'] == member_id:
        member_name = m['display_name']
        return member_name

## Functions
def open_db():
  db = sqlite3.connect(database_path)
  return db
