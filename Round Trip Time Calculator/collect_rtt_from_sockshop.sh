#!/bin/bash
ID=1
export ID

sleep 300

while true; do
    bash runLocust.sh -h 10.66.66.53:30873 -c 5
    echo "$ID $(date +"%T")" >> collect_rtt_from_sockshop.txt
    ID=$[$ID+1]
    sleep 60
done


