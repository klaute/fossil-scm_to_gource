#!/bin/bash
#
# usage: ./convert.sh <fossil repository name> <video output file name>
#
# author: Kai Lauterbach - klaute@gmail.com
# date: 2015-04-03
#

fossil timeline -n 99999 -v -R $1 > timeline.txt

python fossil_timeline_to_gource.py timeline.txt > timeline.log

gource -1920x1080 --log-format custom -c 4.0 -s 0.1 timeline.log -o - | \
  ffmpeg -y -b 10000K -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -vpre slow -threads 0 -bf 0 $2.x264.mp4

rm timeline.log

