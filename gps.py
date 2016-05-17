#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time 
import webbrowser
import sys
import urllib2




gps_serial = serial.Serial(sys.argv[1],9600) # args: Serial device,  baudrate


def to_degrees(lats, longs):
  """
  converts the raw values of latitude and longitude from gps module into
  the values required by the google maps to display the exact location.
  """
  #NMEA format for latitude is DDMM.mmmm
  #so parsing values for degree, minutes, seconds form the raw value
  lat_deg = lats[0:2]   
  lat_mins = lats[2:4]  
  lat_secs = round(float(lats[5:])*60/10000, 2)
  
  lat_str = lat_deg +  '['+ lat_mins + '(' + str(lat_secs) + ')'

  #NMEA format for longitude is DDDMM.mmmm
  #so parsing values for degree, minutes, seconds form the raw value
  lon_deg = longs[0:3] 
  lon_mins = longs[3:5]
  lon_secs = round(float(longs[6:])*60/10000, 2)
  
  lon_str = lon_deg +  "["+ lon_mins + "(" + str(lon_secs) + ')'

  return [lat_str, lon_str]



def Write_to_file(GPS_coordinates):
  """
  this function Writes the current location into a file
  """
  with open('accident_coordinates.txt','w') as acc:
          acc.write(GPS_coordinates)

def read():
  """
  read the data from gps module via serial port.
  this function continuously reads the data from serial port
  and displays the current location which can be directly shown 
  on the google maps.
  """
  show = 0
  while True:
    
    gps_data = gps_serial.readline()
    
    if gps_data and not gps_data == '':
      
      if gps_data.startswith('$GPGGA,'):
        
        location_data = gps_data.split(',')
        latitude = location_data[2]
        longitude = location_data[4]
        if not  latitude == '' and not longitude =='':
          print "location: " ,to_degrees(latitude, longitude)[0] ,location_data[3] ,to_degrees(latitude, longitude)[1], location_data[5] 
          Write_to_file(to_degrees(latitude, longitude)[0] +location_data[3] +to_degrees(latitude, longitude)[1]+ location_data[5])
                
    time.sleep(1)

if __name__ == '__main__':

  read()
