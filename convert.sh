#!/bin/bash

fossil timeline -n 99999 -v -R $1 > timeline.txt

python fossil_timeline_to_gource.py timeline.txt > timeline.log

gource -1280x720 --log-format custom -c 4.0 -s 0.1 timeline.log -o - | \
  ffmpeg -y -b 10000K -r 60 -f image2pipe -vcodec ppm -i - -vcodec libx264 -vpre slow -threads 0 -bf 0 $2.x264.mp4

rm timeline.log

