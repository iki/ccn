#! /bin/bash

################# Video for any value ###########
Physical="Pollution"

################ SCRIPT to not modify #############
rm file.tmp
rm "2D-$Physical-video.gif"
chain=""
for i in `ls -1 Pollution*.eps`
do
        chain+=" $i"
done
echo ${chain} | tr "\n" " " > file.tmp

echo "[Building video] $Physical..."
convert -verbose -delay 50 -alpha Off -density 240 `cat file.tmp` 2D-$Physical-video.gif
rm file.tmp                                                                                                                                             
~           
