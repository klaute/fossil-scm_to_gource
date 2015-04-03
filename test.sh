#!/bin/bash
#
# usage: ./test.sh <fossil repository name>
#
# author: Kai Lauterbach - klaute@gmail.com
# date: 2015-04-03
#
fossil timeline -n 99999 -v -R $1 > timeline.txt

python fossil_timeline_to_gource.py timeline.txt > timeline.log

gource -1280x720 --log-format custom -c 4.0 -s 0.1 timeline.log

rm timeline.log

