#!/bin/bash
a=$1
student_username=${a%@*}
tar -xvzf *_file_/*.tar.gz > /dev/null
clang++ -std=c++11 helloworld.cpp -o helloworld
output=$(./helloworld)
./helloworld > /dev/null
ret_val=$?

score=0
if [ "$student_username" == "$output" ]; then
    score=$(( $score + 50 ))
fi

if [ "$ret_val" == "10" ]; then
    score=$(( $score + 50 ))
fi
echo "$score" > score.txt
