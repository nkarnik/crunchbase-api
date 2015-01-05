import csv
import operator

def parse():
  schools = dict()
  companies = dict()
  with open("allfound.csv", "rb") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
      print "!!!".join(row)
      print row[5]
      schools[row[5]] = 0
      try:
        companies[row[0]].append(row)
      except:
        companies[row[0]] = []
        companies[row[0]].append(row)
    return schools, companies

def calculate(schools, companies):

  for company in companies.keys():
    compinfo = companies[company]
    attrib = int(compinfo[0][1]) / float(len(compinfo))
    for founder in compinfo:
      schools[founder[5]] += attrib

  return schools

def sorts(schools):

  sorted_x = sorted(schools.items(), key=operator.itemgetter(1))
  return sorted_x
