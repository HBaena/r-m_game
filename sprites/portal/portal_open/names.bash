#! /bin/bash
#
names=$(ls *.png) 
let i=1
for name in $names; do
    mv "$name" "portal_open_$i.png"
    let i=i+1
done