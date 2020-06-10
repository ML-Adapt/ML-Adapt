#!/bin/bash
ID=1
export ID
experimento=(0)
#experimento=(1)
#experimento=(2)
#experimento=(2 2 2 2 0 2 2 1 2 0 2 2 1 1 0 2 1 0 0 1 0 2 2 1 1 0 1 1 0 0)
#experimento=(1 1 2 1 1 0 0 2 2 2 0 0 0 0 0 0 2 1 2 2 1 0 1 1 2 2 0 0 1 2)

FRONTEND_ADDR=http://10.66.66.53:30873

for number_random in "${experimento[@]}"
do
    if [ $number_random -eq 2 ]
    then
        echo "High: $ID $(date +"%T")" >> random_load_test_with_echo_parameter.txt
        locust --host=$FRONTEND_ADDR  -c "${USERS:-150}" --no-web --only-summary -t 300m
    fi
    if [ $number_random -eq 1 ]
    then
        echo "Normal: $ID $(date +"%T")" >> random_load_test_with_echo_parameter.txt
        locust --host=$FRONTEND_ADDR  -c "${USERS:-100}" --no-web --only-summary -t 300m
    fi
    if [ $number_random -eq 0 ]
    then
        echo "Low: $ID $(date +"%T")" >> random_load_test_with_echo_parameter.txt
        locust --host=$FRONTEND_ADDR -c "${USERS:-50}" --no-web --only-summary -t 300m
    fi

    ID=$[$ID+1]
done

mapek=$(pgrep -f "python3 mape-k.py")
rtt=$(pgrep -f "/bin/bash ./collect_rtt_from_sockshop.sh")
kill -9 $mapek
kill -9 $rtt
echo "End: $(date +"%T")" >> random_load_test_with_echo_parameter.txt

