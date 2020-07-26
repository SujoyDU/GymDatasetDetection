#!/bin/bash
vid=$($1 | sed -n 1p)
ffmpeg -ss $2 -i $vid -to $3 -c copy $4