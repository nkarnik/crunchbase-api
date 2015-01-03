import traceback
import requests
import json
import csv
import sys
import time
from keys import *


def getTotalFunding(orgjson):

  funding = orgjson["data"]["properties"]["total_funding_usd"]
  return funding


def getLatLong(street, city):

  street = street.replace(" ", "+")

  #request_url = "http://www.datasciencetoolkit.org/street2coordinates/" + street +"%2c+Baltimore%2c+MD"
  request_url = "http://www.datasciencetoolkit.org/street2coordinates/" + street + "%2c" + city + "%2c+CA"
  jreq = requests.get(request_url).json()

  #return jreq
  lat = jreq[jreq.keys()[0]]["latitude"]
  lon = jreq[jreq.keys()[0]]["longitude"]
  return (lat, lon)



def getOrganization(org):

  request_url = "http://api.crunchbase.com/v/2/organization/" + org + "?user_key=" + key3

  jreq = requests.get(request_url).json()
  return jreq


def validate(orgjson):

  
  if len(orgjson.keys()) < 2:
    print "invalid"
    return False

  return True


def getLocation(orgjson):

  location = orgjson["data"]["relationships"]["headquarters"]["items"][0]
  
  latitude = location["latitude"]
  longitude = location["longitude"]
  city = location["city"]

  if (location["street_1"] is None) and (location["street_2"] is None):
    return False

  elif (location["street_1"] is None):
    street = location["street_2"]

  elif (location["street_2"] is None):
    street = location["street_1"]

  else:
    street = location["street_1"] + " " + location["street_2"]

  return street, city


def getFoundRow(org):
  jorg = getOrganization(org)
  print jorg

  if validate(jorg):
    founders = getFounders(jorg)
    for founder in founders:
      try:
        first_name = founder["data"]["properties"]["first_name"]
        last_name = founder["data"]["properties"]["last_name"]
        degrees = getDegrees(founder)
        for degree in degrees:
          print degree
          print first_name, last_name, org

      except:
        print "error"

    return founders

def getDegrees(fjson):
  try:
    degs = fjson["data"]["relationships"]["degrees"]["items"]
    info = []
    for degree in degs:
      school = degree["organization_name"]
      degtype = degree["degree_type_name"]
      completed = degree["completed_on"]
      print school, degtype, completed
      tup = (school, degtype, completed)
      info.append(tup)
    return info

  except:
    print "no degrees"

  
def getFounders(orgjson):

  founderPaths = []
  foundersOut = []

  try:
    founders = orgjson["data"]["relationships"]["founders"]["items"]

    for founder in founders:
      founderPaths.append(founder["path"])


    for fp in founderPaths:
      
      request_url = "http://api.crunchbase.com/v/2/" + fp + "?user_key=" + key3
      fdata = requests.get(request_url).json()
      foundersOut.append(fdata)      

  except:
    print "error"

  return foundersOut

  




def getFundingRounds(orgjson):

  fundingRounds = orgjson["data"]["relationships"]["funding_rounds"]["items"]
  rounds = []  
  frs = []

  for fundingRound in fundingRounds:
    rounds.append(fundingRound["path"])

  #for fr in rounds:
  #  frs.append(getFunding(fr))

  return rounds


def getFunding(path):

  request_url = "http://api.crunchbase.com/v/2/" + path + "?user_key=" + key3
  jreq = requests.get(request_url).json()
  return jreq


#def buildRow(row, rjson):
#
#  date = rjson["data"]
#  try:


def fullFundingRound(org):

  jorg = getOrganization(org)
  rounds = getFundingRounds(jorg)
  return rounds


def getOrgRow(org):

  try:
    jorg = getOrganization(org)
    if validate(jorg):
      print "valid"
      #print jorg
      funding = getTotalFunding(jorg)
      print funding
      add = getLocation(jorg)
      address = str(add[0])
      city = str(add[1])
      lat, lon = getLatLong(address, city)
      rounds = getFundingRounds(jorg)
      funds = {"rounds": []}
      for r in rounds:
         funds["rounds"].append(str(r))
      print lat, lon
      tup = (org, funding, address, city,  lat, lon, funds)

      print tup
      return tup

  except:
    traceback.print_exc()
    print "error"

def writeRows(orgs, fname):

  f = open(fname, 'wt')

  try:
    writer = csv.writer(f)
    for org in orgs:
      row = getOrgRow(org)
      time.sleep(1.25)
      print row
      if row is not None:
        writer.writerow(row)

  finally:
    f.close()


def writeRow(row, fname):
  "starting write process"

  f = open(fname, 'a')

  try:
    writer = csv.writer(f)
    print "opened file"
    if row is not None:
      writer.writerow(row)

  finally:
    print "error writing row"
    f.close()


def writeSample(name):

  f = name + "valid.csv"

  infile = open(f, "rt")
  l = []
  c = 0

  try:
    reader = csv.reader(infile)
    for row in reader:
        if c > 5: break
        print row[0]
        c += 1
        l.append(row[0])

  finally:
    infile.close()

  writeRows(l, "asdf.csv")

def writeMost(name):

  f = name + "valid.csv"

  infile = open(f, "rt")
  outfile = name + "2.csv"
  #infile = open("sfvalid.csv", "rt")
  l = []
  c = 0

  try:
    reader = csv.reader(infile)
    for row in reader:
        if c < 1000: 
          c += 1
          print c
          continue

        if c > 2000: break

        print row[0]
        c += 1
        l.append(row[0])

  finally:
    infile.close()

  writeRows(l, outfile)
