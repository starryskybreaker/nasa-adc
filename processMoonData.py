"""
Code to calculate azimuth/elevation angles and put everything into a txt file
It takes a good while to run... probably something to do with the 7 million data entries
Works now!
"""

import csv
import numpy as np
import math

#Earth Cartesian Position with respect to Lunar Fixed Frame at a single time instant
earthCart = np.array([361000, 0, -42100])

#method to calculate azimuth angle
def calc_azimuth(lat, long):
    #the radius from the moon to the earth (stored in radE)
    sqE = np.square(earthCart)
    sumE = np.sum(sqE)
    radE = math.sqrt(sumE)
    #the latitude and longitude of earth from the moon in radians
    latE = math.asin(earthCart[2]/radE)
    longE = math.atan2(earthCart[1], earthCart[0])
    
    #y & x values that get plugged into azimuth angle formula
    y = math.sin(longE - long) * math.cos(latE)
    x = math.cos(lat) * math.sin(latE) - math.sin(lat) * math.cos(latE) * math.cos(longE - long)
    
    #azimuth in degrees
    azimuth = math.degrees(math.atan2(y, x))
    
    return azimuth

#method to calculate elevation angle (takes in latitutde and longitude in radians and height in km)
def calc_elevation(lat, long, height):
    #radius of moon at this (lat, long)
    radius = 1737.4 + height
    #convert (lat, long) to cartesian coordinates (x, y, z)
    x = radius * math.cos(lat) * math.cos(long)
    y = radius * math.cos(lat) * math.sin(long)
    z = radius * math.sin(lat)
    coordCart = np.array([x, y, z])
    
    #find earth coordinates minus current location coordinates
    AB = earthCart - coordCart
    #distance????
    rangeAB = math.sqrt(AB[0]**2 + AB[1]**2 + AB[2]**2)
    #idk wat this is... was in formula sheet tho
    rz = (AB[0] * math.cos(lat) * math.cos(long)) + (AB[1] * math.cos(lat) * math.sin(long)) + (AB[2] * math.sin(lat))
    #elevation angle, converted to degrees
    elevationAB = math.degrees(math.asin(rz/rangeAB))
    
    return elevationAB


#create/overwrite txt file to store data
f = open("moondata.txt", "w")

with open('moondata.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = csv.reader(read_obj)
    
    # Iterate over each row in the csv using reader object
    for row in csv_reader:
        
        #convert latitude and longitude to radians and store in radLatLong list
        radLatLong = [math.radians(float(row[0])), math.radians(float(row[1]))]
        #calculate azimuth angle (input latitude and longitude)
        azimuth = calc_azimuth(radLatLong[0], radLatLong[1])
        #calculate elevation angle (input radian latitude, radian longitude, and terrain height in km)
        elevation = calc_elevation(radLatLong[0], radLatLong[1], float(row[2])/1000)
        
        #variable to store string that will be inserted into the txt file
        addRow = ''
        #add every value in this row of csv to addRow variable, separated by commas
        for num in row:
            addRow += num + ','
        #add azimuth and elevation angles to addRow variable, separated by commas and create new line after
        addRow += str(azimuth) + ',' + str(elevation) + '\n'
        
        #add lat, long, height, slope, azimuth, elevation to txt file in one line
        f.write(addRow)

#close txt file to save changes
f.close()
        
