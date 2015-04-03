#
# description: Fossil timeline (web rss) to gource custom log convert script.
#
# author: Kai Lauterbach - klaute@gmail.com
# version: v0.1
# date: 2015-04-02
#

import xml.etree.ElementTree as ET
import sys
import time
import datetime

###

NEW_FILE_INDICATOR     = "(new file)"
DELETED_FILE_INDICATOR =  "(deleted)"

TAG_DATE_NAME   = "pubDate"
TAG_USER_NAME   = "{http://purl.org/dc/elements/1.1/}creator"
TAG_FILE_NAME   = "link"
TAG_FILE_TYPE   = "link"
TAG_ENTRY_COLOR = "color"

log = {}

### xml processing

tree = ET.parse('timeline.xml')
root = tree.getroot()

for child in root.iter("item"):

  tmpdata = {"color": "ffffff", # default backgroudn color is white
             "type":       "M", # default file mode is modified
             "file":        "", # no default filename
             "user":        ""} # no default user
  date = "00000000000000"

  for subchild in child:

    if TAG_DATE_NAME == subchild.tag:
      stxt = subchild.text.split(" ")
      s = stxt[1] + "/" + stxt[2] + "/" + stxt[3] + " " + stxt[4]
      date = str(int(time.mktime(datetime.datetime.strptime(s, "%d/%b/%Y %H:%M:%S").timetuple())))

    if TAG_USER_NAME == subchild.tag:
      tmpdata["user"] = subchild.text

    if TAG_FILE_NAME == subchild.tag:
      tmptxt = subchild.text
      tmptxt = tmptxt.replace(" " + NEW_FILE_INDICATOR, "")
      tmptxt = tmptxt.replace(" " + DELETED_FILE_INDICATOR, "")

      tmpdata["file"] = tmptxt

    if TAG_FILE_TYPE == subchild.tag:
      if NEW_FILE_INDICATOR in subchild.text:
        tmpdata["type"] = "A"
      if DELETED_FILE_INDICATOR in subchild.text:
        tmpdata["type"] = "D"

    if TAG_ENTRY_COLOR == subchild.tag:
      tmpdata["color"] = subchild.text

  log[date] = tmpdata
  #sys.stdout.write("added " + str(date) + " = " + str(log[date]) + "\n")

#print "----------"

for key in sorted(log.keys()):
  tmpdata = log[key]
  sys.stdout.write(key + "|" +
                   tmpdata["user"] + "|" +
                   tmpdata["type"] + "|" +
                   tmpdata["file"] + "|" +
                   tmpdata["color"] + "\n")

