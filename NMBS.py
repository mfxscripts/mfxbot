#!/usr/bin/python
##
# Fetches train info.
# API: http://project.irail.be/wiki/API/APIv1
##

## Imports.
import re
from xml.etree.ElementTree import ElementTree
from urllib import urlopen

def get_api_xml(url):
  tree = ElementTree()
  api_results = []
  try:
    xml = tree.parse(urlopen(url))
    for connection in xml:
      departure = connection.find('departure')
      from_station = departure.find('station').text
      to_station = departure.find('direction').text
      vehicle = departure.find('vehicle').text
      vehicle_type = ''
      m = re.match('^(BE\.NMBS\.)([A-Z]+)([0-9]+)$', vehicle)
      if m:
        vehicle_type = m.group(2)
      departure_time = departure.find('time').attrib['formatted']
      departure_time = departure_time[11:-4]
      api_results.append([from_station,to_station,departure_time,vehicle_type])
  except Exception, e:
      print 'Couldn\'t parse xml: ' + e
  return api_results

def get_next_trains(departure, destination):
  message = ''
  api_url = 'http://api.irail.be/connections/?to='+ destination +'&from='+ departure + '&lang=NL'
  results = get_api_xml(api_url)
  if len(results) > 0:
    for x in results:
      train_from = x[0]
      train_to = x[1]
      train_time = x[2]
      train_type = x[3]
      message += train_time + ' ' + train_to + ' (' + train_type + ')\n'
    return message
  else:
    return ''
