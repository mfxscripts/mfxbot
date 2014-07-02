#!/usr/bin/python
##

## Imports.
import subprocess
import wolframalpha
import random

## Vars.
wolframalpha_appid = '9XRJAL-TXWW5ATQK8';

## Functions.
def status(s):

  uptime = subprocess.check_output(['uptime'])
  temp = subprocess.check_output(['/home/p/bin/gettemp'])
  output = uptime.rstrip() + ', temperature: ' + temp
  s.post_shout(output)

def help(s):

  s.post_shout("Mijn handleiding kan je vinden op: https://github.com/mfxscripts/mfxbot")

def tell_fortune(s):
  
  fortune = subprocess.check_output(['fortune', '-n', '250'])
  fortune = fortune.replace('\n', ' ')
  fortune = ' '.join(fortune.split())
  s.post_shout(fortune)

def drwho_quote(s):
  
  quote = subprocess.check_output(['fortune', '-n', '250', 'drwho'])
  s.post_shout(quote)

def tetten(s):
  replies = [
             '( . Y . ) tetjes!',
             'DIKKE TETTEUH',
             'b00bies.',
             'Al die tettenzotten hier...',
             '3( ( . Y . ) TETTTTTTTTTTTTTEUH ( . Y . ) 3(',
             'tetjes van plezier...',
             'CYBORG TETTEN 3(',
             'https://duckduckgo.com/?q=tetten',
             'TETTEN. TETTEN. TETTEN.',
             'Oh jaaa. Lekkere tetten.',
             'Mijn systemen zoeken het net af voor NSFW tetten.',
             'Jij bent een tettenzot. Ik ben een tettenbot 8)'
            ]
  s.post_shout(replies[random.randint(0,len(replies)-1)])

def roll_d20(s, author):
  result = random.randint(1,20)
  if (result == 1): 
    s.post_shout(author + ' rolt een ... 1. Sukkel :(')
  elif (result == 20):
    s.post_shout(author + ' rolt een ... 20!!! CRITICAL! 3( 3( 3(')
  else:
    s.post_shout(author + ' rolt een ... ' + str(result) + '.')

def find_answer(s, question):

  # First try wolframalpha
  c = wolframalpha.Client(wolframalpha_appid)
  r = c.query(question)

  if len(r.pods) > 1:
    answer = r.pods[1].text
    answer = answer.replace('Wolfram|Alpha', 'MFxBot')
    if 0 < len(answer) <= 250:
      s.post_shout(answer)
    else:
      s.post_shout('Ken der gin gedacht van :(')
  else:
    s.post_shout('Ken der gin gedacht van :(')
