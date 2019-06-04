#! /bin/bash

IMAGES=$(ls 'sprites/'$1'/'*.png)
for image in $IMAGES; do
    convert $image '-trim' $image 
done