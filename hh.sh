#!/bin/bash
while [ 1 ]
do
	n=`date +%M`
	[ $n == "00" -o $n == "30" ] && echo -e '\a' && read -p "acted on `date +%H:%M`? " a
	sleep 61
done
