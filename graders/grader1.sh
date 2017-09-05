#!/bin/bash
echo "Hello world from grader1"
echo "$1"
a=$1
student_username=${a%@*}
echo "$student_username"
ls *_file_/*.tar.gz
tar -xvzf *_file_/*.tar.gz
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
