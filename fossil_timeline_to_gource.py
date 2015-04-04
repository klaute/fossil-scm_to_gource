#
# description: Fossil timeline (verbose commandline) to gource custom log convert script.
#
# author: Kai Lauterbach - klaute@gmail.com
# version: v0.2
# date: 2015-04-02
#

import sys
import re
import time
import datetime
import copy

###

NEW_FILE_INDICATOR = "ADDED "
DELETED_FILE_INDICATOR = "DELETED "
MODIFIED_FILE_INDICATOR = "EDITED "

log = []

### timeline processing

try:
  filename = sys.argv[1]
except:
  filename = 'timeline.txt'

lines = [line.strip() for line in open(filename)]

tmpdata = {"date":       "0",
           "color": "ffffff", # default backgroudn color is white
           "type":       "M", # default file mode is modified
           "file":        "", # no default filename
           "user":        ""} # no default user
datekey   =          "0" # gource timestamp
date_time =   "00:00:00" # time of commit
date      = "0000-00-00" # date of commit

search4user = 0

for line in lines:

  # read date
  if line.startswith("=== "):
    tstr = line.split(" ")
    tmpdata = {"date":       "0",
               "color": "ffffff", # default backgroudn color is white
               "type":       "M", # default file mode is modified
               "file":        "", # no default filename
               "user":        ""} # no default user
    date        = tstr[1] + " " # remember the date string (day)
    datekey     = "0"
    date_time   = "00:00:00"
    #print "1:" + date
    search4user = 0

  # read time
  tmat =  re.match("(\d{2})[/:-](\d{2})[/:-](\d{2})", line)
  if tmat is not None:
    date_time = tmat.group(0)
    #print "2:" + date_time
    datekey = str(int(time.mktime(
                  datetime.datetime.strptime(
                    date + date_time,
                    "%Y-%m-%d %H:%M:%S").timetuple())))
    tmpdata["date"] = datekey
    search4user = 1
    #print "3:" + datekey

  # read user
  if 2 == search4user:
    search4user = 0
    tstr = line.split(" ")
    #print "gne " + tstr[0]
    tmpdata["user"] = tstr[0].replace(')', '').replace(".(none", "")

  if 1 == search4user:
    #print line
    if "(user:" in line:
      tstr = line.split(" ")

      for tmp in tstr:
        if 2 == search4user:
          search4user = 0
          #print "tmp " + tmp.replace(')', "")
          tmpdata["user"] = tmp.replace(')', "")

        if "(user:" in tmp:
          search4user = 2

  # read color
  # fossil does not print out color information (imho)

  # read file and type
  toadd = 0
  if line.startswith(NEW_FILE_INDICATOR):
    toadd = 1
    tmpdata["type"] = "A"
  if line.startswith(DELETED_FILE_INDICATOR):
    toadd = 1
    tmpdata["type"] = "D"
  if line.startswith(MODIFIED_FILE_INDICATOR):
    toadd = 1
    tmpdata["type"] = "M"

  # add data to gource output data list
  if 1 == toadd:
    tstr = line.split(" ", 1) # Only one split
    #tstr[1] = tstr[1].replace("/", "//") # fix path name
    tmpdata["file"] = tstr[1]

    log.append(copy.deepcopy(tmpdata))

# print out the results
for tmpdata in reversed(log):
  sys.stdout.write(tmpdata["date"] + "|" +
                   tmpdata["user"] + "|" +
                   tmpdata["type"] + "|" +
                   tmpdata["file"] + "\n")

